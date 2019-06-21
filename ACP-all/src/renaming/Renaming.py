# ------------------
# 13/6/2019
# parse collect definitions and rewrite the rules
# unsafe rules are forgotten
# -------------------

### TODO attention solver_renamed change donc revoir avec enumerate_combine ...
### no renamed_unsafe

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
        # self.renamed_unsafe = []
        # second local solver for renamed rules
        self.solver_renamed = Solver()
        #self.solver_renamed = SolverFor('LIA') # 
        #self.solver_renamed = SolverFor('AUFLIA') # 
        #self.solver_renamed = SolverFor('QF_NIA') # 
        #self.solver_renamed = SolverFor('QF_UFLIA') # 
        #self.solver_renamed = SolverFor('QF_UF') # 
        # (default: 4294967295)
        #self.solver_renamed.set(timeout =  4294967295) 
        #self.solver_renamed.set(timeout = 1000000000) 
        #self.solver_renamed.set(timeout = 1000) 
        #self.solver_renamed.set(timeout= 0) ### no timeout 
        #timeout (unsigned int) timeout (in milliseconds) (UINT_MAX and 0 mean no timeout) (default: 4294967295)
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
#         #parse unsafe rules 
#         for rule in self.unsafe:
#             self.renamed_unsafe.append(Rule(self.parse(rule.get_cond()), self.parse(rule.get_conc())))            
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
    
    # ------------------- TODO not used
    # add the unsafes in the solver_renamed
    def add_unsafes_in_solver(self):
        for rule in self.renamed_unsafe:
            self.solver_renamed.add(built_quantified(rule.toBoolRef(), self.variables, True)) 
    # --- add_unsafes_in_solver 
               
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
            print ("rewrite louche " + str(exp))
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

    # ---------------
    # Compute indicator in solver_renamed
    # D, C are Z3 renamed expressions
    # Auxiliary only for classify_and_store
    # without FACT checking
    # TODO is it correct with def ?
    # compute indicator of a renamed rule !* (D => C) 
    # in the context of definitions
    # TODO ????
    # obvious: !*rules  & ?*D unsat
    # tautology/redundancy: !*rules &  ?* (D & ~C) unsat
    # unsafe: !*rules    !*(D=>C) ?*D unsat
    def renamed_indicator(self, D, C):
        #print ("renamed_indicator " + str(self.solver)) # + " \n csys " + str(csys))
        res = Indicator.NONE
        #print("1 " + str(self.solver_renamed))
        self.solver_renamed.push()
        # checking obvious
        if (self.variables):
            self.solver_renamed.add(Exists(self.variables, D))
        else:
            self.solver_renamed.add(D)
        check = (self.solver_renamed.check() == unsat)
        self.solver_renamed.pop()
        if (check):
            res = Indicator.OBVIOUS
        else: 
            # checking tautology
            #print ("2 " + str(self.solver))
            self.solver_renamed.push()
            if (self.variables):
                self.solver_renamed.add(Exists(self.variables, And(D, Not(C))))
            else:
                self.solver_renamed.add(D)
                self.solver_renamed.add(Not(C))
            check = (self.solver_renamed.check() == unsat)
            #print ("RuleSet compute indic " + str(self.solver.check()))
            self.solver_renamed.pop()
            if (check):
                res = Indicator.TAUTOLOGY
            else: 
                # checking unsafe
                #print ("3 " + str(self.solver))
                self.solver_renamed.push()
                if (self.variables):
                    self.solver_renamed.add(ForAll(self.variables, Implies(D, C)))
                    self.solver_renamed.add(Exists(self.variables, D))
                else:
                    self.solver_renamed.add(D)
                    self.solver_renamed.add(C)
                check = (self.solver_renamed.check() == unsat)
                self.solver_renamed.pop()
                if (check):
                    res = Indicator.UNSAFE 
        return res
    # --- renamed_indicator 
       
# --- end Renaming