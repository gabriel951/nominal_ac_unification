# In this file we try to solve Diophantine equation and print the Table of solutions
# 
# An alternative approach to the one took here is to implement an algorithm 
# as described in the paper "Efficient Solution of Linear Diophantine Equations"
# 
# There is a module in Python to solve diophantine equations, maybe it's worth
# checking it. 
 
import math

var_index = 1 

# definition of least common multiple
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

# represents a diophantine equation
class Dio_eq: 
    # left and right are lists with the coefficients on the left and right side
    def __init__(self, left, right):
        self.left = left
        self.right = right

    # calculate the bound 
    def calc_bound(self): 
        # find the maximum lcm(a_i, b_j)
        max_lcm = 0
        for a_i in self.left: 
            for b_j in self.right: 
                if lcm(a_i, b_j) > max_lcm: 
                    max_lcm = lcm(a_i, b_j)

        return max(len(self.left), len(self.right)) * max_lcm

# Consider the equation a_1 X_1 + ... + a_n X_n = k 
# this class contains the solution (X_1, ..., X_n) and the value k of the equation
# but does contain the value of the coefficients (a_1, ..., a_n) 
class Solution: 
    def __init__(self, values, total): 
        self.values = values
        self.total = total

    def __str__(self): 
        return str(self.values)


def dot_product(vec1, vec2): 
    assert(len(vec1) == len(vec2))

    value = 0 
    for i in range(len(vec1)): 
        value += vec1[i] * vec2[i]
    return value


