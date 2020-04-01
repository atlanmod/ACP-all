#### test package BDD 
from pyeda.inter import *
from functools import reduce

### ---------
# #f = expr("a & b | a & c | b & c")
# #f = expr("a & b | a & ~b | a & c")
# # print(f) # Or(And(a, b), And(a, c), And(b, c))
# # f = expr2bdd(f)
# # print(str(f)) # no rep TODO trouver infos mesure ou 
# # print(str(f.to_dot()))
# f1 = expr2bdd(expr("a & b"))
# f2 = expr2bdd(expr("a & c"))
# f = f1.__and__(f2)
# print(str(f.to_dot()))

#X1 = bddvar('P_1(h)') # NO expected name to match [a-zA-Z][a-zA-Z0-9_]*, got P_1(h)
#X1 = bddvar("P_1(h)") # NO expected name to match [a-zA-Z][a-zA-Z0-9_]*, got P_1(h)
#print(str(X1))
# 
# X = bddvars('x', 4)
# print(str(X)) # farray([x[0], x[1], x[2], x[3]])
# exp = VAR[0] &   ~VAR[1] # TODO prefixe ?
# print(str(exp.to_dot()))
### autre moyen voir le code source The :mod:`pyeda.boolalg.bdd`
### exp = VAR[0].__and__(VAR[1].__invert__()) of course BUT Binary

# -------------------
# 26/3/2020
# Test Adi2009 
# -------------------

from Normalized_OK import * #@UnusedWildImport
from pyeda.boolalg.bdd import BDDNODEONE, BDDNODEZERO

# --------------------------
Patient = DeclareSort('Patient')
Hospital = DeclareSort('Hospital')

table = Normalized_Enumerate()
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

table.classify(size)
table.check_simplified(size)
table.parse_rules()
#table.check_renamed()
#table.normalize() but convert in binary 
print(str(table.definitions))
table.set_REQ(REQ)
table.compute_unsafe_problems() 
table.tactic_conversion()

print(str(table))
#### creation des variables
VAR = bddvars('VAR', len(table.definitions))
# # exp = VAR[0] &   ~VAR[1]
# exp = VAR[0].__and__(VAR[1].__invert__(), VAR[2]) 
# print(str(exp.to_dot()))
### TODO de là apres tactic à un stade ou un autre on peut créer 
### les BDD au moins de réductions ?
#print(str(table.binary)) # ou allred
# tmp = []
# for I in range(6):
#     if (table.binary[0][I] == 0):
#         tmp.append(VAR[I].__invert__())
#     elif   (table.binary[0][I] == 1):
#         tmp.append(VAR[I])
# res = reduce(lambda a,b: a.__and__(b), tmp)
# print(str(res.to_dot()))

### test renamed BDD : subtituer definitions[I] -> VAR[I] puis BDD
### peut-etre meme +simple apres normalize ?

### normalization could simplify it
def convert_BDD (keys, exp):
    #print("rule= " + str(exp))
    if isinstance(exp, bool):
        if (exp.is_true()):
            return BDDNODEONE
        elif (exp.is_false()):
            return BDDNODEZERO
    elif (is_expr(exp)):
        if (is_app(exp)):
            op = exp.decl().kind()
            if (op == Z3_OP_AND):
                res = [convert_BDD(keys, X) for X in exp.children()]
                return reduce(lambda a,b: a.__and__(b), res)
            elif (op == Z3_OP_OR):
                res = [convert_BDD(keys, X) for X in exp.children()]
                return reduce(lambda a,b: a.__or__(b), res)
            elif (op == Z3_OP_NOT):
                return convert_BDD(keys, exp.children()[0]).__invert__() 
            elif (op == Z3_OP_IMPLIES): # TODO ?
                return  reduce(lambda a,b: a.__or__(b), 
                               [convert_BDD(keys, exp.children()[0]).__invert__(), convert_BDD(keys, exp.children()[1])]) 
            else:
                # TODO VAR[I] may be better with P_(I, ...) ...
                return VAR[keys.index(exp)]                          
        else:
            print ("convert_BDD missing ??? " + str(exp))
    # --- end if
    else: # it should be a rule
        return  reduce(lambda a,b: a.__or__(b), 
                       [convert_BDD(keys, exp.get_cond()).__invert__(), convert_BDD(keys, exp.get_conc())]) 
# --- convert_BDD

