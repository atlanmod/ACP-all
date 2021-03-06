# -------------------
# 7/10/2019
# example RBSIM needs predicates not PROP!
# # # R23
# table.add_rule(AGE < 67, Not(Retired))
# # R24
# table.add_rule(AGE >= 67, Retired) #### HERE unsat 
# -----------------------


from Normalized_OK_V2 import * #@UnusedWildImport
#from Enumerate import * #@UnusedWildImport

from time import * #@UnusedWildImport
from math import * #@UnusedWildImport

# --------------------------
Person = DeclareSort('Person')
#Resource = DeclareSort('Resource')

table = Normalized_enumerate()
#table = Enumerate()
table.add_variable("X", Person) # the person
# Variables ordered !
X = table.get_variable(0)

# ---------------- the predicates
# Have Health Insurance
HHI = Function('HHI', Person, BoolSort())  
# Basic Insurance Coverage = ADEQUATE or NOT
BIC = Function('BIC', Person, BoolSort())
# Have Live Insurance
HLI = Function('HLI', Person, BoolSort())
# Should Have Live Insurance
SHLI = Function('SHLI', Person, BoolSort())
Married = Function('Married', Person, BoolSort())
Children = Function('Children', Person, BoolSort())
# Category Of Fund = NONE
COFNone = Function('COFNone', Person, BoolSort())
# Category Of Fund = MONEY MARKET 
COFMoney = Function('COFMoney', Person, BoolSort())
# Category Of Fund = G&I = a mixed growth and income fund
COFGI = Function('COFGI', Person, BoolSort())
# Category Of Fund = CONSERVATIVE GROWTH
COFCons = Function('COFCons', Person, BoolSort())
# Category Of Fund = AGRESSIVE
COFAgressive = Function('COFAgressive', Person, BoolSort())
# Category Of Fund = TAX-FREE
COFTaxFree = Function('COFTaxFree', Person, BoolSort())
# Category Of Fund = INCOME
COFIncome = Function('COFIncome', Person, BoolSort())
# Investment Goal = RETIREMENT 
IGRetired = Function('IGRetired', Person, BoolSort())
# Investment Goal = CHILDREN'S EDUCATION 
IGChildren = Function('IGChildren', Person, BoolSort())
# Investment Goal = HOME OWNERSHIP
IGHome = Function('IGHome', Person, BoolSort())
# Investment Goal = CURRENT INCOME
IGIncome = Function('IGIncome', Person, BoolSort())
# Investment Goal = INVEST SPARE CASH
IGCash = Function('IGCash', Person, BoolSort())
# Risk Tolerance = LOW
RTLow = Function('RTLow', Person, BoolSort())
# Risk Tolerance = MEDIUM
RTMedium = Function('RTMedium', Person, BoolSort())
# Risk Tolerance = HIGH
RTHigh = Function('RTHigh', Person, BoolSort())
# Tax Bracket = HIGH
Tax = Function('Tax', Person, BoolSort())
# Life Stage = RETIRED or NOT
Retired = Function('Retired', Person, BoolSort())
# Pension = NO or YES
Pension = Function('Pension', Person, BoolSort())
# Individual Retirement Account = NO or YES
IRA = Function('IRA', Person, BoolSort())
# Children Headed For College = YES or NO
CHC = Function('CHC', Person, BoolSort())
# Children's Education Already Funded = YES or NO
CEAF = Function('CEAF', Person, BoolSort())
# Own Home
Home = Function('Home', Person, BoolSort())
# Want Home
Want = Function('Want', Person, BoolSort())
# Enjoy Gambling = YES
Gambling = Function('Gambling', Person, BoolSort())
# Budgeting Very Important = YES
Important = Function('Important', Person, BoolSort())
# Worry About Money At Night = YES 
Worry = Function('Worry', Person, BoolSort())
# Budget But Splurge Sometimes = YES
Budget = Function('Budget', Person, BoolSort())
# College Tuition Level = CHEAP
College = Function('College', Person, BoolSort())
# Children Have Scholarship = YES
Scholarship = Function('Scholarship', Person, BoolSort())
# Children Eligible For Loans = YES
Loan = Function('Loan', Person, BoolSort())
# Children Have Trust Fund = YES
Fund = Function('Fund', Person, BoolSort())
# Children Headed For College = YES 
Headed = Function('Headed', Person, BoolSort())

