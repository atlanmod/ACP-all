# -------------------
# 26/3/2020
# test Table ...pour Shaikh2010
# -------------------

### -------------
from Normalized_OK import * #@UnusedWildImport

# version sans sous-typage
Data = DeclareSort('Data')
Person = DeclareSort('Person')

root = Const('root', Person)
tech = Const('tech', Person)
data = Const('data', Data)

table = Normalized_Enumerate() 
#table = Iterative_hashing() 
# Variables
table.add_variable("A", Person)
table.add_variable("C", Person)
table.add_variable("D", Data)
A = table.get_variable(0)
C = table.get_variable(1)
D = table.get_variable(2)

#  predicates 
rights = Function('rights', Person, Data, BoolSort()) 
pread = Function('pread', Person, Data, BoolSort()) 
pwrite = Function('pwrite', Person, Data, BoolSort()) 
pdelete = Function('pdelete', Person, Data, BoolSort()) 
person = Function('person', Person, BoolSort()) 
administrator = Function('administrator', Person, BoolSort()) 
technician = Function('technician', Person, BoolSort()) 
delegate = Function('delegate', Person, Person, BoolSort()) 

# rules original
size=8
table.add_rule(administrator(A), person(A)) #0
table.add_rule(technician(A), person(A))  #1
table.add_rule(And(administrator(A), technician(A)), False) #2
table.add_rule(rights(A, D), And(pread(A, D), pwrite(A, D), pdelete(A, D))) #3
table.add_rule(administrator(A), rights(A, D)) #4
table.add_rule(technician(C), And(pread(C, D), pwrite(C, D))) #5
table.add_rule(And(administrator(A), technician(C), delegate(A, C)), rights(C, D)) #6
table.add_rule(pdelete(A, D), administrator(A)) #7

#  ----------------- problems  
# And(administrator(A), technician(A)) [1, 1, -1, -1]
# And(administrator(A), technician(C), delegate(A, C)) [1, -1, 1, 1]
### BUT this last problem is a junk

#### --------------- analysis
start = process_time()
# REQ = [administrator(A), technician(A), technician(C), delegate(A, C)]

REQ = [administrator(A), technician(A), technician(C), delegate(A, C)] # dico ordering
# Ordering REQ [administrator(A), technician(A), technician(C), delegate(A, C)]

#ALLOWED = [[-1]*len(REQ)] # both
#ALLOWED = [] # no
#ALLOWED = [[1, 1, -1, -1]] # yes
ALLOWED = [[-1, 1, 1, -1], [-1, 0, 0, -1]] # since relations between technicians 

table.compute_table(REQ, size, ALLOWED)
 
# print ("size = " + str(size) + " time = " + str(floor(process_time()-start)))
# #print (str(table))
# print (str(table.get_info()))
# #table.show()
table.show_problems()
#table.classify_problems()
# table.check_problems(size)
# #print ("size= " + str(size) + " time= " + str(floor(process_time()-start)) + " " + str(table.count) + " / " + str(table.total))

# # print(str(table.check_undefined(Exists(table.variables, And(administrator(A), technician(C), delegate(A, C))), size))) # unsat
# #### TESTS ==================
# S= Solver()
# # S.add(ForAll([A, C, D], Not(And(administrator(A), technician(A)))))
# # S.add(Exists([A, C, D], And(administrator(A), technician(C), delegate(A, C))))
# #S.add(Exists([A, C, D], And(And(administrator(A), technician(C), delegate(A, C)), Not(And(administrator(A), technician(A))))))
# #S.add(Not(ForAll([A, C, D], Implies(And(administrator(A), technician(C), delegate(A, C)), And(administrator(A), technician(A)))))) # sat 
# #S.add(Not(ForAll([A, C], Implies(technician(C),  technician(A))))) # sat
# #S.add(ForAll([A, C], And(technician(C),  Not(technician(A))))) # unsat
# #S.add(ForAll([A, C], And(Not(technician(C)),  technician(A)))) # unsat
# # S.add(Exists([A, C], And(Not(technician(C)),  technician(A)))) # sat BUT
# print(str(S.check())) 
