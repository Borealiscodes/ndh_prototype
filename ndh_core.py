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

class TernaryVector80(ctypes.Structure):
    """Maps directly to the repr(i8) array sequences in the native Rust core."""
    _fields_ = [("data", ctypes.c_int8 * 80)]

class QuestOperator80x80(ctypes.Structure):
    """Maps directly to a dense, nested 80x80 ternary operator grid in Rust memory."""
    _fields_ = [("rows", TernaryVector80 * 80)]

class RasaTensor80x80(ctypes.Structure):
    """Maps directly to a dense 80x80 ternary emotional velocity tracking grid in Rust memory."""
    _fields_ = [("matrix", TernaryVector80 * 80)]

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
        
        self.lib.evaluate_safe_radial_diffusion.argtypes = [ctypes.c_double]
        self.lib.evaluate_safe_radial_diffusion.restype = ctypes.c_double
        
        # Explicit typing for continuous-vector dot product tracks
        self.lib.ternary_dot_product_80d.argtypes = [ctypes.POINTER(TernaryVector80), ctypes.POINTER(ctypes.c_double)]
        self.lib.ternary_dot_product_80d.restype = ctypes.c_double
        
        self.lib.ternary_matrix_multiply_80d.argtypes = [
            ctypes.POINTER(TernaryVector80), # Array pointer of 80 discrete rows
            ctypes.POINTER(ctypes.c_double), # Input 80D float state vector
            ctypes.POINTER(ctypes.c_double)  # Output 80D float destination vector
        ]

        # Version 4.0 First-Order Spatial Sigma-Delta Error Diffusion Entry Point
        self.lib.apply_spatial_sigma_delta_loop.argtypes = [
            ctypes.POINTER(ctypes.c_double), # Continuous input vector tensor (80 floats)
            ctypes.POINTER(ctypes.c_int8),   # Destination ternary trit tracking buffer (80 elements)
            ctypes.POINTER(ctypes.c_double)  # Pre-generated triangular dither matrix field
        ]

        # Quest Algebra Operator Endpoint Declarations
        self.lib.apply_quest_operator_80d.argtypes = [
            ctypes.POINTER(QuestOperator80x80), # Narrative transformation operator matrix
            ctypes.POINTER(ctypes.c_double),    # Current 80D narrative trajectory tracking state
            ctypes.POINTER(ctypes.c_double)     # Evaluated next-state trajectory destination
        ]

        self.lib.compose_quest_operators_80d.argtypes = [
            ctypes.POINTER(QuestOperator80x80), # Operator A
            ctypes.POINTER(QuestOperator80x80), # Operator B
            ctypes.POINTER(QuestOperator80x80)  # Output combined narrative operator matrix
        ]

        # Phase V Rasa Curvature Flow Operator Entry Point
        self.lib.apply_rasa_curvature_flow.argtypes = [
            ctypes.POINTER(RasaTensor80x80),    # Emotional-Tensor operator reference
            ctypes.POINTER(SymplecticState),    # Active Symplectic phase space state (mutates p)
            ctypes.c_double                     # Curvature scale factor (eta)
        ]

    @staticmethod
    def stochastic_triangular_dither() -> float:
        """Implements error-decorrelated noise injection to mask Base-3 quantization rounding noise."""
        r1 = random.uniform(-0.5, 0.5)
        r2 = random.uniform(-0.5, 0.5)
        return r1 + r2

    def base3_quantize(self, val: float) -> float:
        """Forces continuous clouds into an unyielding ternary alphabet."""
        dithered = val + self.stochastic_triangular_dither() * 0.05
        if dithered < -0.33:
            return -1.0
        elif dithered > 0.33:
            return 1.0
        return 0.0