# receives a list with coefficients a_1, ..., a_n and a value k 
# finds all the possibilities of (X_1, ..., X_n) such that 
# a_1 X_1 + ... + a_n X_n <= k 
def gen_solutions(equation, k):
    assert(len(equation) > 0)

    sol_lst = []
    a_1 = equation[0]

    # base case
    if len(equation) == 1: 
        for X_1 in range(0, (k//a_1) + 1): 
            eq_value = Solution([X_1], X_1 * a_1)
            sol_lst.append(eq_value)
        return sol_lst

    # inductive case
    sol_lst1 = gen_solutions(equation[1:], k)
    for sol in sol_lst1: 
        max_value_X_1 = (k - sol.total)//a_1
        for X_1 in range(0, max_value_X_1 + 1): 
            new_sol = Solution([X_1] + sol.values, X_1 * a_1 + sol.total)
            sol_lst.append(new_sol)
            
    return sol_lst


# receives a list of solutions, eliminate every solution of the form (0, ..., 0)
def elim_zero_sol(sol_lst):
    new_sol_lst = []
    for sol in sol_lst: 
        if sol.total != 0: 
            new_sol_lst.append(sol)
    return new_sol_lst

# check if a solution "sol" = (X_1, ..., X_n) can be obtained as a linear combination
# of the solutions in the list "sol_lst". 
# returns True in case "sol" is dependent and False otherwise
def check_linear_dependency(sol, sol_lst): 
    for sol1 in sol_lst: 
        assert(len(sol) == len(sol1))

        # We will check whether we can subtract sol1 from sol and still obtain 
        # all components >= 0. If we can, this means sol is linearly dependent
        all_components_ge0 = True
        for i in range(len(sol)): 
            if sol[i] - sol1[i] < 0:  
                all_components_ge0 = False

        if all_components_ge0: 
            return True
    return False



# print a Table with the solutions to a diophantine equation. 
# TO DO: make the Table prettier
def print_dio_table(sol_lst, dio_eq): 
    print("The table of solutions is: ")
    for sol in sol_lst: 
        print(sol)

# print the system of equations obtained 
def print_system(solutions, original_var_names): 
    global var_index 

    print("\nThe system after we solve the equations is: ")
    for i in range(len(original_var_names)): 
        X = original_var_names[i]
        print("\n" + X + " = f(", end='')

        for j in range(len(solutions)): 
            sol = solutions[j]
            #assert(len(sol) == len(original_var_names))
            if sol[i] != 0: 
                if sol[i] != 1: 
                    print(str(sol[i]), end='')
                print("Z_" + str(var_index + j) + ", ", end='')
        print(")", end='')


    print("\n")
        


# receives a diophantine equation and the names of the corresponding variables 
# solves it, outputing the table of solutions
def dio_solver(dio_eq, var_names): 
    
    # calculate upper bound
    up_bound = dio_eq.calc_bound()
    print("Upper bound is: " + str(up_bound))

    # calculate all the possible solutions for the left-side and right-side 
    # separately
    solutions = []
    left_sol_lst = elim_zero_sol(gen_solutions(dio_eq.left, up_bound))
    right_sol_lst = elim_zero_sol(gen_solutions(dio_eq.right, up_bound))

    # sort them 
    left_sol_lst.sort(key = lambda sol: sol.total)
    right_sol_lst.sort(key = lambda sol: sol.total)


    for left_sol in left_sol_lst: 
        for right_sol in right_sol_lst: 
            # only continue if left hand side and right hand side have the same value
            if left_sol.total != right_sol.total: 
                continue  

            # combine the left-hand side and the right-hand side, but check if the
            # result is linearly independent from what we already have
            dependent = check_linear_dependency(left_sol.values + right_sol.values, solutions)
            if not dependent: 
                solutions.append(left_sol.values + right_sol.values)

    #print(solutions)

    # print the table of solutions
    print_dio_table(solutions, dio_eq)

    # print the new system of solutions
    print_system(solutions, var_names)


def main(): 
    global var_index 
    # X_1 + X_2 = Y_1 + Y_2
    #print("For the equation X_1 + X_2 = Y_1 + Y_2")
    #dio_solver(Dio_eq([1, 1], [1, 1]), ["X_1", "X_2", "Y_1", "Y_2"])

    # Stickel's example: 
    #print("\nFor the equation 2X_1 + X_2 + X_3 = 2Y_1 + Y_2")
    #dio_solver(Dio_eq([2, 1, 1], [2, 1]), ["X_1", "X_2", "X_3", "Y_1", "Y_2"])

    # Stickel's modified example
    # P0: f(2X_1, X_2, X_3) =? f(2pi X_2, Y_1)
    #print("\nFor the equation 2X_1 + X_2 + X_3 = 2piX_2 + Y_2")
    #dio_solver(Dio_eq([2, 1, 1], [2, 1]), ["X_1", "X_2", "X_3", "pi X_2", "Y_2"])

    # P1: f(pi Z_1, 2 piZ_5, pi Z_6) =? f(Z_3, Z_5, Z_6, Z_7)
    var_index = 8
    print("\nFor the equation X_1 + 2X_2 + X_3 = Y_1 + Y_2 + Y_3 + Y_4")
    dio_solver(Dio_eq([1, 2, 1], [1, 1, 1, 1]), 
            ["pi Z_1", "pi Z_5", "pi Z_6", "Z_3", "Z_5", "Z_6", "Z_7"])

    # P2: pi * f(Z_11, Z_15, Z_19, 2Z_20, Z_22, Z_25) =? 
    # f(Z_18, Z_19, Z_20, Z_21, Z_22, Z_23, Z_24, Z_25, Z_26, Z_27)
    # OBS: Z_19, Z_20, Z_22 and Z_25 are doubly suspended
    #var_index = 30
    #print("\nFor the equation X_1 + X_2 + X_3 + 2X_4 + X_5 + X_6 = \
    #       Y_1 + Y_2 + Y_3 + Y_4 + Y_5 + Y_6 + Y_7 + Y_8 + Y_9 + Y_10")
    #dio_solver(Dio_eq([1, 1, 1, 2, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]), 
    #        ["pi Z_11", "pi Z_15", "pi Z_19", "pi Z_20", "pi Z_22", "pi Z_25", 
    #            "Z_18", "Z_19", "Z_20", "Z_21", "Z_22", "Z_23", "Z_24", "Z_25", 
    #            "Z_26", "Z_27"])
    

main()
