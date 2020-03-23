# -------------------
# 23/3/2020
## inpired from termostat control system in
# Logical Foundations for Rule-Based Systems De Antoni Ligeza
# or in papers from G. Nalepa
# -------------------

from Normalized_OK import * #@UnusedWildImport

# --------------------------
Day = DeclareSort('Day')
Weather = DeclareSort('Weather')
Season = DeclareSort('Season')
Month = DeclareSort('Month')

table = Normalized_Enumerate()
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

### add some explicit unsafe rules for exclusion (21)
table.add_rule(And(monday(X), tuesday(X)), False)
table.add_rule(And(monday(X), wednesday(X)), False)
table.add_rule(And(monday(X), thursday(X)), False)
table.add_rule(And(monday(X), friday(X)), False)
table.add_rule(And(monday(X), saturday(X)), False)
table.add_rule(And(monday(X), sunday(X)), False)
table.add_rule(And(tuesday(X), wednesday(X)), False)
table.add_rule(And(tuesday(X), thursday(X)), False)
table.add_rule(And(tuesday(X), friday(X)), False)
table.add_rule(And(tuesday(X), saturday(X)), False)
table.add_rule(And(tuesday(X), sunday(X)), False)
table.add_rule(And(wednesday(X), thursday(X)), False)
table.add_rule(And(wednesday(X), friday(X)), False)
table.add_rule(And(wednesday(X), saturday(X)), False)
table.add_rule(And(wednesday(X), sunday(X)), False)
table.add_rule(And(thursday(X), friday(X)), False)
table.add_rule(And(thursday(X), saturday(X)), False)
table.add_rule(And(thursday(X), sunday(X)), False)
table.add_rule(And(friday(X), saturday(X)), False)
table.add_rule(And(friday(X), sunday(X)), False)
table.add_rule(And(saturday(X), sunday(X)), False)
### for seasons should imply month exclusivity ? no only for group (6)
table.add_rule(And(season(X, spring), season(X, summer)), False)
table.add_rule(And(season(X, spring), season(X, autumn)), False)
table.add_rule(And(season(X, spring), season(X, winter)), False)
table.add_rule(And(season(X, summer), season(X, autumn)), False)
table.add_rule(And(season(X, summer), season(X, winter)), False)
table.add_rule(And(season(X, autumn), season(X, winter)), False)
### thus may be sufficient intra season
### hence rather than 12*11/2=66 we have 4*3+6=18
table.add_rule(And(month(X, december), month(X, january)), False)
table.add_rule(And(month(X, december), month(X, february)), False)
table.add_rule(And(month(X, january), month(X, february)), False)
table.add_rule(And(month(X, march), month(X, april)), False)
table.add_rule(And(month(X, march), month(X, may)), False)
table.add_rule(And(month(X, april), month(X, may)), False)
table.add_rule(And(month(X, june), month(X, july)), False)
table.add_rule(And(month(X, june), month(X, august)), False)
table.add_rule(And(month(X, july), month(X, august)), False)
table.add_rule(And(month(X, september), month(X, october)), False)
table.add_rule(And(month(X, september), month(X, november)), False)
table.add_rule(And(month(X, october), month(X, november)), False)
# ----

### -------- analysis 
start = process_time()
size = 18 
#size =  18 + 21 + 18 # = 57

REQ = [monday(X), tuesday(X), wednesday(X), thursday(X), friday(X), saturday(X), sunday(X), #[0 .. 6]
    (time(X) >= 9),  (time(X) < 17), (time(X) >= 0), (time(X) < 9), (time(X) >= 17), (time(X) < 24), #[7 .. 12]
       month(X, january), month(X, february), month(X, december), month(X, march), month(X, april), month(X, may),
        month(X, june), month(X, july), month(X, august), month(X, september), month(X, october),
         month(X, november)] # [13 .. 24]
ALLOWED = [[-1]*len(REQ)] #
# some of the day relations
# exclu = gener_exclusive([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), 
#                          (2, 3), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 7), (4, 5), (4, 6), (5, 6)], len(REQ), (1, 1)) 
# exclu1 = gener_exclusive([(9, 9), (12, 12), (8, 11)], len(REQ), (0, 0)) # # Not(0 <= time(X)) # Not(time(X) < 24) # Not(time(X) < 17) # Not(time(X) >= 24) 
# nexclu = gener_exclusive([(7, 8), (7, 11)] , len(REQ), (0, 0)) # Not(9 <= time(X)) & Not(time(X) < 17) # Not(9 <= time(X)) & Not(time(X) <= 17)
# exclu2 = gener_exclusive([(7, 10), (8, 11)] , len(REQ), (1, 1)) # (9 <= time(X)) (time(X) < 9) # (time(X) < 17), (17 <= time(X)),            
# excluD = [0, 0, 0, 0, 0, 0, 0] + [-1]*(25-7) # exhaustive days
# excluM = [-1]*13 + [0]*12 # exhaustive months
# ALLOWED = gener_allowed2(exclu + exclu1 + nexclu + exclu2 + [excluD] + [excluM], len(REQ)) 
### will find no problems ?

table.compute_table(REQ, size, ALLOWED)

print ("size= " + str(size) + " time= " + str(floor(process_time()-start)))
# print (str(table))
print (str(table.get_info()))
#table.show()
table.show_problems()
#table.check_problems(size)

### many explicit unsafe not too much a problem since
### eliminated by the initial_problems
### and time is really smaller

#table.compare_problems(REQ, size)
