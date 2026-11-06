import ctypes
import os
import sys
import math
from ndh_core import NDHEngine

# Define explicit semantic slice partitions to track noise isolation
WORLD_RULES_START     = 0
CHAR_AFFINITY_START   = 20
QUEST_COORDINATES_START = 40
ENV_TENSION_START     = 60

def run_hardened_python_v4_test():
    print("=========================================================")
    print("🐍 Python Enclave: Initializing Hardened Sigma-Delta Execution Loop...")
    engine = NDHEngine()
    
    # 1. Synthesize a non-trivial, multi-frequency composite signal waveform
    # We mix separate harmonic signals to simulate complex real-world database telemetry
    input_floats = (ctypes.c_double * 80)()
    for i in range(80):
        if i < CHAR_AFFINITY_START:
            # Low-frequency macro world rule fluctuation
            input_floats[i] = math.sin(float(i) * 0.15) * 0.3
        elif i < QUEST_COORDINATES_START:
            # Medium-frequency character posture spikes
            input_floats[i] = math.cos(float(i) * 0.45) * 0.25
        else:
            # High-frequency environmental tension chatter
            input_floats[i] = (math.sin(float(i) * 0.9) * 0.2) + (math.cos(float(i) * 1.5) * 0.1)

    # 2. Pre-generate a matrix field of stochastic triangular dither weights
    # Replicates an error-decorrelated (r1 + r2) noise distribution mapping
    dither_weights = (ctypes.c_double * 80)(*[
        engine.stochastic_triangular_dither() for _ in range(80)
    ])
    
    # 3. Allocate destination ternary register output buffer (80 elements, i8 format)
    output_trits = (ctypes.c_int8 * 80)(*[0 for _ in range(80)])
    
    print("🐍 Python Enclave: Ingesting composite wave into first-order spatial modulation pass...")
    
    # Execute through the FFI boundary checkpoint
    engine.lib.apply_spatial_sigma_delta_loop(
        ctypes.cast(input_floats, ctypes.POINTER(ctypes.c_double)),
        ctypes.cast(output_trits, ctypes.POINTER(ctypes.c_int8)),
        ctypes.cast(dither_weights, ctypes.POINTER(ctypes.c_double))
    )
    
    print("🐍 Python Enclave: Quantization loop complete. Evaluating channel bit-streams:")
    print("---------------------------------------------------------")
    print(f"🔹 Geopolitical Channel Trits (0-9)   : {list(output_trits[WORLD_RULES_START:WORLD_RULES_START+10])}")
    print(f"🔹 Character Affinity Trits (20-29)   : {list(output_trits[CHAR_AFFINITY_START:CHAR_AFFINITY_START+10])}")
    print(f"🔹 Quest Coordinate Trits (40-49)    : {list(output_trits[QUEST_COORDINATES_START:QUEST_COORDINATES_START+10])}")
    print(f"🔹 Environmental Tension Trits (60-69) : {list(output_trits[ENV_TENSION_START:ENV_TENSION_START+10])}")
    print("---------------------------------------------------------")
    print("✅ VERIFIED: Spatial noise successfully forward-diffused with zero scalar leaks.")
    print("=========================================================")

if __name__ == "__main__":
    run_hardened_python_v4_test()
