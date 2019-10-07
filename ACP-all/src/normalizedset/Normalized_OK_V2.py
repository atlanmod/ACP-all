# ------------------
# 24/9/2019
# Look for problems in undefined 
# Check is already a problem and if already seen
# Finally check if it is a problem add it 
# With check_unsat and prime at each level 
## change heuristic: no new problem by combining
# compute self.MIN as the  minimum measure for allreq
# separate init_problems but add them as problems
# add display for size presentation
# add sort allred
# -------------------

from NormalizedSet import  * #@UnusedWildImport
from Prime import * #@UnusedWildImport
from time import * #@UnusedWildImport
from math import * #@UnusedWildImport
from Enumerate import * #@UnusedWildImport

# --------------------------
# Class for Iterative_hashing method 
# Process the stored rules and classify them
class Normalized_enumerate(NormalizedSet):
    
    # --------------------
    # init constructor 
    def __init__(self):
        super().__init__()
        # to store the list of REQ key propositions
        self.REQ = []
        # to store classification of REQ=1 !REQ=0
        self.REQB = []
        # to store normalized and simplified problems
        self.normalized_problems = []
        # local solver
        self.local_solver = Solver()
        # to store binary from TACTIC
        self.binary = []    
        # reduce a Binary to a Binary:REQ 
        self.req_fun = lambda X: [X[I] for I in range(len(self.REQB)) if (self.REQB[I] == 1)]     
        # to measure time
        self.start = 0
        # to measure defined bit in a Binary
        self.measure = lambda X: sum([1 for I in X if (I != -1)])   
        # to store problems if heuristic is satisfied
        self.Hresult = []  
        # to store initial problems
        self.init_problems = []
        # minimal size in allreq
        self.MIN = 1
        # maximal #atoms in allreq
        self.MAXK = 0
    # --- end init

    # -------------------
    # To provide some numeric data
    def get_info(self):
        res = super().get_info() + "number of problems " + str(len(self.normalized_problems)) + "\n"
        return res 
    # --- end get_info
    
    # --------------------
    # show problems from all_normalized_unsafe
    def show_problems(self):
        print (" ----------------- problems  ")   
        for binary in self.normalized_problems:
                print(str(self.reverse_binary_req(binary)))
        print (" ----")
    # --- show_problems
    
    # --------------------
    # show problems from all_normalized_unsafe
    def display_problems(self, level):
        PBs = [self.reverse_binary_req(pb) for pb in self.normalized_problems if (self.measure(pb) == self.MIN + level -1)]
        if (PBs):
            print ("Found " + str(len(PBs)) + " problems of size " + str(self.MIN + level -1) + " time= " + str(floor(process_time()-self.start)))
            for pb in PBs:
                print(str(pb))
            print (" ----")
    # --- display_problems

    #------------------
    # compute table with frontier enumeration
    # lreq is a List[ahead predicate]    
    #  and check request syntax
    def compute_table(self, lreq, size):
        self.start = process_time()
        self.classify(size)
        self.check_simplified(size)
        self.parse_rules()
        self.check_renamed()
        #print (str(self))
        # compute REQ and REQB
        self.REQ = []
        for key in self.definitions:
            defi = self.definitions[key]
            if (defi in lreq):
                self.REQ.append(key)
        self.REQB = [1 if X in self.REQ else 0 for X in self.definitions.keys()]
        print (" REQB is = " + str(len(self.REQB)) + "/" + str(self.REQB) + " size REQ= " + str(len(self.REQ)))   
        self.enumerate_frontierOK()     # TACTIC + combine allreq breadth_frist
    # --- end compute_table

    #---------------------
    # new enumeration method from TACTIC
    # combine reduction to :REQ (similar to Negative) BREADTH-FIRST
    # and use is_included_in to check already a problem
    # and allseen list
    def enumerate_frontierOK(self):
        NBREQ = len(self.REQ)
        print("definitions " + str(self.definitions))
        # TACTIC applied to all renamed, but  possible on original 
        aux = TACTIC(Not(And(*[X.toBoolRef() for X in self.renamed])))
        #print (str([X.toBoolRef() for X in self.renamed]))
        aux = [list(X) for X in aux] # !!! Goals
        #print ("TACTIC: " + str(aux))
        # conversion to binary
        for andlist in aux:
            self.binary.append(self.convert_binary(andlist))  
        prime(self.binary) 
        print ("compute_problems from " + str(len(self.binary)) + " / " + str(self.binary))
        #print ("real " + str(self.reverse_list_binary(self.binary)))
        # check for if binary/REQ is a problem and store it 
        # and remove the corresponding undefined   
        self.initial_problems()     
        # ---------------------     
        # compute all remaining reductions
        # and sort in increasing self.measure
        allred = []
        for binary in self.binary:
            red = self.req_fun(binary)
            if ((red not in allred)  and (sum(red) > -NBREQ)):
                if (allred):
                    I = 0
                    while (I < len(allred) and self.measure(red) > self.measure(allred[I])):
                        I += 1
                    if (I == len(allred)):
                        allred.append(red)
                    else:
                        allred.insert(I, red)
                else:
                    allred = [red]
                # --- end sorting
        print ("allred= " + str(len(allred)) + " / " + str(allred))
        if (allred):
            #self.MIN = min([self.measure(R) for R in allred])
            self.MIN = self.measure(allred[0])
        # -----------
        # compute max number of atoms
        allatoms = [-1]*NBREQ
        for binary in allred:
            for I in range(NBREQ):
                if ((binary[I] == 1) or (binary[I] == 0)):
                    allatoms[I] = 1
        self.MAXK = self.measure(allatoms) 
        print ("MIN= " + str(self.MIN) + " MAXK= " + str(self.MAXK))
        # set init as problems and display minimal ones
        self.normalized_problems = self.init_problems
        self.display_problems(1)     
        # compute all combinations of reduction to :REQ
        elements = [] # last index of combined element
        size = len(allred)
        elements.extend(range(size))
        combinations = allred
        # store the sat enumerated requests
        allseen = [] # to avoid side-effect
        allseen.extend(allred)
        prev = 1 ### speed feeling
        level = 2 # number of conjunctions
        # compute all combinations of reductions
        while (combinations): # total 
            print (">>>>> starting level= " + str(level) + " size= " + str(len(combinations)) + " #allseen= " + str(len(allseen)) + 
                   " vitesse " + str(len(combinations)/prev))
            #print (" combinations= " + str(combinations))  
            # combine each in combinations with elements in allred 
            # and avoiding duplications
            I = 0
            newcombi = []
            newelts = []
            newpbs = []
            while (I < len(combinations)):
                other = combinations[I]
                last = elements[I]
                ### enumerate the combination not already tested
                for J in range(last+1, size):
                    binreq = allred[J]  
                    # compute AND return base and if maximal combination
                    common, maxi = make_common(other, binreq)
                    #print ("other " + str(other) + " binreq= " + str(binreq) + " base " + str(base) + " J= " + str(J))
                    # check if already seen   
                    if (common and (common not in allseen)):
                        # check if utile is included in problems
                        if (all([not is_included_in(common, X) for X in self.normalized_problems + newpbs])):
                            renamed = self.reverse_binary_req_renamed(common)
                            if (self.check_undefined_request(renamed)):
                                #print (" found problem " + str(self.reverse_binary_req(utile)))
                                newpbs.append(common)
                            elif (maxi):  # only defined not need to continue 
                                allseen.append(common)     
                            elif (J == size-1):  
                                allseen.append(common)                           
                            else: # store non defined requests to keep for the new level
                                newcombi.append(common)   
                                newelts.append(J)
                                allseen.append(common)  
                            # --- checking  undefinedness
                        # --- already a problem  
                    # --- allseen   
                # --- for J in allred  
                I += 1
            # --- end of one level
            # transfer and compute new level 
            prev = len(combinations)
            combinations = newcombi
            elements = newelts
            self.final_clean(level, newpbs)
            ### heuristic no new problem
            if (not newpbs) and (not self.Hresult) and self.normalized_problems: # compute heuristic
                print ("Heuristic says sufficient level is " + str(level))
                self.Hresult = self.normalized_problems.copy() # because of prime
            print("end #level= " + str(level) + " #problems here " + str(len(self.normalized_problems)) + " time = " + str(floor(process_time()-self.start)))
            print()                         
            level += 1
        # --- end while combinations
        print("checking checking= " + str(self.checking) + " allseen " + str(len(allseen)))
        # final problems 
        finalPB = [PB for PB in self.normalized_problems  if (self.measure(PB) >= (self.MIN+level-1))]
        if (finalPB):
            print("---- final problems of size >= " + str((self.MIN+level-1)))
            for PB in finalPB:
                print (str(self.reverse_binary_req(PB)))
            print("----")
        print("#total number of problems " + str(len(self.normalized_problems))) # + " / " + str(self.normalized_problems))            
        if (self.Hresult):
            self.check_heuristic()
    # --- enumerate_frontierOK

    # ------------------------
    # Compute initial problems and clean self.binary
    def initial_problems(self):
        I = 0
        while (I < len(self.binary)):
            binreq = self.req_fun(self.binary[I])
            renamed = self.reverse_binary_req_renamed(binreq)
            if (self.check_undefined_request(renamed)):
                if (binreq not in self.init_problems):
                    print(" is a problem " + str(binreq))
                    print("    " + str(renamed))
                    self.init_problems.append(binreq)
                del self.binary[I]
            else:
                I += 1
        # simplification initial problems
        prime(self.init_problems)
        prime(self.binary) 
        # print ("initial problems " + str(self.init_problems))  
        print (" and undefined are " + str(len(self.binary)) + " / " + str(self.binary))     
    # --- initial_problems
    
    # ---------------------
    # final cleaning: remove unsat and move initil problems
    def final_clean(self, level, newpbs):
        # remove unsat cases
        I = 0
        while (I < len(newpbs)):
            pb = newpbs[I]
            renamed = self.reverse_binary_req_renamed(pb)
            if (self.check_unsat_request(renamed)):
                del newpbs[I]
            else:
                I += 1
        # --- 
        # add as problems and simplify
        self.normalized_problems.extend(newpbs)
        # prime simplification
        prime(self.normalized_problems)
        # display the new ones found at this level
        self.display_problems(level)
    # --- final_clean
    
    # ------------------
    # translate a binary REQ into a Z3BoolRef
    # return a Z3BoolRef
    # self.REQ contains the definitions keys
    def reverse_binary_req_renamed(self, binary):
        nbreq = len(self.REQ)
        z3term = []
        for i in range(nbreq):
            if (binary[i] == 1):
                z3term.append(self.REQ[i])
            elif (binary[i] == 0):
                z3term.append(Not(self.REQ[i]))
        # ---
        if (len(z3term) == 1):
            return z3term[0]
        else:
            return And(*z3term)
    # --- reverse_binary_req   
    
    # ------------------
    # translate a binary REQ into a Z3BoolRef
    # return a List[Z3BoolRef]
    # self.REQ contains the definitions keys
    def reverse_binary_req(self, binary):
        keys = self.REQ
        z3term = []
        for key in keys:
            if (binary[keys.index(key)] == 1):
                z3term.append(self.definitions[key])
            elif (binary[keys.index(key)] == 0):
                z3term.append(Not(self.definitions[key]))
        # ---
        if (len(z3term) == 1):
            return z3term[0]
        else:
            return And(*z3term)
    # --- reverse_binary

    # ------------------------ 
    # check that problems are really undefined 
    def check_problems(self, size):
        self.solver.reset()
        self.solver.add(ForAll(self.variables, self.toBoolRef(self.rules, size)))
        for binary in self.normalized_problems:
            self.solver.push()
            pb = self.reverse_binary_req(binary)
            self.solver.add(Exists(self.variables, pb))
            res = self.solver.check()
            # There are unknown
            if (res == unknown):
                print ("unknwon for " + str(pb))
            elif (res == sat):
                print("error ??? " + str(pb))
            else:
                print("Yes it is " + str(pb))
            self.solver.pop()
    # --- check_problems
    
    # ====================== compare the problems
    
    # ----------------------
    # Check equivalence of the two set of problems
    # Enumerate and Normalized_OK
    # self.problems <=> self.normalized_problems
    # size of rule system and predicates for REQ
    def compare_problems(self, lreq, size):
        # from enumerate (transfert to enumerate)
        self.start = process_time()
        print ("------------ compute with enumerate algorithm")
        aux = Enumerate()
        aux.rules = self.rules
        aux.variables = self.variables
        aux.compute_table(lreq, size)
        #print ("problems " + str([aux.rewrite(X) for X in aux.problems]))
        pb = Exists(aux.variables, Or(*[aux.rewrite(X) for X in aux.problems]))
        print ("enumerate: found= " + str(len(aux.problems)) + " in " + str(floor(process_time()-self.start)))
        print ("------------ compute with combine algorithm")
        self.start = process_time()
        #print ("pb= " + str(pb))
        # from OK
        self.compute_table(lreq, size) 
        print ("combine: found= " + str(len(self.normalized_problems)) + " in " + str(floor(process_time()-self.start)))
        # frontier problems
        pb_OK = Exists(self.variables,  Or(*[self.reverse_binary_req(X) for X in self.normalized_problems]))
        #print ("pb_OK " + str(pb_OK))
        # one way
        self.solver.reset()  
        self.solver.add(pb)
        self.solver.add(Not(pb_OK))
        print (" => is " + str(self.solver.check().__eq__(unsat)))  
        # other way
        self.solver.reset()  
        self.solver.add(Not(pb))
        self.solver.add(pb_OK)
        print (" <= is " + str(self.solver.check().__eq__(unsat)))        
    # --- compare_problems
    
    # ----------------------
    # Check equivalence of the two set of problems
    # self.Hresult <=> self.normalized_problems
    def check_heuristic(self):
        print("Check heuristic ---- ")
        # heuristic problems
        pb = Exists(self.variables,  Or(*[self.reverse_binary_req(X) for X in self.Hresult]))
        #print ("pb " + str(pb))
        # frontier problems
        pb_OK = Exists(self.variables,  Or(*[self.reverse_binary_req(X) for X in self.normalized_problems]))
        #print ("pb_OK " + str(pb_OK))
        # one way
        self.solver.reset()  
        self.solver.add(pb)
        self.solver.add(Not(pb_OK))
        print (" => is " + str(self.solver.check().__eq__(unsat)))  
        # other way
        self.solver.reset()  
        self.solver.add(Not(pb))
        self.solver.add(pb_OK)
        print (" <= is " + str(self.solver.check().__eq__(unsat)))        
    # --- check_heuristic
        
    # ------------------------
    # check that all problems are captured 
    # return True if all are there
    def all_problems(self, size):
        self.solver.reset()
        self.solver.add(Exists(self.variables, Not(self.toBoolRef(self.rules, size))))
        for binary in self.normalized_problems:
            pb = Not(self.reverse_binary_req(binary))
            self.solver.add(ForAll(self.variables, pb))
        # --- end for
        res = self.solver.check()
        # There are unknown
        if (res == unknown):
            print ("unknwon thus I don't know")
        elif (res == sat):
            print("some problems are not captured ! ")
        else:
            print("all problems captured ! ")
    # --- all_problems
    
# --- end Normalized_OK