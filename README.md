# FsmTemplateC #

Simple template for C Finite State Machine

## About this module ##

This small python3 module generates skeleton C code for a finite state machine (FSM). Given a list of states, list of inputs, and a state transition table, the code generated makes it easy to edit and create transition guards and handle inputs. The FSM makes use of look-up tables and does not require searches, exhaustive if-statements, or switch statements. A C99 compiler is required.

## Prerequisites ##

Python3 with the [Jinja2](http://jinja.pocoo.org) module is required. A C99 supported compiler is required to compile the generated C code (gcc or clang, for example). A POSIX macro is defined at the beginning of the generated source file but is not required and can be safely removed.

## Try it out ##

First clone the repository

    git clone https://github.com/ChisholmKyle/FsmTemplateC && FsmTemplateC

To run the example [fsm_example.py](example/fsm_example.py), on the command line type

    cd example
    python3 fsm_example.py

and have a look at the output source and header files generated in the
subdirectory fsm_example.

You can also run a basic [turnstile state machine](https://en.wikipedia.org/wiki/Finite-state_machine#Example:_coin-operated_turnstile). The initial skeleton code is generated from the script [turnstile_example.py](example/turnstile_example.py). The skeleton code was modified to add the appropriate functionality and a complete C code example can be complied from the [example/turnstile_complete](example/turnstile_complete) folder. Assuming `gcc` is installed, compile and run the C code from a terminal as follows:
    
    cd example/turnstile_complete
    gcc -std=c99 fsm_turnstile.c turnstile.c && ./a.out

The standard terminal output should look like

    INPUT   STATE   MESSAGE

    -   0
    push    0   could not push locked turnstile
    -   0
    coin    1   unlocked turnstile
    -   1
    -   1
    push    0   locked turnstile
    -   0
    push    0   could not push locked turnstile
    coin    1   unlocked turnstile
    coin    1   wasted money on unlocked turnstile
    -   1
    push    0   locked turnstile

## Further Documentation ##

Refer to [fsm_example.py](example/fsm_example.py) for the following description. First,


Anyways, here is an example with four states called "one", "two", "three", and "four". Here are the typedefs for the header:

    /* transition check */
    typedef enum eFsmExampleCheck {
        EFSM_EXAMPLE_TR_RETREAT,
        EFSM_EXAMPLE_TR_ADVANCE,
        EFSM_EXAMPLE_TR_CONTINUE
    } eFsmExampleCheck;

    /* states (enum) */
    typedef enum eFsmExampleState {
        EFSM_EXAMPLE_ST_ONE,
        EFSM_EXAMPLE_ST_TWO,
        EFSM_EXAMPLE_ST_THREE,
        EFSM_EXAMPLE_ST_FOUR,
        EFSM_EXAMPLE_NUM_STATES
    } eFsmExampleState;

    /* finite state machine struct */
    typedef struct FsmExample {
        eFsmExampleCheck check;
        eFsmExampleState cur;
        eFsmExampleState cmd;
        void (***state_transitions)(struct FsmExample *, void *);
        void (*run)(struct FsmExample *, void *);
    } FsmExample;

    /* transition functions */
    typedef void (*pFsmExampleStateTransitions)(FsmExample *, void *);

- enum `eFsmExampleCheck` is used to determine whether a transition was blocked with `EFSM_EXAMPLE_TR_RETREAT`, allowed to progress with `EFSM_EXAMPLE_TR_ADVANCE`, or the function call was not preceded by a transition with `EFSM_EXAMPLE_TR_CONTINUE`. It's usage becomes clear in the example source code below.
- enum `eFsmExampleState` is simply the list of states.
- The `FsmExample` struct is the heart of the state machine with the transition check, function lookup table, current state, commanded state, and an alias to the primary function that runs the machine.
- Every function pointer (alias) in `FsmExample` should only be called from the struct and has to have its first input as a pointer to itself so as to maintain a persistent state, object-oriented style.

Now for ALL the function declarations in the header:

    /* fsm declarations */
    void fsm_example_one_one (FsmExample *fsm, void *fopts);
    void fsm_example_one_two (FsmExample *fsm, void *fopts);
    void fsm_example_one_three (FsmExample *fsm, void *fopts);
    void fsm_example_one_four (FsmExample *fsm, void *fopts);
    void fsm_example_two_one (FsmExample *fsm, void *fopts);
    void fsm_example_two_two (FsmExample *fsm, void *fopts);
    void fsm_example_two_three (FsmExample *fsm, void *fopts);
    void fsm_example_two_four (FsmExample *fsm, void *fopts);
    void fsm_example_three_one (FsmExample *fsm, void *fopts);
    void fsm_example_three_two (FsmExample *fsm, void *fopts);
    void fsm_example_three_three (FsmExample *fsm, void *fopts);
    void fsm_example_three_four (FsmExample *fsm, void *fopts);
    void fsm_example_four_one (FsmExample *fsm, void *fopts);
    void fsm_example_four_two (FsmExample *fsm, void *fopts);
    void fsm_example_four_three (FsmExample *fsm, void *fopts);
    void fsm_example_four_four (FsmExample *fsm, void *fopts);

    void fsm_example_run (FsmExample *fsm, void *fopts);

Function names are in the format `{prefix}_{from}_{to}`, where `{from}` is the previous (current) state and `{to}` is the next state. The function `{prefix}_run` is to be aliased to `FsmExample.run`. Finally, the magic happens with a macro. Here we build the transition table, which is really a matrix of function pointers:

    /* creation macro */
    #define FSM_EXAMPLE_CREATE() \
    { \
        .check = EFSM_EXAMPLE_TR_CONTINUE, \
        .cur = EFSM_EXAMPLE_ST_ONE, \
        .cmd = EFSM_EXAMPLE_ST_ONE, \
        .state_transitions = (pFsmExampleStateTransitions * [EFSM_EXAMPLE_NUM_STATES]) { \
            (pFsmExampleStateTransitions [EFSM_EXAMPLE_NUM_STATES]) { \
                fsm_example_one_one, \
                fsm_example_one_two, \
                fsm_example_one_three, \
                fsm_example_one_four \
            }, \
            (pFsmExampleStateTransitions [EFSM_EXAMPLE_NUM_STATES]) { \
                fsm_example_two_one, \
                fsm_example_two_two, \
                fsm_example_two_three, \
                fsm_example_two_four \
            }, \
            (pFsmExampleStateTransitions [EFSM_EXAMPLE_NUM_STATES]) { \
                fsm_example_three_one, \
                fsm_example_three_two, \
                fsm_example_three_three, \
                fsm_example_three_four \
            }, \
            (pFsmExampleStateTransitions [EFSM_EXAMPLE_NUM_STATES]) { \
                fsm_example_four_one, \
                fsm_example_four_two, \
                fsm_example_four_three, \
                fsm_example_four_four \
            } \
        }, \
        .run = fsm_example_run \
    }

When creating the FSM, the macro `FSM_EXAMPLE_CREATE()` has to be used and is demonstrated below.

Now, in the source code every state transition function declared above should be populated. The `fopts` pointer can be cast to any data type (usually a struct or array). Every transition must set `fsm->check` to be equal to either `EFSM_EXAMPLE_TR_RETREAT` to block it from transitioning or `EFSM_EXAMPLE_TR_ADVANCE` to allow it to transition to the commanded state. Here is an example transition function from state "three" to "two":

    void fsm_example_three_two (FsmExample *fsm, void *fopts) {
        /* cast fopts to whatever you passed to fsm->run() */
        fsm->check = EFSM_EXAMPLE_TR_RETREAT;
        /* write code here. Optionally allow for transition to advance
           by setting fsm->check = EFSM_EXAMPLE_TR_ADVANCE; */
    }

Here is the function for running in state "four" (not a transition):

    /* continue in state four */
    void fsm_example_four_four (FsmExample *fsm, void *fopts) {
        /* check if this function was called from a transition. */
        if (fsm->check == EFSM_EXAMPLE_TR_ADVANCE) {
            /* transitioned successfully from fsm->cur to fsm->cmd (here) */
        } else if (fsm->check == EFSM_EXAMPLE_TR_RETREAT) {
            /* failed to transition to fsm->cmd, fell back to fsm->cur (here) */
        } else {
            /* no prior transition (fsm->check == EFSM_EXAMPLE_TR_CONTINUE) */
        }
    }

Here is the primary `FsmExample.run` function:

    /* execute transition function */
    void fsm_example_run (FsmExample *fsm, void *fopts) {
        fsm->state_transitions[fsm->cur][fsm->cmd](fsm, fopts);
        /* advance to requested state or return to current state */
        if (fsm->cmd != fsm->cur) {
            if (fsm->check == EFSM_EXAMPLE_TR_ADVANCE) {
                fsm->state_transitions[fsm->cmd][fsm->cmd](fsm, fopts);
                fsm->cur = fsm->cmd;
            } else {
                fsm->state_transitions[fsm->cur][fsm->cur](fsm, fopts);
                fsm->cmd = fsm->cur;
            }
        }
        /* continue running */
        fsm->check = EFSM_EXAMPLE_TR_CONTINUE;
    }

Finally here is the very simple actual usage in your code:

    /* create FSM */
    FsmExample my_fsm = FSM_EXAMPLE_CREATE();
    /* infinite loop */
    for (;;) {
        /* wait for timer signal, inputs, interrupts, whatever */
        /* optionally set the command state to whatever you want
            for example: my_fsm.cmd = EFSM_EXAMPLE_ST_FOUR;
         */
        /* run state machine */
        my_fsm.run(&my_fsm, NULL);
    }

All that header business and all those functions just to have a simple and fast interface is worth it in my mind. It's especially great if you have a script to auto-generate all those typedefs and functions. Oh hey, you can use my python [script][1] if you like (requires jinja2 and Python).


  [1]: https://github.com/ChisholmKyle/FsmTemplateC
