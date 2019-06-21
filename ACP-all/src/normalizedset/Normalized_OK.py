# ------------------
# 21/6/2019
# Look for problems in undefined 
# Check is already a problem and if already seen
# Finally check if it is a problem add it 
# With check_unsat and prime at each level
# -------------------

from NormalizedSet import  * #@UnusedWildImport
from prime import * #@UnusedWildImport
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
        # to store binary from tactic
        self.binary = []    
        # reduce a Binary to a Binary:REQ 
        self.req_fun = lambda X: [X[I] for I in range(len(self.REQB)) if (self.REQB[I] == 1)]     
        # to count call to check
        self.count = 0
        # to measure time
        self.start = 0
        # to measure defined bit in a Binary
        self.measure = lambda X: sum([1 for I in X if (I != -1)])     
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
        #print (" ----------------- problems  ")   
        for binary in self.normalized_problems:
                print(str(self.reverse_binary_req(binary)))
        print ("\n")
    # --- show_problems

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
        self.enumerate_frontierOK()     # tactic + combine allreq breadth_frist
    # --- end compute_table

    #---------------------
    # new enumeration method from tactic
    # combine reduction to :REQ (similar to Negative) BREADTH-FIRST
    # and use is_included_in to check already a problem
    # and allseen list
    def enumerate_frontierOK(self):
        NBREQ = len(self.REQ)
        print("definitions " + str(self.definitions))
        # tactic applied to all renamed 
        aux = tactic(Not(And(*[X.toBoolRef() for X in self.renamed])))
        aux = [list(X) for X in aux] # !!! Goals
        # conversion to binary
        for andlist in aux:
            #print (str(andlist))
            self.binary.append(self.convert_binary(andlist))  
        prime(self.binary) 
        print ("compute_problems from " + str(len(self.binary)) + " / " + str(self.binary))
        #print ("en clair " + str(self.reverse_list_binary(self.binary)))
        # check for if binary/REQ is a problem and store it 
        # and remove the corresponding undefined   
        self.initial_problems()          
        # compute all remaining reductions
        allreq = []
        for binary in self.binary:
            red = self.req_fun(binary)
            if ((red not in allreq)  and (sum(red) > -NBREQ)):
                #print(str(red))
                allreq.append(red)
        print ("allreq= " + str(len(allreq))) # + " / " + str(allreq))
        # compute all combinations of reduction to :REQ
        elements = [] # last index of combined element
        size = len(allreq)
        elements.extend(range(size))
        combinations = allreq
        # store the sat enumerated requests
        allseen = [] # to avoid side-effect
        allseen.extend(allreq)
        prev = 1 ### speed feeling
        level = 2 # number of conjunctions
        # compute all combinations of reductions
        while (combinations):
            print ("level= " + str(level) + " size= " + str(len(combinations)) + " allseen= " + str(len(allseen)) + 
                   " vitesse " + str(len(combinations)/prev) + " time = " + str(floor(process_time()-self.start)))         
            #print (" combinations= " + str(combinations))   
            # combine each in combinations with elements in allreq 
            # and avoiding duplications
            I = 0
            newcombi = []
            newelts = []
            while (I < len(combinations)):
                other = combinations[I]
                last = elements[I]
                ### enumerate the combination not already tested
                for J in range(last+1, size):
                    binreq = allreq[J]  
                    # compute AND return common and if maximal combination
                    common, maxi = make_common(other, binreq)
                    #print ("other " + str(other) + " binreq= " + str(binreq) + " common " + str(common) + " J= " + str(J))
                    # check if already seen   
                    if (common and (common not in allseen)):
                        #print (str(common) + " inclusion in PBs? " +  str(any([is_included_in(common, X) for X in self.normalized_problems])))  
                        # check if common is included in problems
                        if (all([not is_included_in(common, X) for X in self.normalized_problems])):
                            renamed = self.reverse_binary_req_renamed(common)
                            if (self.check_undefined_request(renamed)):
                                #print ("problem " + str(common))
                                self.normalized_problems.append(common)
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
                # --- for J in allreq  
                I += 1
            # --- end of one level
            # transfer and compute new level 
            prev = len(combinations)
            combinations = newcombi
            elements = newelts
            self.final_clean()
            level += 1
        # --- combinations
        print("checking count= " + str(self.count) + " allseen " + str(len(allseen)))
        print("#final set of problems " + str(len(self.normalized_problems))) # + " / " + str(self.normalized_problems))
    # --- enumerate_frontierOK

    # ------------------------
    # Compute initial problems and clean self.binary
    def initial_problems(self):
        I = 0
        while (I < len(self.binary)):
            binreq = self.req_fun(self.binary[I])
            renamed = self.reverse_binary_req_renamed(binreq)
            if (self.check_undefined_request(renamed)):
                #print(" is a problem " + str(binary) + str(renamed))
                self.normalized_problems.append(binreq)
                del self.binary[I]
            else:
                I += 1
        # simplification
        prime(self.normalized_problems)
        prime(self.binary) 
        print ("initial problems " + str(self.normalized_problems))        
        self.show_problems()     
        print (" and undefined are " + str(len(self.binary)) + " / " + str(self.binary))          
    # --- initial_problems
    
    # ---------------------
    # final cleaning: remove unsat and simplify with prime
    def final_clean(self):
        # remove unsat cases
        I = 0
        while (I < len(self.normalized_problems)):
            pb = self.normalized_problems[I]
            renamed = self.reverse_binary_req_renamed(pb)
            if (self.check_unsat_request(renamed)):
                #print ("is unsat " + str(pb))
                del self.normalized_problems[I]
            else:
                I += 1
        # --- 
        #print("\n Problems at the level: " + str(level) + "\n")
        #print("#problems BEFORE prime " + str(len(self.normalized_problems))) 
        prime(self.normalized_problems) 
        print("#problems here " + str(len(self.normalized_problems)))
        #self.show_problems()
    # --- 

    # ------------------from Negative
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
    
