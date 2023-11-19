from term import *
from permutation import *

# definition of a substitution 
class Subs: 
    def __init__(self, name, sub_lst):
        self.name = name
        self.sub_lst = sub_lst

    def __str__(self): 
        name = self.name + ":\n" 
        for basic_sub in self.sub_lst: 
            name += (basic_sub[0] + " ->  " + 
                    apply(self, Susp_var([], basic_sub[0], ID_PERM)).__str__() + 
                    "\n")
        return name  

# composition of two substitutions
def compose(sigma1, sigma2): 
    name = sigma1.name + sigma2.name
    sub_lst = sigma1.sub_lst + sigma2.sub_lst
    return Subs(name, sub_lst)

# apply the substitution {X -> s} in the term t
def apply_basic_sub(X, s, t): 
    if isinstance(t, Atom): 
        return t

    elif isinstance(t, Susp_var): 
        if t.var == X: 
            return apply_perm(t.perm, t.perm_name, s) 
        else: 
            return t

    elif isinstance(t, Abst): 
        t.body = apply_basic_sub(X, s, t.body)  
        return t

    elif isinstance(t, App): 
        new_args = []
        for arg in t.args: 
            new_args.append(apply_basic_sub(X, s, arg))
        return App(t.symbol, new_args)

    elif isinstance(t, ACApp): 
        new_args = []
        for arg in t.args: 
            new_args.append(apply_basic_sub(X, s, arg))
        result = ACApp(t.symbol, new_args)
        return flatten(result)

    else: 
        quit("term passed is not really a term") 

# apply a substitution in a term t
def apply(sigma, t): 
    if len(sigma.sub_lst) == 0: 
        return t
    else: 
        (X, s) = (sigma.sub_lst[0][0], sigma.sub_lst[0][1]) 
        cdr_sigma = Subs(sigma.name, sigma.sub_lst[1:])
        return apply_basic_sub(X, s, apply(cdr_sigma, t))


# print the substitution name along how it acts on the variables in var_lst
def print_subs(sigma, var_lst, arrow_sign = ' -> ', latex=False): 
    if latex == False: 
        print(sigma.name + ":")
        for var in var_lst: 
            t = apply(sigma, Susp_var([], var, ID_PERM))
            if isinstance(t, ACApp): 
                print(var + arrow_sign, end='') 
                print_ac(t)
            else: 
                print(var + arrow_sign + t.__str__())

    else: 
        print("$" + sigma.name + "$:")
        print("\\begin{align*}")
        for i in range(len(var_lst)): 
            var = var_lst[i]
            t = apply(sigma, Susp_var([], var, ID_PERM))
            print(var + " &" + arrow_sign, end='')
            if isinstance(t, ACApp): 
                print_ac(t)
            else: 
                print(t.__str__())
            if i != len(var_lst) - 1:
                print("\\\\")
        print("\\end{align*}")
