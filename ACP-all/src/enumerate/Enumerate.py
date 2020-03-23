# ------------------
# 4/2/2020
# parse collect definitions and rewrite the rules
# -------------------

from Utility import * #@UnusedWildImport
from Renaming import * #@UnusedWildImport
from time import * #@UnusedWildImport
from math import * #@UnusedWildImport

# --------------------------
# Class for Table inheriting rule set 
class Enumerate(Renaming):
    
    # --------------------
    # init constructor 
    def __init__(self):
        super().__init__()
        # to store the list of REQ propositions
        self.REQ = []
        # to store problems List[Z3boolref]
        self.problems = []
        # aux to count check 
        self.check= 0     
        # local solver to check unsat
        self.local_solver = Solver()
    # --- end init
        
    # --------------------
    def __str__(self):
        result = super().__str__()
        result += " =================== Problems ================ \n"     
        #result += "unknwon ? " + str(self.unknown)   + "\n"
        result += str(self.problems)   + "\n"
        #result += str([self.rewrite(X) for X in self.problems])   + "\n"
        result += "---\n"      
        for X in self.problems:
            result += str(self.rewrite(X)) + "\n"
        result += "---\n"      
        return result
    # --- end str
    
    # --------------------
    def get_info(self):
        result = super().get_info()
        result += " REQ= " + str(self.REQ) + "\n"     
        result += " #problems= " + str(len(self.problems)) + "\n"     
        result += " #check= " + str(self.check) + "\n"     
        return result
    # --- get_info
    
    #------------------
    # initialize renamed system and choose list of propositions for requests
    # here lreq is a list of syntactic expression to catch
    def initialize(self, lreq, size):
        self.classify(size)
        #self.check_simplified(size)
        #print (str(self.get_info()))
        self.parse_rules()
        #print (str(self))     
        # lreq is a List[ahead predicate]
        for key in self.definitions:
            defi = self.definitions[key]
            if (defi in lreq):
                self.REQ.append(key)
        #print ("REQ= " + str(self.REQ))
        self.check_renamed()
    # ---- initialize
    
    # ----------------
    # main entry point to apply enumerate
    # to measure time and simplify
    def compute_table(self, size, lreq):
        start = process_time()
        self.initialize(size, lreq)
        print ("#REQ= " + str(len(self.REQ)))
        self.enumerate_check([[X, []] for X in self.REQ])
        #print ("size= " + str(size) + " time " + str(floor(process_time()-start)) + " #PB= " + str(len(self.problems)) )
        # remove unsat cases
        tmp = []
        for pb in self.problems:
            if (not self.check_unsat_request(pb)):
                tmp.append(pb)
        #print (" #real problems " + str(count) + " add time " + str(floor(process_time()-start)))
        self.problems = tmp
    # --- compute_table 
        
#     #------------------
#     # brute enumerate AND-term from REQ
#     # check is sat with self.rules
#     # iterative combinations
#     def enumerate(self):
#         # this the list of starting points List[List[proposition], List[List[Z3]]
#         # representing pending conjunction to test in case of sat (not a problem)
#         self.enumerate_check([[X, []] for X in self.REQ])
#     # ---- enumerate_check   
     
    #------------------
    # enumerate breadth to get simplest set of problems
    # lprop a list of List[List[Z3 , List[List[Z3]]] as starting points of the search
    # first is a simple prop and last
    # a list of list for the conjunctions of already checked propositions 
    def enumerate_check(self, lprop):
        if (len(lprop) > 0):
            print ("enumerate_check " + str(len(lprop))) # + " how? " + str(len(lprop[0][1])) + "/" + str(lprop[0][1]))
            current = lprop[0][0] # an atomic proposition
            notcurrent = Not(current) # its negation
            #print ("current " + str(current))
            pb = self.check_undefined_request(current)
            pbnot = self.check_undefined_request(notcurrent)
            if (pb):
                self.problems.append(current)
                if (pbnot):
                    self.problems.append(notcurrent)
                    self.enumerate_check(lprop[1:]) 
                else:
                    # notcurrent is defined
                    res = self.check_conj(notcurrent, lprop[0][1])    
                    if (len(lprop) > 1): 
                        lprop[1] = [lprop[1][0], res]
                        self.enumerate_check(lprop[1:]) # 
                    # ---
            else: # current is defined 
                if (pbnot):
                    self.problems.append(notcurrent)
                    # first is sat
                    res = self.check_conj(current, lprop[0][1])
                    if (len(lprop) > 1): 
                        lprop[1] = [lprop[1][0], res]                    
                        self.enumerate_check(lprop[1:]) 
                else:
                    #  both are sat
                    res = self.check_conj(current, lprop[0][1])                     
                    res = res + self.check_conj(notcurrent, lprop[0][1]) 
                    if (len(lprop) > 1): 
                        lprop[1] = [lprop[1][0], res]     
                        self.enumerate_check(lprop[1:]) 
            # --- if (pb)
    # ---- enumerate_check
    
    # ---------------------
    # listoflconj : List[List[Z3]] representing current conjunctions
    # target : head element to modify List[Prop, List[List[Z3]]]
    # return List[Z3] to add as a new conjunction
    # req is a renamed expression
    # unkown is considered as sat    
    def check_conj(self, prop, listoflconj):
        if (len(listoflconj) > 0):
            res = []
            for lconj in listoflconj:
                tocheck = lconj + [prop]
                req = And(*tocheck)
                if (self.check_undefined_request(req)):
                    self.problems.append(req)
                else:
                    res.append(tocheck)
                # --- if 
            # --- for lconj
        else:
            res = [[prop]]
        #print ("check_conj lprop[1]= " + str(res))    
        return res                    
    # --- check_conj

    # -------------------- TODO move to renaming
    # Check if !*store & ~?request is unsat
    # renamed is a renamed z3 term
    # solver_renamed contains definitions and renamed rules
    # return True if undefined
    def check_undefined_request(self, renamed):
        #print ("check_undefined_request " + str(renamed))
        self.check += 1 # to see  
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
    
    # -------------------move to renaming
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
    
    # --------------------
    # check problems are all included in Not(self.store) 
    # return True if problems and self.store is unsat
    # attention existential request   
    # should use a dedicated solver_renamed 
    def check_problems(self):
        #self.solver_renamed.add(ForAll(self.variables, self.toBoolRef(self.store, len(self.store))))  
        #print(str(Or(*[self.rewrite(X) for X in self.problems])))  
        self.solver.push()  
        self.solver.set(timeout = 100000) # 100s
        self.solver.add(Exists(self.variables, Or(*[self.rewrite(X) for X in self.problems])))
        res = self.solver.check()      
        if (res == unsat):
            print("all problems are in Not(R) !")
        elif (res == sat):
            print("PROBLEMSsss with check_problems !")
        else:
            print("check_problems unknown ! ")
        self.solver.pop()  
    # ----check_sat_request    
    
# --- Enumerate