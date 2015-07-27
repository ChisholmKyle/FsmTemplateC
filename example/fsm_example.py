import sys
import os
sys.path.append(os.path.abspath("../"))
import template.fsm as fsm

prefix = 'fsm_example'

fsm_param = {
    'type': 'FsmExample',
    'states': ['one', 'two', 'three', 'four']
    # 'fopts': {
    #     'type': 'FsmExampleFopts *',
    #     'name': 'example_fopts'
    # }
}

folder = 'fsm_example'

# get code snippets
code = fsm.Fsm(fsm_param).ccodefiles(folder, prefix)
