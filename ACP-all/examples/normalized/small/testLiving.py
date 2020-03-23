# -------------------
# 23/3/2020
# Test Living from  http://hssc.sla.mdx.ac.uk/staffpages/rvb/teaching/BIS3226/hand03.pdf
# -------------------

from Normalized_OK import * #@UnusedWildImport

# a notion of day and also of permission
# IF   saturday OR sunday                     THEN   go to cinema
# IF   NOT (saturday OR sunday)               THEN   go to work
# IF   go to cinema                           THEN   go outside
# IF   go to work AND NOT at work             THEN   go outside
# IF   NOT (can go outside)                   THEN   stay home
# IF   good weather                           THEN   can go outside
# IF   raining                                THEN   have an umbrella
# IF   raining AND have an umbrella           THEN   can go outside

# --------------------------
Day = DeclareSort('Day')
Activity = DeclareSort('Activity')
Object = DeclareSort('Object')
Weather = DeclareSort('Weather')

table = Normalized_Enumerate()
# Variables
table.add_variable("X", Day)
table.add_variable("Y", Activity)
X = table.get_variable(0)
Y = table.get_variable(1)
# more 
work = Const('work', Activity)
cinema = Const('cinema', Activity)
outside = Const('outside', Activity)
home = Const('home', Activity)
umbrella = Const('umbrella', Object)
goodweather = Const('goodweather', BoolSort())
raining = Const('raining', BoolSort())

saturday = Function('saturday', Day, BoolSort()) 
sunday = Function('sunday', Day, BoolSort())     
goto = Function('goto', Activity, BoolSort())
doing = Function('doing', Activity, BoolSort())
own = Function('own', Object, BoolSort())
cango = Function('cango', Activity, BoolSort())

table.add_rule(Or(saturday(X), sunday(X)), goto(cinema))
table.add_rule(Not(Or(saturday(X), sunday(X))), goto(work))
table.add_rule(goto(cinema), goto(outside))
table.add_rule(And(goto(work), Not(doing(work))), goto(outside))
### Action => permit action
table.add_rule(goto(Y), cango(Y))
table.add_rule(Not(cango(outside)), doing(home))
table.add_rule(goodweather, cango(outside))
table.add_rule(raining, own(umbrella))
table.add_rule(And(raining, own(umbrella)), cango(outside))
#### --------------- ### NO PROBLEM

### --------------- essai ajout problems ?

### -------- analysis 
size = 9
REQ = [saturday(X), sunday(X), goodweather, raining] # dico ordering
#ALLOWED = [[-1]*len(REQ)] # etat= 17 transitions= 18
# ALLOWED = [[0, 0, -1, -1], [0, 1, -1, -1], [1, 0, -1, -1]] # not sunday and saturday
# # and not both 
# ALLOWED = [[0, 0, 0, 0], [0, 1, 0, 0], [1, 0, 0, 0],
#            [0, 0, 1, 0], [0, 1, 1, 0], [1, 0, 1, 0],
#            [0, 0, 0, 1], [0, 1, 0, 1], [1, 0, 0, 1]] # etat= 15 transitions= 16
# definitions OrderedDict([(P_0(X), saturday(X)), (P_1(X), sunday(X)), (P_2(cinema), goto(cinema)), (P_3(work), goto(work)), (P_4(outside), goto(outside)), (P_5(work), doing(work)), (P_6(Y), goto(Y)), (P_7(Y), cango(Y)), (P_8(outside), cango(outside)), (P_9(home), doing(home)), (goodweather, goodweather), (raining, raining), (P_10(umbrella), own(umbrella))])
# size= 13 REQ-pos [0, 1, 10, 11] mapping {0: 0, 1: 1, 10: 2, 11: 3}
ALLOWED = gener_allowed2([[1, 1, -1, -1], [-1, -1, 1, 1]], 4)
#print(str(ALLOWED))
# 
#NOTRELREQ = []

# table.classify(size)
# table.check_simplified(size)
# table.parse_rules()
# table.check_renamed()
# table.normalize()
# table.compute_dnf()

table.compute_table(REQ, size, ALLOWED) #, NOTRELREQ)
  
#print (str(table))
# print (str(table.get_info()))
# #table.show()
table.show_problems()
# table.check_problems(size)
#table.classify_problems()

#table.compare_problems(size, REQ)


