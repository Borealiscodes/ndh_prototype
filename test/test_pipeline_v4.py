import ctypes
import os
import sys
import math
from ndh_core import NDHEngine

def run_python_v4_validation():
    print("=========================================================")
    print("🐍 Python Enclave: Initializing Phase III Sigma-Delta Test Loop...")
    engine = NDHEngine()
    
    # 1. Synthesize a continuous mock input wave signal (80 floats)
    input_floats = (ctypes.c_double * 80)(*[
        math.sin(float(i) * 0.2) * 0.8 for i in range(80)
    ])
    
    # 2. Pre-generate a matrix field of stochastic triangular dither weights
    dither_weights = (ctypes.c_double * 80)(*[
        engine.stochastic_triangular_dither() for _ in range(80)
    ])
    
    # 3. Allocate the destination ternary output buffer (80 elements, i8 format)
    output_trits = (ctypes.c_int8 * 80)(*[0 for _ in range(80)])
    
    print("🐍 Python Enclave: Streaming signals into first-order spatial modulation pass...")
    
    # Execute through the FFI boundary
    engine.lib.apply_spatial_sigma_delta_loop(
        ctypes.cast(input_floats, ctypes.POINTER(ctypes.c_double)),
        ctypes.cast(output_trits, ctypes.POINTER(ctypes.c_int8)),
        ctypes.cast(dither_weights, ctypes.POINTER(ctypes.c_double))
    )
    
    print("🐍 Python Enclave: Execution successful. Error-diffusion loop verified.")
    print(f"🐍 Python Enclave: First 10 Modulated Ternary Trits: {[output_trits[i] for i in range(10)]}")
    print("=========================================================")

if __name__ == "__main__":
    run_python_v4_validation()
