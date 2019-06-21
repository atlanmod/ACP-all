#------------
# 5/4/2019
# DNF => CNF both are Binary that is List[1/0/-1]
#------------

# TODO don't use characteristic now

from NormalizedRule import * #@UnusedWildImport

#--------------
# TODO add a new characteristic from original rules
# Rule with binary to enumerate in the iterative process
# TODO what are the atoms ?
class BinaryRule(NormalizedRule):
 
    # --------------------
    # create a new rule 
    def __init__(self, cond, conc):
        super().__init__([], cond, conc) # not used
    # --- end init
 
    # --------------------
    def __str__(self):
        return super().__str__()
    # --- end str
    
#     # --------------------
#     # get the condition as a Z3 BoolRef
#     # return an BoolRef
#     # TODO
#     def get_cond(self):
#         if (isinstance(self.cond, bool)):
#             return self.cond
#         elif (is_expr(self.cond)):
#             return self.cond
#         elif (self.cond): # a list
#             if (len(self.cond)==1):
#                 return self.cond[0]
#             else:
#                 return And(*self.cond)
#         else:
#             print ("Rule.get_cond: syntax error!" )
#     # --- end get_cond
    
#     # --------------------
#     # It has an OR meaning
#     # TODO 
#     def get_conc(self):
#         if (isinstance(self.conc, bool)):
#             return self.conc
#         elif (is_expr(self.conc)):
#             return self.conc
#         elif (self.conc): # a list
#             if (len(self.conc)==1):
#                 return self.conc[0]
#             else:
#                 return Or(*self.conc)
#         else:
#             print ("Rule.get_conc: syntax error!" )        
#     # --- end get_conc

#     # --------------------
#     # redefine Z3 BoolRef generation
#     # attention False possible
#     # TODO
#     def z3(self):
#         D = self.get_cond()
#         C = self.get_conc()
#         return Implies(D, C)
#     # --- end z3

# -- end class BinaryRule