#     # TODO define a basic one with reset + R + etc 
#     def check_undefined_request(self, renamed):
#         self.solver.reset()
#         print ("size= ? " + str(len(self.stored)))
#         self.solver.add(ForAll(self.variables, self.toBoolRef(self.rules, size)))
#         Exists(self.variables, self.rewrite())
#         pb = self.reverse_binary_req(renamed)
#         self.solver.add(Exists(self.variables, pb))
#         res = self.solver.check()
#         # There are unknown
#         if (res == unknown):
#             print ("unknwon for " + str(pb))
#         return (res == unsat)
    # ---
    # -------------------- TODO move to renaming
    # Check if !*store & ~?request is unsat
    # renamed is a renamed z3 term
    # solver_renamed contains definitions and renamed rules
    # return True if undefined
    def check_undefined_request(self, renamed):
        #print ("check_undefined_request " + str(renamed))
        self.count += 1 
        self.solver_renamed.push()
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

    # ------------------from Negative
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

    # -------------------move to renaming
    # check unsat of original request
    # use a local solver and return True/False
    # return True if unsat
    def check_unsat_request(self, renamed):
        self.local_solver.reset()
        self.local_solver.add(built_quantified(self.rewrite(renamed), self.variables, False))
        res = self.local_solver.check()
        if (res == unknown):
            print ("check unsat request unknown: " + str(self.rewrite(renamed)))        
        return res == unsat        
    # --- check_unsat_request
        
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
            elif (res != unsat):
                print("error ??? " + str(pb))
            self.solver.pop()
    # --- check_problems
    
    # ====================== compare the problems
    
    # ----------------------
    # Check equivalence of the two set of problems
    # Enumerate and Normalized_OK
    # self.problems <=> self.normalized_problems
    # size of rule system and predicates for REQ
    ### TODO pb side-effects ?
    def compare_problems(self, size, lreq):
        # TODO from enumerate (transfert to enumerate)
        print ("------------ compute with enumerate algorithm")
        aux = Enumerate()
        #for X in self.variables:
        aux.rules = self.rules
        aux.variables = self.variables
        aux.compute_table(size, lreq)
        #print ("problems " + str([aux.rewrite(X) for X in aux.problems]))
        pb = Exists(aux.variables, Or(*[aux.rewrite(X) for X in aux.problems]))
        #print ("pb= " + str(pb))
        # from OK
        print ("------------ compute with combine algorithm")
        self.compute_table(lreq, size) # order
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
    
# --- end Normalized_OK