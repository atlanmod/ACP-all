# ------------------------------
# 20/6/2019
# some additional utility functions
#--------------------------

from z3 import * #@UnusedWildImport
from z3.z3util import * #@UnusedWildImport

#------------- tactic from Z3
skip = Tactic('skip')
NNF = Tactic('nnf')
simplify = Tactic('simplify')
split = Tactic('split-clause')
CNF = Tactic('tseitin-cnf')
tactic = Then(NNF, simplify, Repeat(OrElse(split, skip)), simplify) 
DNF = Then(CNF, simplify, Repeat(OrElse(Then(simplify, split), skip))) 
# 

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
# return a z3 renamed exprssion with a quantifier
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
# compare two binary REQ and compute "common" bits
# left, right are two binarys all with same length
# return a common binary REQ or [] if fails
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

# -------------
# compute common binary of binaries in lbinary
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
        defined = False
        column = 0 # 1 or 0
        for J in range(len(lbinary)):
            bit = lbinary[J][I]
            if (bit != -1):
                if (defined): # it was set to
                    if (column != bit):
                        defined = False
                else:
                    column = bit
                    defined = True
        # --- for J
        if (defined):
            res += 1
    # --- for I 
    return res
# --- estimate_1

# ----------------------
# TODO estimate MAX bound of common size
# complete all combinations and forget unsat
# and measure 
# nbreq size of atoms
# lbinaryreq, lasts: combinations and corresponding last index
# allreq: reductions from tactic
# return True if no need to continue
def estimate(nbreq, lbinaryreq, lasts, allreq):
    res = 0  # to store current max
    size = len(allreq)
    for K in range(len(lbinaryreq)):
        localmax = 0  # to count local max
        binary = lbinaryreq[K]
        #print ("binary " + str(binary))
        # count bit defined for each column
        for I in range(nbreq):
            bitl = binary[I]
            if (bitl != -1):
                defined = True
                column = bitl  # 1 or 0                
            else:
                defined = False
                column = 0  # default not used
            # ---
            for J in range(lasts[K]+1, size):
                bitr = allreq[J][I]
                if (bitr != -1):
                    if (defined):  # it was set to
                        if (column != bitr):
                            defined = False
                    else:
                        column = bitr
                        defined = True
            # --- for J
            if (defined):
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
# # compare two binary and compute "common" bits
# # left, right are two binarys
# # mask is a REQB binary, all with same length
# # return a common binary or [] if fails
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

# ----------
# test binary inclusion
# lbin1 => lbin2 two Binary
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
# TODO non plus complexe
# a solution could be to expand -1 and test is_included_in for each ...
# TODO calculer sort de diff successfive
# test binary inclusion of lbin into a List[Binary]
# all binary have the same length
# TODO principle A = BA + CA
# possible en parrallel bit/bit
# def is_included(lbin, lbins):
#     # aux to combine bit to bit
#     #aux = lambda X,Y:  
#     #size = len(lbin)
#     for bit in lbin:
#         for right in lbins:
#  
#         # --- end for right
#     # TODO how to compare ?
# # --- is_included

