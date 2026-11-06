import ctypes
from ndh_core import NDHEngine, SymplecticState, RasaTensor80x80

def run_python_rasa_validation():
    print("=========================================================")
    print("🐍 Python Enclave: Initializing Rasa Curvature Flow Validation...")
    engine = NDHEngine()
    
    # 1. Allocate and format the active Symplectic State space
    state = SymplecticState()
    for i in range(40):
        state.q[i] = 1.0  # Set active baseline positions
        state.p[i] = 1.0  # Set baseline tracking velocity
        
    # 2. Build a dense 80x80 mock Rasa Emotional-Tensor matrix
    rasa_tensor = RasaTensor80x80()
    for r in range(80):
        for c in range(80):
            # Alternate fields strictly between -1, 0, 1 to simulate a discrete aesthetic tensor
            if (r + c) % 3 == 1:
                rasa_tensor.matrix[r].data[c] = 1
            elif (r + c) % 3 == 2:
                rasa_tensor.matrix[r].data[c] = -1
            else:
                rasa_tensor.matrix[r].data[c] = 0

    print("🐍 Python Enclave: Projecting aesthetic force field against the phase space...")
    
    # Execute the curvature mutation step crossing the C-FFI gate (eta scale = 0.05)
    scaling_eta = 0.05
    engine.lib.apply_rasa_curvature_flow(
        ctypes.byref(rasa_tensor),
        ctypes.byref(state),
        ctypes.c_double(scaling_eta)
    )
    
    print("🐍 Python Enclave: Transformation complete. Phase-space bounds enforced safely.")
    print(f"🐍 Python Enclave: First 5 Mutated Momentum Coordinates [p]: {[state.p[i] for i in range(5)]}")
    print("=========================================================")

if __name__ == "__main__":
    run_python_rasa_validation()
