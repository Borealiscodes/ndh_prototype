using Libdl

function run_julia_quest_algebra_validation()
    println("=========================================================")
    println("🟣 Julia Enclave: Binding High-Altitude Quest Algebra Substrate...")
    
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
    compose_ptr = Libdl.dlsym(rust_lib, :compose_quest_operators_80d)
    apply_ptr = Libdl.dlsym(rust_lib, :apply_quest_operator_80d)
    
    # 1. Allocate matching 80-dimensional story state tracking vectors
    current_story_state = ones(Float64, 80)
    next_story_state = zeros(Float64, 80)
    
    # 2. Build flat 6400-element data fields to represent the 80x80 operators
    raw_op_alpha = zeros(Int8, 6400)
    raw_op_beta = zeros(Int8, 6400)
    raw_composite = zeros(Int8, 6400)
    
    # Populate the array offsets to mirror the Python configuration logic
    for i in 0:79
        raw_op_alpha[(i * 80) + i + 1] = 1 # Julia uses 1-based indexing for calculations
        if i < 79
            raw_op_beta[(i * 80) + i + 2] = -1
        end
    end
    
    println("🟣 Julia Enclave: Invoking low-latency FFI narrative composition layer...")
    
    # Compile the quest operators together
    ccall(compose_ptr, Cvoid,
          (Ptr{Int8}, Ptr{Int8}, Ptr{Int8}),
          raw_op_alpha, raw_op_beta, raw_composite)
          
    println("🟣 Julia Enclave: Projecting composite state transitions across the vector space...")
    
    # Apply the combined checkpoint matrix to the trajectory path
    ccall(apply_ptr, Cvoid,
          (Ptr{Int8}, Ptr{Float64}, Ptr{Float64}),
          raw_composite, current_story_state, next_story_state)
          
    println("🟣 Julia Enclave: Narrative trajectory updated successfully.")
    println("🟣 Julia Enclave: First 5 Calculated Story Coordinates: ", next_story_state[1:5])
    println("=========================================================")
    
    Libdl.dlclose(rust_lib)
end

run_julia_quest_algebra_validation()
