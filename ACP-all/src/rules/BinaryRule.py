#------------
# 5/4/2019
# DNF => CNF both are Binary that is List[1/0/-1]
#------------

# TODO don't use characteristic now

from NormalizedRule import * #@UnusedWildImport

#--------------
# TODO add a new characteristic from original rules
# Rule with binary to enumerate in the iterative process
# TODO what are the atoms ?
class BinaryRule(NormalizedRule):
 
    # --------------------
    # create a new rule 
    def __init__(self, cond, conc):
        super().__init__([], cond, conc) # not used
    # --- end init
 
    # --------------------
    def __str__(self):
        return super().__str__()
    # --- end str
    

# -- end class BinaryRule
