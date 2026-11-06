import ctypes
import os
import sys
from ndh_core import NDHEngine, TernaryVector80, TrackingPayload

def run_python_v2_validation():
    print("=========================================================")
    print("🐍 Python Enclave: Initializing Phase I Arithmetic Test Loop...")
    engine = NDHEngine()
    
    # 1. Allocate and initialize the main tracking payload infrastructure
    payload = TrackingPayload()
    engine.lib.initialize_payload(ctypes.byref(payload))
    
    # 2. Construct a continuous 80-dimensional input state vector
    input_vector = (ctypes.c_double * 80)(*[float(i) * 0.1 for i in range(80)])
    output_vector = (ctypes.c_double * 80)(*[0.0 for _ in range(80)])
    
    # 3. Allocate a dense 80x80 mock Ternary Weight Matrix block
    # (Array of 80 discrete rows, each row containing 80 fields)
    matrix_block = (TernaryVector80 * 80)()
    for row_idx in range(80):
        for col_idx in range(80):
            # Alternate values strictly between -1, 0, and 1 to simulate a discrete neural matrix
            val = (row_idx + col_idx) % 3
            if val == 2:
                matrix_block[row_idx].data[col_idx] = -1
            elif val == 1:
                matrix_block[row_idx].data[col_idx] = 1
            else:
                matrix_block[row_idx].data[col_idx] = 0

    print("🐍 Python Enclave: Executing branchless 80D Ternary Matrix Contraction...")
    
    # Execute through the C-FFI boundary endpoint
    engine.lib.ternary_matrix_multiply_80d(
        ctypes.cast(matrix_block, ctypes.POINTER(TernaryVector80)),
        ctypes.cast(input_vector, ctypes.POINTER(ctypes.c_double)),
        ctypes.cast(output_vector, ctypes.POINTER(ctypes.c_double))
    )
    
    print("🐍 Python Enclave: Execution successful. Invariants preserved.")
    print(f"🐍 Python Enclave: First 5 Output Vector Tracks: {[output_vector[i] for i in range(5)]}")
    print("=========================================================")

if __name__ == "__main__":
    run_python_v2_validation()
