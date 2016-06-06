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
    # struct type and name for passing data to state machine functions
    # by pointer
    'fopts': {
        'type': 'FsmTurnstileFopts',
        'name': 'fopts'
    },
    # list of states
    'states': ['locked', 'unlocked'],
    # list of inputs (can be any length > 0)
    'inputs': ['coin', 'push'],
    # map inputs to commands (next desired state) using a transition table
    # index corresponds to 'inputs' array
    # for this example, index 0 is 'a', index 1 is 'b', and index 2 is 'c'
    'transitiontable': {
        'locked':   ['unlocked',       ''],
        'unlocked': [        '', 'locked']
    }
}

# folder to contain generated code
folder = 'turnstile_example'

# generate FSM code
code = fsm.Fsm(fsm_param).genccode(folder, prefix)
