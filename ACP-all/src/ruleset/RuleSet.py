# ------------------
# 29/3/2019
# Class for rule system
# -------------------

### TODO clean useless methods

from z3 import * #@UnusedWildImport
from Rule import * #@UnusedWildImport
from Indicator import * #@UnusedWildImport

# ---------------------
# self.variables: universally quantified
class RuleSet():
    
    # by default it is True
    def __init__(self):
        # quantifier variables common to all
        self.variables = []
        # cond => conc 
        self.rules = []
        # local solver
        self.solver = Solver()
        self.solver.set(timeout = 1000) ### 1s important parameter
        # to count unknow cases
        self.unknown = 0
    # --- end init
    
    # --------------------
    def __str__(self):
        result = "============== Rule set =======================\n"
        result += "Quantifiers: " + str(self.variables) + "\n"
        result += "\n".join([str(x) for x in self.rules])
        return result + "\n"
    # --- end str

    # -------------------
    # To provide some numeric data
    def get_info(self):
        return "Total number of rules " + str(self.number_rule()) + "\n"
    # --- end get_info
    
    # --------------------
    # Built the corresponding BoolRef of some normalized
    # without the ForAll quantifier 
    # only the first end normalized
    def toBoolRef(self, rules, end):
        if (end > 0):
            args = []
            for k in range(0, end):
                    r = rules[k]
                    args.append(Implies(r.get_cond(), r.get_conc()))
            return And(*args)
        else:
            return True
    # --- end of toBoolRef
    
    # --------------------
    # Built the corresponding BoolRef of rules
    # without the ForAll quantifier  but forget the ith
    # only the first end normalized
    def toBoolRef_but(self, rules, ith):
            args = []
            for k in range(0, len(rules)):
                if (k != ith):
                    r = rules[k]
                    args.append(Implies(r.get_cond(), r.get_conc()))
            return And(*args)
    # --- end of toBoolRef    

    # --------------------
    # add a variable: name sort
    def add_variable(self, name, sort):
        self.variables.append(Const(name, sort))
    # --- end add_variable
    
    # --------------------
    # one getter
    def get_variable(self, i):
        return self.variables[i]
    # --- end get_variable
    
    # --------------------
    # add a rule
    # cond, conc: are ExpRef 
    # rule (cond => conc)
    def add_rule(self, cond, conc):
        self.rules.append(Rule(cond, conc))
    # --- end add_rule
    
    # --------------------
    # rule getter
    def get_rule(self, i):
        return self.rules[i]
    # --- end get_rule
    
    # --------------------
    # some size informations
    def number_rule(self):
        return len(self.rules)
    def number_variable(self):
        return len(self.variables)
    # --- end of some informations

    # -------------------
    # check unsatisfiability of !* csys !* exp if flag=True
    # else check !*csys ?* exp
    # return true if unsat
    def check_quantified_unsat(self, csys, exp, flag):
        self.solver.reset()
        if (self.variables):
            self.solver.add(ForAll(self.variables, csys))
            if (flag):
                self.solver.add(ForAll(self.variables, exp))
            else:
                self.solver.add(Exists(self.variables, exp))
        else:
            self.solver.add(csys)
            self.solver.add(exp)
        return (self.solver.check().__eq__(unsat))        
    # --- end check_quantified_unsat    

    # ---------------------
    # test unsatisfiability
    def is_unsatisfiable(self, end):
        self.solver.reset()
        if (self.variables):
            self.solver.add(ForAll(self.variables, self.toBoolRef(self.rules, end)))
        else:
            self.solver.add(self.toBoolRef(self.rules, end))
        res = self.solver.check()
        if (res == unknown):
            print ("is_unsatisfiable " + str(res))
        return (res == unsat)
    # --- end is_unsatisfiability
    
    # --------------------
    # test tautology with free variables
    # and return True if unsat else False if sat or unknown
    # check against rules under construction !* csys & ?* (cond & ~conc) 
    def is_tautology(self, csys, cond, conc):
        self.solver.reset()
        if (self.variables):
            self.solver.add(ForAll(self.variables, csys))
            self.solver.add(Exists(self.variables, And(cond, Not(conc))))
        else:
            self.solver.add(csys)
            self.solver.add(And(cond, Not(conc)))
        return (self.solver.check().__eq__(unsat))
    # --- end is_tautology         
    
    # --------------------
    # test tautology with free variables 
    # and return True if unsat else False if sat or unknown
    # check against rules in the solver and !* csys & ?* (cond & ~conc) 
    def is_tautology_bis(self, csys, cond, conc):
        self.solver.push()
        if (self.variables):
            self.solver.add(ForAll(self.variables, csys))
            self.solver.add(Exists(self.variables, And(cond, Not(conc))))
        else:
            self.solver.add(csys)
            self.solver.add(And(cond, Not(conc)))
        res = self.solver.check().__eq__(unsat)
        self.solver.pop() # restore original context
        return res
    # --- end is_tautology_bis       
        
    # --------------------
    # test obvious with free variables
    # and return True if unsat else False if sat or unknown
    # check against rules under construction !* csys & ?* cond
    def is_obvious(self, csys, cond):
        self.solver.reset()
        if (self.variables):
            self.solver.add(ForAll(self.variables, csys))
            self.solver.add(Exists(self.variables, cond))
        else:
            self.solver.add(csys)
            self.solver.add(cond)
        return (self.solver.check().__eq__(unsat))
    # --- end is_obvious          

    # --------------------
    # test obvious with free variables
    # and return True if unsat else False if sat or unknown
    # check against rules in the solver and !* csys & ?* cond 
    def is_obvious_bis(self, csys, cond):
        #print ("is obvious bis solver: " + str(self.solver))
        self.solver.push()
        if (self.variables):
            self.solver.add(ForAll(self.variables, csys))
            self.solver.add(Exists(self.variables, cond))
        else:
            self.solver.add(csys)
            self.solver.add(cond)
        res = self.solver.check().__eq__(unsat)
        self.solver.pop() # restore original context
        return res        
    # --- end is_obvious_bis   
    
    # --------------------
    # test unsafeness with free variables !*(D=>C) ?*D is unsat
    # Global check is !* csys & !*(D=>C) ?*D unsat
    def is_unsafe(self, csys, cond, conc):
        self.solver.reset()
        if (self.variables):
            self.solver.add(ForAll(self.variables, csys))
            self.solver.add(ForAll(self.variables, Implies(cond, conc)))
            self.solver.add(Exists(self.variables, cond))
        else:
            self.solver.add(csys)
            self.solver.add(And(cond, conc))
        return self.solver.check().__eq__(unsat)
    # --- end is_unsafe   
    
    # --------------------
    # test unsafeness with free variables !*(D=>C) ?*D is unsat
    # TODO number is the rule numbering, if == -1 local check
    # Global check agaist rules in the solver and !* csys & !*(D=>C) ?*D unsat
    def is_unsafe_bis(self, csys, cond, conc):
        self.solver.push()
        if (self.variables):
            self.solver.add(ForAll(self.variables, csys))
            self.solver.add(ForAll(self.variables, Implies(cond, conc)))
            self.solver.add(Exists(self.variables, cond))
        else:
            self.solver.add(csys)
            self.solver.add(And(cond, conc))
        res = self.solver.check().__eq__(unsat)
        self.solver.pop() # restore original context
        return res             
    # --- end is_unsafe_bis 
    
    # --------------------
    # test fact with free variables
    # !* csys !*(D=>C) ?*~C is unsat
    def is_fact(self, csys, cond, conc):
        self.solver.reset()
        if (self.variables):
            self.solver.add(ForAll(self.variables, csys))
            self.solver.add(ForAll(self.variables, Implies(cond, conc)))
            self.solver.add(Exists(self.variables, Not(conc)))
        else:
            self.solver.add(csys)
            self.solver.add(Implies(cond, conc))
            self.solver.add( Not(conc))            
        return self.solver.check().__eq__(unsat)
    # --- end is_fact

    # --------------------
    # test rule implication (D1 => C1) => (D2 => C2)
    # !* csys (!*(D1=>C2) ?* (D2~C2)
    def is_implied(self, csys, D1, C1, D2, C2):
        self.solver.reset()
        if (self.variables):
            self.solver.add(ForAll(self.variables, csys))
            self.solver.add(ForAll(self.variables, Implies(D1, C1)))
            self.solver.add(Exists(self.variables, And(D2, Not(C2))))
        else:
            self.solver.add(csys)
            self.solver.add(Implies(D1, C1))
            self.solver.add(And(D2, Not(C2)))            
        return self.solver.check().__eq__(unsat)
    # --- end is_fact

    # ----------------------
    # check if exp is undefined for the rule system
    # apply req !* R from definition
    # req should have explicit quantifiers
    def check_undefined(self, req, end):
        #print ("check_undefined " + str(req))
        self.solver.reset()
        if (self.variables):
            #print("toboolref " + str(self.toBoolRef(end)))
            self.solver.add(ForAll(self.variables, self.toBoolRef(self.rules, end)))
            self.solver.add(req)
        else:
            self.solver.add(And(self.toBoolRef(self.rules, end), req))
        #print ("Check_undefined: " + str(exp) + " is " + str(self.solver.check()))
        return self.solver.check()
    # --- end check_undefined   
    
    # ------------
    # add a new fact in the solver here !*exp
    def add_in_solver(self, exp):
        if (self.variables):
            self.solver.add(ForAll(self.variables, exp))
        else:
            self.solver.add(exp)
    # --- add_in_solver
        
    # ------------
    # !!!Don't reset the solver
    # compute indicator of an original rule !* (D => C) 
    # in the solver context enriched with !* csys
    # obvious: !*rules & !* csys & ?*D unsat
    # tautology/redundancy: !*rules & !* csys & ?* (D & ~C) unsat
    # unsafe: !*rules & !* csys   !*(D=>C) ?*D unsat
    # fact: !*rules & !* csys !*(D=>C) ?*~C unsat NOT HERE
    # TODO what is the good ordering ? check it
    # TODO how to optimize it ? 
    # TODO quantifier not needed for PROP
    def compute_indicator(self, csys, D, C):
        #print ("compute_indicator " + str(D) + "  " + str(C))
        if (C == False): # explicit unsafe
            return Indicator.UNSAFE
        res = Indicator.NONE
        self.solver.push()
        # enriched the current context (csys != False)
        if (not isinstance(csys, bool)): 
            if (self.variables):
                self.solver.add(ForAll(self.variables, csys))
            else:
                self.solver.add(csys)
        self.solver.push()
        # checking obvious
        if (self.variables):
            self.solver.add(Exists(self.variables, D))
        else:
            self.solver.add(D)
        check = (self.solver.check() == unsat)
        #print("compute_indicator obvious " + str(self.solver))        
        self.solver.pop()
        if (check):
            res = Indicator.OBVIOUS
        else: 
            # checking tautology
            self.solver.push()
            if (self.variables):
                self.solver.add(Exists(self.variables, And(D, Not(C))))
            else:
                self.solver.add(D)
                self.solver.add(Not(C))
            check = (self.solver.check() == unsat)
            #print ("tauto " + str(self.solver))
            self.solver.pop()
            if (check):
                res = Indicator.TAUTOLOGY
            else: 
                # checking unsafe
                self.solver.push()
                if (self.variables):
                    self.solver.add(ForAll(self.variables, Implies(D, C)))
                    self.solver.add(Exists(self.variables, D))
                else:
                    self.solver.add(D)
                    self.solver.add(C)
                check = (self.solver.check() == unsat)
                #print ("unsafe " + str(self.solver))                
                self.solver.pop()
                if (check):
                    res = Indicator.UNSAFE 
        # final pop to restore initial context
        self.solver.pop()
        return res
    # --- compute_indicator    
    
# --- end RuleSet