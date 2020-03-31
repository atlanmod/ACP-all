# ---------------------
# 31/3/2020
# Use BDD from pyeda
# ----------------------

from pyeda.inter import * #@UnusedWildImport
from functools import reduce 
from pyeda.boolalg.bdd import BDDNODEONE, BDDNODEZERO
from Normalized_OK import * #@UnusedWildImport

#### TODO may be reconsider it
class BDD_Build(Normalized_Enumerate):
    
    # --------------------
    # init constructor 
    def __init__(self):
        super().__init__()
        #### creation des variables
        self.VARS = self.bddvars('VARS', len(self.definitions))
        self.KEYS = list(self.definitions.keys())
    # ---

    # ---------------
    # convert to BDD a renamed expression or rule
    ### normalization could simplify it
    def convert_BDD (self, exp):
        #print("rule= " + str(exp))
        if isinstance(exp, bool):
            if (exp.is_true()):
                return BDDNODEONE
            elif (exp.is_false()):
                return BDDNODEZERO
        elif (is_expr(exp)):
            if (is_app(exp)):
                op = exp.decl().kind()
                if (op == Z3_OP_AND):
                    res = [self.convert_BDD(X) for X in exp.children()]
                    return reduce(lambda a,b: a.__and__(b), res)
                elif (op == Z3_OP_OR):
                    res = [self.convert_BDD(X) for X in exp.children()]
                    return reduce(lambda a,b: a.__or__(b), res)
                elif (op == Z3_OP_NOT):
                    return self.convert_BDD(exp.children()[0]).__invert__() 
#                 elif (op == Z3_OP_IMPLIES): # TODO ?
#                     return  reduce(lambda a,b: a.__or__(b), 
#                                    [convert_BDD(exp.children()[0]).__invert__(), convert_BDD(keys, exp.children()[1])]) 
                else:
                    # TODO VAR[I] may be better with P_(I, ...) ...
                    return self.VARS[self.KEYS.index(exp)]                          
            else:
                print ("convert_BDD missing ??? " + str(exp))
        # --- end if
        else: # it should be a rule
            return  reduce(lambda a,b: a.__or__(b), 
                           [self.convert_BDD(exp.get_cond()).__invert__(), self.convert_BDD(exp.get_conc())]) 
    # --- convert_BDD

    # -----------------
    # convert the renamed rules in a BDD
    # return a BDD
    def convert(self):
        return reduce(lambda a,b: a.__and__(b), [self.convert_BDD(R) for R in self.renamed])
    # --- convert
    

# --- BDD