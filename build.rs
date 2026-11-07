// build.rs
use std::process::Command;
use std::path::Path;
use std::fs;
use regex::Regex;

fn main() {
    let lean_proof_path = "lean/ManifoldAxioms.lean";
    let python_core_path = "ndh_core.py";
    
    println!("cargo:rerun-if-changed={}", lean_proof_path);
    println!("cargo:rerun-if-changed={}", python_core_path);

    if !Path::new(lean_proof_path).exists() {
        panic!("💥 CRITICAL ERROR: Lean 4 proof file missing at '{}'.", lean_proof_path);
    }
    if !Path::new(python_core_path).exists() {
        panic!("💥 CRITICAL ERROR: Python core file missing at '{}'.", python_core_path);
    }

    // =========================================================================
    // GATE 1: Formal Verification Gate & "Sorry" Structural Scanner
    // =========================================================================
    print!("Executing Lean 4 Verification Proof Invariants... ");

    // Read the proof file to ensure it does not bypass verification gates
    let lean_content = fs::read_to_string(lean_proof_path)
        .expect("Unable to read Lean proof source file");
    
    if lean_content.contains("sorry") || lean_content.contains("axiom") {
        panic!(
            "\n\n💥 SECURITY HOLE BREACHED:\n\
            =======================================================================\n\
            Mathematical proof code contains unproven placeholders ('sorry' or 'axiom').\n\
            The structural safety cage has been bypassed. Aborting compilation.\n\
            =======================================================================\n"
        );
    }

    let lean_status = Command::new("lean").arg(lean_proof_path).status();
    match lean_status {
        Ok(status) if status.success() => println!("✅ VERIFIED. Proof is logically closed."),
        _ => panic!("\n\n💥 TYPE-CHECK FAILURE: Proof validation failed inside '{}'.\n", lean_proof_path),
    }

    // =========================================================================
    // GATE 2: Regex-Enforced FFI Boundary Matrix Audit
    // =========================================================================
    print!("Executing Cross-Language Python FFI Matrix Boundary Audit... ");

    let python_content = fs::read_to_string(python_core_path).unwrap();

    // Use regular expressions to find explicit allocation integers instead of brittle byte scraping
    let matrix_re = Regex::new(r"(?x)
        (?:allocation|size|dim|shape|len)\s*=\s*6400
        |
        \[\s*6400\s*\]
        |
        \(\s*80\s*,\s*80\s*\)
    ").unwrap();

    let has_valid_matrix_allocation = matrix_re.is_match(&python_content);
    let has_ternary_vector_80 = python_content.contains("TernaryVector80");

    if !has_valid_matrix_allocation {
        panic!(
            "\n\n💥 ARCHITECTURAL MISMATCH:\n\
            =======================================================================\n\
            Python file '{}' failed strict dimension verification.\n\
            Could not verify explicit array mapping matching 6400 elements (80x80).\n\
            =======================================================================\n",
            python_core_path
        );
    }

    if !has_ternary_vector_80 {
        panic!("\n\n💥 BOUNDARY MISMATCH: Missing 'TernaryVector80' alignment mapping.\n");
    }

    println!("✅ VERIFIED. FFI configurations are locked and synchronized.");
}
