# ------------------
# 24/9/2019
# parse collect definitions and rewrite the rules
# -------------------

from z3.z3util import * #@UnusedWildImport
from SimplifySet import * #@UnusedWildImport
from collections import * #@UnusedWildImport
from Utility import * #@UnusedWildImport

# --------------------------
# Class for Table inheriting rule set 
class Renaming(SimplifySet):
    
    # --------------------
    # init constructor 
    def __init__(self):
        super().__init__()
        # to store link exp : proposition
        self.propositions =  {}
        # to store definitions needs to preserve ordering
        self.definitions = OrderedDict() 
        # radix of propositions
        self.root = "P_"
        # counter for new proposition
        self.counter = 0
        # new rules after renaming
        self.renamed = []
        # second local solver for renamed rules
        self.solver_renamed = Solver()
        # aux to count check 
        self.checking = 0             
    # --- end init
        
    # --------------------
    def __str__(self):
        result = super().__str__()
        result += " ----------- definitions -------------- \n"
        result += str(self.definitions) + "\n"     
        #result += " number of propositions " + str(len(self.definitions)) + "\n"     
        result += " number of propositions " + str(self.counter) + "\n"     
        result += " ----------- rules renamed -------------- \n"
        for er in self.renamed: # + self.renamed_unsafe:
            result += str(er) + "\n"     
        return result
    # --- end str

    #------------------
    # add a new definition in self.definitions
    # add predicates capturing free variables as definitions
    # return the corresponding predicate call or proposition
    def add_definition(self, exp):
        #print("add_definition for " + str(exp))
        key = exp
        if (key not in self.propositions):
            if (is_const(exp)): # this is a proposition
                self.propositions[exp] = exp
                self.definitions[exp] = exp
            else: # this is an application or quantifier
                self.counter += 1
                freevars = get_vars(exp)
                signature = [X.sort() for X in freevars]
                signature.append(BoolSort())
                #print ("freevars: " + str(freevars) + " signature " + str(signature))
                pred = Function(self.root + str(self.counter), signature)
                #print ("predicate " + str(pred) + " " + str(pred.ast))
                #  should defined call 
                call = pred(freevars)
                #prop = Const(self.root + str(self.counter), BoolSort())
                # FuncDecl not BoolSort
                self.propositions[key] = call
                self.definitions[call] = exp
            #print ("add_definition " + str(self.propositions[key]))
        # --- if exp
        return self.propositions[key]
    # ---     

    #------------------
    # parse the rules and add new definitions in the solver_renamed
    def parse_rules(self):
        #parse store rules 
        for rule in self.store:
            self.renamed.append(Rule(self.parse(rule.get_cond()), self.parse(rule.get_conc())))
        # load definitions in Solver
        self.add_definitions_in_solver()
        # self.solver contains the definitions and the renamed rules
        for rule in self.renamed:
            self.solver_renamed.add(built_quantified(rule.toBoolRef(), self.variables, True))
        #self.add_unsafes_in_solver() TODO remove
    # --- 
    
    # -------------------
    # add the definitions in the solver_renamed
    def add_definitions_in_solver(self):
        for de in self.definitions:
            # forget propositions 
            defi = self.definitions[de]
            if (not is_const(defi)):
                self.solver_renamed.add(built_quantified(de == defi, self.variables, True))
    # --- add_definitions_in_solver 

    # ---------------
    # simple parsing for conditions and conclusions
    # only the top-level
    # rename internal parts with Tseitin
    # return the renamed expression
    # side effect on self.definitions and self.propositions
    def parse(self, exp):
        #print ("size_nodes " + str(exp) + str(type(exp)) + str(is_int(exp)))
        # may be bad ...
        if isinstance(exp, bool):
            return exp # True+False
        elif is_const(exp): # this is a BoolRef constant
            return self.add_definition(exp)
        elif (is_expr(exp)):
                if (is_app(exp)):
                    op = exp.decl().kind()
                    #print ("app " + str(exp.decl()))
                    if (op == Z3_OP_AND):
                        res = [self.parse(X) for X in exp.children()]
                        return And(*res)
                    elif (op == Z3_OP_OR):
                        res = [self.parse(X) for X in exp.children()]
                        return Or(*res)
                    elif (op == Z3_OP_NOT):
                        return Not(self.parse(exp.children()[0]))                    
                    else:
                        # renaming
                        return self.add_definition(exp)                 
                elif (is_quantifier(exp)):
                    # renaming
                    return self.add_definition(exp)                 
                else:
                    print ("else ??? " + str(exp))
        # --- end if
        else:
            print ("parse louche " + str(exp))
    # --- end parse

    # --------------------
    # rewrite a renamed expression into the original form
    # using self.definitions
    # return a Z3 boolref
    def rewrite(self, exp):
        #print ("size_nodes " + str(exp) + str(type(exp)) + str(is_int(exp)))
        if isinstance(exp, bool):
            return exp # True+False
        elif (exp in self.definitions):
            return self.definitions[exp]
        #elif (is_expr(exp)):
        elif (is_app(exp)):
            op = exp.decl().kind()
            #print ("app " + str(exp.decl()))
            if (op == Z3_OP_AND):
                return And(*[self.rewrite(X) for X in exp.children()])
            elif (op == Z3_OP_OR):
                return Or(*[self.rewrite(X) for X in exp.children()])
            elif (op == Z3_OP_NOT):
                return Not(self.rewrite(exp.children()[0]))             
        else:
            print ("wrong expression to rewrite " + str(exp))
    # --- rewrite 

    # --------------------
    # check  self.definitions => self.store <=> self.renamed
    # use a local solver
    def check_renamed(self):
        local = Solver()
        for de in self.definitions:
            # forget propositions 
            defi = self.definitions[de]
            if (not is_const(defi)):
                local.add(built_quantified(de == defi, self.variables, True))
        # definition loaded
        z3store = ForAll(self.variables, self.toBoolRef(self.store, len(self.store)))
        z3renamed = ForAll(self.variables, self.toBoolRef(self.renamed, len(self.renamed)))
        local.push()
        local.add(z3store)
        local.add(Not(z3renamed))
        # unknown are considered sat
        print("self.definitions => (self.store => self.renamed): " + str(local.check()))
        local.pop()
        local.push()
        local.add(Not(z3store))
        local.add(z3renamed)
        print("self.definitions => (self.renamed => self.store): " + str(local.check()))
        local.pop()
    # ----check_renamed
    
    # -------------------- 
    # Check if !*store & ~?request is unsat
    # renamed is a renamed z3 term
    # solver_renamed contains definitions and renamed rules
    # return True if undefined
    def check_undefined_request(self, renamed):
        #print ("check_undefined_request " + str(renamed))
        self.checking += 1 # to see  
        self.solver_renamed.push()
        # prop as variables 
        self.solver_renamed.add(built_quantified(renamed, self.variables, False))
        #print(str(self.solver_renamed))
        # unknown are considered sat
        res = self.solver_renamed.check()
        #print("undefined request " + str(renamed) + " ? " + str(res))        
        self.solver_renamed.pop()
        if (res == unknown):
            self.unknown += 1
            print ("check undefined request unknown: " + str(renamed))     
        return res == unsat
    # ----check_undefined_request    
    
    # -------------------
    # check unsat of original request
    # use a local solver and return True/False
    def check_unsat_request(self, renamed):
        self.local_solver.reset()
        self.local_solver.add(built_quantified(self.rewrite(renamed), self.variables, False))
        res = self.local_solver.check()
        if (res == unknown):
            print ("check unsat request unknown: " + str(self.rewrite(renamed)))        
        return res == unsat        
    # --- check_unsat_request
    
