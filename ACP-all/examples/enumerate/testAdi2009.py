# -------------------
# 21/6/2019
# Test Adi2009 
# -------------------

from Enumerate import * #@UnusedWildImport

# --------------------------
Patient = DeclareSort('Patient')
Hospital = DeclareSort('Hospital')

table = Enumerate()
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

### -------- analysis 
size = 5

#### definition of the inputs request atom to consider 
REQ = [nurse(h), doctor(h), sameward(h, p), chief(h)]

table.compute_table(size, REQ) # compute the problems
print ("--------- Show results")
print (str(table))
print (table.get_info())
print ("--------- Check undefinedness (=> Not(R))")
table.check_problems()

#### get these two problems
# ---
# And(nurse(h), doctor(h), Not(sameward(h, p)))
# And(nurse(h), Not(doctor(h)), Not(sameward(h, p)), chief(h))
# ---

#### =================== 3  undefined examples
# print(str(table.check_undefined(Exists(table.variables, And(doctor(h), chief(h), nurse(h), Not(sameward(h, p)))), size)))
# print(str(table.check_undefined(Exists(table.variables, And(Not(doctor(h)), chief(h), nurse(h), Not(sameward(h, p)))), size)))
# print(str(table.check_undefined(Exists(table.variables, And(doctor(h), Not(chief(h)), nurse(h), Not(sameward(h, p)))), size)))
# S = Solver()
# S.help()

