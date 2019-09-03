
#include <malloc.h>

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

/*----------------------*
 * CREATE STATE MACHINE *
 *----------------------*/

/**
 *  @brief Create state machine
 */
FsmTurnstile * fsm_turnstile_create (void) {

    FsmTurnstile *fsm = (FsmTurnstile *) malloc(sizeof(FsmTurnstile));
    if (fsm == NULL) {
        return NULL;
    }

    fsm->input = EFSM_TURNSTILE_NOINPUT;
    fsm->check = EFSM_TURNSTILE_TR_CONTINUE;
    fsm->cur = EFSM_TURNSTILE_ST_LOCKED;
    fsm->cmd = EFSM_TURNSTILE_ST_LOCKED;
    fsm->run = fsm_turnstile_run;

    // set future pointer allocations to NULL
    fsm->transition_table = NULL;
    fsm->state_transitions = NULL;

    /* transition table */

    fsm->transition_table = (eFsmTurnstileState **) malloc(EFSM_TURNSTILE_NUM_STATES * sizeof(eFsmTurnstileState *));
    if (fsm->transition_table == NULL) {
        fsm_turnstile_free(fsm);
        return NULL;
    }
    // set future pointer allocations to NULL
    for (int k = 0; k < EFSM_TURNSTILE_NUM_STATES; k++) {
        fsm->transition_table[k] = NULL;
    }

    fsm->transition_table[0] = (eFsmTurnstileState *) malloc(EFSM_TURNSTILE_NUM_INPUTS * sizeof(eFsmTurnstileState));
    if (fsm->transition_table[0] == NULL) {
        fsm_turnstile_free(fsm);
        return NULL;
    }
    
    fsm->transition_table[0][0] = EFSM_TURNSTILE_ST_UNLOCKED;
    fsm->transition_table[0][1] = EFSM_TURNSTILE_ST_LOCKED;

    fsm->transition_table[1] = (eFsmTurnstileState *) malloc(EFSM_TURNSTILE_NUM_INPUTS * sizeof(eFsmTurnstileState));
    if (fsm->transition_table[1] == NULL) {
        fsm_turnstile_free(fsm);
        return NULL;
    }
    
    fsm->transition_table[1][0] = EFSM_TURNSTILE_ST_UNLOCKED;
    fsm->transition_table[1][1] = EFSM_TURNSTILE_ST_LOCKED;

    /* state transitions */

    fsm->state_transitions = (pFsmTurnstileStateTransitions **) malloc(EFSM_TURNSTILE_NUM_STATES * sizeof(pFsmTurnstileStateTransitions *));
    if (fsm->state_transitions == NULL) {
        fsm_turnstile_free(fsm);
        return NULL;
    }
    // set future pointer allocations to NULL
    for (int k = 0; k < EFSM_TURNSTILE_NUM_STATES; k++) {
        fsm->state_transitions[k] = NULL;
    }

    fsm->state_transitions[0] = (pFsmTurnstileStateTransitions *) malloc(EFSM_TURNSTILE_NUM_STATES * sizeof(pFsmTurnstileStateTransitions));
    if (fsm->state_transitions[0] == NULL) {
        fsm_turnstile_free(fsm);
        return NULL;
    }
    
    fsm->state_transitions[0][0] = fsm_turnstile_locked_locked;
    fsm->state_transitions[0][1] = fsm_turnstile_locked_unlocked;

    fsm->state_transitions[1] = (pFsmTurnstileStateTransitions *) malloc(EFSM_TURNSTILE_NUM_STATES * sizeof(pFsmTurnstileStateTransitions));
    if (fsm->state_transitions[1] == NULL) {
        fsm_turnstile_free(fsm);
        return NULL;
    }
    
    fsm->state_transitions[1][0] = fsm_turnstile_unlocked_locked;
    fsm->state_transitions[1][1] = fsm_turnstile_unlocked_unlocked;

    return fsm;

}


/**
 *  @brief Free state machine
 */
void fsm_turnstile_free (FsmTurnstile *fsm) {
    if (fsm != NULL) {
        if (fsm->transition_table != NULL) {
            for (int k = 0; k < EFSM_TURNSTILE_NUM_STATES; ++k)
            {
                if (fsm->transition_table[k] != NULL) {
                    free(fsm->transition_table[k]);
                    fsm->transition_table[k] = NULL;
                }
            }
            free(fsm->transition_table);
            fsm->transition_table = NULL;
        }
        if (fsm->state_transitions != NULL) {
            for (int k = 0; k < EFSM_TURNSTILE_NUM_STATES; ++k)
            {
                if (fsm->state_transitions[k] != NULL) {
                    free(fsm->state_transitions[k]);
                    fsm->state_transitions[k] = NULL;
                }
            }
            free(fsm->state_transitions);
            fsm->state_transitions = NULL;
        }
    }
    free(fsm);
}

