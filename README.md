# FsmTemplateC #

Simple template for C Finite State Machine

## About this module ##

This small Python3 module generates skeleton C code for a finite state machine (FSM). Given a list of states, list of inputs, and a state transition table, the code generated makes it easy to edit and create transition guards and handle inputs. The FSM makes use of look-up tables and does not require searches, exhaustive if-statements, or switch statements.

## Prerequisites ##

Python3 with the [Jinja2](http://jinja.pocoo.org) module is required. A C compiler is required to compile the generated C code (gcc or clang, for example).

## Try it out ##

First clone the repository

    git clone https://github.com/ChisholmKyle/FsmTemplateC && cd FsmTemplateC

To run the example [fsm_example.py](example/fsm_example.py), on the command line type

    cd example
    python3 fsm_example.py

and have a look at the output source and header files generated in the newly-created
subdirectory fsm_example. Note that the `python3` command calls python 3.x and may be different on your machine.

You can also run a basic [turnstile state machine](https://en.wikipedia.org/wiki/Finite-state_machine#Example:_coin-operated_turnstile). The initial skeleton code is generated from the script [turnstile_example.py](example/turnstile_example.py). The skeleton code was modified to add the appropriate functionality and a complete C code example can be complied from the [example/turnstile_complete](example/turnstile_complete) folder. Assuming `make` and `gcc` are installed, compile and run the C code from a terminal as follows:

    cd turnstile_complete
    make && ./turnstile

The standard terminal output should look like

    INPUT   STATE   MESSAGE

    -       0
    push    0       could not push locked turnstile
    -       0
    coin    1       unlocked turnstile
    -       1
    -       1
    push    0       locked turnstile
    -       0
    push    0       could not push locked turnstile
    coin    1       unlocked turnstile
    coin    1       wasted money on unlocked turnstile
    -       1
    push    0       locked turnstile

## Current Status ##

This is a minimal and custom implementation which is not intended to replace a more formalized and feature-rich library such as [SCM](http://smc.sourceforge.net) and there's no formal documentation. Only this README, examples, and the generated code have comments that may help you get started. Please feel free to add any features, examples, documentation or fix some bugs!
