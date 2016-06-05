#define _POSIX_C_SOURCE 200809L
#include <unistd.h>

/* run file with command
gcc -std=c99 fsm_turnstile.c turnstile.c && ./a.out
*/

#include <stdio.h>
#include "fsm_turnstile.h"

#define NUM_ITERS (16)

int main(void) {

    /* create fsm */
    FsmTurnstile fsm = FSM_TURNSTILE_CREATE();
    /* create fopts */
    FsmTurnstileFopts fopts = {
        .coin = false,
        .push = false
    };

    const size_t num_iters = NUM_ITERS;
    bool saved_input_coin[NUM_ITERS];
    bool saved_input_push[NUM_ITERS];
    eFsmTurnstileState saved_state[NUM_ITERS];

    /* simulate timed loop */
    for (size_t k = 0; k < num_iters; k++) {
        /* reset */
        fopts.push = false;
        fopts.coin = false;

        /* simulate push */
        if (k == 2) {
            fopts.push = true;
        }

        /* simulate coin */
        if (k == 3) {
            fopts.coin = true;
        }

        /* simulate push */
        if (k == 6) {
            fopts.push = true;
        }

        /* simulate push */
        if (k == 8) {
            fopts.push = true;
        }

        /* simulate coin */
        if (k == 10) {
            fopts.coin = true;
        }

        /* simulate coin */
        if (k == 12) {
            fopts.coin = true;
        }

        /* simulate push */
        if (k == 14) {
            fopts.push = true;
        }

        /* give command to state machine based on input */
        if (fopts.coin) {
            fsm.cmd = EFSM_TURNSTILE_ST_UNLOCKED;
            fopts.push = false;
        } else if (fopts.push) {
            fsm.cmd = EFSM_TURNSTILE_ST_LOCKED;
        }

        /* run state machine */
        fsm.run(&fsm, &fopts);

        /* save state for output */
        saved_input_coin[k] = fopts.coin;
        saved_input_push[k] = fopts.push;
        saved_state[k] = fsm.cur;

    }

    /* output results */
    printf("\ncoin\tpush\tstate\n");
    for (size_t k = 0; k < num_iters; k++) {
        printf("\n%d\t%d\t%d", saved_input_coin[k], saved_input_push[k], saved_state[k]);
    }
    printf("\n");

    return 0;
}

