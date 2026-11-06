use std::process::Command;
use std::path::Path;

fn main() {
    // 1. Establish structural file tracking pathways
    let lean_proof_path = "lean/ManifoldAxioms.lean";
    
    // Tell Cargo to re-run this validation check if the Lean math script changes
    println!("cargo:rerun-if-changed={}", lean_proof_path);

    // 2. Verify that the Lean 4 compiler substrate exists in the environment
    if !Path::new(lean_proof_path).exists() {
        panic!(
            "💥 CRITICAL ERROR: Lean 4 proof file missing at '{}'. \
            Verification enclave boundary breached. Aborting compilation.", 
            lean_proof_path
        );
    }

    print!("Executing High-Altitude Lean 4 Verification Proof Invariants... ");

    // 3. Invoke Lean 4 to type-check and mathematically verify the manifold constraints
    let lean_status = Command::new("lean")
        .arg(lean_proof_path)
        .status();

    // 4. Evaluate the compiler gate outcome
    match lean_status {
        Ok(status) if status.success() => {
            println!("✅ VERIFIED. Mathematical invariants check out.");
            println!("Proceeding safely to native Rust binary compilation layer.");
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
}
