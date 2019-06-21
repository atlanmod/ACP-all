# -------------------
# 21/6/2019
# Test Adi2009 
# -------------------

from Normalized_OK import * #@UnusedWildImport

# --------------------------
Patient = DeclareSort('Patient')
Hospital = DeclareSort('Hospital')

table = Normalized_enumerate()
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
# 
# And(nurse(h), doctor(h), Not(sameward(h, p)))
# And(nurse(h), Not(doctor(h)), Not(sameward(h, p)), chief(h))

### -------- analysis 
size = 5
REQ = [nurse(h), doctor(h), sameward(h, p), chief(h)]

table.compute_table(REQ, size)
  
print (str(table))
print (str(table.get_info()))
print ("--------- Show problems")
table.show_problems()
print ("--------- Check undefinedness (=> Not(R))")
table.check_problems(size)
print ("--------- Compare both results ")
table.compare_problems(size, REQ)
