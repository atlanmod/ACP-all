# -------------------
# 25/3/2020
# test simple
# -------------------



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

#### EX0
# size = 2
# table.add_rule(D1(X), C1(X))
# table.add_rule(D2(X), Not(C1(X)))
# REQ = [D1(X), D2(X)] # all indep
# ALLOWED = [[-1, -1]]
# NOTRELREQ = []
#  ----------------- problems
# And(D1(X), D2(X))

#### EX1 
# size = 2
# table.add_rule(And(D1(X), D2(X)), C1(X))
# table.add_rule(And(D1(X), D2(X)), Not(C1(X)))
# REQ = [D1(X), D2(X), D3(X), D4(X)]
#  ----------------- problems
# And(D1(X), D2(X))

#### EX2 
# size = 3
# table.add_rule(And(D1(X), D2(X)), And(D3(X), C2(X)))
# table.add_rule(And(D1(X), D2(X), D3(X)), C2(X))
# table.add_rule(C2(X), False)
# REQ = [D1(X), D2(X), D3(X), D4(X)]
#  ----------------- problems
# And(D1(X), D2(X))

#### EX3 
# size = 4
# table.add_rule(And(D1(X), D2(X)), And(D3(X), C2(X)))
# table.add_rule(D1(X), C3(X))
# table.add_rule(D2(X), C4(X))
# table.add_rule(D3(X), Or(Not(C3(X)), Not(C4(X))))
# REQ = [D1(X), D2(X), D3(X), D4(X)]
#  ----------------- problems
# And(D1(X), D2(X))

#### EX3a fix ?* D1D2D3
# size = 4 
# table.add_rule(And(D1(X), D2(X)), Or(And(D3(X), C2(X)), Exists(X, And(D1(X), D2(X), D3(X)))))
# table.add_rule(D1(X), Or(C3(X), Exists(X, And(D1(X), D2(X), D3(X)))))
# table.add_rule(D2(X), Or(C4(X), Exists(X, And(D1(X), D2(X), D3(X)))))
# table.add_rule(D3(X), Or(Not(C3(X)), Not(C4(X)), Exists(X, And(D1(X), D2(X), D3(X)))))
# REQ = [D1(X), D2(X), D3(X), D4(X)]
#  ----------------- problems
# NO PB

# ### EX3b fix ?* D1D2~D3
# size = 4 
# table.add_rule(And(D1(X), D2(X)), Or(And(D3(X), C2(X)), Exists(X, And(D1(X), D2(X), Not(D3(X))))))
# table.add_rule(D1(X), Or(C3(X), Exists(X, And(D1(X), D2(X), Not(D3(X))))))
# table.add_rule(D2(X), Or(C4(X), Exists(X, And(D1(X), D2(X), Not(D3(X))))))
# table.add_rule(D3(X), Or(Not(C3(X)), Not(C4(X)), Exists(X, And(D1(X), D2(X), Not(D3(X))))))
# REQ = [D1(X), D2(X), D3(X), D4(X)]
# #  ----------------- problems
# # no pb 

### ==============
#### EX4 actual in sac2020
# size = 2 
# table.add_rule(D1(X), And(D3(X), C2(X)))
# table.add_rule(And(D1(X), D3(X)), False)
# REQ = [D1(X), D2(X), D3(X), D4(X)]
# ## ----------------- problems
## D1(X) direct avec tactic en fait

#### EX4a fix D1~D3
# size = 2
# table.add_rule(D1(X), Or(And(D3(X), C2(X)), Exists(X, And(D1(X), Not(D3(X))))))
# table.add_rule(And(D1(X), D3(X)), False)
# REQ = [D1(X), D2(X), D3(X), D4(X)]
#  ----------------- problems
# And(D1(X), D3(X))

### EX4b fix D1D3
# size = 2
# table.add_rule(D1(X), And(D3(X), C2(X)))
# table.add_rule(And(D1(X), D3(X)), Exists(Y, And(D1(Y), D3(Y))))
# REQ = [D1(X), D2(X), D3(X), D4(X)]
#  ----------------- problems
# And(D1(X), Not(D3(X)))
### effectivement l'autre est corrigé

### EX4c fix D1 YES
# size = 2
# table.add_rule(D1(X), Or(And(D3(X), C2(X)), Exists(Y, D1(Y))))
# table.add_rule(And(D1(X), D3(X)), Exists(Y, D1(Y)))
# REQ = [D1(X), D2(X), D3(X), D4(X)]
#  ----------------- problems
# D1 sur les deux rules OK (sur une cela ne marcherait pas)

