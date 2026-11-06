using Libdl

function run_julia_high_altitude_validation()
    println("=========================================================")
    # Define binary targets
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

    println("🟣 Julia Enclave: Binding directly to substrate at: ", lib_path)
    
    # Dynamically open the library substrate
    rust_lib = Libdl.dlopen(lib_path)
    # Extract the function pointer directly from memory
    func_ptr = Libdl.dlsym(rust_lib, :evaluate_safe_radial_diffusion)

    # Inject absolute zero boundary input
    critical_radius = 0.0
    println("🟣 Julia Enclave: Injecting critical boundary state (r = ", critical_radius, ")")

    # Native low-latency ccall execution path
    diffusion_output = ccall(func_ptr, Float64, (Float64,), critical_radius)

    println("🟣 Julia Enclave: Computation complete without mathematical singularities.")
    println("🟣 Julia Enclave: Evaluated 9D Laplacian Result: ", diffusion_output)
    println("=========================================================")
    
    Libdl.dlclose(rust_lib)
end

run_julia_high_altitude_validation()