# ---------------- the functions
Age = Function('Age', Person, IntSort()) # Your age
CS = Function('CS', Person, IntSort()) # Current Saving
MS = Function('MS', Person, IntSort()) # Monthly Salary
NoY2R = Function('NoY2R', Person, IntSort()) # Number Of Years To Retirement
AoOC = Function('AoOC', Person, IntSort()) # Age of Oldest Child
AoYC = Function('AoYC', Person, IntSort()) # Age Of Youngest Child 

### only top-level expressions of correct requests
### Change some integer expressions
REQ =   [HHI(X), BIC(X), HLI(X), Married(X), Children(X), AoOC(X) <= 7, AoOC(X) > 7,\
          CS(X) < 6*MS(X), NoY2R(X) < 10, NoY2R(X) >= 10, NoY2R(X) < 20, NoY2R(X) >= 20,\
             Age(X) < 65, Age(X) >= 65, RTLow(X), RTMedium(X), RTHigh(X), Tax(X), Pension(X), \
                           IRA(X), CHC(X), Home(X), Want(X), Gambling(X), Important(X), Worry(X), Budget(X),\
            AoYC(X) < 16, AoYC(X) >= 16, College(X), Scholarship(X), Loan(X), Fund(X), Headed(X)]


# # ---------------- the rules 
# ------------- business rules = 36
# R1 
#table.add_rule(Not(HHI(X)), Not(BIC(X)))
table.add_rule(BIC(X), HHI(X)) # 
# # R2
table.add_rule(And(Not(HLI(X)), SHLI(X)), Not(BIC(X)))
# # R3
table.add_rule(And(HHI(X), HLI(X)), BIC(X))
# # # R4
table.add_rule(Or(Married(X), Children(X)), SHLI(X))

### rules 10 from 22 are the conclusive ones
# # R10
table.add_rule(Not(BIC(X)), COFNone(X))
# # R11
table.add_rule(CS(X) < 6*MS(X), COFMoney(X))
# # R12 
table.add_rule(And(IGRetired(X), NoY2R(X) < 10), COFCons(X))
# # R13
table.add_rule(And(IGRetired(X), NoY2R(X) >= 10, NoY2R(X) < 20), COFGI(X))
# # R14
table.add_rule(And(IGRetired(X), NoY2R(X) >= 20), COFAgressive(X))
# # R15
table.add_rule(And(IGChildren(X), AoOC(X) < 7), COFGI(X))
# # R16
table.add_rule(And(IGChildren(X), AoOC(X) > 7), COFCons(X))
# R17
table.add_rule(IGHome(X), COFGI(X))
# R18
table.add_rule(IGIncome(X), COFIncome(X))
# R19
table.add_rule(And(IGCash(X), RTLow(X)), COFCons(X))
# R20
table.add_rule(And(IGCash(X), RTMedium(X)), COFGI(X))
# R21
table.add_rule(And(IGCash(X), RTHigh(X)), COFAgressive(X))
# R22
table.add_rule(And(IGCash(X), RTMedium(X), Tax(X)), COFTaxFree(X))