#BDD = BDDNODEONE # True
#for rule in table.renamed:

BDD = reduce(lambda a,b: a.__and__(b), [convert_BDD(list(table.definitions.keys()), R) for R in table.renamed])
# --- 


#print(str(table.renamed[0]))
# BDD = convert_BDD(list(table.definitions.keys()), table.renamed[0])
#BDD = convert_BDD(list(table.definitions.keys()), table.renamed[0].get_cond())
#BDD = convert_BDD(list(table.definitions.keys()), table.renamed[0].get_conc())
# BDD = convert_BDD(list(table.definitions.keys()), table.renamed[1].get_conc())
#BDD = convert_BDD(list(table.definitions.keys()), list(table.definitions.keys())[5])
#BDD = convert_BDD(list(table.definitions.keys()), Or(Not(list(table.definitions.keys())[5]), list(table.definitions.keys())[0]))
print(str(BDD.to_dot()))


# #table.compare_problems(size, REQ)
# #### test BDD
# table.classify(size)
# table.check_simplified(size)
# table.parse_rules()
# table.set_REQ(REQ)
# start = process_time()
# #BDD = table.convert()
# #print ("time to BDD " + str(floor(process_time()-start)))
# #print(str(BDD.to_dot()))
# 
# 
# ### test conversion 
# table.VARS = bddvars('VARS', len(table.definitions))
# table.KEYS = list(table.definitions.keys()) 
# # binary = [-1]*len(table.REQ) if empty ???
# binary = [1]*len(table.REQ) # 0s
# #binary = [0]*len(table.REQ) # 0s
# binary = [1, 0, 0, 1, 0, 1, 0, -1, -1, 0, 1, 0] + [-1]*(len(table.REQ) - 12) # 0s
# tmp = []
# for I in range(len(table.REQ)):
#     if (binary[I] == 0):
#         tmp.append(table.VARS[I].__invert__())
#     elif   (binary[I] == 1):
#         tmp.append(table.VARS[I])
# res = reduce(lambda a,b: a.__and__(b), tmp)
# print ("conversion time  " + str(floor(process_time()-start)))
# print(str(res.to_dot()))

#print(str(minimizing(product([[0, -1, -1, -1], [-1, 0, -1, -1], [-1, -1, 1, -1]], [[0, -1, -1, -1], [-1, -1, 1, -1], [-1, -1, -1, 0]]))))
# table.convert2BDD([1, 0, -1, 1, 0])
bdd1 = table.convert2BDD([0, 1, 1, 0])
# bdd2 = table.convert2BDD([-1, 0, -1, -1])
# #bdd = bdd1 | bdd2 ### seems to works
# bdd = bdd1.__or__(bdd2) ### idem
# print(str(bdd.to_dot()))
# bdd = table.convert_or([[0, -1, -1, -1], [-1, 0, -1, -1], [-1, -1, 1, -1], [0, -1, -1, -1]])
print(str(bdd1.satisfy_count()) + " " + str(bdd1.satisfy_one())) ### because of and-term only one
### thus translation into renamed will be simple
var0 = list(bdd1.satisfy_one().keys())[3]
print(str(type(var0)) + " " + str(var0.indices)) # <class 'pyeda.boolalg.bdd.BDDVariable'>
### and indices seems that
#print(str(type(table.VARS))) # <class 'pyeda.boolalg.bfarray.farray'>
#print(str(table.VARS[2].uniqid))
table.bdd2renamed(bdd1)
# table.bdd2renamed(bdd1)
# from pyeda.inter import *
# print(str(isinstance(BDDNODEONE, BinaryDecisionDiagram))) # False
# #print(str(bdd1.box(0).is_zero())) # TRUE
# print(str(BinaryDecisionDiagram.box(0).is_zero())) # TRUE
# print(str(isinstance(BinaryDecisionDiagram.box(0), BinaryDecisionDiagram))) # TRUE
# print(str(table.convert_or(ALLOWED).to_dot())) # graph BDD { n4534798544 [label=1,shape=box]; }
# print(str(table.convert_or([]).to_dot())) # graph BDD { n4421095312 [label=0,shape=box]; }
# print(str(table.convert2BDD([-1]*4).to_dot()))
# print(str(table.convert2BDD([-1]*4).is_one())) # TRUE
#print(str(bdd2.inputs)) # (VARS[1],)
