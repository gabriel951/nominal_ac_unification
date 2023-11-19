# In this file we generate all solutions to the problem 
# P = \{f(X, W) \approx^? f(\pi X, \pi Y) \}, where the order of \pi is k  

from substitution import *

# Permutation and Permutation Name
PERM = [("a", "b")]

PI = "\\pi"
SIGMA = "\\sigma"

# list with the number of the branches that loop
LOOP_BRANCH_LST = [3, 7]

# generates the appropriate substitution for a given branch at a certain iteration i
def subs_branch(branch, i): 
    # the name of the substitution
    name = SIGMA + "_{B" + str(branch) + "}"

    # the variable names we are instantiating
    xi = "X_" + str(i)
    yi = "Y_" + str(i)
    wi = "W_" + str(i)

    # these terms will be used (possibly more than once) in the instantiation
    pi_Yi = Susp_var(PERM, "Y_" + str(i), PI) # pi Y_i
    pi2_Yi = Susp_var(PERM + PERM, "Y_" + str(i), PI + "^{2}") # pi^2 Y_i
    Y_i1 = Susp_var([], "Y_" + str(i+1), ID_PERM) # Y_{i+1}
    pi_n1_Y_i1 = Susp_var(inverse_perm(PERM), "Y_" + str(i+1), PI + "^{-1}") # pi^{-1} Y_{i+1}

    W_i1 = Susp_var([], "W_" + str(i+1), ID_PERM) #W_{i+1}

    Z_i1 = Susp_var([], "Z_" + str(i+1), ID_PERM) #Z_{i+1}
    pi_n1_Z_i1 = Susp_var(inverse_perm(PERM), "Z_" + str(i+1), PI + "^{-1}") # pi^{-1} Z_{i+1}

    pi_Xi =  Susp_var(PERM, "X_" + str(i), PI) # pi X_i
    pi_n1_Xi = Susp_var(inverse_perm(PERM), "X_" + str(i), PI + "^{-1}")# pi^{-1} X_i
    X_i1 = Susp_var([], "X_" + str(i+1), ID_PERM)# X_{i+1}
    
    if branch == 1: 
        sub_lst = [(wi, pi_Yi)]
        return Subs(name, sub_lst)

    elif branch == 2: 
        x_pair = (xi, pi_Yi)
        w_pair = (wi, pi2_Yi)
        sub_lst = [x_pair, w_pair]
        return Subs(name, sub_lst)

    elif branch == 3: 
        x_pair = (xi, ACApp("f", [Y_i1, X_i1])) 
        w_pair = (wi, W_i1)
        y_pair = (yi, pi_n1_Y_i1)
        sub_lst = [x_pair, w_pair, y_pair]
        return Subs(name, sub_lst)

    elif branch == 6: 
        w_pair = (wi, ACApp("f", [Z_i1, pi_Xi]))
        y_pair = (yi, ACApp("f", [pi_n1_Z_i1, pi_n1_Xi]))
        sub_lst = [w_pair, y_pair]
        return Subs(name, sub_lst)

    elif branch == 7: 
        x_pair = (xi, ACApp("f", [Y_i1, X_i1])) 
        w_pair = (wi, ACApp("f", [W_i1, Z_i1]))
        y_pair = (yi, ACApp("f", [pi_n1_Z_i1, pi_n1_Y_i1]))
        sub_lst = [x_pair, w_pair, y_pair]
        return Subs(name, sub_lst)

    else: 
        quit("subs_branch called with wrong argument branch")

# generates the appropriate fixpoint equation for a given branch at a certain
# iteration i 
def fp_branch(branch, i): 
    if branch == 1: 
        # TO DO: put PI here
        return [("\\pi X_{" + str(i) + "}  \\approx^? X_{" + str(i) + "}")]
    else: 
        return []

def test_subs_branch(): 
    print("Starting test for iteration i = " + str(0))
    for branch in [1, 2, 3, 6, 7]: 
        print("branch " + str(branch) + " - ", end='')
        print(subs_branch(branch, 0))

    print("Starting test for iteration i = " + str(10))
    for branch in [1, 2, 3, 6, 7]: 
        print("branch " + str(branch) + " - ", end='')
        print(subs_branch(branch, 10))

# print a triple of solution
def print_triple(Delta, sigma, fp_eq): 
    print("(", end='')
    print(Delta, end='')
    print(", ", end='')
    print(sigma.name, end='')
    print(", ", end= '')
    print(fp_eq, end='')
    print(")")
    print("where ", end='')
    print_subs(sigma, ["X_0", "Y_0", "W_0"])
    print("\n")

# print a triple of solution in latex format
# if you want the LaTeX code to print it 
def print_triple_latex(Delta, sigma, fp_eq, verbose=False): 
    # change the name of sigma 
    print("$(", end = '')
    print("\\emptyset, ", end = '')

    print(sigma.name, end='')
    print(", ", end= '')

    if len(fp_eq) == 0: 
        print("\\emptyset ", end='')
    else: 
        # since, there is only one equation, print it
        print(fp_eq[0], end='')

    print(")$")
   
    if verbose: 
        print("where ", end='')
        print_subs(sigma, ["X_0", "Y_0", "W_0"], " \mapsto ", True)

    print("\n")


# given a path, construct and print solution.
def construct_sol(path, verbose=False): 
    # context 
    context = []

    # substitution
    subs = Subs("", []) # id sub
    for i in range(len(path)): 
        cur_sub = subs_branch(path[i], i)
        subs = compose(cur_sub, subs)

    # fixpoint equation 
    fp_eq = fp_branch(path[-1], len(path)-1)

    # print the triple
    if verbose == False: 
        print("The solution of path ", end='')
        print(path, end='')
        print(" is: ")
        print_triple_latex(context, subs, fp_eq, False)

    if verbose == True: 
        print("The solution of path ", end='')
        print(path, end='')
        print(" is: ")
        print_triple_latex(context, subs, fp_eq, True)

# generates all solutions the algorithm should output
# receives as parameter the order k of the permutation \pi 
def gen_all_solutions(k): 

    # find all paths of solutions
    # branches 4 and 5 do not generate solutions
    paths = [[1], [2], [3], [6], [7]]
    for i in range(2, 2*k+1):
        # generates all paths of length i, from the paths of length i-1
        # that finished in one of the indices that cause a loop
        for path in paths:  
            if len(path) == i-1 and path[-1] in LOOP_BRANCH_LST: 
                for new_branch in [1, 2, 3, 6, 7]: 
                    paths.append(path + [new_branch])

    # we must filter the paths that ended in an index that caused a loop 
    valid_paths = []
    for path in paths: 
        if not path[-1] in LOOP_BRANCH_LST:
            valid_paths.append(path)
    
    # construct a solution for the correspondent path. First in nonverbose and then in verbose 
    for path in valid_paths: 
        construct_sol(path, verbose=False) 

    for path in valid_paths: 
        construct_sol(path, verbose=True) 

#### 
def main(): 
    # generate all solutions when the order of the permutation is 2
    gen_all_solutions(2)

    ## Below some tests that were made
    # tests the substitutions in each branch 
    # test_subs_branch()
    # this let us check our calculations in the example
    # construct_sol([7], verbose=True)
    # construct_sol([3, 3], verbose=True)
    # construct_sol([1], verbose=True)
    # construct_sol([7, 7, 1], verbose=True)
    # construct_sol([7, 7, 3])


main()
