using Libdl

# Define structural mirrors to match the FFI serialization layouts precisely
struct SymplecticState
    q::NTuple{40, Float64}
    p::NTuple{40, Float64}
end

function run_julia_rasa_validation()
    println("=========================================================")
    println("🟣 Julia Enclave: Binding High-Altitude Rasa Geometry Substrate...")
    
    # Locate shared library binary pathway
    lib_name = "libndh_core_rust.so"
    if Sys.isapple()
        lib_name = "libndh_core_rust.dylib"
    elseif Sys.iswindows()
        lib_name = "ndh_core_rust.dll"
    end
    
    lib_path = joinpath(@__DIR__, "target", "release", lib_name)
    if !isfile(lib_path)
        lib_path = joinpath(@__DIR__, "target", "debug", lib_name)
    end
    
    rust_lib = Libdl.dlopen(lib_path)
    rasa_ptr = Libdl.dlsym(rust_lib, :apply_rasa_curvature_flow)
    
    # 1. Allocate initial Symplectic canonical tracking variables
    q_data = ones(Float64, 40)
    p_data = ones(Float64, 40)
    
    # 2. Build flat 6400-element discrete data fields to represent the 80x80 tensor
    raw_tensor_data = Int8[((div(i, 80) + mod(i, 80)) % 3 == 1 ? 1 : ((div(i, 80) + mod(i, 80)) % 3 == 2 ? -1 : 0)) for i in 0:6399]
    
    println("🟣 Julia Enclave: Invoking direct low-latency ccall transformation step...")
    
    # Execute emotional momentum mutation (eta scale = 0.05)
    scaling_eta = 0.05
    
    # In Julia, we pass mutable arrays directly as pointers to match Rust structures
    ccall(rasa_ptr, Cvoid,
          (Ptr{Int8}, Ptr{Float64}, Float64),
          raw_tensor_data, [q_data; p_data], scaling_eta)
          
    println("🟣 Julia Enclave: Curvature-flow computation completed successfully.")
    # Extract the first 5 mutated momentum elements from the combined state vector path
    println("🟣 Julia Enclave: Enforced Momentum Outputs [p]: ", p_data[1:5])
    println("=========================================================")
    
    Libdl.dlclose(rust_lib)
end

run_julia_rasa_validation()
