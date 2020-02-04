# --------------
# 29/3/2019
# try to simplify a list of binary List[List[1/0/-1]]
# ---------------

from z3 import * #@UnusedWildImport

# ------------------
# check using solver that these are two equivalent propositions
# two sum of binary and non empty List[Binary] 
def check(lbin1, lbin2):
    #print (str(lbin1) + " " + str(lbin2))
    if (lbin1):
        nbvars = len(lbin1[0])
        lvars = [Const("X"+str(i), BoolSort()) for i in range(nbvars)]
        prop1 = Or(*[And([lvars[i] if l[i]==1 else Not(lvars[i]) for i in range(nbvars)  if l[i]!=-1])  for l in lbin1])
    else:
        prop1 = False
    #print(str(prop1))
    if (lbin2):
        nbvars = len(lbin2[0])
        lvars = [Const("X"+str(i), BoolSort()) for i in range(nbvars)]
        prop2 = Or(*[And([lvars[i] if l[i]==1 else Not(lvars[i]) for i in range(nbvars)  if l[i]!=-1])  for l in lbin2])
    else:
        prop2 = False
    #print(str(prop2))
    S = Solver()
    S.set(timeout = 1000) ### 1second
    S.add(prop1)
    S.add(Not(prop2))
    #print(" => " + str(S.check()))
    res = S.check().__eq__(unsat)
    S.add(prop2)
    S.add(Not(prop1))
    #print(" <= " + str(S.check()))
    return res and S.check().__eq__(unsat)
# --- end of check

# ----------
# test binary subsumption
def is_subsumed_by(lbin1, lbin2):
    subsumed = True
    i = 0
    while (i < len(lbin1)) and subsumed:
        digit1 = lbin1[i]
        digit2 = lbin2[i]
        subsumed = subsumed and ((digit2 == -1) or (digit1 == digit2))
        i += 1
    # --- end while
    return subsumed
# ------------

# ----------------
# combine two lists of binary with -1
# they have the same length and works if only one diff
### -1 /{0,1} => -1 ; 1/0 = -1 only once ; equal
# return two values -1 failure, 0 equal,  1,2 else merging
# 1 = one res combined, 2,3, left or right is one and rres/lres the other
def combine(lbin1, lbin2):
    #print ("bin1,2 " + str(lbin1) + " " + str(lbin2))
    res = []
    lres = [] # result for special left case
    rres = [] # results for special right case
    i = 0
    left = 0 # number of -1 in left not in right 
    right = 0 # number of -1 in right not in left 
    diff = 0 # number of 1/0 differences
    while ((i < len(lbin1)) and diff < 2):
        if (lbin1[i] == lbin2[i]):
            res.append(lbin1[i])
            lres.append(lbin1[i])
            rres.append(lbin1[i])
        elif (lbin1[i] == -1):
            left += 1
            res.append(-1)
            lres.append(-1)
            rres.append(lbin2[i])
        elif (lbin2[i] == -1):
            right += 1
            res.append(-1)
            lres.append(lbin1[i])
            rres.append(-1)
        else:
            diff += 1 # 0 versus 1
            res.append(-1)
            lres.append(-1)
            rres.append(-1)   
        # --- end if
        i += 1
    # --- end while
    #print ("diff= " + str(diff)  + "/" + str(posdiff) + " left= " + str(left) + " right= " + str(right))
    #print (" res= " + str(res)  + " lres= " + str(lres) + " rres= " + str(rres))
    # analyze results
    if (diff == 0):
        if (left == 0) and (right == 0):
            return 0, None # equal
        elif (left > 0) and (right == 0):
            return 1, res
        elif (left == 0) and (right > 0):
            return 1, res
        else:
            return -1, None
    elif (diff == 1):
        if (left == 0) and (right == 0):
            return 1, res
        elif (left > 0) and (right == 0):
            return 2, rres
        elif (left == 0) and (right > 0):
            return 3, lres
        else:
            return -1, None 
    else:
        return -1, None # failure
# --- end combine

# ------------------
# compute some combinations
# if cas=1 store merged and remove all combined
# !!! side effect on lmins
def combine_all(lmins):
    nochange = True
    #result = lmins.copy()
    result = lmins
    i = 0
    finish = False 
    # main loop for combining
    while (i < len(result) and not finish):
        #print ("tour " + str(i) + " " + str(result))
        merged = []
        j = i+1
        while (j < len(result)  and not finish):
            rmin = result[j]
            value, new = combine(result[i], rmin)
            #print ("combine " + str(result[i]) + " " + str(rmin) + " value " + str(value) + " new " + str(new))
            if (value == 0): # equal should be removed
                del result[j] 
                nochange = False
            elif (value == 1): # merge case
                finish = (sum(new) == -1*len(new)) # only in this case
                del result[j]
                if (new not in result):
                    merged.append(new)
                    nochange = False
                j += 1
            elif (value == 2): # left remains uncombined
                if (new not in result):
                    result[j] = new
                    nochange = False
                j += 1
            elif (value == 3): # right remains uncombined
                if (new not in result):
                    result[i] = new
                    nochange = False
                j += 1            
            else: # value = 4 or -1
                j += 1
            # --- end if new
        # --- end while j rmin
        if (merged):
            del result[i]
            result.extend(merged)
        i += 1
    # --- end while i 
    #print ("result " + str(result))
    return nochange
# --- end combine_all

# ------------------
# compute the prime implicants of a list of min terms
# each is a list of {1, 0, -1}
# iterate the combination of all until not possible
def prime(lmins):
    # initial groups
    iterate = lmins 
    while True:
        #print ("--- original " + str(len(iterate)) + " " + str(iterate) + " ------------ ")
        nochange = combine_all(iterate)
        #print ("-------------- result " + str(len(iterate)) + " " + str(result) ) #+ " nochange= " + str(nochange))
        #print ("check " + str(check(iterate, result)))
        #input("wait ? ")
        #iterate = result
        if nochange:
            break;
    return iterate
# --- end prime


