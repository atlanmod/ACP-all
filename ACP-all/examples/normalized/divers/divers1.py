# -------------------
# 25/3/2020
# test simple
# -------------------

# TODO exemple avec cas junk

### -------------
from Normalized_OK import * #@UnusedWildImport

Person = DeclareSort('Person')
String = DeclareSort('String')
 
table = Normalized_Enumerate()
# Variables
table.add_variable("X", IntSort())
table.add_variable("Y", IntSort())
table.add_variable("Z", Person)
table.add_variable("T", String)
X = table.get_variable(0)
Y = table.get_variable(1)
Z = table.get_variable(2)
T = table.get_variable(3)
 
#  predicates 
D = Function('D', IntSort(), IntSort()) 
DI = Function('DI', IntSort(), IntSort()) 
DJ = Function('DJ', IntSort(), IntSort()) 
Permit = Function('Permit', IntSort(), BoolSort()) 
P = Function('P', IntSort(), BoolSort()) 
Q = Const('Q', BoolSort())
Q1 = Const('Q1', BoolSort())
Q2 = Const('Q2', BoolSort())
Q3 = Const('Q3', BoolSort())
Q4 = Const('Q4', BoolSort())
Q5 = Const('Q5', BoolSort())
R1 = Const('R1', BoolSort())
D1 = Function('D1', IntSort(), BoolSort())
D2 = Function('D2', IntSort(), BoolSort())
D3 = Function('D3', IntSort(), BoolSort())
D4 = Function('D4', IntSort(), BoolSort())
D5 = Function('D5', IntSort(), BoolSort())
D6 = Function('D6', IntSort(), BoolSort())
D7 = Function('D7', IntSort(), IntSort(), BoolSort())
D8 = Function('D8', IntSort(), IntSort(), BoolSort())
C1 = Function('C1', IntSort(), BoolSort())
C2 = Function('C2', IntSort(), BoolSort())
C3 = Function('C3', IntSort(), BoolSort())
C4 = Function('C4', IntSort(), BoolSort())
C5 = Function('C5', IntSort(), BoolSort())
registered = Function('registered', Person, BoolSort())
age = Function('age', Person, IntSort())
connected = Function('connected', Person, String, BoolSort())
password = Function('password', Person, String, BoolSort())

# #### EX0
# size = 5
# #table.add_rule(D2(X), C3(X)) # to force D2 as reduction but useless
# table.add_rule(And(D2(X), Not(D1(X))), False) # unsat BUT pb here
# table.add_rule(And(D1(X), D2(X)), Not(C2(X))) # D1D2 pb
# table.add_rule(And(D1(X), D2(X)), C2(X))
# table.add_rule(D1(X), C1(X)) # D1 pb
# table.add_rule(D1(X), Not(C1(X)))
# REQ = [D1(X), D2(X)] 
# ALLOWED = [[-1, -1]]
# #  ----------------- problems
# # D1(X), D2(X) 
# ## computed initially and simplified NOT the right one

#### difference avec le précédent
#### on a pas unsafe explicit entre ~D1 et D2
#### EX1 !* ~D1 & D2=?* D1 unsat
# size = 5
# table.add_rule(D1(X), C1(X)) # D1 pb
# table.add_rule(D1(X), Not(C1(X)))
# table.add_rule(And(D1(X), Exists(Y, D1(Y))), Not(C2(X))) # D1D2 pb
# table.add_rule(And(D1(X), Exists(Y, D1(Y))), C2(X))
# table.add_rule(Exists(Y, D1(Y)), C3(X)) # to force D2 as reduction 
# REQ = [D1(X), Exists(Y, D1(Y))] 
# ALLOWED = [[-1, -1]]
#  ----------------- problems
# D1 et Exists(Y, D1(Y))
#### Ordering of problem detection [ordering rules has no effect]

### EX1a
size = 3
table.add_rule(D1(X), C1(X)) # D1 pb
table.add_rule(D1(X), Not(C1(X)))
table.add_rule(Exists(Y, D1(Y)), C3(X)) # to force D2 as reduction 
REQ = [D1(X), Exists(Y, D1(Y))] 
#ALLOWED = [[-1, -1]]
ALLOWED = [[1, 1], [0, 0]] # same
#  ----------------- problems
# D1 et Exists(Y, D1(Y)) 
### in fact they are equivalent but syntactically different

# # --------- analysis

table.compute_table(REQ, size, ALLOWED) 
 
# print (str(table.get_info()))
# #table.show()
table.show_problems()
# table.check_problems(size)
# # #print (str(table))

# # TESTS =====================
#print(str(table.check_undefined(Exists(Y, D1(Y)), size))) # EX1a unsat

# S = Solver()
# S.add(ForAll(X, And(Not(D1(X)), Exists(Y, D1(Y))))) ### from EX1
# print("unsat ? " + str(S.check()))


