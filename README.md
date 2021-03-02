# ERCompletionReasoningLSTM
This system was developed for a [paper](https://github.com/aaronEberhart/me/raw/master/papers/AAAI-MAKE2020CompletionReasoningEmulationfortheDescriptionLogicEL%2B.pdf) that was accepted at the AAAI-MAKE 2020 conference.

## predicateTest.py

This file is simply a series of checks to confirm that the proper exceptions are raised for malformed predicate usage.

## reasonerTest.py

This is a simple Python ER syntax generator and reasoner with room for potential expansion in the future. Has complex logging built in for analysis, so it's not very fast, but it can describe its behavior quite well. There is a plain random generator, as well as a sequential random generator that creates semi-predictable structured patterns with randomness alongside.

## datasetGenerators.py

This file contains code to generate data for use in the LSTM. If desired, the code from this file can be imported so that it can output directly to functions in main.py, though this is generally time consuming and using the saved .npz files is much faster.

## main.py

This file builds a prediction model of the reasoner with an LSTM. It can be run from a python IDE or in the terminal. Output will be saved to a folder in the same directory as main.py, depending on which options are chosen.

This is the manual for the command line options:

usage: main.py [-h] [-e EPOCHS] [-l LEARNINGRATE] [-s] [-m] [-c CROSS]
[-p PERTURB]

optional arguments:

|Argument  |Meaning                        |
|:--------:|:-----------------------------:|
|-h, --help|show this help message and exit|
|-e, --epochs|number of epochs for each system|
|-l LEARNINGRATE, --learningRate LEARNINGRATE|learning rate of each system, number between 0.0 and 1.0|
|-s, --snomed|use SNOMED dataset|
|-m, --mix|use test set from different souce than train|
|-c CROSS, --cross CROSS|cross validation folds, default 10|
|-p PERTURB, --perturb PERTURB|perturb each kb by proportion between 0 and 1 and compare|


