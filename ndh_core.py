import ctypes
import os
import sys
import random

# Define C-FFI Structural Invariants
class SymplecticState(ctypes.Structure):
    _fields_ = [
        ("q", ctypes.c_double * 40),
        ("p", ctypes.c_double * 40)
    ]

class TrackingPayload(ctypes.Structure):
    _fields_ = [
        ("state", SymplecticState),
        ("matrix", ctypes.c_double * 6400) # 80x80 flattened array
    ]

class NDHEngine:
    def __init__(self):
        # Locate shared object substrate
        lib_name = "libndh_core_rust.so"
        if sys.platform == "darwin":
            lib_name = "libndh_core_rust.dylib"
        elif sys.platform == "win32":
            lib_name = "ndh_core_rust.dll"
            
        lib_path = os.path.join(os.path.dirname(__file__), "target", "release", lib_name)
        if not os.path.exists(lib_path):
            lib_path = os.path.join(os.path.dirname(__file__), "target", "debug", lib_name)
            
        try:
            self.lib = ctypes.CDLL(lib_path)
        except OSError as e:
            raise RuntimeError(f"Failed to find compiled Rust substrate at {lib_path}. Run 'cargo build --release' first.") from e

        # Register function pointer serialization boundaries
        self.lib.initialize_payload.argtypes = [ctypes.POINTER(TrackingPayload)]
        self.lib.apply_canonical_shear.argtypes = [ctypes.POINTER(SymplecticState), ctypes.c_double]
        self.lib.tikhonov_regularize_diagonal.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_double]

    @staticmethod
    def stochastic_triangular_dither() -> float:
        """Implements error-decorrelated noise injection to mask Base-3 quantization rounding noise."""
        r1 = random.uniform(-0.5, 0.5)
        r2 = random.uniform(-0.5, 0.5)
        return r1 + r2

    def base3_quantize(self, val: float) -> float:
        """Forces continuous continuous clouds into an unyielding ternary alphabet."""
        dithered = val + self.stochastic_triangular_dither() * 0.05
        if dithered < -0.33:
            return -1.0
        elif dithered > 0.33:
            return 1.0
        return 0.0
