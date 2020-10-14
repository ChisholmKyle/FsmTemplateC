import sys
import os
sys.path.append(os.path.abspath("../"))
import template.fsm as fsm

# Example courtesy of https://github.com/Borbonjuggler

# dict parameter for generating FSM
fsm_param = {
    # struct type base name
    'type': 'FsmLZA',
    # struct type and name for passing data to state machine functions
    # by pointer (these custom names are optional)
    'fopts': {
        'type': 'FsmLZAFopts',
        'name': 'fopts'
    },
    # list of states (can be any length > 0)
    'states': [ 'init', 'resetLight', 'setYellowLight', 'setRedLight', 'security' ],
    # list of inputs (can be any length > 0)
    'inputs': [ 'RADIO_READY', 'OCCUPIED', 'NOT_OCCUPIED', 'TIME_UP', 'SECURITY' ],
    
    # map inputs to commands (next desired state) using a transition table
    'transitiontable': {
        # current state     |'RADIO_READY'|   'OCCUPIED'    | 'NOT_OCCUPIED' |  'TIME_UP'   |  'SECURITY' |
        'init':             [ 'resetLight',               '',               '',            '',          '' ],
        'resetLight':       [           '', 'setYellowLight',               '',            '',  'security' ],
        'setYellowLight':   [           '',               '',               '', 'setRedLight',  'security' ],
        'setRedLight':      [           '',    'setRedLight',     'resetLight',            '',  'security' ],
        'security':         [           '',               '',               '',            '',           '']         
    }
}

# function prefix
prefix = 'fsm_LZA'

# folder to contain generated code
folder = 'fsm_LZA'

# generate FSM code
code = fsm.Fsm(fsm_param).genccode(folder, prefix)
