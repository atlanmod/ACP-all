# ------------------
# 24/9/2019
# Class to do a pass of simplification and classification
# remove  tautology and DON'T classify explicit unsafe 
# simplified are stored in store
# -------------------

from RuleSet import * #@UnusedWildImport
from Utility import * #@UnusedWildImport

# ---------------------
# self.variables: universally quantified
class SimplifySet(RuleSet):
    
    # by default it is True
    def __init__(self):
        RuleSet.__init__(self)
        # to store unsafe
        self.unsafe = []
        # to store others
        self.store = []
    # --- end init
    
    # --------------------
    def __str__(self):
        result = super().__str__()
        result += "\n============== Simplify Rules =======================\n ----------- Store -------------- \n"
        for r in self.store:
            result += str(r) + "\n"
        result += " ----------- Unsafe -------------- \n"
        for er in self.unsafe:
            result += str(er) + "\n"
        return result
    # --- end str

    # -------------------
    # To provide some numeric data
    def get_info(self):
        result = super().get_info()
        result +=   "number of stored " + str(len(self.store)) + "\n" 
        result += "number of unsafes " + str(len(self.unsafe)) + "\n"
        #result += "number of unknown " + str(len(self.temp)) + "\n"
        return result
    # --- end get_info
    
    # -------------------
    # provide the current classified rules
    def get_current_rules(self):
        return self.unsafe + self.store
    # --- end get_info
    
    # -----------------------------
    # first classification: eliminate tautology
    # simplify  unsafe  using current system
    def classify(self, size):
        if (self.is_unsatisfiable(size)):
            # TODO exception
            print ("SimplifySet.classify system is unsatisfiable !")
        else:
            self.classify_rules(self.rules[:size])
        # ---
        # load stored rules in the solver
        self.solver.reset()
        # add unsafe here since more problems and more abstract
        for rule in self.store: # + self.unsafe: 
            self.solver.add(built_quantified(rule.toBoolRef(), self.variables, True))
    # --- end of classify
    
    # -----------------------------
    # first classification: eliminate tautology
    def classify_rules(self, rules):
        self.solver.reset()          
        self.store = []  
        for rule in  rules:
            cond = rule.get_cond()
            conc = rule.get_conc()
            crules = self.get_current_rules()
            csys = self.toBoolRef(crules, len(crules))
            #print ("SimplifySet.classify " + str(rule)) # + " tauto? " + str(self.is_tautology(csys, cond, conc)))
            indic = self.compute_indicator(csys, cond, conc)
            if (indic != Indicator.TAUTOLOGY): 
                self.store.append(rule)
            else:
                print(" classify_rules " + str(rule) + " is redundant! ")
            ### forget obvious and tautology
            #--- if indic
        # ---
    # --- classify_rules    

    # --------------------------
    # check equivalence of two z3 BoolRef with free variables
    # use a new solver to be more flexible
    # TODO quantifiers not need for prop
    def check(self, rules1, rules2):
        #print ("SimplifySet.check " + str(rules1) + " " +str(rules2))
        # rules1 and Not(rules2) 
        localsolver = Solver()
        if (self.variables):
            localsolver.add(ForAll(self.variables, rules1))
            localsolver.add(Exists(self.variables, Not(rules2)))
        else: 
            localsolver.add(rules1)
            localsolver.add(Not(rules2))
        #print (str(localsolver))
        print (" => " + str(localsolver.check()))
        # NOT rules1 and rules2 
        localsolver.reset()
        if (self.variables):
            localsolver.add(Exists(self.variables, Not(rules1)))
            localsolver.add(ForAll(self.variables, rules2))
        else:
            localsolver.add(Not(rules1))
            localsolver.add(rules2)
        #print (str(localsolver))
        print (" <= " + str(localsolver.check()))
    # ----- end check
    
    # --------------------------
    # check the validity of the transformation
    # self.rules <=> self.store # and self.unsafe
    # TODO case bool to SEE
    def check_simplified(self, end):
        # normalized and Not(exclusive) 
        z3rules = self.toBoolRef(self.rules, end)
        newrules = self.store #+ self.unsafe
        z3new = self.toBoolRef(newrules, len(newrules))
        #print (str(z3new))
        self.check(z3rules, z3new)
    # ----- end check

# --- end SimplifySet