### EX4d fix D1D3 et D1~D3 sur chacune 
# size = 2
# table.add_rule(D1(X), Or(And(D3(X), C2(X)), Exists(Y, And(D1(Y), Not(D3(Y))))))
# table.add_rule(And(D1(X), D3(X)), Exists(Y, And(D1(Y), D3(Y))))
# REQ = [D1(X), D2(X), D3(X), D4(X)]
#  ----------------- problems
# fix sur chacune OK mais +complexe à faire et resultat aussi
### 
### =============

### EX6 : show simplif between l=2 and l=1
### ex papier sec@sac
# size = 3
# table.add_rule(And(D1(X), D2(X)), Not(D3(X)))
# table.add_rule(D1(X), Not(C1(X)))
# table.add_rule(D2(X), C1(X))
# REQ = [D1(X), D2(X), D3(X)]
# ALLOWED = [[-1, -1, -1]]
# NOTRELREQ = []
# #  ----------------- problems
# And(D1(X), D2(X))

### EX7 
# size = 5
# ### these 2 produce a size(PB)=4 at l=2
# table.add_rule(And(D1(X), D2(X)), C4(X))
# table.add_rule(And(D3(X), D4(X)), Not(C4(X)))
# ### these 3 produce a size(PB)=3 at l=3
# table.add_rule(D1(X), Not(C1(X)))
# table.add_rule(D2(X), Not(C2(X)))
# table.add_rule(D3(X), Or(C1(X), C2(X)))
# REQ = [D1(X), D2(X), D3(X)]
# ALLOWED = [[-1, -1, -1]]
# NOTRELREQ = []
# #  ----------------- problems
# D1D2D3

### EX8bis
# size = 4
# ### 2 rules pb 2 at l=2
# table.add_rule(D1(X), Not(C1(X)))
# table.add_rule(D2(X), C1(X))
# ### same thing
# table.add_rule(D1(X), Not(C2(X)))
# table.add_rule(Not(D2(X)), C2(X))
# REQ = [D1(X), D2(X)]
# ALLOWED = [[-1, -1]]
# NOTRELREQ = []
#  ----------------- problems
### but found D1 as initial

### EX8 : 
# size = 8
# ### pb And(D1(X), Not(D3(X)), D2(X)) at l=2
# table.add_rule(D1(X), Or(D3(X), Not(C1(X))))
# table.add_rule(D2(X), Or(D3(X), C1(X)))
# # ...
# table.add_rule(D1(X), Or(D3(X), Not(C2(X))))
# table.add_rule(Not(D2(X)), Or(D3(X), C2(X)))
# ### same on Not(D3(X))
# table.add_rule(D1(X), Or(Not(D3(X)), Not(C1(X))))
# table.add_rule(D2(X), Or(Not(D3(X)), C1(X)))
# table.add_rule(D1(X), Or(Not(D3(X)), Not(C2(X))))
# table.add_rule(Not(D2(X)), Or(Not(D3(X)), C2(X)))
# REQ = [D1(X), D2(X), D3(X)]
# ALLOWED = [[-1, -1, -1]]
# NOTRELREQ = []
#  ----------------- problems
### D1 found at initial

### EX8a 
# size = 4
# table.add_rule(D1(X), Or(D3(X), Not(C1(X))))
# table.add_rule(D2(X), Or(D3(X), C1(X)))
# table.add_rule(Not(D2(X)), Or(D4(X), C2(X)))
# table.add_rule(D1(X), Or(D4(X), Not(C2(X))))
# REQ = [D1(X), D2(X), D3(X), D4(X)]
# ALLOWED = [[-1, -1, -1, -1]]
# NOTRELREQ = []
## ----------------- problems
# # And(D1(X), Not(D3(X)), D2(X))
# # And(D1(X), Not(D2(X)), Not(D4(X))) 
# # And(D1(X), Not(D3(X)), Not(D4(X)))
#### BDD_V3
# And(D1(X), Not(D3(X)), D2(X))
# And(D1(X), Not(D2(X)), Not(D4(X)))
### new BDD_V3 paths but simplif the same
# # And(D1(X), Not(D3(X)), D2(X))
# # And(D1(X), D3(X), Not(D2(X)), Not(D4(X))) 
# # And(D1(X), Not(D3(X)), Not(D2(X)), Not(D4(X)))

