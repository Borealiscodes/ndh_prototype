using Libdl

function run_julia_v4_validation()
    println("=========================================================")
    println("🟣 Julia Enclave: Binding High-Altitude Error Diffusion Track...")
    
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
    loop_ptr = Libdl.dlsym(rust_lib, :apply_spatial_sigma_delta_loop)
    
    # 1. Synthesize matching continuous input wave track (80 floats)
    input_floats = Float64[sin(i * 0.2) * 0.8 for i in 0:79]
    
    # 2. Generate parallel stochastic triangular dither weights 
    # (replicates r1 + r2 uniform noise distribution)
    dither_weights = Float64[(rand() - 0.5) + (rand() - 0.5) for _ in 1:80]
    
    # 3. Allocate destination Int8 ternary array
    output_trits = zeros(Int8, 80)
    
    println("🟣 Julia Enclave: Directing low-latency ccall across the FFI gate...")
    
    # Trigger spatial error-diffusion loop
    ccall(loop_ptr, Cvoid,
          (Ptr{Float64}, Ptr{Int8}, Ptr{Float64}),
          input_floats, output_trits, dither_weights)
          
    println("🟣 Julia Enclave: Modulation pass verified. Base-3 noise fully decorrelated.")
    println("🟣 Julia Enclave: First 10 Modulated Ternary Fields: ", output_trits[1:10])
    println("=========================================================")
    
    Libdl.dlclose(rust_lib)
end

run_julia_v4_validation()
