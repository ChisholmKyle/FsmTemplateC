#define _POSIX_C_SOURCE 200809L
#include <unistd.h>

/* ***************
 * Include Files *
 * ***************/

#include "fsm_turnstile.h"

/* ***********
 * Functions *
 * ***********/

/*--------------------------*
 *  RUNNING STATE FUNCTIONS *
 *--------------------------*/

/**
 *  @brief Running function in state `locked`
 */
void fsm_turnstile_locked_locked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts) {

    /* msg */
    if (fsm->check == EFSM_TURNSTILE_TR_BADINPUT &&
        fsm->input == EFSM_TURNSTILE_IN_PUSH) {
        fopts->msg = "could not push locked turnstile";
    }

}

/**
 *  @brief Running function in state `unlocked`
 */
void fsm_turnstile_unlocked_unlocked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts) {

    /* msg */
    if (fsm->check == EFSM_TURNSTILE_TR_BADINPUT &&
        fsm->input == EFSM_TURNSTILE_IN_COIN) {
        fopts->msg = "wasted money on unlocked turnstile";
    }

}


/*----------------------*
 * TRANSITION FUNCTIONS *
 *----------------------*/

/**
 *  @brief Transition function from `locked` to `unlocked`
 */
void fsm_turnstile_locked_unlocked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts) {

    /* advance */
    fsm->check = EFSM_TURNSTILE_TR_ADVANCE;

    /* msg */
    fopts->msg = "unlocked turnstile";

}

/**
 *  @brief Transition function from `unlocked` to `locked`
 */
void fsm_turnstile_unlocked_locked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts) {

    /* advance */
    fsm->check = EFSM_TURNSTILE_TR_ADVANCE;

    /* msg */
    fopts->msg = "locked turnstile";

}


/*-------------------*
 * RUN STATE MACHINE *
 *-------------------*/

/**
 *  @brief Run state machine
 */
void fsm_turnstile_run (FsmTurnstile *fsm, FsmTurnstileFopts *fopts, const eFsmTurnstileInput input) {

    /* transition table - get command from input */
    if (input < EFSM_TURNSTILE_NUM_INPUTS) {
        fsm->input = input;
        fsm->cmd = fsm->transition_table[fsm->cur][input];
        if (fsm->cmd == fsm->cur) {
            /* not able to go to new input */
            fsm->check = EFSM_TURNSTILE_TR_BADINPUT;
        }
    }

    /* run process */
    if (fsm->state_transitions[fsm->cur][fsm->cmd] == NULL) {
        fsm->check = EFSM_TURNSTILE_TR_RETREAT;
    } else {
        fsm->state_transitions[fsm->cur][fsm->cmd](fsm, fopts);
    }

    /* advance to requested state or return to current state */
    if (fsm->cmd != fsm->cur) {
        if (fsm->check == EFSM_TURNSTILE_TR_ADVANCE) {
            fsm->state_transitions[fsm->cmd][fsm->cmd](fsm, fopts);
            fsm->cur = fsm->cmd;
        } else {
            fsm->state_transitions[fsm->cur][fsm->cur](fsm, fopts);
            fsm->cmd = fsm->cur;
        }
    }

    /* continue running */
    fsm->input = EFSM_TURNSTILE_NOINPUT;
    fsm->check = EFSM_TURNSTILE_TR_CONTINUE;
}

