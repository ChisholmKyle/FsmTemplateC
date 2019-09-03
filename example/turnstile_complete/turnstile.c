#define _POSIX_C_SOURCE 200809L
#include <unistd.h>

/* run file with command
gcc -std=c99 fsm_turnstile.c turnstile.c && ./a.out
*/

#include <stdio.h>
#include "fsm_turnstile.h"

#define NUM_ITERS (13)

#define PRINT_INPUT(x) ((x) == EFSM_TURNSTILE_IN_PUSH ? "push" : ((x) == EFSM_TURNSTILE_IN_COIN ? "coin" : "-"))

int main(void) {

    /* set up example iterations - simulate timed loop */
    const size_t num_iters = NUM_ITERS;
    eFsmTurnstileInput saved_input[NUM_ITERS];
    eFsmTurnstileState saved_state[NUM_ITERS];
    const char *saved_msg[NUM_ITERS];

    /* create fsm */
    FsmTurnstile *fsm = fsm_turnstile_create();
    if (fsm == NULL) return 1;

    /* create fopts */
    FsmTurnstileFopts fopts;

    /* initialize input */
    eFsmTurnstileInput input = EFSM_TURNSTILE_NOINPUT;

    /* simulate timed loop */
    for (size_t k = 0; k < num_iters; k++) {
        /* reset */
        fopts.msg = "";
        input = EFSM_TURNSTILE_NOINPUT;

        /* simulate push */
        if (k == 1) {
            input = EFSM_TURNSTILE_IN_PUSH;
        }

        /* simulate coin */
        if (k == 3) {
            input = EFSM_TURNSTILE_IN_COIN;
        }

        /* simulate push */
        if (k == 6) {
            input = EFSM_TURNSTILE_IN_PUSH;
        }

        /* simulate push */
        if (k == 8) {
            input = EFSM_TURNSTILE_IN_PUSH;
        }

        /* simulate coin */
        if (k == 9) {
            input = EFSM_TURNSTILE_IN_COIN;
        }

        /* simulate coin */
        if (k == 10) {
            input = EFSM_TURNSTILE_IN_COIN;
        }

        /* simulate push */
        if (k == 12) {
            input = EFSM_TURNSTILE_IN_PUSH;
        }

        /* run state machine */
        fsm_turnstile_run (fsm, &fopts, input);

        /* save state for output */
        saved_input[k] = input;
        saved_state[k] = fsm->cur;
        saved_msg[k] = fopts.msg;
    }

    /* output results */
    printf("\nINPUT\tSTATE\tMESSAGE\n");
    for (size_t k = 0; k < num_iters; k++) {
        printf("\n%s\t%d\t%s", PRINT_INPUT(saved_input[k]), saved_state[k], saved_msg[k]);
    }
    printf("\n");

    fsm_turnstile_free(fsm);
    fsm = NULL;

    return 0;
}

