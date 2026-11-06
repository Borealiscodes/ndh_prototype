pub mod symplectic;

use symplectic::{
    SymplecticState, TernaryTrit, TernaryVector80, DIM_80, DIM_40,
};

pub use symplectic::{
    ternary_dot_product_80d, 
    ternary_matrix_multiply_80d,
    evaluate_safe_radial_diffusion,
    apply_canonical_shear, 
    tikhonov_regularize_diagonal,
    apply_spatial_sigma_delta_loop, // Added symbol tracking
};

#[repr(C, align(64))]
pub struct TrackingPayload {
    pub state: SymplecticState,
    pub matrix: [f64; DIM_80 * DIM_80],
}

#[no_mangle]
pub extern "C" fn initialize_payload(payload: *mut TrackingPayload) {
    if payload.is_null() { return; }
    unsafe {
        let p = &mut *payload;
        p.state.q = [0.0; DIM_40];
        p.state.p = [1.0; DIM_40];
        p.matrix = [0.0; DIM_80 * DIM_80];
    }
}

