import sys
import os
import template.fsm as fsm

# function prefix
prefix = 'fsm_example'

# dict parameter for generating FSM
fsm_param = {
    # struct type base name
    'type': 'FsmExample',
    # list of states (can be any length > 0)
    'states': ['one', 'two', 'three', 'four'],
    # list of inputs (can be any length > 0)
    'inputs': ['a', 'b', 'c'],
    # map inputs to commands (next desired state) using a transition table
    # index corresponds to 'inputs' array
    # for this example, index 0 is 'a', index 1 is 'b', and index 2 is 'c'
    'transitiontable': {
        'one':   [  'two',     '', 'four'],
        'two':   ['three',  'one',     ''],
        'three': [  'two', 'four',  'one'],
        'four':  [     '',  'one',     '']
    }
}

# folder to contain generated code
folder = 'fsm_example'

# generate FSM code
fsm.Fsm(fsm_param).genccode(folder, prefix)

# folder to contain generated code
folder = 'fsm_example_cpp'
# C++ interface (optional)
fsm_param['cpp'] = True
# generate FSM code
fsm.Fsm(fsm_param).genccode(folder, prefix)
