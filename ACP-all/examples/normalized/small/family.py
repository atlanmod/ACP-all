# -------------------
# 23/3/2020
# family from Sasikumar2007 page 38
# -------------------

# TODO see relations

from Normalized_OK import * #@UnusedWildImport

# --------------------------
Person = DeclareSort('Person')

table = Normalized_Enumerate()
#table = Enumerate()
# Variables
table.add_variable("X", Person)
table.add_variable("Y", Person)
table.add_variable("Z", Person)
X = table.get_variable(0)
Y = table.get_variable(1)
Z = table.get_variable(2)
# # more 
# X= Const('X', Hospital)
# toubib = Const('toubib', Hospital)
# nounou = Const('nounou', Hospital)
# bob = Const('bob', Patient)

# predicates 
father = Function('father', Person, Person, BoolSort()) 
mother = Function('mother', Person, Person, BoolSort()) 
wife = Function('wife', Person, Person, BoolSort()) 
husband = Function('husband', Person, Person, BoolSort()) 

### 

#p1: If father(X,Y) and wife(Z,X) then mother(Z,Y)
table.add_rule(And(father(X,Y), wife(Z,X)), mother(Z,Y))
#p2: If mother(X,Y) and husband(Z,X) then father(Z,Y) 
table.add_rule(And(mother(X,Y), husband(Z,X)), father(Z,Y))
#p3: If wife(X,Y) then husband(Y,X)
table.add_rule(wife(X,Y), husband(Y,X))
#p4: If husband(X,Y) then wife(Y,X)
table.add_rule(husband(Y,X), wife(X,Y))
#p5: If father(X,Z) and mother(Y,Z) then husband(X,Y) 
table.add_rule(And(father(X,Z), mother(Y,Z)), husband(X,Y)) 
#p6: If father(X,Z) and mother(Y,Z) then wife(Y,X)
table.add_rule(And(father(X,Z), mother(Y,Z)), wife(Y,X)) ### it is redundant !!!
#### ---------------

### -------- analysis 
size = 6
### those in conditions
REQ = [father(X,Y), father(X,Z), mother(X,Y), mother(Y,Z), husband(Z,X), husband(Y,X), wife(X,Y), wife(Z,X)]
ALLOWED = [[-1]*len(REQ)] # etat= 40 transitions= 56
### TODO ya des relations ? 
# REQ = [father(X,Y), father(X,Z), father(Z,Y), mother(X,Y), mother(Y,Z), mother(Z,Y), 
#        husband(Z,X), husband(Y,X), husband(X,Y), wife(X,Y), wife(Y,X), wife(Z,X)]
# definitions OrderedDict([(P_0(X, Y), father(X, Y)), (P_1(Z, X), wife(Z, X)), (P_2(Z, Y), mother(Z, Y)), (P_3(X, Y), mother(X, Y)), (P_4(Z, X), husband(Z, X)), (P_5(Z, Y), father(Z, Y)), (P_6(X, Y), wife(X, Y)), (P_7(Y, X), husband(Y, X)), (P_8(X, Z), father(X, Z)), (P_9(Y, Z), mother(Y, Z)), (P_10(X, Y), husband(X, Y))])
# size= 11 REQ-pos [0, 1, 3, 4, 6, 7, 8, 9] mapping {0: 0, 1: 1, 3: 2, 4: 3, 6: 4, 7: 5, 8: 6, 9: 7}
DENIED = []

table.compute_table(REQ, size, DENIED) # ALLOWED) 
  
#print (str(table))
#print (str(table.get_info()))
table.show_problems()
#table.check_problems(size)
#table.classify_problems()

#table.compare_problems(size, REQ)
# enumerate: found= 32 in 2
# combine: found= 2 in 0

# ======================
# And(wife(X, Y), Not(husband(Y, X))) from 3
# And(Not(wife(X, Y)), husband(Y, X))  from 4

# etat= 40 transitions= 56
#  time= 12 surtout du a prime mais incremental = 0 ?
#  ----------------- The current problems  
# And(Not(wife(X, Y)), husband(Y, X))
# And(wife(X, Y), Not(husband(Y, X)))
#  ----