#     #### 23/9/2019 ================= add for personal tactic
#     # =============
#     # compute the NNF of the negation of the simplified rule systems
#     # split the disjunction to get a sum of products terms
#     # they are represented as List[Z3Exp]
#     # return a List(Or) of ... TODO
#     # TODO may be better after renamed
#     def nnfnot(self):
#         # renamed contains a list of Implies
#         traces = {} # dico[Int x List[List[Int]]]
#         res = []
#         counter = 0
#         for I in range(len(self.renamed)):
#             rule = self.renamed[I]
#             print (" rule " + str(rule))
#             trans = NNF(And(rule.get_cond(), Not(rule.get_conc())))
#             print ("nnf= " + str(trans))
#             ### reduction to conjunctions 
#             pieces = Repeat(OrElse(SPLIT, SKIP))(trans[0])
#             #print (str(pieces))
#             ### these are Goal/And becomes list() 
#             alls = [list(X) for X in pieces]
#             # TODO Binary conversion
#             for andlist in alls:
#                 res.append(self.convert_binary(andlist))
#             # need to count the expressions
#             for J in range(len(alls)):
#                 print ("conversion= " + str(res[counter]))
#                 traces[counter] = [[I]]
#                 counter += 1
#         # ---
#         print ("#binaries= " + str(len(res)))
#         ### TODO process some simplifications ?
#         ### check two-way inclusion but is it useful ?
#         #return res, traces
#     # --- nnfnot
           
# --- end Renaming