# R23
table.add_rule(Age(X) < 65, Not(Retired(X)))
# R24
table.add_rule(Age(X) >= 65, Retired(X)) 
# R31
table.add_rule(And(Not(Pension(X)), IRA(X)), IGRetired(X))
# R32
table.add_rule(And(Headed(X), Not(CEAF(X))), IGChildren(X))
# R33
table.add_rule(And(Not(Home(X)), Want(X)), IGHome(X))
# R34
table.add_rule(Retired(X), IGIncome(X))
# R35 
table.add_rule(And(Or(Home(X), Not(Want(X))), Or(Pension(X), IRA(X)), Or(Not(Children(X)), CEAF(X)), Not(Retired(X))), IGCash(X))
# R41
table.add_rule(Gambling(X), RTHigh(X))
# R42
table.add_rule(Important(X), RTLow(X))
# R43
table.add_rule(Worry(X), RTLow(X))
# R44
table.add_rule(Budget(X), RTMedium(X))
# R45
table.add_rule(And(Children(X), AoYC(X) < 16), Headed(X))
# R46
table.add_rule(And(Children(X), AoYC(X) >= 16), Not(Headed(X)))
# R47
table.add_rule(Not(Children(X)), Not(Headed(X)))
# R51
table.add_rule(College(X), CEAF(X))
# R52
table.add_rule(Scholarship(X), CEAF(X))
# R53
table.add_rule(Loan(X), CEAF(X))
# R54
table.add_rule(Fund(X), CEAF(X))
# R55
table.add_rule(And(Not(Fund(X)), Not(Loan(X)), Not(Scholarship(X))), Not(CEAF(X)))
### -------- 

# ---------------- the rules 
# some implicit rules = 21 between !REQ
# others ? not really obvious
# COF* are disjunct seems natural
table.add_rule(And(COFNone(X), COFMoney(X)), False) 
table.add_rule(And(COFNone(X), COFGI(X)), False) 
table.add_rule(And(COFNone(X), COFCons(X)), False) 
table.add_rule(And(COFNone(X), COFAgressive(X)), False) 
table.add_rule(And(COFNone(X), COFTaxFree(X)), False) 
table.add_rule(And(COFNone(X), COFIncome(X)), False) 
# 
table.add_rule(And(COFMoney(X), COFGI(X)), False) 
table.add_rule(And(COFMoney(X), COFCons(X)), False) 
table.add_rule(And(COFMoney(X), COFAgressive(X)), False) 
table.add_rule(And(COFMoney(X), COFTaxFree(X)), False) 
table.add_rule(And(COFMoney(X), COFIncome(X)), False) 
#
table.add_rule(And(COFGI(X), COFCons(X)), False) 
table.add_rule(And(COFGI(X), COFAgressive(X)), False) 
table.add_rule(And(COFGI(X), COFTaxFree(X)), False) 
table.add_rule(And(COFGI(X), COFIncome(X)), False) 
#
table.add_rule(And(COFCons(X), COFAgressive(X)), False) 
table.add_rule(And(COFCons(X), COFTaxFree(X)), False)
table.add_rule(And(COFCons(X), COFIncome(X)), False)
# 
table.add_rule(And(COFAgressive(X), COFTaxFree(X)), False) 
table.add_rule(And(COFAgressive(X), COFIncome(X)), False) 
#
table.add_rule(And(COFTaxFree(X), COFIncome(X)), False) 
## ------------
### -------- analysis 
#======================================analysis
start = process_time()
size = 36 # 
### with some explicit unsafe !REQ
#size = 57  # 36 + 21

#print (str(table))

table.compute_table(REQ, size)
# print ("size= " + str(size) + " time= " + str(floor(process_time()-start)))
#     
# print (str(table.get_info()))
# table.show_problems()
# table.check_problems(size)
#  
# #table.compare_problems(size, REQ)

### ============= Enumerate
#  level  ----------- 2
#  problems [And(BIC(X), Not(HHI(X))), And(Not(Children(X)), Headed(X)), And(Not(RTLow(X)), Important(X)), And(Not(RTLow(X)), Worry(X)), And(Not(RTMedium(X)), Budget(X)), And(Not(RTHigh(X)), Gambling(X)), And(Headed(X), Not(AoYC(X) < 16)), And(Headed(X), AoYC(X) >= 16)]
#  time  763 checking 2048
