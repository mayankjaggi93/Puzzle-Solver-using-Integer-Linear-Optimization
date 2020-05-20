## Executive Summary

The aim of this project is to solve 3-In-A-Row and ABC path puzzle for the given problem statement by creating a solver. 3-In-A-Row puzzle requires the solver to fill the grey blocks in the cells with either blue or white cells whilst there are no more than two consecutive cells along rows and columns of same color. ABC path puzzle requires the solver to fill alphabets A to Y in a grid of 5x5 as per the hints provided along rows, columns and diagonals of the grid. The position of A in the grid is provided along with the puzzle.

We came up with two Binary Integer Linear Programming Models (one for each puzzle) which are flexible enough to support any initial version of the two puzzles, i.e. a square grid of any even number of rows and columns for 3-In-A-Row puzzle and a 5x5 grid with any combination of hints for 24 alphabets and initial position for alphabet A.

The parameters are defined to be fed into the model in a separate data file. Linear constraints are defined for the two puzzles as per their rules and requirements. Model is generalized as much as possible to make it scalable.
The model (parameters, objective function and constraints) is coded as per AMPL syntax to solve the two IP formulations, giving binary matrices depicting the desired results.

In this context, a Python application was developed simplifying the user input and the model interpretability. A user manual to enlighten the client throughout the steps to be followed in order to solve each of the puzzles.
