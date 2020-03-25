# ------------------------------
# 24/3/2020
# some additional utility functions
#--------------------------

from z3 import * #@UnusedWildImport
from z3.z3util import * #@UnusedWildImport
from PLA import * #@UnusedWildImport

#------------- TACTIC from Z3
SKIP = Tactic('skip')
NNF = Tactic('nnf')
SIMPLIFY = Tactic('simplify')
SPLIT = Tactic('split-clause')
CNF = Tactic('tseitin-cnf')
TACTIC = Then(NNF, SIMPLIFY, Repeat(OrElse(SPLIT, SKIP)), SIMPLIFY) 
DNF = Then(CNF, SIMPLIFY, Repeat(OrElse(Then(SIMPLIFY, SPLIT), SKIP))) 
# to counte the new variables
COUNTER_VARS = 0

# -----------------------
# list of defined bit positions (0,1)
# abin:Binary
def defined(abin):
    return [I for I in range(len(abin)) if (abin[I] != -1)]
# --- defined

# -----------------------
# list of undefined bit positions (== -1)
# abin:Binary
def undefined(abin):
    return [I for I in range(len(abin)) if (abin[I] == -1)]
# --- undefined

# -----------------------
# compute the number of defined bits in a List[Binary]
def measure(lbin):
    return sum([sum([1 for B in BIN if B != -1]) for BIN in lbin])
# --- measure

# -----------------------
# Rename the variables of this expression
# Returns a list of Const() and the new expression
def renaming(Z3exp):
    global COUNTER_VARS
    varss = get_vars(Z3exp)
    newvars = []
    for v in varss:
        newvars.append(Const(v.decl().name() + '_' + str(COUNTER_VARS), v.sort()))
        COUNTER_VARS += 1
    return (newvars, substitute(Z3exp, [(varss[I], newvars[I]) for I in range(len(varss))]))
# --- renaming

# -----------------------
# reduce a (X) Binary:REQB to a Binary:REQ with Y=self.REQB 
# makes a projection of the Binary on correct literals
def req_reduce(X, Y):
    return [X[I] for I in range(len(Y)) if (Y[I] == 1)]   
# --- req_reduce

# -----------------------
# test if a Binary is !REQ or :REQ
# second argument is REQB
# return True if :REQ
def is_REQ(binary, reqb):
    I = 0
    finish = False
    while (I < len(binary) and not finish):
        finish = (reqb[I] == 0) and (binary[I] != -1) 
        I += 1
    return ((I == len(binary)) and not finish)
# --- is_REQ

# -----------------------
# deep equal for two List[Binary] without repetition
def equals(l1, l2):
    if (len(l1) == len(l2)):
        for s1 in l1:
            if (s1 not in l2):
                return False
        return True
    else:
        return False
# --- equals

# -----------------------
# add the needed free variables
# flag = True => ForAll else Exists
# variables the declared free variables
# rename is a renamed expression
# return a z3 renamed expression with a quantifier
def built_quantified(renamed, variables, flag):
    freevars = [] 
    ids = [X.get_id() for X in variables]
    for X in get_vars(renamed):
        #print (" built_quantified " + str(X) + " " + str(variables))
        # attention check type (X in variables)
        # TODO optimize ?
        if (X.get_id() in ids):
            freevars.append(X)
    if (freevars):
        if (flag):
            return ForAll(freevars, renamed)
        else:
            return Exists(freevars, renamed)
    else:
        return renamed
# --- built_quantified

# -----------------------
# look at two Binary to compute index of 
# the new combine included in  toremove
# last is the last index, size the number of Binary to combine
# toremove is included in a new combine 
def compute_index(tocombine, toremove, last, size):
    # test here is toremove[I] == 1 => tocombine[I] == 1
    check = all([((toremove[I] == 0) or (tocombine[I] == 1)) for I in range(last)])
    if (check):
        nb1 = sum(toremove[last+1:size])
        # only one single 1 in toremove
        if (nb1 == 1): 
            return toremove.index(1, last+1) 
        else:
            return -1 # failed
    else:
        return -1 # failed
# --- compute_index

# -----------------
# compare two binary REQ and compute "base" bits
# left, right are two binarys all with same length
# return a base binary REQ or [] if fails
# and maximal indicator
def make_common(left, right):
    #print ("make_common " + str(left) + " / " + str(right))
    size = len(left)
    res = [-1]*size
    i = 0
    finish = False
    maximal = True
    while (i < size) and not finish:
        if (left[i] == right[i]):
            res[i] = left[i] 
            if (res[i] == -1):
                maximal = False
        elif  ((left[i] == -1) or (right[i] == -1)):
            res[i] = -(left[i] * right[i])
        else: # 1!=0
            finish = True
        # --- if 
        i += 1
    #print("make_common= " + str([] if finish else res))
    return (([], False) if finish else (res, maximal))
