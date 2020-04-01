# -------------------
# 31/3/2020
# Test Adi2009 
# -------------------

#from Normalized_OK import * #@UnusedWildImport
from Normalized_BDD import * #@UnusedWildImport

# --------------------------
Patient = DeclareSort('Patient')
Hospital = DeclareSort('Hospital')

#table = Normalized_Enumerate()
table = Normalized_BDD()

# Variables
table.add_variable("p", Patient)
table.add_variable("h", Hospital)
p = table.get_variable(0)
h = table.get_variable(1)
# more 
X= Const('X', Hospital)
toubib = Const('toubib', Hospital)
nounou = Const('nounou', Hospital)
bob = Const('bob', Patient)

# 4/1 + 3/2 predicates 
hospital = Function('hospital', Hospital, BoolSort()) 
doctor = Function('doctor', Hospital, BoolSort())     
nurse = Function('nurse', Hospital, BoolSort())
chief = Function('chief', Hospital, BoolSort())
pread = Function('pread', Hospital, Patient, BoolSort())
pwrite = Function('pwrite', Hospital, Patient, BoolSort())
sameward = Function('sameward', Hospital, Patient, BoolSort())

### 
table.add_rule(And(nurse(h), doctor(h)), sameward(h, p)) # 0
table.add_rule(doctor(h), And(pread(h, p), pwrite(h, p))) # 1
table.add_rule(And(nurse(h), Not(sameward(h, p))), Not(pread(h, p))) # 2
table.add_rule(And(doctor(h), sameward(h, p)), pread(h, p)) #3
table.add_rule(chief(h), pread(h, p)) #4
#### ---------------

#  =================== Problems ================ 
# And(nurse(h), doctor(h), Not(sameward(h, p))) [1, 1, 0, -1]
# And(nurse(h), Not(sameward(h, p)), chief(h))  [1, -1, 0, 1]

### -------- analysis 
size = 5
REQ = [nurse(h), doctor(h), sameward(h, p), chief(h)]
ALLOWED = [[-1]*len(REQ)] # two
# Ordering REQ [nurse(h), doctor(h), sameward(h, p), chief(h)]
#ALLOWED = [] # 0
#ALLOWED = [[1, 1, 0, -1]] # two because 1 1 0 1 is common
#ALLOWED = [[1, 1, 0, 1]] # two because 1 1 0 1 is common
#ALLOWED = [[1, 1, 0, 0]] # only this
#ALLOWED = [[1, 0, 0, 1]] # only this

# table.classify(size)
# table.check_simplified(size)
# table.parse_rules()
# table.check_renamed()
# table.normalize()
# table.compute_dnf()

table.compute_table(REQ, size, ALLOWED)
  
print (str(table))
#print (str(table.get_info()))
#table.show()
#print(str(table.normalized_problems))
table.show_problems()
#table.classify_problems()
#table.check_problems(size)

#### tests ======================

