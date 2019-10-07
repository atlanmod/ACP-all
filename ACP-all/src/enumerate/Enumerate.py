# ------------------
# 24/9/2019
# parse collect definitions and rewrite the rules
# new breadth first by level of size for request
# no prime simplification
# -------------------

from Utility import * #@UnusedWildImport
from Renaming import * #@UnusedWildImport
from time import * #@UnusedWildImport
from math import * #@UnusedWildImport
from Prime import * #@UnusedWildImport

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
        # local solver to check unsat
        self.local_solver = Solver()
    # --- end init
        
    # --------------------
    def __str__(self):
        result = super().__str__()
        result += " =================== Problems ================ \n"     
        result += "unknwon ? " + str(self.unknown)   + "\n"
        result += str(self.problems)   + "\n"
        #result += str([self.rewrite(X) for X in self.problems])   + "\n"
        result += "---\n"      
        for X in self.problems:
            result += str(self.rewrite(And(*X))) + "\n"
        result += "---\n"      
        return result
    # --- end str
    
    # --------------------
    def get_info(self):
        result = super().get_info()
        result += " REQ= " + str(self.REQ) + "\n"     
        result += " #problems= " + str(len(self.problems)) + "\n"     
        result += " #check= " + str(self.checking) + "\n"     
        return result
    # --- get_info
    
    #------------------
    # initialize renamed system and choose list of propositions for requests
    # here lreq is a list of syntactic expression to catch
    def initialize(self, size, lreq):
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
    def compute_table(self, lreq, size):
        self.initialize(size, lreq)
        print ("#REQ= " + str(len(self.REQ)))
        self.enumerate_check(self.REQ)
        #print ("size= " + str(size) + " time " + str(floor(process_time()-start)) + " #PB= " + str(len(self.problems)) )
        print (" final problems " + str([self.rewrite(And(*X)) for X in self.problems]))
    # --- compute_table 
        
    #------------------
    # enumerate breadth to get simplest set of problems
    # lprop a list of List[Z3]
    def enumerate_check(self, lprop):
        start = process_time()
        latoms = [] # List[Z3] atom or negation
        # first step check X and Not(X)
        for X in lprop:
            if (self.check_undefined_request(X)):
                    self.problems.append(X)
            else:
                latoms.append(X)
            if (self.check_undefined_request(Not(X))):
                    self.problems.append(Not(X))
            else:
                latoms.append(Not(X))
        # --- for 
        print (" level  -----------  1 ")        
        level = 1 # will be the size of the prod to check
        print(" problems " + str(self.problems))
        print(" time  " + str(floor(process_time()-start)))
        print (" ----- ")
        lprop = [[X] for X in latoms]
        while (len(lprop) > 0):
            #print (" #lprop= " + str(len(lprop)) + " lprop= " + str(lprop))  
            level += 1
            print (" level  ----------- " + str(level))            
            nextlevel = []
            # compute distinct enumeration 
            for I in range(len(lprop)):    
                for atom in latoms:
                    prod = lprop[I]
                    if (atom not in prod):
                        ### build and sort prod regarding latoms
                        prod = sortit(prod, atom, latoms)
                        #print ("prod " + str(prod))
                        # check if already seen
                        if (prod and (prod not in self.problems + nextlevel)):
                            ## check it and classify it 
                            req = And(*prod)
                            if (self.check_undefined_request(req)):
                                self.problems.append(prod)
                            else:
                                nextlevel.append(prod)
                        # --- if not in
                # --- end for prod
            lprop = nextlevel
            # remove unsat cases
            tmp = []
            for pb in self.problems:
                if (not self.check_unsat_request(And(*pb))):
                    # print ("PB sat: " + str(pb))
                    tmp.append(pb)
            self.problems = tmp
            print(" problems " + str([self.rewrite(And(*X)) for X in self.problems]))
            print(" time  " + str(floor(process_time()-start)) + " checking " + str(self.checking))
            print (" ----- ")
        # --- end while
    # ---- enumerate_check

    # --------------------
    # check problems are all included in Not(self.store) 
    # return True if problems and self.store is unsat
    # attention existential request   
    # should use a dedicated solver_renamed 
    def check_problems(self, size):
        #self.solver_renamed.add(ForAll(self.variables, self.toBoolRef(self.store, len(self.store))))  
        #print(str(Or(*[self.rewrite(X) for X in self.problems])))  
        self.solver.push()  
        self.solver.set(timeout = 100000) # 100s
        self.solver.add(Exists(self.variables, Or(*[self.rewrite(And(*X)) for X in self.problems])))
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