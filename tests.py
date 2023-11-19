from term import *
from permutation import *
from substitution import * 

# this function purpose is to return a list of (possibly) interesting terms
# that will be used by other functions
def get_term_lst(): 
    # the terms 
    pi_X = Susp_var([("a", "b")], "X", "pi")
    id_X = Susp_var([], "X", ID_PERM)
    atom_a = Atom("a")
    atom_b = Atom("b")
    ac_f_1 = ACApp("f", [pi_X, atom_a]) 
    ac_f_2 = flatten(ACApp("f", [ac_f_1, ac_f_1]))

    # 
    term_lst = []
    term_lst.append(pi_X)
    term_lst.append(id_X)
    term_lst.append(atom_a)
    term_lst.append(atom_b)
    term_lst.append(ac_f_1)
    term_lst.append(ac_f_2)

    return term_lst

### for file terms.py
def test_with_terms(): 
    # creation of terms
    pi_X = Susp_var(["a", "b"], "X", "pi")
    id_X = Susp_var([], "X", "")
    #print(pi_X)
    atom_a = Atom("a")
    atom_b = Atom("b")
    ac_t_1 = ACApp("f", [pi_X, atom_a]) 
    #print(ac_t_1)
    ac_t_2 = ACApp("f", [ac_t_1, ac_t_1])
    #print(ac_t_2)

    # function flatten
    #print(flatten(ac_t_1))
    #print(flatten(ac_t_2))

    # get_args_dic
    #terms_occur = get_args_dic([pi_X, atom_a, id_X, atom_a, atom_b, pi_X]) 
    #terms_occur = get_args_dic([pi_X, atom_a, pi_X, atom_a]) 
    #print(terms_occur)

    # print_ac
    #print_ac(ac_t_2)
    #print_ac(flatten(ac_t_2))

### for file permutation.py
def test_with_perm(): 
    # get_name_exp_perm
    #print(get_name_exp_perm("pi^k"))
    #print(get_name_exp_perm("pi^{k}"))

    # get_perm_name
    #print(get_perm_name("pi^1", "pi^2")) 
    #print(get_perm_name("pi", "pi^2")) 
    #print(get_perm_name("pi^1", "pi^k"))
    #print(get_perm_name("pi^n", "pi^k"))
    #print(get_perm_name("gamma", "pi"))
    #print(get_perm_name("Id", "pi"))

    # apply perm
    term_lst = get_term_lst() 
    for t in term_lst: 
        print("Starting for t = ", end='')
        print(t)
        print("Applying permutation pi = (a b) \nResult: ", end='')
        print(apply_perm([("a", "b")], "pi", t))
        print("Applying permutation gamma = (c d) \nResult: ", end='')
        print(apply_perm([("c", "d")], "gamma", t))
        print("\n")

def test_with_subs(): 
    a = Atom("a")
    b = Atom("b")
    sigma = Subs("sigma", [("X", a)])
    sigma_1 = Subs("sigma_1", [("X", a), ("Y", b)])
    term_lst = get_term_lst() 
    for t in term_lst: 
        print("Starting for t = ", end='')
        print(t)
        print("Applying substitution sigma = X -> a \nResult: ", end='')
        print(apply(sigma, t))
        print("Applying substitution sigma_1 = X -> a, Y -> b \nResult: ", end='')
        print(apply(sigma_1, t))
        print("\n")


def main(): 
    # tests for the file term 
    test_with_terms()

    # tests for the file permtutation
    #test_with_perm()

    # test for substitution
    #test_with_subs()

main()
