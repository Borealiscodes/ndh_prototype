pub mod symplectic;

use symplectic::{SymplecticState, DIM_80};

/// Zero-allocation hardware register configuration for FFI crossing
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
        p.state.q = [0.0; 40];
        p.state.p = [1.0; 40]; // Initialize momentum non-zero to satisfy boundary rest conditions
        p.matrix = [0.0; DIM_80 * DIM_80];
    }
}
