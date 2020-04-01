# ------------------
# 1/4/2020
# Look for problems (correct requests which are undefined)
# Check is already a problem and if already seen
# Finally check if it is a problem add it 
# With check_unsat and minimizing at each level 
## change heuristic: no new problem by combining
# compute self.MIN as the  minimum measure for allreq
# separate init_problems but add them as problems
# add display for size presentation
# add sort allred
# -------------------
### stop at heuristic

### TODO Try to use BDD 

from pyeda.inter import bddvars, BinaryDecisionDiagram, bdd2expr
#from functools import reduce 
#from pyeda.boolalg.bdd import BDDNODEONE, BDDNODEZERO # may be not
#from pyeda.boolalg.bdd import  * #@UnusedWildImport
from Normalized_OK import  * #@UnusedWildImport

# --------------------------
# Class for Iterative_hashing method 
# Process the stored rules and classify them
class Normalized_BDD(Normalized_Enumerate):
    
    # --------------------
    # init constructor 
    def __init__(self):
        super().__init__()
        #### for BDD variables
        self.VARS = [] 
    # --- end init

    # -------------------
    # To provide some numeric data
    def get_info(self):
        res = super().get_info() 
        res += "number of problems " + str(len(self.normalized_problems)) + "\n"
        res += "number of unsafe problems " + str(len(self.unsafe_problems)) + "\n"
        return res 
    # --- end get_info
    
    # --------------------
    # show problems from all_normalized_unsafe
    # TODO BDD here bdd2expr(bdd, conj=False) neither prime neither minimal ?
    # At least using satisfy_all() and minimizing could do that
    def show_problems(self):
        print (" ----------------- The current problems  ")  
        print(str(bdd2expr(self.normalized_problems, False))) 
        print (" ----")
    # --- show_problems
    
    # --------------------
    # show problems from all_normalized_unsafe
    # TODO là aussi peut changer qq chose but How
    def display_problems(self, level):
        PBs = [self.reverse_binary_req(pb) for pb in self.normalized_problems if (len(defined(pb)) == self.MIN + level -1)]
        if (PBs):
            print ("Found " + str(len(PBs)) + " problems of size " + str(self.MIN + level -1) + " time= " + str(floor(process_time()-self.start)))
            for pb in PBs:
                print(str(pb))
            print (" ----")
    # --- display_problems

    #------------------
    # compute table with frontier enumeration
    # lreq is a List[ahead predicate]  
    # allowed : List[Binary:REQ] space for REQ variables   
    #  and check request syntax
    def compute_table(self, lreq, size, allowed):
        self.init_table(size)
        # compute REQ and REQB
        self.set_REQ(lreq)
        # only with REQ
        self.VARS = bddvars('VARS', len(self.REQ))
        self.compute_unsafe_problems() 
        #print(str(self.get_info()))
        self.enumerate(allowed)     # TACTIC + combine allreq breadth_frist
    # --- end compute_table

    #---------------------
    # new enumeration method from TACTIC
    # combine reduction to :REQ BREADTH-FIRST
    # and use is_included_in to check already a problem
    # and allseen list
    # allowed : List[Binary:REQ] space for REQ variables   
    # TODO review init is it useful to BDD ?
    # TODO sans heuristic pour voir
    def enumerate(self, allowed):
        # TODO compute BDD
        allowedBDD = self.convert_or(allowed) # TODO
        #print(str(allowedBDD.to_dot()))
        self.allowed = allowed ### TODO change later 
        NBREQ = len(self.REQ)
        print("definitions " + str(self.definitions))
        # display REQ and its position in Binary:REQ
        print("Ordering REQ " + str([self.definitions[D] for D in self.REQ]))
        # --- tactic and binary conversion 
        self.tactic_conversion()
        #print ("real " + str(self.reverse_list_binary(self.binary)))
        # check for if binary/REQ is a problem and store it 
        # and remove the corresponding undefined   
        self.initial_problems()     
        # --- reductions
        allred = self.sort_reductions(NBREQ)
        print ("MIN= " + str(self.MIN))
        # set init as problems and display minimal ones
        # self.normalized_problems = self.init_problems
        self.normalized_problems = self.convert_or(self.init_problems) # TODO BDD
        #self.display_problems(1)     ## TODO pb here binary versus BDD ?
        # -------
        # TODO convert allred into BDD
        allredBDD = [self.convert2BDD(B) for B in allred]
        self.allowed = allowedBDD
        #print(self.pack([B.to_dot() for B in allredBDD]))
        # compute all combinations of reduction to :REQ
        elements = [] # last index of combined element
        size = len(allredBDD) # TODO
        elements.extend(range(size))
        combinations = allredBDD # TODO
        # store the sat enumerated requests
        allseen = [] # to avoid side-effect
        allseen.extend(allredBDD) # TODO
        prev = 1 ### speed feeling
        level = 2 # number of conjunctions
        # compute all combinations of reductions
        heuristic = False
        # stop at heuristic
        #while (combinations and not heuristic):
        while (combinations): # total 
            print (">>>>> starting level= " + str(level) + " size= " + str(len(combinations)) + " #allseen= " + str(len(allseen)))
            if (prev > 0):
                print(" vitesse " + str(len(combinations)/prev))
            # combine each in combinations with elements in allred 
            # and avoiding duplications
            I = 0
            newcombi = []
            newelts = []
            #newpbs = []
            while (I < len(combinations)):
                other = combinations[I]
                last = elements[I]
                ### enumerate the combination not already tested
                for J in range(last+1, size):
                    binreq = allredBDD[J]  # TODO
                    # compute AND return base and if maximal combination
                    commonBDD = other.__and__(binreq)
                    print(" other= " + str(self.bdd2renamed(other)))
                    print(" binreq= " + str(self.bdd2renamed(binreq)))
                    # TODO show both 
                    maxiBDD = len(commonBDD.inputs)
                    renamedBDD = self.bdd2renamed(commonBDD) # TODO remove later   
                    print(" common= " + str(renamedBDD))
                    # check if already seen   
                    if ((not commonBDD.is_zero()) and (commonBDD not in allseen)): 
                        # check if  denied and put in already seen 
                        print("not seen ! allowed ? " + str(not commonBDD.__and__(self.allowed).is_zero()))                  
                        if (not commonBDD.__and__(self.allowed).is_zero()): # TODO
                            # check if common is included in problems 
                            print("not included ? " + str(not commonBDD.__and__(self.normalized_problems.__invert__()).is_zero()))
                            if (not commonBDD.__and__(self.normalized_problems.__invert__()).is_zero()):
                                #renamedBDD = self.bdd2renamed(commonBDD) # TODO 
                                if (self.check_undefined_request(renamedBDD)): # TODO 
                                    # TODO will be BDD sans heuristic
                                    print("found problem: " + str(renamedBDD))
                                    self.normalized_problems.__or__(commonBDD)
                                elif (maxiBDD):  # only defined not need to continue 
                                    allseen.append(commonBDD)   # TODO  
                                elif (J == size-1):  
                                    allseen.append(commonBDD)  # TODO                         
                                else: # store non defined requests to keep for the new level
                                    newcombi.append(commonBDD)   # TODO
                                    newelts.append(J)
                                    allseen.append(commonBDD)  # TODO
                                # --- checking  undefinedness
                            # --- already a problem 
                            else:
                                allseen.append(commonBDD)   # TODO
                        # --- allowed
                    # --- allseen   
                # --- for J in allred  
                I += 1
            # --- end of one level
            # transfer and compute new level 
            prev = len(combinations)
            combinations = newcombi
            elements = newelts
            #self.final_clean(level, newpbs) # TODO BDD
            ### heuristic no new problem old test
            #if (not newpbs) and (not self.Hresult) and self.normalized_problems
            #print("measures " + str(measure(self.Hresult)) + " =?= " + str(measure(self.normalized_problems)))
            #print("length " + str(len(self.Hresult)) + " =?= " + str(len(self.normalized_problems)))
