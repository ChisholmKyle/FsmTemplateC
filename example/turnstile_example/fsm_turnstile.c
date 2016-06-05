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

    /* do nothing */
    (void)fopts;

}

/**
 *  @brief Running function in state `unlocked`
 */
void fsm_turnstile_unlocked_unlocked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts) {

    /* do nothing */
    (void)fopts;

}

/*----------------------*
 * TRANSITION FUNCTIONS *
 *----------------------*/

/**
 *  @brief Transition function from `locked` to `unlocked`
 */
void fsm_turnstile_locked_unlocked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts) {

    /* by default, do not transition (guard/retreat) */
    fsm->check = EFSM_TURNSTILE_TR_RETREAT;

    /* advance if coin is inserted */
    if (fopts->coin) {
        fsm->check = EFSM_TURNSTILE_TR_ADVANCE;
    }

}

/**
 *  @brief Transition function from `unlocked` to `locked`
 */
void fsm_turnstile_unlocked_locked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts) {

    /* by default, do not transition (guard/retreat) */
    fsm->check = EFSM_TURNSTILE_TR_RETREAT;

    /* advance if turnsile is pushed */
    if (fopts->push) {
        fsm->check = EFSM_TURNSTILE_TR_ADVANCE;
    }

}


/*-------------------*
 * RUN STATE MACHINE *
 *-------------------*/

/**
 *  @brief Run state machine
 */
void fsm_turnstile_run (FsmTurnstile *fsm, FsmTurnstileFopts *fopts) {

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
    fsm->check = EFSM_TURNSTILE_TR_CONTINUE;
}

