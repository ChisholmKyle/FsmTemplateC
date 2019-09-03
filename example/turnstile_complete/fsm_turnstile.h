#ifndef FSM_TURNSTILE_H
#define FSM_TURNSTILE_H

/* ***************************
 * Typedefs and Declarations *
 * ***************************/

/* function options (EDIT) */
typedef struct FsmTurnstileFopts {
    /* define your options struct here */
    const char *msg;
} FsmTurnstileFopts;

/* transition check */
typedef enum eFsmTurnstileCheck {
	EFSM_TURNSTILE_TR_RETREAT,
	EFSM_TURNSTILE_TR_ADVANCE,
	EFSM_TURNSTILE_TR_CONTINUE,
	EFSM_TURNSTILE_TR_BADINPUT
} eFsmTurnstileCheck;

/* states (enum) */
typedef enum eFsmTurnstileState {
	EFSM_TURNSTILE_ST_LOCKED,
	EFSM_TURNSTILE_ST_UNLOCKED,
	EFSM_TURNSTILE_NUM_STATES
} eFsmTurnstileState;

/* inputs (enum) */
typedef enum eFsmTurnstileInput {
	EFSM_TURNSTILE_IN_COIN,
	EFSM_TURNSTILE_IN_PUSH,
	EFSM_TURNSTILE_NUM_INPUTS,
	EFSM_TURNSTILE_NOINPUT
} eFsmTurnstileInput;

/* finite state machine struct */
typedef struct FsmTurnstile {
	eFsmTurnstileInput input;
	eFsmTurnstileCheck check;
	eFsmTurnstileState cur;
	eFsmTurnstileState cmd;
	eFsmTurnstileState **transition_table;
	void (***state_transitions)(struct FsmTurnstile *, FsmTurnstileFopts *);
	void (*run)(struct FsmTurnstile *, FsmTurnstileFopts *, const eFsmTurnstileInput);
} FsmTurnstile;

/* transition functions */
typedef void (*pFsmTurnstileStateTransitions)(struct FsmTurnstile *, FsmTurnstileFopts *);

/* fsm declarations */
void fsm_turnstile_locked_locked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts);
void fsm_turnstile_locked_unlocked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts);
void fsm_turnstile_unlocked_locked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts);
void fsm_turnstile_unlocked_unlocked (FsmTurnstile *fsm, FsmTurnstileFopts *fopts);
void fsm_turnstile_run (FsmTurnstile *fsm, FsmTurnstileFopts *fopts, const eFsmTurnstileInput input);

/* create */
FsmTurnstile *fsm_turnstile_create(void);

/* free */
void fsm_turnstile_free (FsmTurnstile *fsm);



#endif
