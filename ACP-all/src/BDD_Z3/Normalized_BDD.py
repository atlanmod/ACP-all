# ------------------
# 2/4/2020
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
### without heuristic

### TODO Try to use BDD 
### TODO simplify is different and also remove final unsat or defined allowed

from pyeda.inter import bddvars, BinaryDecisionDiagram, bdd2expr, Variable, espresso_exprs
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

    # --------------------
    # show problems with prime implicants 
    # At least using satisfy_all() and minimizing could do that
    def show_problems(self):
        print (" ----------------- The current problems [not simplified] ")  
        #print(str(bdd2expr(self.normalized_problems, False))) 
        # TODO case 1
        res = []
        if (not self.normalized_problems.is_zero()):
            ### with prime implicants
            #renameds = bdd2expr(self.normalized_problems, False).complete_sum().xs
            # espresso produces several simplifications
            start = process_time()
            renameds = espresso_exprs(bdd2expr(self.normalized_problems, False))[0].xs
            print ("espresso time= " + str(floor(process_time()-start)))
            ## ATTENTION pyeda expr <class 'pyeda.boolalg.expr.OrOp'>
            #print(str(renameds))
            for renamed in renameds:
                tmp = And(*[self.REQ[N.indices[0]] if (isinstance(N, Variable)) 
                                 else Not(self.REQ[N.__invert__().indices[0]])
                                 for N in renamed.xs])
                tmp = self.rewrite(tmp)
                print(str(tmp))     
                res.append(tmp)  
        #print(str(res))     
        print (" ----" + str(len(res)))
        return res
    # --- show_problems

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
    def enumerate(self, allowed):
        # compute BDD for allowed
        allowedBDD = self.convert_or(allowed) 
        #print(str(allowedBDD.to_dot()))
        self.allowed = allowed ### change later 
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
        # set init as problems a BDD
        self.normalized_problems = self.convert_or(self.init_problems) 
        #self.display_problems(1)     ## TODO pb here binary versus BDD ?
        # -------
        # convert allred into BDD
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
        allseen.extend(allredBDD) 
        prev = 1 ### speed feeling
        level = 2 # number of conjunctions
        # compute all combinations of reductions
        while (combinations): # total 
            print (">>>>> starting level= " + str(level) + " size= " + str(len(combinations)) + " #allseen= " + str(len(allseen)))
            if (prev > 0):
                print(" vitesse " + str(len(combinations)/prev))
            # combine each in combinations with elements in allred 
            # and avoiding duplications
            I = 0
            newcombi = []
            newelts = []
            while (I < len(combinations)):
                other = combinations[I]
                last = elements[I]
                ### enumerate the combination not already tested
                for J in range(last+1, size):
                    binreq = allredBDD[J] 
                    # compute AND return base and if maximal combination
                    commonBDD = other.__and__(binreq)
                    #print(" other= " + str(self.bdd2renamed(other)))
                    #print(" binreq= " + str(self.bdd2renamed(binreq)))
                    maxiBDD = len(commonBDD.inputs)
                    #print("is zero? " + str(commonBDD.is_zero()))
                    if (not commonBDD.is_zero()): 
                        renamedBDD = self.bdd2renamed(commonBDD) # TODO to move later   
                        #print(" common= " + str(renamedBDD))
                        # check if already seen   
                        if (commonBDD not in allseen): 
                            # check if  denied and put in already seen 
                            #print("not seen ! allowed ? " + str(not commonBDD.__and__(self.allowed).is_zero()))                  
                            if (not commonBDD.__and__(self.allowed).is_zero()): 
                                # check if common is included in problems 
                                #print("not included ? " + str(not commonBDD.__and__(self.normalized_problems.__invert__()).is_zero()))
                                if (not commonBDD.__and__(self.normalized_problems.__invert__()).is_zero()):
                                    #renamedBDD = self.bdd2renamed(commonBDD) # TODO 
                                    if (self.check_undefined_request(renamedBDD)): 
                                        print("found problem: " + str(renamedBDD))
                                        self.normalized_problems = self.normalized_problems.__or__(commonBDD)
                                    elif (maxiBDD):  # only defined not need to continue 
                                        allseen.append(commonBDD)    
                                    elif (J == size-1):  
                                        allseen.append(commonBDD)                      
                                    else: # store non defined requests to keep for the new level
                                        newcombi.append(commonBDD)  
                                        newelts.append(J)
                                        allseen.append(commonBDD)  
                                    # --- checking  undefinedness
                                # --- already a problem 
                                else:
                                    allseen.append(commonBDD)   
                            # --- allowed
                        # --- allseen   
                    # --- if common not unsat
                # --- for J in allred  
                I += 1
            # --- end of one level
            # transfer and compute new level 
            prev = len(combinations)
            combinations = newcombi
            elements = newelts
            print("end #level= " + str(level) +  " time = " + str(floor(process_time()-self.start)))
            print()                         
            level += 1
        # --- end while combinations
        print("checking checking= " + str(self.checking) + " allseen " + str(len(allseen)))
    # --- enumerate

#     # ------------------------
#     # Compute initial problems and clean self.binary
#     def initial_problems(self):
#         I = 0
#         while (I < len(self.binary)):
#             binreq = req_reduce(self.binary[I], self.REQB)
#             # eliminate -1*
#             if (sum(binreq) != -len(binreq)):
#                 # check if req intersect allowed
#                 if (product([binreq], self.allowed)):
#                     renamed = self.reverse_binary_req_renamed(binreq)
#                     if (self.check_undefined_request(renamed)):
#                         if (binreq not in self.init_problems):
#                             #print(" is a problem " + str(binreq))
#                             print("    " + str(self.rewrite(renamed)))
#                             self.init_problems.append(binreq)
#                         del self.binary[I]
#                     else:
#                         I += 1
#                     # --- undefinedness
#                 else:
#                     I += 1
#                 # --- denied
#             else:
#                 I += 1
#             # --- != -1*
#         # simplification initial problems
#         self.init_problems = minimizing(self.init_problems)
#         #self.binary = minimizing(self.binary) #  deactivate it 
#         print (" found initial problems " + str(len(self.init_problems)))
#         print (" and undefined are " + str(len(self.binary)) + " / " + str(self.binary))     
#     # --- initial_problems
#     
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
                tmp = self.convert2BDD(binary).__or__(tmp) 
        else:
            tmp = BinaryDecisionDiagram.box(0)
        #print(str(tmp.to_dot()))  
        return tmp     
    # ---
    
    # ---------------  
    # Convert a bdd into a renamed Z3 expression
    # bdd is a BDD for an AND-term
    # return a Z3 renamed expression
    def bdd2renamed(self, bdd):
        path = bdd.satisfy_one() # only one in fact
        #print("path= " + str(path)) # TODO cas None 
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