### EX8c OK useful for simplif
# size = 4
# table.add_rule(D1(X), Not(C1(X)))
# table.add_rule(D2(X), C1(X))
# table.add_rule(D3(X), C2(X))
# table.add_rule(Not(D4(X)), Not(C2(X)))
# REQ = [D1(X), D2(X), D3(X), D4(X)]
# ALLOWED = [[-1, -1, -1, -1]]
# NOTRELREQ = []
#  ----------------- The current problems  
# And(D3(X), Not(D4(X)))
# And(D1(X), D2(X))
#  ----------------- The current problems  TODO ?
# And(Not(D1(X)), D3(X), Not(D4(X)))
# And(Not(D2(X)), D3(X), Not(D4(X)))
# And(D1(X), D2(X))
#  ----

### EX8ab 
# size = 3
# table.add_rule(D1(X), Or(D3(X), Not(C1(X))))
# table.add_rule(D2(X), Or(D3(X), C1(X)))
# table.add_rule(Not(D2(X)), Or(D4(X), C2(X)))
# REQ = [D1(X), D2(X), D3(X), D4(X)]
# ALLOWED = [[-1, -1, -1, -1]]
# NOTRELREQ = []
### --------
# And(D1(X), Not(D3(X)), D2(X)) 

### EX8aa simplif path 
# size = 3
# table.add_rule(D2(X), C2(X))
# table.add_rule(D3(X), C1(X))
# table.add_rule(D4(X), Not(C2(X)))
# REQ = [D2(X), D3(X), D4(X)]
# ALLOWED = [[-1, -1, -1]]
# NOTRELREQ = []
## ----------------- problems
# And(D2(X), D4(X))

### EX8b : simplif
# size = 3
# table.add_rule(D1(X), Or(D3(X), Not(C1(X))))
# table.add_rule(D2(X), Or(D3(X), C1(X)))
# table.add_rule(Not(D2(X)), Or(D4(X), C1(X)))
# REQ = [D1(X), D2(X), D3(X), D4(X)]
# ALLOWED = [[-1, -1, -1, -1]]
# NOTRELREQ = []
#  ----------------- problems
# # And(D1(X), Not(D3(X)), D2(X))
# # And(D1(X), Not(D3(X)), Not(D4(X)))

### EX9 : heuristic is wrong Shannon or full combine find it
### path simplif 
size = 4+2
### pb size = 2
table.add_rule(D1(X), Not(C1(X)))
table.add_rule(D2(X), C1(X))
### pb size=4
table.add_rule(D3(X), Not(And(C2(X), C3(X), C4(X))))
table.add_rule(D4(X), C2(X))
table.add_rule(D5(X), C3(X))
table.add_rule(D6(X), C4(X))
REQ = [D1(X), D2(X), D3(X), D4(X), D5(X), D6(X)]
ALLOWED = [[-1, -1, -1, -1, -1, -1]]
#NOTRELREQ = []
# #  ----------------- Normalized_OK_V2
# # And(D1(X), D2(X))
#  ----------------- The REAL problems  
# And(D1(X), D2(X))
# And(D3(X), D4(X), D5(X), D6(X))
#  ----
#  ----------------- The current problems  TODO ?
# And(Not(D1(X)), D3(X), D4(X), D5(X), D6(X))
# And(Not(D2(X)), D3(X), D4(X), D5(X), D6(X))
# And(D1(X), D2(X))
#  ----


### EX10 path simplif
# size = 6
# table.add_rule(D1(X), C1(X))
# table.add_rule(D2(X), C2(X))
# table.add_rule(D3(X), D4(X))
# table.add_rule(D4(X), C2(X))
# table.add_rule(D5(X), C3(X))
# table.add_rule(D6(X), C4(X))
# REQ = [D1(X), D2(X), D3(X), D4(X), D5(X), D6(X)]
# ALLOWED = [[-1, -1, -1, -1, -1, -1]]
# NOTRELREQ = []
#  ----------------- problems
# And(D3(X), Not(D4(X)))

### EX11 
# size = 3
# table.add_rule(D1(X), C1(X))
# table.add_rule(D2(X), C2(X))
# table.add_rule(And(C1(X), C2(X)), False)
# REQ = [D1(X), D2(X)]
### Normalized => D1D2 PB

