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
    'states': ['one', 'two', 'three', 'four']
    # optional data type and name for passing data to state machine functions
    # 'fopts': {
    #     'type': 'FsmExampleFopts *',
    #     'name': 'example_fopts'
    # }
}

# folder to contain generated code
folder = 'fsm_example'

# generate FSM code
code = fsm.Fsm(fsm_param).ccodefiles(folder, prefix)
