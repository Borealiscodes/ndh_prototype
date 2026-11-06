import ctypes
import os
import sys

# Define FFI Type Maps to match Rust structures precisely
class SymplecticState(ctypes.Structure):
    _fields_ = [
        ("q", ctypes.c_double * 40),
        ("p", ctypes.c_double * 40)
    ]

def run_python_forensic_validation():
    print("=========================================================")
    # Establish binary pathway target
    lib_name = "libndh_core_rust.so"
    if sys.platform == "darwin":
        lib_name = "libndh_core_rust.dylib"
    elif sys.platform == "win32":
        lib_name = "ndh_core_rust.dll"
        
    lib_path = os.path.join(os.path.dirname(__file__), "target", "release", lib_name)
    if not os.path.exists(lib_path):
        lib_path = os.path.join(os.path.dirname(__file__), "target", "debug", lib_name)
        
    print(f"🐍 Python Enclave: Loading Rust binary from {lib_path}")
    rust_engine = ctypes.CDLL(lib_path)
    
    # Configure function signature mappings
    rust_engine.evaluate_safe_radial_diffusion.argtypes = [ctypes.c_double]
    rust_engine.evaluate_safe_radial_diffusion.restype = ctypes.c_double
    
    # Test Boundary Condition: absolute mechanical rest
    critical_radius = 0.0
    print(f"🐍 Python Enclave: Streaming critical rest telemetry (r = {critical_radius})")
    
    # Execute through the FFI boundary
    diffusion_output = rust_engine.evaluate_safe_radial_diffusion(critical_radius)
    
    print(f"🐍 Python Enclave: Execution successful. No hardware crash.")
    print(f"🐍 Python Enclave: Evaluated 9D Laplacian Output: {diffusion_output}")
    print("=========================================================")

if __name__ == "__main__":
    run_python_forensic_validation()
