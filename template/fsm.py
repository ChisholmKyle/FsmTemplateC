from template import utils
from jinja2 import Template

_fsm_decl_include_list = []
_fsm_fcns_include_list = []

_fsm_decl_template = Template("""\
/* function options (EDIT) */
typedef void * {{param.fopts.type}};

/* transition check */
typedef enum e{{ param.type }}Check {
\tE{{ prefix|upper }}_TR_RETREAT,
\tE{{ prefix|upper }}_TR_ADVANCE,
\tE{{ prefix|upper }}_TR_CONTINUE,
\tE{{ prefix|upper }}_TR_NEW
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
\te{{ param.type }}State new;
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
({{ param.type }} *fsm, {{param.fopts.type}} *{{param.fopts.name}});
{%  endfor -%}
{%  endfor -%}
void {{ prefix|lower }}_run ({{ param.type }} *fsm, \
{{param.fopts.type}} *{{param.fopts.name}});

/* creation macro */
#define {{ prefix|upper }}_CREATE() \\
{ \\
\t.check = E{{ prefix|upper }}_TR_CONTINUE, \\
\t.cur = E{{ prefix|upper }}_ST_{{ param.states|first|upper }}, \\
\t.cmd = E{{ prefix|upper }}_ST_{{ param.states|first|upper }}, \\
\t.new = E{{ prefix|upper }}_ST_{{ param.states|first|upper }}, \\
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
/*--------------------------*
 *  RUNNING STATE FUNCTIONS *
 *--------------------------*/

{% for state in param.states -%}
/* continue in state {{ state }} */
void {{ prefix|lower }}_{{ state|lower }}_{{ state|lower }} \
({{ param.type }} *fsm, {{param.fopts.type}} *{{param.fopts.name}}) {

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
{% if (stateone != statetwo) %}
/**
 *  @brief Transition function from `{{ stateone|lower }}` to `{{ statetwo|lower }}`
 *
 *  @details
 *
 *  To advance to '{{ statetwo|lower }}' state, set
 *  `fsm->check = E{{ prefix|upper }}_TR_ADVANCE;`
 *  To return to '{{ stateone|lower }}' state, set
 *  `fsm->check = E{{ prefix|upper }}_TR_RETREAT;`
 *  To continue in this transition at next step, set
 *  `fsm->check = E{{ prefix|upper }}_TR_CONTINUE;`
 */
void {{ prefix|lower }}_{{ stateone|lower }}_{{ statetwo|lower }} \
({{ param.type }} *fsm, {{param.fopts.type}} *{{param.fopts.name}}) {

    /* by default, do not transition (guard/retreat) */
    (void)({{param.fopts.name}});
    fsm->check = E{{ prefix|upper }}_TR_RETREAT;

    /* check if this transition was just entered from a running state. */
    if (fsm->check == E{{ prefix|upper }}_TR_NEW) {
        /* first call of this transition function from '{{ stateone|lower }}' state */
    } else {
        /* continued with this transition from last step */
    }
    /* NOTE: Before returning from this funciton,
       Consider setting transition to
       advance: fsm->check = E{{ prefix|upper }}_TR_ADVANCE;
       or
       continue: fsm->check = E{{ prefix|upper }}_TR_CONTINUE; */

}
{% endif -%}
{% endfor %}
{% endfor %}

/*-----------------------------*
 * EXECUTE TRANSITION FUNCTION *
 *-----------------------------*/

void {{ prefix|lower }}_run ({{ param.type }} *fsm, \
{{param.fopts.type}} *{{param.fopts.name}}) {

    /* if a new state is requested */
    if (fsm->new != fsm->cmd
        && fsm->cmd == fsm->cur) {
        /* can only call when not in transition
           ie. The transition process must relinquish control by setting
           E{{ prefix|upper }}_TR_RETREAT or
           E{{ prefix|upper }}_TR_ADVANCE
           before a fsm->new is set
        */
        fsm->cmd = fsm->new;
        fsm->check = E{{ prefix|upper }}_TR_NEW;
    }

    /* run process */
    fsm->state_transitions[fsm->cur][fsm->cmd](fsm, {{param.fopts.name}});

    /* advance to requested state or return to current state */
    if (fsm->cmd != fsm->cur) {
        if (fsm->check == E{{ prefix|upper }}_TR_ADVANCE) {
            fsm->state_transitions[fsm->cmd][fsm->cmd](fsm, {{param.fopts.name}});
            fsm->cur = fsm->cmd;
        } else if (fsm->check == E{{ prefix|upper }}_TR_RETREAT) {
            fsm->state_transitions[fsm->cur][fsm->cur](fsm, {{param.fopts.name}});
            fsm->cmd = fsm->cur;
            fsm->new = fsm->cmd;
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
