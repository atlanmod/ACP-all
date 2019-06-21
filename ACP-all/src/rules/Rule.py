# ------------------
# 11/1/2019
# simple Z3 rule
# -------------------

from z3 import * #@UnusedWildImport

# -----------------------------------------------------
# Class rule
# Free variables are assumed to be shared and declared at the top
# Implies(cond, conc) basically
class Rule():
    
    def __init__(self, cond, conc):
        # BoolRef condition
        self.cond = cond
        # BoolRef conclusion
        self.conc = conc
    # --- end init
    
    # --------------------
    def __str__(self):
        return "<" + str(self.cond) + " => " + str(self.conc) + ">"
    # --- end str

    # --------------------
    # generate a Z3 BoolRef
    def z3(self):
        cond = self.get_cond()
        conc = self.get_conc()
        return Implies(cond, conc)
    # --- end z3
    
    # --------------------
    # readers
    def get_cond(self):
        return self.cond
    def get_conc(self):
        return self.conc
    # --- end readers    
    
    # --------------------
    # setter
    def set_cond(self, new):
        self.cond = new
    def set_conc(self, new):
        self.conc = new
    # --- end setter
    
    # --------------------
    # test obvious and return yes or no
    # obvious is a simple tautology ?*D unsat
    # with free variables
    # if unknown return no
    def is_obvious(self, variables):
        if (isinstance(self.get_cond(), bool)):
            return not self.get_cond()
        else:
            S = Solver()
            if (variables):
                S.add(Exists(variables, self.get_cond()))
            else:
                S.add(self.get_cond())
            return (S.check().__eq__(unsat))
    # --- end is_obvious  
    
    # --------------------
    # test tautology and return yes or no
    # with free variables
    # if unknown return no
    def is_tautology(self, variables):
        S = Solver()
        if (variables):
            S.add(Exists(variables, And(self.get_cond(), Not(self.get_conc()))))
        else:
            S.add(And(self.get_cond(), Not(self.get_conc())))
        return (S.check().__eq__(unsat))
    # --- end is_tautology     
    
    # --------------------
    # test satisfiability and return yes or no
    # with free variables
    # if unknown return no
    def is_unsatisfiable(self, variables):
        S = Solver()
        if (variables):
            S.add(ForAll(variables, Or(Not(self.get_cond()), self.get_conc())))
        else:
            S.add(Or(Not(self.get_cond()), self.get_conc()))
        return (S.check().__eq__(unsat))
    # --- end is_unsatisfiable   

    # --------------------
    # Built the corresponding BoolRef
    # without the ForAll quantifier 
    def toBoolRef(self):
        return Implies(self.get_cond(), self.get_conc())
    # --- end of toBoolRef
    
# --- end Rule