### EX12 with !REQ dependant 
### prime not suffisant
# size = 2
# table.add_rule(D7(X, Y), Y <= 0)
# table.add_rule(D8(X, Y), Y > 0)
# REQ = [D7(X, Y), D8(X, Y)] # REQ dependent
# ALLOWED = [[-1, -1]]
# NOTRELREQ = [[[1, -1], [-1, 1]], [[0, -1], [-1, 0]]] # need it
# NOTRELREQ = [[[0, -1], [-1, 0]]] # yes
# NOTRELREQ = [[[1, -1], [-1, 1]]] # no
#  ----------------- The current problems  
# And(D7(X, Y), D8(X, Y))
#  ----
### basic shannon don't find it
### but with solver yes
### new BDD_V3 not found see EX12a

### EX12a change atoms
# size = 5
# table.add_rule(D7(X, Y), Or(Y < 0, Y == 0))
# table.add_rule(D8(X, Y), Y > 0)
# table.add_rule(And(Y < 0, Y == 0), False)
# table.add_rule(And(Y < 0, Y > 0), False)
# table.add_rule(And(Y > 0, Y == 0), False)
# REQ = [D7(X, Y), D8(X, Y)] # !REQ dependent
# ALLOWED = [[-1, -1]]
# NOTRELREQ = [] # 
### found And(D7(X, Y), D8(X, Y)) OK

### EX13 with !REQ dependant 
# size = 2
# table.add_rule(D1(X), C1(X))
# table.add_rule(D2(Y), Not(C1(Y)))
# REQ = [D1(X), D2(Y)]
# ALLOWED = [[-1, -1]]
# NOTRELREQ = [] # 
#### And(D1(X), D2(Y)) is not a problem!!!

### EX14  needs a first test no REQ and no !REQ 
# size = 2
# table.add_rule((Y < 0), C1(X))
# table.add_rule(D2(Y), (Y <= 0))
# REQ = [D2(Y), (Y < 0), (Y <= 0)] # REQ dependent 
# ALLOWED = [[-1, -1, -1]]
# NOTRELREQ = [] # 
### And(D2(Y), Not(Y <= 0))
### BDD_V3 found it

### EX14aa 
# size = 2
# table.add_rule((Y < 0), C1(X))
# table.add_rule(D2(Y), Or(Y < 0, Y == 0))
# REQ = [D2(Y), (Y < 0)] # REQ dependent
# ALLOWED = [[-1, -1]]
# NOTRELREQ = [] # 
# definitions OrderedDict([(P_0(Y), Y < 0), (P_1(X), C1(X)), (P_2(Y), D2(Y)), (P_3(Y), Y == 0)])
# size= 4 REQ-pos [0, 2] mapping {0: 0, 2: 1}

### EX14ab
# size = 3
# table.add_rule((Y < 0), C1(X))
# table.add_rule(D2(Y), Y < 0)
# table.add_rule(And(Y < 0, Y > 0), False)
# REQ = [D2(Y), (Y < 0)] # REQ dependent 
# ALLOWED = [[-1, -1]]
# NOTRELREQ = [] # 
### BDD_V3 And(Not(Y < 0), D2(Y)) OK

### EX14b  
# size = 5
# table.add_rule((Y < 0), C1(X))
# table.add_rule(D2(Y), Or(Y < 0, Y == 0)) 
# table.add_rule(And(Y < 0, Y == 0), False)
# table.add_rule(And(Y < 0, Y > 0), False)
# table.add_rule(And(Y > 0, Y == 0), False)
# REQ = [D2(Y), (Y < 0)] # REQ dependent 
# ALLOWED = [[-1, -1]]
# NOTRELREQ = [] # 
### NO problem 

### EX14c it is unsat ...
# size = 3
# table.add_rule((Y < 0), C1(X))
# table.add_rule(D2(Y), Or(Y < 0, Y == 0))
# table.add_rule(And(Y < 0, Or(Y < 0, Y == 0)), False)
# REQ = [D2(Y), (Y < 0)]
# ALLOWED = [[-1, -1]]
# NOTRELREQ = [] # 
# ### 

### EX14d 
# size = 5
# table.add_rule((Y < 0), C1(X))
# table.add_rule(D2(Y), Or(Y > 0, Y == 0)) # error here
# table.add_rule(And(Y < 0, Y == 0), False)
# table.add_rule(And(Y < 0, Y > 0), False)
# table.add_rule(And(Y > 0, Y == 0), False)
# REQ = [D2(Y), (Y < 0)] # REQ dependent
# ALLOWED = [[-1, -1]]
# NOTRELREQ = [] # 
### BDD_V3 And(D2(Y), (Y < 0)) OK

