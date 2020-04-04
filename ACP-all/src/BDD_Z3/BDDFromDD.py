# ---------------------
# 31/3/2020
# Use BDD from pyeda
# ----------------------

### TODO essai traduction renamed
### may be from binary !!!

from dd.autoref import BDD #a
# from pyeda.inter import * #@UnusedWildImport
# from functools import reduce 
# from pyeda.boolalg.bdd import BDDNODEONE, BDDNODEZERO
from Normalized_OK import * #@UnusedWildImport

#### TODO may be reconsider it
class BDD_Build(Normalized_Enumerate):
    
    # --------------------
    # init constructor 
    def __init__(self):
        super().__init__()
        ### the BDD manager
        self.BDD = BDD()
        ### list of boolean variables
        self.VARS_name = [] # TODO may be keys ?
        #### for BDD variables
        self.VARS = [] 
        #### index of these variables in definitions
        self.KEYS = [] 
    # ---

#     # ---------------
#     # convert to BDD a renamed expression or rule
#     # bdd: the bdd manager
#     ### normalization could simplify it
#     def convert_BDD (self, exp, bdd):
#         #print("rule= " + str(exp))
#         if isinstance(exp, bool):
#             if (exp == True):
#                 return bdd.true
#             else:
#                 return bdd.false
#         elif (is_expr(exp)):
#             if (is_app(exp)):
#                 op = exp.decl().kind()
#                 if (op == Z3_OP_AND):
#                     ### op bdd nary or not ?
#                     res = [self.convert_BDD(X) for X in exp.children()]
#                     return reduce(lambda a,b: a.__and__(b), res)
#                 elif (op == Z3_OP_OR):
#                     res = [self.convert_BDD(X) for X in exp.children()]
#                     return reduce(lambda a,b: a.__or__(b), res)
#                 elif (op == Z3_OP_NOT):
#                     return self.convert_BDD(exp.children()[0]).__invert__() 
# #                 elif (op == Z3_OP_IMPLIES): # TODO ?
# #                     return  reduce(lambda a,b: a.__or__(b), 
# #                                    [convert_BDD(exp.children()[0]).__invert__(), convert_BDD(keys, exp.children()[1])]) 
#                 else:
#                     # TODO VAR[I] may be better with P_(I, ...) ...
#                     return self.VARS[self.KEYS.index(exp)]                          
#             else:
#                 print ("convert_BDD missing ??? " + str(exp))
#         # --- end if
#         else: # it should be a rule
#             return  reduce(lambda a,b: a.__or__(b), 
#                            [self.convert_BDD(exp.get_cond()).__invert__(), self.convert_BDD(exp.get_conc())]) 
#     # --- convert_BDD

    # -----------------
    # start the convertion
    # should be done after processing REQ
    # side effect on the BDD manager
    def start_bdd(self):
        self.VARS_name = ['X'+str(I) for I in range(len(self.definitions))]
        self.BDD.declare(self.VARS_name)
        self.VARS = [self.BDD.var(V) for V in self.VARS_name]
        self.KEYS = list(self.definitions.keys()) 
        self.VALUES = list(self.definitions.values()) 
        print("KEYS" + str(self.KEYS))
        print("VALUES" + str(self.VALUES))
#         for B in  [self.convert_BDD(R) for R in self.renamed]:
#             bdd = B & bdd
#         bdd.dump('/Users/jroyer/Desktop/TMP.pdf')
    # --- convert
    
    # ---------------    
    # conversion of a Binary into BDD
    # return a BDD
    def convert2BDD(self, binary):
        tmp = self.BDD.true
        for I in range(len(binary)):
            if (binary[I] == 0):
                tmp = self.VARS[I].__invert__().__and__(tmp)
            elif   (binary[I] == 1):
                tmp = self.VARS[I].__and__(tmp)
        return tmp     
    # ---

    # ---------------  
    # Convert a list of binary into an or BDD  
    # lbinary: List[Binary] to convert
    # PB here with or type ?
    # return a BDD
    def convert_or(self, lbinary):
        if (lbinary):
            tmp = self.convert2BDD(lbinary[0])
            for binary in lbinary[1:]:
                tmp = self.convert2BDD(binary).__or__(tmp) 
        else:
            tmp = self.BDD.false
        #print(str(tmp.to_dot()))  
        return tmp     
    # ---
    
    # ---------------  
    # Convert a bdd into a renamed Z3 expression
    # bdd is a BDD for an AND-term
    # return a Z3 renamed expression
    def bdd2renamed(self, bdd):
        path = bdd.satisfy_one() # only one in fact
        #print("path= " + str(path)) # TODO cas None 
        # we have only one dimension vars
        return And(*[self.REQ[V.indices[0]] if (W == 1) else Not(self.REQ[V.indices[0]])
                     for (V, W) in path.items()])
    # --- bdd2renamed
        

# --- BDD