#             if (len(self.Hresult) == len(self.normalized_problems)): # compute heuristic
#                 heuristic = True
#                 print ("Heuristic says sufficient level is " + str(level))
#                 #self.Hresult = self.normalized_problems 
            print("end #level= " + str(level) +  " time = " + str(floor(process_time()-self.start)))
            print()                         
            level += 1
        # --- end while combinations
        print("checking checking= " + str(self.checking) + " allseen " + str(len(allseen)))
#         # final problems 
#         finalPB = [PB for PB in self.normalized_problems  if (len(defined(PB)) >= (self.MIN+level-1))]
#         if (finalPB):
#             print("---- final problems of size >= " + str((self.MIN+level-1)))
#             for PB in finalPB:
#                 print (str(self.reverse_binary_req(PB)))
#             print("----")
#        print("#total number of problems " + str(len(self.normalized_problems))) 
    # --- enumerate


    # ---------------------
    # final cleaning: remove unsat and move initial problems
    def final_clean(self, level, newpbs): # TODO with BDD ?
        # add as problems and simplify
        self.Hresult = self.normalized_problems.copy() # To store it and check change
        self.normalized_problems.extend(newpbs)
        self.normalized_problems = minimizing(self.normalized_problems)
        # display the new ones found at this level
        self.display_problems(level)
    # --- final_clean

    # ------------------------
    # Compute initial problems and clean self.binary
    def initial_problems(self):
        I = 0
        while (I < len(self.binary)):
            binreq = req_reduce(self.binary[I], self.REQB)
            # eliminate -1*
            if (sum(binreq) != -len(binreq)):
                # check if req intersect allowed
                if (product([binreq], self.allowed)):
                    renamed = self.reverse_binary_req_renamed(binreq)
                    if (self.check_undefined_request(renamed)):
                        if (binreq not in self.init_problems):
                            #print(" is a problem " + str(binreq))
                            print("    " + str(self.rewrite(renamed)))
                            self.init_problems.append(binreq)
                        del self.binary[I]
                    else:
                        I += 1
                    # --- undefinedness
                else:
                    I += 1
                # --- denied
            else:
                I += 1
            # --- != -1*
        # simplification initial problems
        self.init_problems = minimizing(self.init_problems)
        #self.binary = minimizing(self.binary) #  deactivate it 
        print (" found initial problems " + str(len(self.init_problems)))
        print (" and undefined are " + str(len(self.binary)) + " / " + str(self.binary))     
    # --- initial_problems
    
    ### ============== new for BDD
    
    # ---------------    
    # conversion of a Binary into BDD
    # return a BDD
    def convert2BDD(self, binary):
        tmp = BinaryDecisionDiagram.box(1)
        for I in range(len(binary)):
            if (binary[I] == 0):
                tmp = self.VARS[I].__invert__().__and__(tmp)
            elif   (binary[I] == 1):
                tmp = self.VARS[I].__and__(tmp)
        #print(str(tmp.to_dot()))   
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
                #tmp = tmp | self.convert2BDD(binary)
                tmp = self.convert2BDD(binary).__or__(tmp) ### passe ?
                #tmp = reduce(lambda a,b: a.__or__(b), [tmp, self.convert2BDD(binary)])
        else:
            #tmp = BDDNODEZERO
            tmp = BinaryDecisionDiagram.box(0)
        #print(str(tmp.to_dot()))  
        return tmp     
    # ---
    
    # ---------------  
    # Convert a bdd into a renamed Z3 expression
    # bdd is a BDD for an AND-term
    # return a Z3 renamed expression
    # TODO PB indices ?
    def bdd2renamed(self, bdd):
        path = bdd.satisfy_one() # only one in fact
        print("path= " + str(path))
        # we have only one dimension vars
        return And(*[self.REQ[V.indices[0]] if (W == 1) else Not(self.REQ[V.indices[0]])
                     for (V, W) in path.items()])
    # --- bdd2renamed
    
    # ====================== utils for dot files
    
    #-------------
    # packs several "graph BDD" in a graph with subgraph
    # add also labels
    # dots: List[dot string]
    def pack(self, dots):
        res = "graph BDD_all {\n"
        for I in range(len(dots)):
            res += "subgraph cluster_" + str(I) + " { label= \"subgraph #" + str(I) + "\";\n" + dots[I][11:] + "\n"
        res += "\n}\n"
        return res
    # --- pack
# --- end Normalized_BDD