# # --------- analysis

table.compute_table(REQ, size, ALLOWED) #, NOTRELREQ)  
 
# print (str(table.get_info()))
# #table.show()
table.show_problems()
# table.check_problems(size)
# # #print (str(table))

#print(str(table.check_undefined(Exists(table.variables, And(D1(X), D2(Y))), size))) ### sat 
#print(str(table.check_undefined_request(And(P_1(X), P_3(Y)))))
#### EX14 ok
# print(str(table.check_undefined(Exists(table.variables, And(D2(Y), Not(Y <= 0))), size))) # unsat
# print(str(table.check_undefined(Exists(table.variables, And(Not(Y < 0), D2(Y), Not(Y <= 0))), size))) # unsat
#print(str(table.check_undefined(Exists(table.variables, And(D2(Y), Not(Y < 0))), size))) # sat
# print(str(table.check_undefined(Exists(table.variables, And(D1(X), D2(Y))), size))) #sat
#print(str(table.check_undefined(Exists(table.variables, And(D2(Y), Y < 0)), size))) # sat
# print(str(table.check_undefined(Exists(table.variables, And(D(X) <= 3, D(X) >=2)), size))) # EX15a unsat it is a PROBLEM
#print(str(table.check_undefined(Exists(table.variables, And(D(X) >= 2, DI(X) < 5)), size))) # EX15d unsat it is a PROBLEM
#print(str(table.check_undefined(Exists(table.variables, And(D3(X), D4(X), D5(X), D6(X))), size))) # EX9 unsat

# #### 
# normalEx8a = Or(And(D1(X), Not(D3(X)), D2(X)), And(D1(X), Not(D2(X)), Not(D4(X))), And(D1(X), Not(D3(X)), Not(D4(X))))
# shannonEx8a = Or(And(D1(X), Not(D3(X)), D2(X)), And(D1(X), Not(D3(X)), Not(D2(X)), Not(D4(X))), And(D1(X), D3(X), Not(D2(X))))
#   Ex9   OK equiv
# normal = Or(And( D3(X), D4(X), D5(X), D6(X)), And(D1(X), D2(X)))
# shannon = Or(And(Not(D1(X)), D3(X), D4(X), D5(X), D6(X)), And(Not(D2(X)), D3(X), D4(X), D5(X), D6(X)), And(D1(X), D2(X)))
# 
# S = Solver()
# S.add(Exists(Y, And(Y < 0, Y > 0)))
# print (str(S.check())) # unsat
# S.reset()
# S.add(Exists(table.variables, shannon))
# S.add(ForAll(table.variables, Not(normal)))
# print ("=> " + str(S.check()))
# S.reset()
# S.add(Exists(table.variables, normal))
# S.add(ForAll(table.variables, Not(shannon)))
# print ("<=  " + str(S.check())) # unsat

#print(str(make_common([1, -1, -1, -1], [-1, 1, 1, -1])))
# print(str(make_and([1, -1, -1, -1], [-1, 1, 1, -1])))
# print(str(make_and([0, -1, -1, -1], [0, -1, -1, -1]))) 

##print(str(negate([1, 1, -1]))) no
# print(str(complement([1, 1, -1]))) # [[0, -1, -1], [-1, 0, -1]]
# print(str(complement([-1, 0, 1]))) # [[-1, 1, -1], [-1, -1, 0]]
# print(str(product([[-1, 1, -1], [-1, -1, 0]], [[0, -1, -1], [-1, 0, -1]])))
# [[0, 1, -1], [0, -1, 0], [-1, 0, 0]]

#### arguments is a DNF of the denied 
# allowed = gener_allowed2([[1, 1, -1, -1], [-1, -1, 1, 1]], 4)
# print(str(allowed))
# print(str(product([[1, 0, 0, 1]], allowed))) # OK
# print(str(product([[1, 1, 0, 1]], allowed))) # NOK

# allowed = gener_allowed2([[1, -1, -1], [-1, 0, -1]], 3) # [0, 1, -1]
# print(str(allowed))
# print(str(product([[1, 0, -1]], allowed))) # []
# print(str(product([[0, 1, -1]], allowed))) # OK