# --- make_common

# -----------------
# intersection of two binary with the same length
# return either [] or a new list
def make_and(left, right):
    #print ("make_common " + str(left) + " / " + str(right))
    size = len(left)
    res = [-1]*size
    i = 0
    finish = False
    while (i < size) and not finish:
        if (left[i] == right[i]):
            res[i] = left[i] 
        elif  ((left[i] == -1) or (right[i] == -1)):
            res[i] = -(left[i] * right[i])
        else: # 1!=0
            finish = True
        # --- if 
        i += 1
    #print("make_common= " + str([] if finish else res))
    return [] if finish else res
# --- make_and

# -----------------
# Check if all left bits [1/0] are compatible
# with the Binary in right
# return true or false
def compare_bits(left, right):
    return all([(right[I] == -1) or (left[I] == right[I])  for I in range(len(left)) if left[I] != -1])
# --- compare_bits

# -----------------
# Compose using make_and the Binary in the two lists
# return a List[Binary] (intersect) or [] (is in negation)
def product(lefts, rights):
    res = []
    for bleft in lefts:
        for bright in rights:
            tmp = make_and(bleft, bright)
            if (tmp):
                res.append(tmp)
    return res
# --- product

# -------------
# compute base binary of binaries in lbinary
# return a Binary or [] if unsat
def make_all_common(nbreq, lbinary):
    res = []
    I = 0
    finish = False
    while (I < nbreq) and not finish:
        bit = -1
        J = 0
        while (J < len(lbinary)) and not finish:
            bitr = lbinary[J][I]
            if (bitr == 0):
                if (bit == 1):
                    finish = True
                else:
                    bit = 0
            elif (bitr == 1):
                bit = abs(bit)
            J += 1
        # --- while J
        res.append(bit)
        I += 1
    # --- while I 
    return [] if finish else res
# --- make_all_common

# -------------
# compute the number of column 1/0
# return this number
def estimate_1(nbreq, lbinary):
    res = 0
    for I in range(nbreq):
        number_defined = False
        column = 0 # 1 or 0
        for J in range(len(lbinary)):
            bit = lbinary[J][I]
            if (bit != -1):
                if (number_defined): # it was set to
                    if (column != bit):
                        number_defined = False
                else:
                    column = bit
                    number_defined = True
        # --- for J
        if (number_defined):
            res += 1
    # --- for I 
    return res
# --- estimate_1

# ----------------------
# TODO estimate MAX bound of base size
# complete all combinations and forget unsat
# and measure 
# nbreq size of atoms
# lbinaryreq, lasts: combinations and corresponding last index
# allreq: reductions from TACTIC
# return True if no need to continue
def estimate(nbreq, lbinaryreq, lasts, allreq):
    res = 0  # to store current max
    size = len(allreq)
    for K in range(len(lbinaryreq)):
        localmax = 0  # to count local max
        binary = lbinaryreq[K]
        #print ("binary " + str(binary))
        # count bit number_defined for each column
        for I in range(nbreq):
            bitl = binary[I]
            if (bitl != -1):
                number_defined = True
                column = bitl  # 1 or 0                
            else:
                number_defined = False
                column = 0  # default not used
            # ---
            for J in range(lasts[K]+1, size):
                bitr = allreq[J][I]
                if (bitr != -1):
                    if (number_defined):  # it was set to
                        if (column != bitr):
                            number_defined = False
                    else:
                        column = bitr
                        number_defined = True
            # --- for J
            if (number_defined):
                localmax += 1            
        # --- for I
        #print ("localmax " + str(localmax))
        if (localmax > res):
            res = localmax
    # --- for K
    return res    
# --- estimate

# # -----------------
# # combined and check exclusivity of two List[1/0]
# # return the union of the combinations and True if exclusive
# def make_combine(left, right):
#     #print ("make_common " + str(left) + " / " + str(right))
#     size = len(left)
#     res = [0]*size
#     I = 0
#     finish = True
#     while (I < size):
#         if ((left[I] == 1) and (right[I] == 1)):
#             finish = False
#             res[I] = 1
#         elif (left[I] == 0):
#             res[I] = right[I]
#         elif (right[I] == 0):
#             res[I] = left[I]
#         I += 1
#     #print("make_common= " + str([] if finish else res))
#     return (res, finish)
# # --- make_common

