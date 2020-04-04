# -------------------
# 2/4/2020
## inpired from termostat control system in
# Logical Foundations for Rule-Based Systems De Antoni Ligeza
# or in papers from G. Nalepa
# -------------------

#from Normalized_OK import * #@UnusedWildImport
#from Normalized_BDD import * #@UnusedWildImport
from BDDFromZ3 import * #@UnusedWildImport

# --------------------------
Day = DeclareSort('Day')
Weather = DeclareSort('Weather')
Season = DeclareSort('Season')
Month = DeclareSort('Month')

#table = Normalized_Enumerate()
# table = Normalized_BDD()
table = BDD_Build()
# Variables
table.add_variable("X", Day)
X = table.get_variable(0)

# constants [may be reuse existing ?]
winter = Const('winter', Season)
spring = Const('spring', Season)
summer = Const('summer', Season)
autumn = Const('autumn', Season)
january = Const('january', Month)
february = Const('february', Month)
march = Const('march', Month)
april = Const('april', Month)
may = Const('may', Month)
june = Const('june', Month)
july = Const('july', Month)
august = Const('august', Month)
september = Const('september', Month)
october = Const('october', Month)
november = Const('november', Month)
december = Const('december', Month)

monday = Function('monday', Day, BoolSort()) 
tuesday = Function('tuesday', Day, BoolSort()) 
wednesday = Function('wednesday', Day, BoolSort()) 
thursday = Function('thursday', Day, BoolSort()) 
friday = Function('friday', Day, BoolSort()) 
saturday = Function('saturday', Day, BoolSort())     
sunday = Function('sunday', Day, BoolSort())     
workday = Function('workday', Day, BoolSort())     
weekend = Function('weekend', Day, BoolSort())     
time = Function('time', Day, IntSort())  
operation = Function('operation', Day, BoolSort()) # is business hours
settemp =  Function('settemp', Day, IntSort(), BoolSort())
season = Function('season', Day, Season, BoolSort())     
month = Function('month', Day, Month, BoolSort())     

### --------- the rules (18)
table.add_rule(Or(monday(X), tuesday(X), wednesday(X), thursday(X), friday(X)), workday(X)) # R1
table.add_rule(Or(saturday(X), sunday(X)), weekend(X)) #R2
table.add_rule(And(workday(X), (9 <= time(X)), (time(X) < 17)), operation(X)) #R3
table.add_rule(And(workday(X), (0 <= time(X)), (time(X) < 9)), Not(operation(X))) #R4
table.add_rule(And(workday(X), (17 <= time(X)), (time(X) < 24)), Not(operation(X))) #R5
table.add_rule(weekend(X), Not(operation(X))) #R6
table.add_rule(Or(month(X, january), month(X, february), month(X, december)), season(X, winter)) #R7
table.add_rule(Or(month(X, march), month(X, april), month(X, may)), season(X, spring)) #R8
table.add_rule(Or(month(X, june), month(X, july), month(X, august)), season(X, summer)) #R9
table.add_rule(Or(month(X, september), month(X, october), month(X, november)), season(X, autumn)) #R10
table.add_rule(And(season(X, spring), operation(X)), settemp(X, 20)) #R11
table.add_rule(And(season(X, spring), Not(operation(X))), settemp(X, 15)) #R12
table.add_rule(And(season(X, summer), operation(X)), settemp(X, 15)) #R13
table.add_rule(And(season(X, summer), Not(operation(X))), settemp(X, 10)) #R14
table.add_rule(And(season(X, autumn), operation(X)), settemp(X, 20)) #R15
table.add_rule(And(season(X, autumn), Not(operation(X))), settemp(X, 15)) #R16
table.add_rule(And(season(X, winter), operation(X)), settemp(X, 25)) #R17
table.add_rule(And(season(X, winter), Not(operation(X))), settemp(X, 20)) #R18
#### ---------------

### -------- analysis 
start = process_time()
size = 18 
#size =  18 + 21 + 18 # = 57

REQ = [monday(X), tuesday(X), wednesday(X), thursday(X), friday(X), saturday(X), sunday(X), #[0 .. 6]
    (time(X) >= 9),  (time(X) < 17), (time(X) >= 0), (time(X) < 9), (time(X) >= 17), (time(X) < 24), #[7 .. 12]
       month(X, january), month(X, february), month(X, december), month(X, march), month(X, april), month(X, may),
        month(X, june), month(X, july), month(X, august), month(X, september), month(X, october),
         month(X, november)] # [13 .. 24]
# Ordering REQ [monday(X), tuesday(X), wednesday(X), thursday(X), friday(X), saturday(X), sunday(X), time(X) >= 9, time(X) < 17, time(X) >= 0, time(X) < 9, time(X) >= 17, time(X) < 24, month(X, january), month(X, february), month(X, december), month(X, march), month(X, april), month(X, may), month(X, june), month(X, july), month(X, august), month(X, september), month(X, october), month(X, november)]

#ALLOWED = [[-1]*len(REQ)] #

### relations à composer 
days = [((0, 1, 2, 3, 4, 5, 6), [[1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]])]
time = [((7, 8), [[0, 0]]), ((7, 11), [[0, 0]]), ((9, 9), [[0, 0]]), ((12, 12), [[0, 0]]), ((8, 11), [[0, 0]])]
time += [((7, 10), [[1, 1]]), ((8, 11), [[1, 1]])] 

### TODO voir aussi replace unsafe explicit

### month: are exclusive similar to days

ALLOWED = gener_allowed(days+time, len(REQ))
#print(str(len(ALLOWED)) + " " + str(ALLOWED))

#table.compute_table(REQ, size, ALLOWED)

# print (str(table))
#print (str(table.get_info()))
#table.show()
#table.show_problems()
#table.check_problems(size)

### many explicit unsafe not too much a problem since
### eliminated by the initial_problems
### and time is really smaller

#table.compare_problems(REQ, size)

#### ========= test BDD
table.classify(size)
table.check_simplified(size)
table.parse_rules()
table.set_REQ(REQ)
start = process_time()
BDD = table.convert()
print ("time to BDD " + str(floor(process_time()-start)))
#print(str(BDD.to_dot()))


# #####some of the day relations OLD
# exclu = gener_exclusive([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), 
#                          (2, 3), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 7), (4, 5), (4, 6), (5, 6)], len(REQ), (1, 1)) 
# exclu1 = gener_exclusive([(9, 9), (12, 12), (8, 11)], len(REQ), (0, 0)) # # Not(0 <= time(X)) # Not(time(X) < 24) # Not(time(X) < 17) # Not(time(X) >= 24) 
# nexclu = gener_exclusive([(7, 8), (7, 11)] , len(REQ), (0, 0)) # Not(9 <= time(X)) & Not(time(X) < 17) # Not(9 <= time(X)) & Not(time(X) <= 17)
# exclu2 = gener_exclusive([(7, 10), (8, 11)] , len(REQ), (1, 1)) # (9 <= time(X)) (time(X) < 9) # (time(X) < 17), (17 <= time(X)),            
# excluD = [0, 0, 0, 0, 0, 0, 0] + [-1]*(25-7) # exhaustive days
# excluM = [-1]*13 + [0]*12 # exhaustive months
# ALLOWED = gener_allowed2(exclu + exclu1 + nexclu + exclu2 + [excluD] + [excluM], len(REQ)) 

