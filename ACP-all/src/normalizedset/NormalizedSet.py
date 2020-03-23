# ------------------
# 4/2/2020
# Class for normalized rule system
# That is renamed rules are transformed into a set of AND => OR
# using some basic tactics from Z3 and a binary conversion to List[1/0/-1]=Binary
# -------------------

# TODO optim binary computation with bit array ?

from Renaming import * #@UnusedWildImport
from BinaryRule import * #@UnusedWildImport

# ---------------------
class NormalizedSet(Renaming):
    
    def __init__(self):
        Renaming.__init__(self)
        self.normalized_store = []
    # --- end init
    
    # --------------------
    def __str__(self):
        result = super().__str__()
        result += " =================== normalizedset ================ \n"     
        result += " ----------- store \n"
        for X in self.normalized_store:
            result += str(X) + "\n"
        return result
    # --- end str

    # -------------------
    # To provide some numeric data
    def get_info(self):
        result = super().get_info()
        result += " #normalized store " + str(len(self.normalized_store)) + "\n"
        return result
    # --- end get_info
        
    # -----------------------------
    # Normalize all the rules
    def normalize(self):
        # self.normalize_unsafes() TODO ya pas
        self.normalized_stored()
    # --- end of normalize
    
    # -----------------------------
    # Normalize the stored rules 
    # simple brute solution costly and management of subexpressions ?    
    def normalized_stored(self):
        for rule in  self.renamed:
            cond = rule.get_cond()
            conc = rule.get_conc()
            # case False => OR:Binary==[]
            if (conc == False):
                cnf = [False]
            else:
                cnf = CNF(conc)[0]
            dnf = DNF(cond) # ApplyResult instances    list of AND-terms:Goal            
            #print ("DNF " + str(dnf) )                    
            #print ("CNF " + str(cnf) )
            # distribute and create the normalized rules
            for Di in dnf:
                binarycond = self.convert_binary(get_list(Di))
                #print("cond: " + str(binarycond))
                for Ci in cnf:
                    #print ("normalize " + str(get_list(Di)) + " " + str(Ci))
                    if (Ci == False):
                        binaryconc = []
                    elif (isinstance(Ci, BoolRef)):
                        binaryconc = self.convert_binary([Ci])
                        if (Ci.decl().kind()  == Z3_OP_OR):
                            binaryconc = self.convert_binary(Ci.children())
                    #print("conc: " + str(binaryconc))
                    self.normalized_store.append(BinaryRule(binarycond, binaryconc))
            # --- end for Di
        # --- end for i
    # --- end of normalized_stored
    
    ##### ================================= Binary transformations 
    
    # ------------------
    # convert a List[Z3prop] into a Binary index reference is self.definitions.keys()
    # return a Binary 
    def convert_binary(self, andlist):
        #print ("convert_binary for " + str(andlist))
        res = [-1]*len(self.definitions)
        keys = list(self.definitions.keys())
        if (not isinstance(andlist, list)): # to change single term
            andlist = [andlist]
        for z3term in andlist:
            #print("convert_binary z3term " + str(type(z3term)))
            # it is Not() or a proposition
            if (is_expr(z3term) and (z3term.decl().kind() == Z3_OP_NOT)): 
                prop = z3term.children()[0]
                #print("convert_binary Not= " + str(prop))
                binary = 0
            else:
                prop = z3term
                binary = 1
            if (prop in keys):
                res[keys.index(prop)] = binary
        # ---
        return res
    # --- convert_binary    
    
    # ------------------
    # translate a binary into a Z3BoolRef
    # flag=True AND else OR    
    # return a Z3BoolRef
    def reverse_binary(self, binary, flag):
        if (binary):
            keys = list(self.definitions.keys())
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
                if (flag):
                    return And(*z3term)
                else:
                    return Or(*z3term)
        else:
            return False
    # --- reverse_binary    
    
    # ------------------
    # translate a binary into a renamed Z3
    # flag=True AND else OR
    # return a List[Z3BoolRef]
    def reverse_renamed(self, binary, flag):
        if (binary):
            keys = list(self.definitions.keys())
            z3term = []
            for key in keys:
                if (binary[keys.index(key)] == 1):
                    z3term.append(self.propositions[self.definitions[key]])
                elif (binary[keys.index(key)] == 0):
                    z3term.append(Not(self.propositions[self.definitions[key]]))
            # ---
            if (len(z3term) == 1):
                return z3term[0]
            else:
                if (flag):
                    return And(*z3term)
                else:
                    return Or(*z3term)
        else:
            return False
    # --- reverse_binary    
    
    # --------------------
    # andterm is a Binary
    # compute its negation
    # return a dnf:List[Binary]
    def negation_binary(self, andterm):
        size = len(andterm)
        res = []
        for i in range(len(andterm)):
            bit = andterm[i]
            if (bit == 1):
                term = [-1]*size
                term[i] = 0
                res.append(term)
            elif (bit == 0):
                term = [-1]*size
                term[i] = 1
                res.append(term)
        return res
    # --- negation_binary

    # --------------------
    # compute the DNF of left and Not(right)
    # left:Binary right:Binary:REQ
    # return a DNF:List[Binary]
    def compose_pos_neg(self, left, right):
        size = len(left)
        res = []
        indice = 0 # for right Binary:REQ 
        for I in range(size):
            lbit = left[I]
            # right is REQ
            if (self.REQB[I] == 0):
                rbit = -1
            else:
                rbit = right[indice]
                indice += 1
            #print (str(lbit) + " " + str(rbit))
            if (rbit != -1):
                if (rbit != lbit):
                    if (lbit == -1):
                        term = left.copy() 
                        term[I] = 1 if (rbit == 0) else 0
                        res.append(term)
                    else:
                        return [left]
                # else opposite nothing to add
        return res
    # --- compose_pos_neg

    # --------------------
    # conc is a Binary representing an OR term
    # compute its DNF
    # return a dnf:List[Binary]
    def binary_dnf(self, conc):
        size = len(conc)
        res = []
        for i in range(len(conc)):
            bit = conc[i]
            if (bit == 1):
                term = [-1]*size
                term[i] = 1
                res.append(term)
            elif (bit == 0):
                term = [-1]*size
                term[i] = 0
                res.append(term)
        return res
    # --- binary_dnf
    
    # ------------------TODO shared with Negative ?
    # check a binary problem against REQ
    # that is REQB bits in binary are -1
    def check_binary_problem(self, binary):
        pb = all([binary[X] == -1 for X in range(self.counter) if (self.REQB[X] == 0)])
        #print("check_binary_problem " + str(binary) + " ? " + str(pb))
        return pb
    # --- check_binary_problem  
    
    # ------------------ TODO from Negative
    # translate Binary into Z3BoolRef
    # lbinary:List[Binary] 
    # return a List[Z3BoolRef]
    def reverse_list_binary(self, lbinary):
        res = []
        keys = list(self.definitions.keys())
        for binary in lbinary:
            z3term = []
            for key in keys:
                if (binary[keys.index(key)] == 1):
                    z3term.append(self.definitions[key])
                elif (binary[keys.index(key)] == 0):
                    z3term.append(Not(self.definitions[key]))
            # ---
            if (len(z3term) == 1):
                res.append(z3term[0])
            else:
                res.append(And(*z3term))
        # ---
        return res
    # --- reverse_list_binary
    
    # ----------------------
    # left, right two List[Binary] representing DNFs
    # they are simplified 
    # compute the product and simplify
    def compose_2_dnf(self, left, right):
        if (left == []):
            return right
        elif (right == []):
            return left
        elif (len(left) == 1):
            return self.compose_binary_dnf(left[0], right)
        else:
            res = self.compose_binary_dnf(left[0], right)
            for binary in left[1:]:
                res.extend(self.compose_binary_dnf(binary, right))
                prime(res)
            # ---
            return res
    # --- compose_2_dnf
    
    # ----------------------
    # left:Binary 
    # right:Binary same size
    # AND of two OR Binary and simplify 
    # and produce [] or AND:Binary or CNF:List[Binary] 
    def compose_2OR_binary(self, left, right):
        #print ("compose_2OR_binary " + str(left) + " " + str(right))
        if (left and right):
            aux_len = lambda X: len([Y for Y in X if (Y != -1)])
            ll = aux_len(left)
            lr = aux_len(right)
            if (ll > lr): # swith to get min at left
                tmp = left 
                left = right 
                right = tmp
            aux = right.copy()
            if (left == right):
                return [left]
            else:
                size = len(left)
                for i in range(size):
                    bitl = left[i]            
                    if (bitl != -1):
                        bitr = right[i]
                        if (bitr != bitl):
                            aux[i] = -1
                # --- end for
                if (sum(aux) == -1*size): # that is False
                    return []
                else:
                    return [left, aux]
        else: # one is False==[]
            return []
    # --- compose_2OR_binary
        
    # ----------------------
    # left:Binary not empty
    # right:List[Binary] representing DNF
    # they are simplified 
    # compute the product and simplify
    def compose_binary_dnf(self, left, right):
        res = []
        for binary in right:
            common = make_common(left, binary)[0]
            if (common):
                res.append(common)
        # --- end for
        return prime(res)
    # --- compose_binary_dnf
    
    # -------------------
    # convert a binary rule into a DNF
    def convert_rule_DNF(self, brule):
        #Binary rule is ANDlist => ORlist
        res = self.negation_binary(Rule.get_cond(brule))
        conc = Rule.get_conc(brule)
        #print ("conc " +str(conc))
        if (conc):
            for I in range(self.counter):
                if (conc[I] != -1):
                    tmp = [-1]*self.counter
                    tmp[I] = conc[I]
                    res.append(tmp)
            # --- 
        return res
    # --- convert_rule_DNF
        
# --- end NormalizedSet