import ctypes
from ndh_core import NDHEngine, QuestOperator80x80

def run_python_quest_algebra_validation():
    print("=========================================================")
    print("🏗️ Python Enclave: Initializing Quest Algebra Verification...")
    engine = NDHEngine()
    
    # 1. Instantiate separate quest milestone operator matrices
    quest_alpha = QuestOperator80x80()  # e.g., Choice A: Align with Faction
    quest_beta = QuestOperator80x80()   # e.g., Choice B: Unlock Technology
    composite_milestone = QuestOperator80x80()
    
    # 2. Populate structural baseline metrics inside the matrices
    for i in range(80):
        quest_alpha.rows[i].data[i] = 1   # Main diagonal identity tracking
        if i < 79:
            quest_beta.rows[i].data[i+1] = -1 # Cross-layer vector offset modifier
            
    # 3. Create a mock 80-dimensional narrative trajectory tracking vector
    current_story_state = (ctypes.c_double * 80)(*[1.0 for _ in range(80)])
    next_story_state = (ctypes.c_double * 80)(*[0.0 for _ in range(80)])
    
    print("🏗️ Python Enclave: Composing Quest Alpha and Quest Beta into unified timeline checkpoint...")
    
    # Execute non-commutative operator composition through the FFI boundary
    engine.lib.compose_quest_operators_80d(
        ctypes.byref(quest_alpha),
        ctypes.byref(quest_beta),
        ctypes.byref(composite_milestone)
    )
    
    print("🏗️ Python Enclave: Projecting composite operator against active story trajectory...")
    engine.lib.apply_quest_operator_80d(
        ctypes.byref(composite_milestone),
        ctypes.cast(current_story_state, ctypes.POINTER(ctypes.c_double)),
        ctypes.cast(next_story_state, ctypes.POINTER(ctypes.c_double))
    )
    
    print("🏗️ Python Enclave: Target narrative state-space computed safely.")
    print(f"🏗️ Python Enclave: First 5 Trajectory Output Channels: {[next_story_state[i] for i in range(5)]}")
    print("=========================================================")

if __name__ == "__main__":
    run_quest_algebra_validation()