# # -----------------
# # compare two binary and compute "base" bits
# # left, right are two binarys
# # mask is a REQB binary, all with same length
# # return a base binary or [] if fails
# # and maximal indicator
# def make_common(left, right, mask):
#     #print ("make_common " + str(left) + " / " + str(right))
#     res = [-1]*len(mask)
#     i = 0
#     finish = False
#     maximal = True
#     while (i < len(mask)) and not finish:
#         # only for REQ==1
#         if (mask[i] == 1):
#             if (left[i] == right[i]):
#                 res[i] = left[i] 
#                 if (res[i] == -1):
#                     maximal = False
#             elif  ((left[i] == -1) or (right[i] == -1)):
#                 res[i] = -(left[i] * right[i])
#             else: # 1!=0
#                 finish = True
#         # --- if mask
#         i += 1
#     #print("make_common= " + str([] if finish else res))
#     #return ([] if finish else res)
#     return (([], False) if finish else (res, maximal))
# # --- make_common

# ----------------
# extract part to simplify and  don't forget duplication
# return a tuple (list of Binary to simplify, the original simplified lbinary)
def extract(size, lbinary, mask):
    # auxiliary to extract part !REQ to simplify 
    result = []
    for Y in lbinary:
        res = [Y[X] for X in range(size) if (mask[X]==0)]
        result.append(res)
    # ---
    return result
# --- extract

# ------------------
# auxiliary to maintain results in combine_all
# in fact two conditions
# side effects on result and commonsout
def add_aux(new, common, result, commonsout):
    if (new not in result):
        result.append(new)
        commonsout.append(common)  
    elif (commonsout[result.index(new)] != common):
        result.append(new)
        commonsout.append(common)
# --- add_aux  

# ------------------
# TODO select all sublist of list of size equal to nb
# return a list of sublists
def select(listpos, nb):
    result = [[]]
    while (nb > 0):
        tmp = []
        listp = listpos
        for sub in result:
            for p in listp:
                tmp.append(sub+[p])
            # first element removed 
            listp = listp[1:]
        listpos = listpos[1:]
        #print (str(listpos))
        result = tmp
        nb -= 1
    # --- while
    return result
# --- select  
 
#----------------------
# expand don't care in a binary
# and return a list of binary
def expand(binary):
    tmp = [[]]
    for i in binary:
        if (i==-1):
            aux = [x+[0] for x in tmp]
            aux += [x+[1] for x in tmp]
            tmp = aux
        else:
            tmp = [x+[i] for x in tmp]
    # --- end for
    return tmp
# --- end of expand

#----------------------
# expand some don't care positions  in a binary
# and return a copy list of binary
# TODO version construction rather than copy as above ?
def expand_some(binary, lpos):
    result = [binary]
    # enumeration of positions
    for pos in lpos:
        tmp = []
        # enumerate binary in tmp
        for abin in result:
            cp0 = abin.copy()
            cp0[pos] = 0
            tmp.append(cp0)
            cp1 = abin.copy()
            cp1[pos] = 1
            tmp.append(cp1)
        # ---
        result = tmp
    # --- end for
    return result
# --- expand_some

# ----------
# test binary inclusion
# lbin1 => lbin2 two Binary of same length
# check if bits 1/0 of lbin1 are 1/0/-1 in lbin2
def is_included_in(lbin1, lbin2):
    subsumed = True
    i = 0
    while (i < len(lbin1)) and subsumed:
        digit1 = lbin1[i]
        digit2 = lbin2[i]
        subsumed = subsumed and ((digit2 == -1) or (digit1 == digit2))
        i += 1
    # --- end while
    return subsumed
# --- is_included_in

# ----------
# test if one List[Binary] of lbin1  is in other:List[Binary]
# lbin:List[List[Binary]]
# other:List[Binary]
def is_in(lbin, other):
    return any([all([B in other for B in LBIN]) for LBIN in lbin])
# --- is_in

# ------------
# newc:List[Integer]
# packets:List[List[Integer]]
# checks if one list in packets in included in newc
# TODO packet/newc are sorted may be useful
def has_no_packet(newc, packets):
    found = True
    I = 0
    while (I < len(packets) and found):
        packet = packets[I]
        # check one packet
        J = 0 
        init = True
        while (J < len(packet) and init):
            init = init and (packet[J] in newc)
            J += 1
        # --- while J
        found = not init
        I += 1
    # --- while I
    return found
# --- has_packet

