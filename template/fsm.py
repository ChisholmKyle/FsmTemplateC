import os
import errno
from jinja2 import Template

_fsm_header_template = Template("""\
#ifndef {{ header.basename|upper }}_H
#define {{ header.basename|upper }}_H

/* ***************
 * Include Files *
 * ***************/

{% for inc_file in header.include -%}
#include "{{ inc_file }}"
{%- endfor %}

/* ***************************
 * Typedefs and Declarations *
 * ***************************/

{% for code_snippet in header.code -%}
{{ code_snippet }}

{% endfor %}
#endif
""")

_fsm_src_template = Template("""\
#define _POSIX_C_SOURCE 200809L
#include <unistd.h>

/* ***************
 * Include Files *
 * ***************/

{% for inc_file in src.include -%}
#include "{{ inc_file }}"
{%- endfor %}

/* ***********
 * Functions *
 * ***********/

{% for code_snippet in src.code -%}
{{ code_snippet }}

{% endfor %}
""")

_fsm_decl_template = Template("""\
/* function options (EDIT) */
typedef struct {{ param.fopts.type }} {
    /* define your options struct here */
} {{ param.fopts.type }};

/* transition check */
typedef enum e{{ param.type }}Check {
\tE{{ prefix|upper }}_TR_RETREAT,
\tE{{ prefix|upper }}_TR_ADVANCE,
\tE{{ prefix|upper }}_TR_CONTINUE,
\tE{{ prefix|upper }}_TR_BADINPUT
} e{{ param.type }}Check;

/* states (enum) */
typedef enum e{{ param.type }}State {
{%- for state in param.states %}
\tE{{ prefix|upper }}_ST_{{ state|upper }},
{%- endfor %}
\tE{{ prefix|upper }}_NUM_STATES
} e{{ param.type }}State;

/* inputs (enum) */
typedef enum e{{ param.type }}Input {
{%- for input in param.inputs %}
\tE{{ prefix|upper }}_IN_{{ input|upper }},
{%- endfor %}
\tE{{ prefix|upper }}_NUM_INPUTS,
\tE{{ prefix|upper }}_NOINPUT
} e{{ param.type }}Input;

/* finite state machine struct */
typedef struct {{ param.type }} {
\te{{ param.type }}Input input;
\te{{ param.type }}Check check;
\te{{ param.type }}State cur;
\te{{ param.type }}State cmd;
\te{{ param.type }}State **transition_table;
\tvoid (***state_transitions)(struct {{ param.type }} *, {{ param.fopts.type }} *);
\tvoid (*run)(struct {{ param.type }} *, {{ param.fopts.type }} *, const e{{ param.type }}Input);
} {{ param.type }};

/* transition functions */
typedef void (*p{{ param.type }}StateTransitions)\
(struct {{ param.type }} *, {{ param.fopts.type }} *);

/* fsm declarations */
{%  for stateone in param.states -%}
{%- for statetwo in param.states -%}
{%- if stateone == statetwo or not stateone in param.transitiontable or statetwo in param.transitiontable[stateone] -%}
void {{ prefix|lower }}_{{ stateone|lower }}_{{ statetwo|lower }} \
({{ param.type }} *fsm, {{ param.fopts.type }} *{{ param.fopts.name }});
{%  endif -%}
{%  endfor -%}
{%  endfor -%}
void {{ prefix|lower }}_run ({{ param.type }} *fsm, \
{{ param.fopts.type }} *{{ param.fopts.name }}, \
const e{{ param.type }}Input input);

/* creation macro */
#define {{ prefix|upper }}_CREATE() \\
{ \\
\t.input = E{{ prefix|upper }}_NOINPUT, \\
\t.check = E{{ prefix|upper }}_TR_CONTINUE, \\
\t.cur = E{{ prefix|upper }}_ST_{{ param.states|first|upper }}, \\
\t.cmd = E{{ prefix|upper }}_ST_{{ param.states|first|upper }}, \\
\t.transition_table = (e{{ param.type }}State * \
[E{{ prefix|upper }}_NUM_STATES]) { \\
{%  for state in param.states %}\t\t(e{{ param.type }}State \
[E{{ prefix|upper }}_NUM_INPUTS]) { \\
{% for next_state in param.transitiontable[state] %}\t\t\t\
{%  if next_state in param.states -%}
E{{ prefix|upper }}_ST_{{ next_state|upper }}
{%- else -%}
E{{ prefix|upper }}_ST_{{ state|upper }}
{%- endif %}
{%- if loop.last %} \\
{%  else -%}, \\
{%  endif -%}
{%- endfor -%}
{%- if loop.last %}\t\t} \\
{%  else %}\t\t}, \\
{%  endif -%}
{%- endfor %}\t}, \\
\t.state_transitions = (p{{ param.type }}StateTransitions * \
[E{{ prefix|upper }}_NUM_STATES]) { \\
{%  for stateone in param.states %}\t\t(p{{ param.type }}StateTransitions \
[E{{ prefix|upper }}_NUM_STATES]) { \\
{% for statetwo in param.states %}\t\t\t\
{% if not stateone == statetwo and stateone in param.transitiontable and not statetwo in param.transitiontable[stateone] -%}
NULL
{%- else -%}
{{ prefix|lower }}_{{ stateone|lower }}_{{ statetwo|lower }}
{%- endif -%}
{%- if loop.last %} \\
{% else -%}, \\
{% endif -%}
{%- endfor -%}
{%- if loop.last %}\t\t} \\
{% else %}\t\t}, \\
{% endif -%}
{%- endfor %}\t}, \\
\t.run = {{ prefix|lower }}_run \\
}
""")

