# -------------------
# 4/4/2020
# Test Adi2009 
# -------------------

from BDDFromDD import * #@UnusedWildImport
#from Normalized_BDD import * #@UnusedWildImport
#from Normalized_BDD import * #@UnusedWildImport

# --------------------------
Patient = DeclareSort('Patient')
Hospital = DeclareSort('Hospital')

table = BDD_Build()
#table = Normalized_Enumerate()
#table = Normalized_BDD()

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

#table.compute_table(REQ, size, ALLOWED)
  
#print (str(table))
#print (str(table.get_info()))
#table.show()
#print(str(table.normalized_problems))
#table.show_problems()
#table.classify_problems()
#table.check_problems(size)

# #### ========= test BDDFromZ3
# table.classify(size)
# table.check_simplified(size)
# table.parse_rules()
# table.set_REQ(REQ)
# start = process_time()
# BDD = table.convert()
# print ("time to BDD " + str(floor(process_time()-start)))
# #print(str(BDD.to_dot()))


#### tests ======================
# renameds = bdd2expr(table.normalized_problems, False)
# #print(str(renameds._encode_dnf())) ### ???
# #print(str(renameds.to_ast())) ### pas causant
# print(str(renameds.is_dnf())) ### true
# print(str(renameds.is_cnf())) ### false
# print(str(renameds.complete_sum())) ### all prime implicant
# print(str(type(renameds.complete_sum()))) ### <class 'pyeda.boolalg.expr.OrOp'>
# ### how to get children ? or args 
# print(str(type(renameds.node))) ### <class 'exprnode.ExprNode'> dans lib ? exprnode.cpython
# # exprnode.or_(*xs)
# print(str(renameds.xs)) ### <class 'exprnode.ExprNode'> dans lib ? exprnode.cpython 
# # (And(VARS[0], ~VARS[1], ~VARS[2], VARS[3]), And(VARS[0], VARS[1], ~VARS[2]))
# print(str(type(renameds.xs))) ### <class 'tuple'>
# renameds = bdd2expr(table.normalized_problems, False).xs
# print(str(renameds))
# ### distinguish VAR from ~VAR ? [<class 'pyeda.boolalg.expr.Variable'>, <class 'pyeda.boolalg.expr.Complement'>,
# one_and = renameds[1].xs
# print(str([type(N) for N in one_and]))
# ### Complement accessing inner variable ?
# comp = one_and[2]
# print(str(comp) + " " + str(type(comp)) + " " + str(comp.node)) # <exprnode.ExprNode object at 0x1030a6810>
# ### il s'agit d'un recodage depuis .data() en string et donc l'indice apparait 
# ### mais comment l'avoir ?
# #print(str(comp.indices)) # (1, ) ### but only for Variable
# ### for Complement invert/Not or ?
# print(str(comp.__invert__())) ### OK inversion BUT how to do that directly ?
# print(str(comp.node.id())) # 140534908345200
# print(str(comp.node.data())) # -2 encoding minus variable id ?
# ### map idvariable -> varindices ?
# ### Rapport entre Complement et NotOp ??? .x() marcherait ?
# 
# 
# from pyeda.boolalg.expr import Variable, Complement
# ### try conversion pyeda DNF -> Z3 possible 
# res = []
# for renamed in renameds:
#     res.append(And(*[table.REQ[N.indices[0]] if (isinstance(N, Variable)) 
#                      else Not(table.REQ[N.__invert__().indices[0]])
#                      for N in renamed.xs]))
# print(str(res))