# --------
# check if a list of literals from props (a dico) has no duplication 
# and no both positive and negative atoms
def correct(literals, props):
    i = 0
    result = True
    while (i < len(literals) and result):
        lit = literals[i]
        # check duplication and not a boolref
        if (lit in literals[i+1:] or not isinstance(lit, BoolRef)):
                result = False
        elif (lit in props):
            if (Not(lit) in literals[i+1:]): # check A and Not(A)
                result = False
        elif (lit.decl().kind()  == Z3_OP_NOT):
            # extract the req 
            req = lit.children()[0]
            if (req not in props): # Not(A) but A not in propositions
                result = False
            if (req in literals[i+1:]): # or duplicate
                result = False
            # --- lit Not(?)
        else:
            result = False
        # --- not in props or ~props
        i += 1
    # --- while
    return result
# --- correct

# ------------------
# get list of atoms in AND-term Goal
def get_list(andgoal):
    if (isinstance(andgoal, bool)):
        return andgoal
    elif (len(andgoal) == 1):
        return andgoal.get(0)
    else:
        return [andgoal.get(i) for i in range(len(andgoal))]
# --- end get_list
# may be us as_expr too

# ----------
# prod, latoms list of Z3
# atom Z3 not in prod
# insert atom in prod but preserve latoms ordering
# and take care of negated
def sortit(prod, atom, latoms):
    #print ("sortit " + str(prod) + "  " + str(atom) + " " + str(latoms))
    if (len(prod) == 0):
        return [atom]
    else:
        res = []
        pos = 0
        for btom in latoms:
            #print (str(pos))
            if (pos < len(prod)):
                inp = prod[pos]
                if (atom == Not(inp)):
                    return []
                elif (inp == Not(atom)):
                    return []
                elif (atom == btom):
                    res.append(atom)
                elif (btom == inp):
                    pos += 1
                    res.append(inp)
                # ---
            elif (atom not in res):   # something to add or not
                res.append(atom)
            # ---
        # ---
        return res
    # ---
# --- sortit

# -------------
# compute the negation of a binary request
# return a List[] representing a union
def negate(binary):
    return [-1 if (bit == -1) else (1 if (bit == 0) else 0) for bit in binary]
# --- negate

# -------------
# compute the complement of a Binary AND term
# Thus return a List[Binary] representing a DNF
def complement(binary):
    size = len(binary)
    tmp = []
    for I in range(size):
        if (binary[I] == 0):
            req = [-1]*size
            req[I] = 1
            tmp.append(req)
        elif (binary[I] == 1):
            req = [-1]*size
            req[I] = 0
            tmp.append(req)
    # ---
    return tmp
# --- complement

# -------------
# hashes a list of binary by converting into tuple 
# TODO but ordering of Binary ???
def hashing(lbinary):
    return hash(tuple([tuple(B) for B in lbinary]))
# --- hashing

# -------------
# compute the REQ position occuring in the List[Binary]
def compute_positions(lbinary, REQB):
    return list(set().union(*[set([P for P in range(len(REQB)) if (REQB[P] == 1 and B[P] != -1)]) for B in lbinary]))
# --- compute_positions

# -------------
# generate allowed requests which are sat
# lpos_combi: a list of tuple (list of positions, list of combinations)
def gener_allowed(lpos_combi, NBREQ):
    res = [[-1]*NBREQ]
    for (lpos, lcombi) in lpos_combi:
        tmp = []        
        for request in res:
            # apply the combinaison to positions
            for combi in lcombi:
                req = request.copy()
                for pos in lpos:
                    # offset between both lists
                    req[pos] = combi[lpos.index(pos)]
                tmp.append(req)
            # --- compute new requests
        # --- request
        res = tmp
    # --- lpos_combi
    return res
# --- gener_allowed

# -------------
# generate allowed requests which are sat
# assumes definitions ordering of REQ 
# conflicts is a list of Binary:REQ defining prohibited binaries 
# it represents  DNF of the denied binary 
def gener_allowed2(conflicts, NBREQ):
    if (conflicts):
        tmp = complement(conflicts[0])
        if (len(conflicts) > 1):
            for conf in conflicts[1:]:
                tmp = minimizing(product(tmp, complement(conf)))
                #prime(tmp)
            # ---
        return tmp
    else:
        return [[-1]*NBREQ]
# --- gener_allowed2

# -------------
# generate binary conflicts from exclusive positions
# conflicts: a list of pair of positions
# pair: a couple of bits
def gener_exclusive(conflicts, NBREQ, pair):
    tmp =  []
    for (P, Q) in conflicts:
        binary = [-1]*NBREQ
        binary[P] = pair[0]
        binary[Q] = pair[1]
        tmp.append(binary)
    return tmp
# --- gener_exclusive