_fsm_fcns_template = Template("""\
/*--------------------------*
 *  RUNNING STATE FUNCTIONS *
 *--------------------------*/
{% for state in param.states %}
/**
 *  @brief Running function in state `{{ state|lower }}`
 */
void {{ prefix|lower }}_{{ state|lower }}_{{ state|lower }} \
({{ param.type }} *fsm, {{ param.fopts.type }} *{{ param.fopts.name }}) {

    /* check if this function was called from a transition. */
    if (fsm->check == E{{ prefix|upper }}_TR_ADVANCE) {
        /* transitioned from fsm->cur to fsm->cmd (here) */
    } else if (fsm->check == E{{ prefix|upper }}_TR_RETREAT) {
        /* fell back to fsm->cur (here) from fsm->cmd */
    } else {
        /* no prior transition (fsm->check == E{{ prefix|upper }}_TR_CONTINUE) */
    }

}
{% endfor %}

/*----------------------*
 * TRANSITION FUNCTIONS *
 *----------------------*/
{%  for stateone in param.states -%}{%  for statetwo in param.states -%}
{% if (stateone != statetwo) -%}
{% if not stateone in param.transitiontable or statetwo in param.transitiontable[stateone] %}
/**
 *  @brief Transition function from `{{ stateone|lower }}` to `{{ statetwo|lower }}`
 *
 *  @details
 *
 *  To advance to '{{ statetwo|lower }}' state, set
 *  `fsm->check = E{{ prefix|upper }}_TR_ADVANCE;`
 *  To return to '{{ stateone|lower }}' state, set
 *  `fsm->check = E{{ prefix|upper }}_TR_RETREAT;`
 */
void {{ prefix|lower }}_{{ stateone|lower }}_{{ statetwo|lower }} \
({{ param.type }} *fsm, {{ param.fopts.type }} *{{ param.fopts.name }}) {

    /* by default, do not transition (guard/retreat) */
    (void)({{ param.fopts.name }});
    fsm->check = E{{ prefix|upper }}_TR_RETREAT;

    /* Transition code goes here.

       NOTE: Before returning from this function,
       Consider setting transition to
       advance: fsm->check = E{{ prefix|upper }}_TR_ADVANCE; */

}
{% endif -%}
{% endif -%}
{% endfor -%}
{% endfor %}

/*-------------------*
 * RUN STATE MACHINE *
 *-------------------*/

/**
 *  @brief Run state machine
 */
void {{ prefix|lower }}_run ({{ param.type }} *fsm, \
{{ param.fopts.type }} *{{ param.fopts.name }}, \
const e{{ param.type }}Input input) {

    /* transition table - get command from input */
    if (input < E{{ prefix|upper }}_NUM_INPUTS) {
        fsm->input = input;
        fsm->cmd = fsm->transition_table[fsm->cur][input];
        if (fsm->cmd == fsm->cur) {
            /* not able to go to new input */
            fsm->check = E{{ prefix|upper }}_TR_BADINPUT;
        }
    }

    /* run process */
    if (fsm->state_transitions[fsm->cur][fsm->cmd] == NULL) {
        fsm->check = E{{ prefix|upper }}_TR_RETREAT;
    } else {
        fsm->state_transitions[fsm->cur][fsm->cmd](fsm, {{ param.fopts.name }});
    }

    /* advance to requested state or return to current state */
    if (fsm->cmd != fsm->cur) {
        if (fsm->check == E{{ prefix|upper }}_TR_ADVANCE) {
            fsm->state_transitions[fsm->cmd][fsm->cmd](fsm, {{ param.fopts.name }});
            fsm->cur = fsm->cmd;
        } else {
            fsm->state_transitions[fsm->cur][fsm->cur](fsm, {{ param.fopts.name }});
            fsm->cmd = fsm->cur;
        }
    }

    /* continue running */
    fsm->input = E{{ prefix|upper }}_NOINPUT;
    fsm->check = E{{ prefix|upper }}_TR_CONTINUE;
}
""")

def mkdir_p(path):
    """Helper function to mimic bash command 'mkdir -p'"""
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class Fsm(object):
    def __init__(self, fsm_param):
        """FSM parameters"""

        self.param = {
            'type': fsm_param['type'],
            'states': fsm_param['states'],
            'inputs': fsm_param['inputs'],
            'transitiontable': fsm_param['transitiontable'],
            'fopts': {
                'type': fsm_param['type'] + 'Opts',
                'name': 'fopts'
            }
        }

        if 'fopts' in fsm_param:
            if 'type' in fsm_param['fopts']:
                self.param['fopts']['type'] = fsm_param['fopts']['type']
            if 'name' in fsm_param['fopts']:
                self.param['fopts']['name'] = fsm_param['fopts']['name']


    def genccode(self, folder, prefix):
        """Create C code"""

        # render code templates
        fsm_decl = _fsm_decl_template.render(prefix=prefix,
                                             param=self.param)
        fsm_fcns = _fsm_fcns_template.render(prefix=prefix,
                                             param=self.param)

        # include file
        header = {
            'filename': "{b}.h".format(b=prefix),
            'basename': prefix,
            'code': [fsm_decl],
            'include': []
        }

        # src file
        src = {
            'filename': "{b}.c".format(b=prefix),
            'code': [fsm_fcns],
            'include': [header['filename']]
        }

        # code wrapper templates
        header_str = _fsm_header_template.render(header=header)
        src_str = _fsm_src_template.render(src=src)

        # make directory
        path = os.path.abspath(folder)
        mkdir_p(path)

        # write header file
        f = open(os.path.join(path, header['filename']), "w")
        f.write(header_str)
        f.close()

        # write source file
        f = open(os.path.join(path, src['filename']), "w")
        f.write(src_str)
        f.close()
