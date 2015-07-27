from template import utils
from jinja2 import Template

_fsm_decl_include_list = []
_fsm_fcns_include_list = []

_fsm_decl_template = Template("""\
/* transition check */
typedef enum e{{ param.type }}Check {
\tE{{ prefix|upper }}_TR_RETREAT,
\tE{{ prefix|upper }}_TR_ADVANCE,
\tE{{ prefix|upper }}_TR_CONTINUE
} e{{ param.type }}Check;

/* states (enum) */
typedef enum e{{ param.type }}State {
{%- for state in param.states %}
\tE{{ prefix|upper }}_ST_{{ state|upper }},
{%- endfor %}
\tE{{ prefix|upper }}_NUM_STATES
} e{{ param.type }}State;

/* finite state machine struct */
typedef struct {{ param.type }} {
\te{{ param.type }}Check check;
\te{{ param.type }}State cur;
\te{{ param.type }}State cmd;
\tvoid (***state_transitions)(struct {{ param.type }} *, {{param.fopts.type}});
\tvoid (*run)(struct {{ param.type }} *, {{param.fopts.type}});
} {{ param.type }};

/* transition ficntions */
typedef void (*p{{ param.type }}StateTransitions)\
(struct {{ param.type }} *, void *);

/* fsm declarations */
{%  for stateone in param.states -%}
{%- for statetwo in param.states -%}
void {{ prefix|lower }}_{{ stateone|lower }}_{{ statetwo|lower }} \
({{ param.type }} *fsm, {{param.fopts.type}}{{param.fopts.name}});
{%  endfor -%}
{%  endfor -%}
void {{ prefix|lower }}_run ({{ param.type }} *fsm, \
{{param.fopts.type}}{{param.fopts.name}});

/* creation macro */
#define {{ prefix|upper }}_CREATE() \\
{ \\
\t.check = E{{ prefix|upper }}_TR_CONTINUE, \\
\t.cur = E{{ prefix|upper }}_ST_{{ param.states|first|upper }}, \\
\t.cmd = E{{ prefix|upper }}_ST_{{ param.states|first|upper }}, \\
\t.state_transitions = (p{{ param.type }}StateTransitions * \
[E{{ prefix|upper }}_NUM_STATES]) { \\
{%  for stateone in param.states %}\t\t(p{{ param.type }}StateTransitions \
[E{{ prefix|upper }}_NUM_STATES]) { \\
{% for statetwo in param.states %}\t\t\t\
{{ prefix|lower }}_{{ stateone|lower }}_{{ statetwo|lower }}
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
/*
    RUNNING STATE FUNCTIONS
 */
{% for state in param.states -%}
/* continue in state {{ state }} */
void {{ prefix|lower }}_{{ state|lower }}_{{ state|lower }} \
({{ param.type }} *fsm, {{param.fopts.type}}{{param.fopts.name}}) {

    /* check if this function was called from a transition. */
    if (fsm->check == E{{ prefix|upper }}_TR_ADVANCE) {
        /* transitioned successfully from fsm->cur to fsm->cmd (here) */
    } else if (fsm->check == E{{ prefix|upper }}_TR_RETREAT) {
        /* failed to transition to fsm->cmd, fell back to fsm->cur (here) */
    } else {
        /* no prior transition (fsm->check == E{{ prefix|upper }}_TR_CONTINUE) */
    }

}
{% endfor %}

/*
    TRANSITION FUNCTIONS
    perform guard checks and transitional operations
    then set fsm->check = E{{ prefix|upper }}_TR_ADVANCE; if it's OK
 */
{%  for stateone in param.states -%}{%  for statetwo in param.states -%}
{% if (stateone != statetwo) %}
void {{ prefix|lower }}_{{ stateone|lower }}_{{ statetwo|lower }} \
({{ param.type }} *fsm, {{param.fopts.type}}{{param.fopts.name}}) {

    fsm->check = E{{ prefix|upper }}_TR_RETREAT;

    /* write code here. Optionally allow for transition to advance
       by setting fsm->check = E{{ prefix|upper }}_TR_ADVANCE; */

}
{% endif -%}
{% endfor %}
{% endfor %}

/* execute transition function */
void {{ prefix|lower }}_run ({{ param.type }} *fsm, \
{{param.fopts.type}}{{param.fopts.name}}) {

    fsm->state_transitions[fsm->cur][fsm->cmd](fsm, fopts);

    /* advance to requested state or return to current state */
    if (fsm->cmd != fsm->cur) {
        if (fsm->check == E{{ prefix|upper }}_TR_ADVANCE) {
            fsm->state_transitions[fsm->cmd][fsm->cmd](fsm, fopts);
            fsm->cur = fsm->cmd;
        } else {
            fsm->state_transitions[fsm->cur][fsm->cur](fsm, fopts);
            fsm->cmd = fsm->cur;
        }
    }
    /* continue running */
    fsm->check = E{{ prefix|upper }}_TR_CONTINUE;
}
""")


class Fsm(object):
    """UKF parameters"""
    def __init__(self, fsm_param):

        self.param = {
            'type': fsm_param['type'],
            'states': utils.copy(fsm_param['states']),
            'fopts': {
                'type': 'void *',
                'name': 'fopts'
            }
        }

        if ('fopts' in fsm_param):
            utils.ifexistscopy(['type', 'name'],
                               self.param['fopts'],
                               fsm_param['fopts'])

    def ccodesnippets(self, prefix, init=None, oneline=None):
        """Create C code initialization string snippet"""

        fsm_prefix = prefix
        fsm_param = utils.copy(self.param)

        fsm_decl = _fsm_decl_template.render(prefix=fsm_prefix,
                                             param=fsm_param)
        fsm_fcns = _fsm_fcns_template.render(prefix=fsm_prefix,
                                             param=fsm_param)

        code = {
            'include': {
                'snippets': [fsm_decl],
                'inclfiles': _fsm_decl_include_list
            },
            'fcns': {
                'snippets': [fsm_fcns],
                'inclfiles': _fsm_fcns_include_list
            }
        }

        return code

    def ccodefiles(self, folder, prefix, subfolder=None):
        """Create C code files"""

        code = self.ccodesnippets(prefix, oneline=False)

        utils.ccodefilesfromclass(folder,
                                  prefix,
                                  code,
                                  subfolder=subfolder)
