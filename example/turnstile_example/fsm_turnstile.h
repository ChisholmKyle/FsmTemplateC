#ifndef FSM_TURNSTILE_H
#define FSM_TURNSTILE_H

/* ***************
 * Include Files *
 * ***************/

#include <stdbool.h>

/* ***************************
 * Typedefs and Declarations *
 * ***************************/

/* function options (EDIT) */
typedef struct FsmTurnstileFopts {
    bool coin;
    bool push;
} FsmTurnstileFopts;

/* transition check */
typedef enum eFsmTurnstileCheck {
	EFSM_TURNSTILE_TR_RETREAT,
	EFSM_TURNSTILE_TR_ADVANCE,
	EFSM_TURNSTILE_TR_CONTINUE
} eFsmTurnstileCheck;

/* states (enum) */
typedef enum eFsmTurnstileState {
	EFSM_TURNSTILE_ST_LOCKED,
	EFSM_TURNSTILE_ST_UNLOCKED,
	EFSM_TURNSTILE_NUM_STATES
} eFsmTurnstileState;

/* finite state machine struct */
typedef struct FsmTurnstile {
	eFsmTurnstileCheck check;
	eFsmTurnstileState cur;
	eFsmTurnstileState cmd;
	void (***state_transitions)(struct FsmTurnstile *, FsmTurnstileFopts *);
	void (*run)(struct FsmTurnstile *, FsmTurnstileFopts *);
} FsmTurnstile;

/* transition functions */
typedef void (*pFsmTurnstileStateTransitions)(struct FsmTurnstile *, FsmTurnstileFopts *);

/* fsm declarations */
void fsm_turnstile_locked_locked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts);
void fsm_turnstile_locked_unlocked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts);
void fsm_turnstile_unlocked_locked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts);
void fsm_turnstile_unlocked_unlocked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts);
void fsm_turnstile_run (FsmTurnstile *fsm, FsmTurnstileFopts *fopts);

/* creation macro */
#define FSM_TURNSTILE_CREATE() \
{ \
	.check = EFSM_TURNSTILE_TR_CONTINUE, \
	.cur = EFSM_TURNSTILE_ST_LOCKED, \
	.cmd = EFSM_TURNSTILE_ST_LOCKED, \
	.state_transitions = (pFsmTurnstileStateTransitions * [EFSM_TURNSTILE_NUM_STATES]) { \
		(pFsmTurnstileStateTransitions [EFSM_TURNSTILE_NUM_STATES]) { \
			fsm_turnstile_locked_locked, \
			fsm_turnstile_locked_unlocked \
		}, \
		(pFsmTurnstileStateTransitions [EFSM_TURNSTILE_NUM_STATES]) { \
			fsm_turnstile_unlocked_locked, \
			fsm_turnstile_unlocked_unlocked \
		} \
	}, \
	.run = fsm_turnstile_run \
}


#endif
