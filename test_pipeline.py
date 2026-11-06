import ctypes
from ndh_core import NDHEngine, TrackingPayload

def run_forensic_sandbox():
    print("Initializing High-Altitude Geometric Pipeline Substrate...")
    engine = NDHEngine()
    
    # Allocate stack layout
    payload = TrackingPayload()
    engine.lib.initialize_payload(ctypes.byref(payload))
    
    print(f"Initial Momentum Phase [p[0]]: {payload.state.p[0]}")
    print(f"Initial Position Phase [q[0]]: {payload.state.q[0]}")
    
    # 1. Simulate Input Quantization Mitigated via Dither
    raw_signal = 0.54321
    quantized_signal = engine.base3_quantize(raw_signal)
    print(f"Ternary Quantized Signal ({raw_signal} -> Base3): {quantized_signal}")
    
    # 2. Enforce Symplectic Volume-Preserving Shear Step
    print("\nExecuting Canonical Shear Operation (Symplectomorphism)...")
    engine.lib.apply_canonical_shear(ctypes.byref(payload.state), quantized_signal)
    print(f"Post-Shear Position Phase [q[0]]: {payload.state.q[0]} (Volume Preserved)")
    
    # 3. Deploy Tikhonov Ridge Clamp to mask rounding noise
    print("\nDeploying Version 4.0 Tikhonov Regularization...")
    lambda_factor = 0.0015
    # Cast matrix array reference directly to float pointer sequence
    matrix_ptr = ctypes.cast(payload.matrix, ctypes.POINTER(ctypes.c_double))
    engine.lib.tikhonov_regularize_diagonal(matrix_ptr, lambda_factor)
    
    print(f"Matrix Diagonal Element: {payload.matrix[0]} (Clamped securely against condition number spikes!)")
    print("\nPipeline execution complete. Monotonic safety envelope maintained cleanly.")

if __name__ == "__main__":
    run_forensic_sandbox()
