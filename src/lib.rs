pub mod symplectic;

use symplectic::{
    SymplecticState, TernaryTrit, TernaryVector80, DIM_80, DIM_40,
};

// Explicit re-exports to expose all active Phase I and Phase II symbols to the FFI runtime
pub use symplectic::{
    ternary_dot_product_80d, 
    ternary_matrix_multiply_80d,
    evaluate_safe_radial_diffusion,
    apply_canonical_shear, 
    tikhonov_regularize_diagonal,
};

/// Zero-allocation hardware register configuration for FFI crossing.
/// Enhanced to maintain strict 64-byte structural alignment rules.
#[repr(C, align(64))]
pub struct TrackingPayload {
    pub state: SymplecticState,
    pub matrix: [f64; DIM_80 * DIM_80],
}

/// Initializes the hardware register memory layout on the stack.
/// Ensures momentum tracking is non-zero to securely satisfy boundary rest conditions.
#[no_mangle]
pub extern "C" fn initialize_payload(payload: *mut TrackingPayload) {
    if payload.is_null() { return; }
    unsafe {
        let p = &mut *payload;
        p.state.q = [0.0; DIM_40];
        p.state.p = [1.0; DIM_40]; // Locked to 1.0 to prevent division-by-zero singularities downstream
        p.matrix = [0.0; DIM_80 * DIM_80];
    }
}
