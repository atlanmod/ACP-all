### ---------------
### enum for checking indicators
### 30/1/2019
### ---------------

from enum import Enum

### ---------------
# all check unsat 
# obvious: !*rules & !* csys & ?*D 
# tautology: !*rules & !* csys & ?* (D & ~C) 
# unsafe: !*rules & !* csys   !*(D=>C) ?*D 
# fact: !*rules & !* csys !*(D=>C) ?*~C 
class Indicator(Enum):
    OBVIOUS = 1
    TAUTOLOGY = 2
    FACT = 3
    UNSAFE = 4
    NONE = 6
# --- end Indicator
