import sys
import os
import template.fsm as fsm

# dict parameter for generating FSM
fsm_param = {
    # main FSM struct type string
    'type': 'FsmTurnstile',
    # struct type and name for passing data to state machine functions
    # by pointer (these custom names are optional)
    'fopts': {
        'type': 'FsmTurnstileFopts',
        'name': 'fopts'
    },
    # list of states
    'states': ['locked', 'unlocked'],
    # list of inputs (can be any length > 0)
    'inputs': ['coin', 'push'],
    # map inputs to commands (next desired state) using a transition table
    # index of array corresponds to 'inputs' array
    # for this example, index 0 is 'coin', index 1 is 'push'
    'transitiontable': {
        # current state |  'coin'  |  'push'  |
        'locked':       ['unlocked',        ''],
        'unlocked':     [        '',  'locked']
    }
}

# folder to contain generated code
folder = 'turnstile_example'
# function prefix
prefix = 'fsm_turnstile'

# generate FSM code
fsm.Fsm(fsm_param).genccode(folder, prefix)
