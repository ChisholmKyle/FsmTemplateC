import sys
import os
sys.path.append(os.path.abspath("../"))
import template.fsm as fsm

# function prefix
prefix = 'fsm_turnstile'

# dict parameter for generating FSM
fsm_param = {
    # struct type string
    'type': 'FsmTurnstile',
    # list of states
    'states': ['locked', 'unlocked'],
    # struct type and name for passing data to state machine functions
    # by pointer
    'fopts': {
        'type': 'FsmTurnstileFopts',
        'name': 'fopts'
    }
}

# folder to contain generated code
folder = 'turnstile_example'

# generate FSM code
code = fsm.Fsm(fsm_param).genccode(folder, prefix)
