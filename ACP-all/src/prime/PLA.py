# ----------
# PLA encoding 
# and minimization with espresso
# 23/3/2020
# -------------

from pyeda.boolalg.espresso import * #@UnusedWildImport

# input codes
_INCODE = {0:1, 1:2, -1:3}
# reverse code
_REVCODE = {1:0, 2:1, 3:-1}

# ----------------
# encode a List[Binary] for 
# lbinary List[Binary] all of same length
# calling espresso
# only one positive output function 
def encoding_PLA(lbinary):
    tmp = set()
    for binary in lbinary:
        tmp.add((tuple([_INCODE[B] for B in binary]), (1,)))
    return tmp
# --- encoding_PLA

# ----------------
# apply espresso to lbinary
# and output the Binary representation
# lbinary List[Binary] all of same length
# return List[Binary]
def minimizing(lbinary):
    res = []
    if (lbinary):
        tmp = encoding_PLA(lbinary)
#         set_config(single_expand= False, # True, #opts.fast,
#                    remove_essential= False, # True, # opts.ess, # or False plutot
#                    #         force_irredundant=opts.irr,
#                    #         unwrap_onset= True #opts.unwrap,
#                    recompute_onset= True #opts.onset,
#                    #         use_super_gasp=opts.strong,
#                    )   
        set_config()     
        tmp = espresso(len(lbinary[0]), 1, tmp)
        # print (str(tmp))
        # decoding 
        for (T, _) in tmp: # since minimize in, out
            res.append([_REVCODE[B] for B in T])
    return res
# --- minimizing
