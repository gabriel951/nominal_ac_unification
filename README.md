# Nominal AC-Unification 
This folder contains preliminar work that has been done to investigate nominal AC-unification. Currently, the efforts 
were focused in clearly presenting the loop and the solutions for the problem $f(X, W) =? f(\pi X, \pi Y)$ and 
in investigating $f(2X_1, X_2, X_3) =? f(2 \pi X_2, Y_1)$. The main files in this directory are `loop.py` and `diophantine.py`.

## The Loop in $f(X, W) =? f(\pi X, \pi Y)$
A Python script to output all the solutions of $f(X, W) =? f(\pi X, \pi Y)$ is available in file
`loop.py`. 

## The Problem $f(2X_1, X_2, X_3) =? f(2 \pi X_2, Y_1)$
To tackle the problem $f(2X_1, X_2, X_3) =? f(2 \pi X_2, Y_1)$ we devised a Python script that solves a Diophantine equation, 
generating a basis of solution. The script is available in file
`diophantine.py`. In contrast to [our formalisations in
PVS](https://github.com/nasa/pvslib/tree/master/nominal), it generates a basis
of solution and not a spanning set, i.e. we also have minimality. With this
script we can manually calculate some specific branches that will be generated when trying to solve this nominal AC-unification 
equational constraint. 

As future work, we could improved the script if, in addition to solving the Diophantine equation it also computed the substitution (in terms of the original variables $X_1$, $X_2$, $X_3$, $Y_1$) and listed the new set of equational constraints that must be solved.
