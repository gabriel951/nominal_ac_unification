from term import *

ID_PERM = "Id" 

# receives a permutation list
# returns the inverse of it
def inverse_perm(perm): 
    return perm[::-1]

# receives a permutation name
# get the base name and the exponent of a permutation
# if called with argument pi^{k} it will return (pi, k)
def get_name_exp_perm(perm):
    components = perm.split("^")
    if len(components) == 0 or len(components) > 2: 
        print(perm + "is not a well-formed permutation name")
        quit()

    base_name = components[0]
    if len(components) > 1: 
        exp = (components[1].replace('{', '')).replace('}', '')
    else: 
        exp = "1"
    return (base_name, exp)


# of the composition of two permutations
# Ex: get_perm_name(pi^k, pi^n) = pi^{k+n}
#     get_perm_name(pi^2, pi^3) = pi^{5}
#     get_perm_name(pi^k, pi^2) = pi^{k+2}
def get_perm_name(perm1, perm2): 
    (name1, exp1) = get_name_exp_perm(perm1)
    (name2, exp2) = get_name_exp_perm(perm2)

    if name1 == ID_PERM: 
        return name2 + "^{" + exp2 + "}"

    elif name2 == ID_PERM: 
        return name1 + "^{" + exp1 + "}"

    elif name1 != name2: 
        return perm1 + " " + perm2
    
    else: 
        try:
           new_exp = str(int(exp1) + int(exp2))
        except: 
           new_exp = exp1 + "+" + exp2
        finally: 
            if new_exp == "" or new_exp == "0": 
                return name1
            else: 
                return name1 + "^{" + new_exp + "}"

# apply a permutation to an atom 
def apply_perm_atom(perm, atom_name): 
    if len(perm) == 0: 
        return atom_name
    else: 
        atom_name = apply_perm_atom(perm[1:], atom_name) 
        swap = perm[0]
        if atom_name == swap[0]: 
            return swap[1]
        elif atom_name == swap[1]: 
            return swap[0]
        else: 
            return atom_name

# apply a permutation to a term t
def apply_perm(perm, perm_name, t): 
    if isinstance(t, Atom): 
        new_t_name = apply_perm_atom(perm, t.name) 
        new_t = Atom(new_t_name)
        return new_t

    elif isinstance(t, Susp_var): 
        new_t_perm = perm + t.perm
        new_t_var = t.var
        new_t_perm_name = get_perm_name(perm_name, t.perm_name)
        new_t = Susp_var(new_t_perm, new_t_var, new_t_perm_name)
        return new_t

    elif isinstance(t, Abst): 
        new_t_atom = apply_perm_atom(perm, t.atom)
        new_t_body = apply_perm(perm, perm_name, t.body)  
        new_t = Abstraction(new_t_atom, new_t_body) 
        return new_t

    elif isinstance(t, App): 
        new_t_symbol = t.symbol
        new_t_args = []
        for arg in t.args: 
            new_t_args.append(apply_perm(perm, perm_name, arg))
        new_t = App(new_t_symbol, new_t_args)
        return new_t 

    elif isinstance(t, ACApp): 
        new_t_symbol = t.symbol
        new_t_args = []
        for arg in t.args: 
            new_t_args.append(apply_perm(perm, perm_name, arg))
        new_t = ACApp(new_t_symbol, new_t_args)
        return new_t 

    else: 
        quit("term passed is not really a term") 

