# definition of a term 
class Atom: 
    def __init__(self, name): 
        self.name = name

    def __str__(self): 
        return self.name

class Susp_var: 
    def __init__(self, perm, var, perm_name): 
        # perm is a list of atom swappings, while perm_name is the name 
        # you may give a permutation, like $\pi$ or $\pi_1$. 
        self.perm = perm
        self.var = var
        self.perm_name = perm_name

    def __str__(self): 
        # build a way to print permutation 
        return self.perm_name + "*" + self.var

class Abst: 
    def __init__(self, atom, body): 
        self.atom = atom 
        self.body = body 

    def __str__(self): 
        return "[" + (self.atom).__str__() + "]" + (self.body).__str__() 

class App: 
    def __init__(self, symbol, args): 
        self.symbol = symbol
        self.args = args
    
    def __str__(self): 
        name = self.symbol + "(" 
        for i in range(len(self.args)): 
            name += self.args[i].__str__()

            if i != len(self.args) - 1: 
                name +=  ", "
        name += ")"
        return name  

class ACApp: 
    def __init__(self, symbol, args): 
        self.symbol = symbol 
        self.args = args

    def __str__(self): 
        name = self.symbol + "(" 
        for i in range(len(self.args)): 
            name += self.args[i].__str__()

            if i != len(self.args) - 1: 
                name +=  ", "
        name += ")"
        return name  

# this function is used in print_ac
# receives a list of arguments, returns a dictionary where each key is either:
#
# 1. a variable name and in this case the value is another dictionary $d$ with
# respect to the permutations that are suspended in this variable. The key
# in $d$ is the permutation name and the value of $d$ is the number of times the
# permutation appear 
#
# 2. a term and in that case the value is a number 
# Ex: get_args_dic([pi X, a, Id X, a, b, pi X]) = {a: 2, X: {pi: 2, Id: 1}} , b: 1}
def get_args_dic(args): 
    terms_occur = {}
    for t in args: 
        if isinstance(t, Susp_var):
            if t.var in terms_occur: 
                if t.perm_name in terms_occur[t.var]:
                    terms_occur[t.var][t.perm_name] += 1
                else: 
                    terms_occur[t.var][t.perm_name] = 1
            else: 
                terms_occur[t.var] = {t.perm_name: 1}

        else: 
            if t in terms_occur: 
                terms_occur[t] += 1
            else: 
                terms_occur[t] = 1

    return terms_occur

# print an AC function application, grouping permutations that are suspended on the
# same variable
# Ex: print_ac(f(a, pi X, pi^2 X)) = f(a, [pi, pi^2]X)
# this function only works for Python 3.6 or above
def print_ac(t): 
    terms_occur = get_args_dic(t.args)

    print(t.symbol + "(", end='') 
    for t in terms_occur: 
        if isinstance(t, str): 
            # get the permutation dictionary for this suspended variable
            perm_dic = terms_occur[t]

            if len(terms_occur[t]) == 1:  
                # first key of the dictionary  
                perm_name = next(iter(perm_dic))

                if perm_dic[perm_name] != 1:
                    print(perm_dic[perm_name], end='')
                print(perm_name, end='')
                print(t, end='')

            else: 
                print("[", end='')
                first_item = True
                for perm_name in perm_dic: 
                    # we may need to print a comma,
                    if first_item != True: 
                        print(", ", end='')
                    first_item = False

                    if perm_dic[perm_name] != 1: 
                        print(perm_dic[perm_name], end='')
                    print(perm_name, end='')
                print("]", end='')
                print(t, end='')
                
        else: 
            if terms_occur[t] != 1: 
                print(terms_occur[t], end='')
            print(t, end='')

        # print the ", " if we are not in the last key  
        if t != list(terms_occur)[-1]:
            print(", ", end='')

    print(")")


# flattens an ACApp term 
def flatten(t): 
    if not isinstance(t, ACApp): 
        return t
    else: 
        new_args = []
        for ti in t.args: 
            if isinstance(ti, ACApp) and ti.symbol == t.symbol: 
                new_args = new_args + flatten(ti).args
            else: 
                new_args.append(ti)
        return ACApp(t.symbol, new_args)
