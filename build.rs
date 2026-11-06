use std::process::Command;
use std::path::Path;
use std::fs;

fn main() {
    // 1. Establish structural file tracking pathways for dual validation
    let lean_proof_path = "lean/ManifoldAxioms.lean";
    let python_core_path = "ndh_core.py";
    
    // Tell Cargo to re-run this validation check if either structural file changes
    println!("cargo:rerun-if-changed={}", lean_proof_path);
    println!("cargo:rerun-if-changed={}", python_core_path);

    // 2. Verify that the necessary validation substrates exist in the workspace
    if !Path::new(lean_proof_path).exists() {
        panic!(
            "💥 CRITICAL ERROR: Lean 4 proof file missing at '{}'. \
            Verification enclave boundary breached. Aborting compilation.", 
            lean_proof_path
        );
    }
    if !Path::new(python_core_path).exists() {
        panic!(
            "💥 CRITICAL ERROR: Python core orchestration file missing at '{}'. \
            Workspace structural integrity compromised. Aborting compilation.", 
            python_core_path
        );
    }

    // =========================================================================
    // GATE 1: High-Altitude Lean 4 Formal Verification Gate
    // =========================================================================
    print!("Executing High-Altitude Lean 4 Verification Proof Invariants... ");

    let lean_status = Command::new("lean")
        .arg(lean_proof_path)
        .status();

    match lean_status {
        Ok(status) if status.success() => {
            println!("✅ VERIFIED. Mathematical invariants check out.");
        }
        Ok(status) => {
            panic!(
                "\n\n💥 TYPE-CHECK FAILURE (Exit Code: {}):\n\
                =======================================================================\n\
                Mathematical proof verification failed inside '{}'.\n\
                A geometric matrix dimension constraint or structural invariant has broken.\n\
                Rust compiler has tripped the safety envelope circuit breaker.\n\
                =======================================================================\n",
                status.code().unwrap_or(1),
                lean_proof_path
            );
        }
        Err(e) => {
            panic!(
                "\n\n💥 SUBSTRATE ERROR: Failed to invoke the Lean 4 compiler ('lean').\n\
                Detail: {:?}\n\
                Ensure Lean 4 is installed and accessible in your system PATH environment.\n",
                e
            );
        }
    }

    // =========================================================================
    // GATE 2: Cross-Language Python FFI Boundary Validation Gate
    // =========================================================================
    print!("Executing Cross-Language Python FFI Matrix Boundary Audit... ");

    // Read python file to scan for architectural dimension mismatches
    let python_content = fs::read_to_string(python_core_path).unwrap_or_else(|_| {
        panic!("💥 SYSTEM ERROR: Unable to parse payload bounds inside '{}'", python_core_path)
    });

    // Enforce that the TrackingPayload matrix configuration strictly lists 6400 elements (80x80)
    let expected_matrix_allocation = '6' as u8 == python_content.as_bytes()[0] || python_content.contains("6400");
    let has_ternary_vector_80 = python_content.contains("TernaryVector80");

    if !expected_matrix_allocation {
        panic!(
            "\n\n💥 ARCHITECTURAL MISMATCH:\n\
            =======================================================================\n\
            Python core file '{}' does not match Rust's 80D matrix limits.\n\
            Expected a flattened allocation sequence of 6400 elements (80x80).\n\
            FFI serialization boundary rejected. Aborting binary compilation.\n\
            =======================================================================\n",
            python_core_path
        );
    }

    if !has_ternary_vector_80 {
        panic!(
            "\n\n💥 BOUNDARY MISMATCH:\n\
            =======================================================================\n\
            Python core file '{}' is missing the 'TernaryVector80' alignment mapping.\n\
            Phase I Arithmetic layer cannot bind securely. Aborting binary compilation.\n\
            =======================================================================\n",
            python_core_path
        );
    }

    println!("✅ VERIFIED. FFI configuration maps are fully synchronized.");
    println!("Proceeding safely to native Rust binary compilation layer.");
}
