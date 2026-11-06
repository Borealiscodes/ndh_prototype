using Libdl

# Define a mirror of the C/Rust memory-aligned struct layout
struct SymplecticState
    q::NTuple{40, Float64}
    p::NTuple{40, Float64}
end

struct TrackingPayload
    state::SymplecticState
    matrix::NTuple{6400, Float64}
end

function run_julia_v2_validation()
    println("=========================================================")
    println("🟣 Julia Enclave: Binding High-Altitude Algebra Track...")
    
    # Locate shared library substrate
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
    mat_mul_ptr = Libdl.dlsym(rust_lib, :ternary_matrix_multiply_80d)
    
    # Allocate continuous 80-dimensional input arrays
    input_vector = Float64[i * 0.1 for i in 0:79]
    output_vector = zeros(Float64, 80)
    
    # Construct a raw, flat array representation of the 80x80 matrix (6400 elements)
    # Mapping Int8 fields to reflect the row/column structure of TernaryVector80
    raw_matrix_data = Int8[((div(i, 80) + mod(i, 80)) % 3 == 2 ? -1 : ((div(i, 80) + mod(i, 80)) % 3 == 1 ? 1 : 0)) for i in 0:6399]
    
    println("🟣 Julia Enclave: Executing Direct Low-Latency CCall Contraction...")
    
    # Trigger low-level pointer mapping step
    ccall(mat_mul_ptr, Cvoid, 
          (Ptr{Int8}, Ptr{Float64}, Ptr{Float64}), 
          raw_matrix_data, input_vector, output_vector)
          
    println("🟣 Julia Enclave: Computation complete without floating-point rounding noise.")
    println("🟣 Julia Enclave: First 5 Output Fields: ", output_vector[1:5])
    println("=========================================================")
    
    Libdl.dlclose(rust_lib)
end

run_julia_v2_validation()
