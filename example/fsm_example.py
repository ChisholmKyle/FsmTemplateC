import sys
import os
sys.path.append(os.path.abspath("../"))
import template.fsm as fsm

# function prefix
prefix = 'fsm_example'

# dict parameter for generating FSM
fsm_param = {
    # struct type string
    'type': 'FsmExample',
    # list of states (can be any length)
    'states': ['one', 'two', 'three', 'four'],
    # struct type and name for passing data to state machine functions
    # by pointer
    'fopts': {
        'type': 'FsmExampleFopts',
        'name': 'fopts'
    }
}

# folder to contain generated code
folder = 'fsm_example'

# generate FSM code
code = fsm.Fsm(fsm_param).ccodefiles(folder, prefix)
