# -------------------
# 25/3/2020
# example RBSIM needs predicates not PROP!
# # # R23
# table.add_rule(AGE < 67, Not(Retired))
# # R24
# table.add_rule(AGE >= 67, Retired) #### HERE unsat 
# -----------------------

from Normalized_OK import * #@UnusedWildImport

from time import * #@UnusedWildImport
from math import * #@UnusedWildImport

# --------------------------
Person = DeclareSort('Person')
#Resource = DeclareSort('Resource')

table = Normalized_Enumerate()
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
# Children Headed For College = YES or NO  TODO revoir not used ????
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

## ------------
### only top-level expressions of correct requests 
### TODO ordering CHC(X), strange ?
REQ = [BIC(X), HHI(X), HLI(X), Married(X), Children(X), CS(X) < 6 * MS(X), 
        NoY2R(X) < 10, NoY2R(X) >= 10, NoY2R(X) < 20, NoY2R(X) >= 20,  # 6 7 8 9
         AoOC(X) < 7, AoOC(X) > 7, # 10 11
         RTLow(X), RTMedium(X), RTHigh(X), Tax(X), 
         Age(X) < 65, Age(X) >= 65, Pension(X), # 16 17
         IRA(X), Headed(X), Home(X), Want(X), Gambling(X), Important(X), Worry(X), Budget(X),
         AoYC(X) < 16, AoYC(X) >= 16, # 27 28
         College(X), Scholarship(X), Loan(X), Fund(X)]

#definitions OrderedDict([(P_0(X), BIC(X)), (P_1(X), HHI(X)), (P_2(X), HLI(X)), (P_3(X), SHLI(X)), (P_4(X), Married(X)), (P_5(X), Children(X)),
#  (P_6(X), COFNone(X)), (P_7(X), CS(X) < 6*MS(X)), (P_8(X), COFMoney(X)), (P_9(X), IGRetired(X)), (P_10(X), NoY2R(X) < 10), (P_11(X), COFCons(X)),
# (P_12(X), NoY2R(X) >= 10), (P_13(X), NoY2R(X) < 20), (P_14(X), COFGI(X)), (P_15(X), NoY2R(X) >= 20), (P_16(X), COFAgressive(X)), (P_17(X), IGChildren(X)), 
# (P_18(X), AoOC(X) < 7), (P_19(X), AoOC(X) > 7), (P_20(X), IGHome(X)), (P_21(X), IGIncome(X)), (P_22(X), COFIncome(X)), (P_23(X), IGCash(X)), 
# (P_24(X), RTLow(X)), (P_25(X), RTMedium(X)), (P_26(X), RTHigh(X)), (P_27(X), Tax(X)), (P_28(X), COFTaxFree(X)), (P_29(X), Age(X) < 65), (P_30(X), Retired(X)), 
# (P_31(X), Age(X) >= 65), (P_32(X), Pension(X)), (P_33(X), IRA(X)), (P_34(X), Headed(X)), (P_35(X), CEAF(X)), (P_36(X), Home(X)), (P_37(X), Want(X)), 
# (P_38(X), Gambling(X)), (P_39(X), Important(X)), (P_40(X), Worry(X)), (P_41(X), Budget(X)), (P_42(X), AoYC(X) < 16), (P_43(X), AoYC(X) >= 16), (P_44(X), 
# College(X)), (P_45(X), Scholarship(X)), (P_46(X), Loan(X)), (P_47(X), Fund(X))])
#size= 48 REQ-pos [0, 1, 2, 4, 5, 7, 10, 12, 13, 15, 19, 24, 25, 26, 27, 29, 31, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47] mapping {0: 0, 1: 1, 2: 2, 4: 3, 5: 4, 7: 5, 10: 6, 12: 7, 13: 8, 15: 9, 19: 10, 24: 11, 25: 12, 26: 13, 27: 14, 29: 15, 31: 16, 32: 17, 33: 18, 34: 19, 36: 20, 37: 21, 38: 22, 39: 23, 40: 24, 41: 25, 42: 26, 43: 27, 44: 28, 45: 29, 46: 30, 47: 31}
#ALLOWED = [[-1]*len(REQ)]
exclu = gener_exclusive([(6, 7), (8, 9), (10, 11), (10, 9), (16, 17), (27, 28)], len(REQ), (1, 1)) #
exclu1 = gener_exclusive([(6, 8), (6, 9), (7, 8), (7, 16)], len(REQ), (1, 0)) #
exclu2 = gener_exclusive([(7, 9) ], len(REQ), (0, 1)) #
exclu3 = gener_exclusive([(6, 7), (8, 9)], len(REQ), (0, 0)) #
ALLOWED = gener_allowed2(exclu+exclu1+exclu2+exclu3, len(REQ)) # 
### TODO add it
# NOTRELREQ = []

### -------- analysis 
#======================================analysis
start = process_time()
size = 36 # 

table.compute_table(REQ, size, ALLOWED) #, NOTRELREQ)
# print ("size= " + str(size) + " time= " + str(floor(process_time()-start)))
#     
# print (str(table.get_info()))
table.show_problems()
# table.check_problems(size)

### TODO patine ? V1= time= 1117
# 12/3/2020 but allowed wrong but give a "maximal idea"
# GREEN nodes= 13 ---------- build finished now collecting 1106
# count= 36240
# count= 82553
# count= 90310
# count= 106493
# count= 72463
# count= 283230
# count= 9222
# count= 53229
# count= 25997
# count= 4
# count= 3
# count= 5
# count= 6
# etat= 416714 transitions= 698750 #  time= 1908
#### avec ALLOWED better
# GREEN nodes= 12 ---------- build finished now collecting 79
# count= 3121
# count= 6277
# count= 6747
# count= 8003
# count= 5557
# count= 20851
# count= 4023
# count= 4023
# count= 4
# count= 3
# count= 5
# count= 6
# etat= 30905 transitions= 51124 #  time= 99
#### with find_well
# GREEN nodes= 12 ---------- build finished now collecting 86
# count= 2940
# count= 6070
# count= 6572
# count= 7828
# count= 5394
# count= 20678
# count= 3967
# count= 3967
# count= 4
# count= 3
# count= 5
# count= 6
# etat= 30905 transitions= 51124  time= 106
