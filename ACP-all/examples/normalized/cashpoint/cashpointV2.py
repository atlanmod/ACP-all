# -------------------
# 26/3/2020
# cashpoint from Nalepa2008
# -------------------
#### clearly a straight translation not the simpler possible specification
#### -------


from Normalized_OK import * #@UnusedWildImport

# --------------------------
User = DeclareSort('User')
CashPoint = DeclareSort('CashPoint')
Option = DeclareSort('Option')
CashpointActivity = DeclareSort('CashpointActivity')
Time = DeclareSort('Time')

table = Normalized_Enumerate()
# Variables
table.add_variable("U", User)
table.add_variable("C", CashPoint)
table.add_variable("O", Option)
table.add_variable("CA", CashpointActivity)
table.add_variable("T", Time)
U = table.get_variable(0)
C = table.get_variable(1)
O = table.get_variable(2)
CA = table.get_variable(3)
T = table.get_variable(4)

payout = Const('payout', Option)
balanceInquiry = Const('balanceInquiry', Option)

askForPIN = Const('askForPIN', CashpointActivity)
takeAwayCard = Const('takeAwayCard', CashpointActivity)
payOutCash = Const('payOutCash', CashpointActivity)
notEnoughFundsInMachine = Const('notEnoughFundsInMachine', CashpointActivity)
notEnoughFundsOnAccount = Const('notEnoughFundsOnAccount', CashpointActivity)
notEnoughFunds = Const('notEnoughFunds', CashpointActivity)
displayBalance = Const('displayBalance', CashpointActivity)

### --------------------------
### functions and predicates 
numberOfBills = Function('numberOfBills', Time, CashPoint, IntSort()) 
desiredAmount = Function('desiredAmount', Time, User, IntSort()) 
freeFunds = Function('freeFunds', Time, User, IntSort()) 
enteredPIN = Function('enteredPIN', Time, User, IntSort()) 
pINInDatabase = Function('pINInDatabase', Time, CashPoint, IntSort()) 
numberOfFailedAttempts  = Function('numberOfFailedAttempts', Time, User, CashPoint, IntSort()) 
menuOption = Function('menuOption', Time, User, Option) 
activity = Function('activity', Time, User, CashPoint, CashpointActivity)
succ = Function('succ', Time, Time)

enoughCashInCashpoint = Function('enoughCashInCashpoint', Time, User, CashPoint, BoolSort()) 
clientHasFreeFunds = Function('clientHasFreeFunds', Time, User, BoolSort()) 
authentication = Function('authentication', Time, User, CashPoint, BoolSort()) 

### + exclusive menuOption
#table.add_rule(And((menuOption(T, U) == payout), (menuOption(T, U) == balanceInquiry)), False)

### Rule: 1 if    numberOfBills is greater or equal to desiredAmount then  enoughCashInCashpoint is true
table.add_rule((numberOfBills(T, C) >= desiredAmount(T, U)), enoughCashInCashpoint(T, U, C))
### Rule: 2 if    numberOfBills is less than desiredAmount then  enoughCashInCashpoint is false
table.add_rule((numberOfBills(T, C) < desiredAmount(T, U)), Not(enoughCashInCashpoint(T, U, C)))
### Rule: 3 if    desiredAmount is greater or equal to freeFunds then  clientHasFreeFunds is true
table.add_rule((desiredAmount(T, U) >= freeFunds(T, U)), clientHasFreeFunds(T, U))
### Rule: 4 if    desiredAmount is less than freeFunds then  clientHasFreeFunds is false 
table.add_rule((desiredAmount(T, U) < freeFunds(T, U)), Not(clientHasFreeFunds(T, U)))
### Rule: 5 if    enteredPIN is pINInDatabase then  authentication is true
table.add_rule((enteredPIN(T, U) == pINInDatabase(T, C)), authentication(T, U,  C))
### Rule: 6 if    enteredPIN is pINInDatabase then  authentication is false and   numberOfFailedAttempts is numberOfFailedAttempts + 1
table.add_rule(And((enteredPIN(T, U) != pINInDatabase(T, C)), Not(authentication(T, U,  C))), (numberOfFailedAttempts(succ(T), U, C) == (numberOfFailedAttempts(succ(T), U, C)+1))) 
### Rule: 7 if    authentication is false and   numberOfFailedAttempts is less than 3 then  action: ’ask_for_pin’ 
table.add_rule(And(Not(authentication(T, U,  C)), numberOfFailedAttempts(T, U, C) < 3), activity(T, U, C) == askForPIN)
### Rule: 8 if    authentication is false and   numberOfFailedAttempts is 3 then  action: ’take_away_card’
table.add_rule(And(Not(authentication(T, U,  C)), numberOfFailedAttempts(T, U, C) == 3), (activity(T, U, C) == takeAwayCard))
### Rule: 9 if    authentication is true and   clientHasFreeFunds is true and   enoughCashInCashpoint is true and   menuOption is ’payout’ then  action: ’payout’
table.add_rule(And(authentication(T, U,  C), clientHasFreeFunds(T, U), enoughCashInCashpoint(T, U, C), menuOption(T, U) == payout), activity(T, U, C) == payOutCash)
### Rule: 10 if    authentication is true and   clientHasFreeFunds is true and   enoughCashInCashpoint is false and   menuOption is ’payout’ then  action: ’not enough funds in machine’
table.add_rule(And(authentication(T, U,  C), clientHasFreeFunds(T, U), Not(enoughCashInCashpoint(T, U, C)), menuOption(T, U) == payout), activity(T, U, C) == notEnoughFundsInMachine)
### Rule: 11 if    authentication is true and   clientHasFreeFunds is false and   enoughCashInCashpoint is true and   menuOption is ’payout’ then  action: ’not enough funds on accound’
table.add_rule(And(authentication(T, U,  C), Not(clientHasFreeFunds(T, U)), enoughCashInCashpoint(T, U, C), menuOption(T, U) == payout), activity(T, U, C) == notEnoughFundsOnAccount)
### Rule: 12 if    authentication is true and   clientHasFreeFunds is false and   enoughCashInCashpoint is false and   menuOption is ’payout’ then  action: ’not enough funds’
table.add_rule(And(authentication(T, U,  C), Not(clientHasFreeFunds(T, U)), Not(enoughCashInCashpoint(T, U, C)), menuOption(T, U) == payout), activity(T, U, C) == notEnoughFunds)
### Rule: 13 if    authentication is true and   menuOption is ’balanceInquiry’ then  action: ’display_balance’
table.add_rule(And(authentication(T, U,  C), menuOption(T, U) == balanceInquiry), activity(T, U, C) == displayBalance)

#======================================analysis
start = process_time()
size = 13 # +1 menuOption unsafe

### PIN and user actions TODO + other infos
REQ = [(menuOption(T, U) == payout), (menuOption(T, U) == balanceInquiry), (numberOfBills(T, C) >= desiredAmount(T, U)), (numberOfBills(T, C) < desiredAmount(T, U)),
       (desiredAmount(T, U) >= freeFunds(T, U)), (desiredAmount(T, U) < freeFunds(T, U)), (enteredPIN(T, U) == pINInDatabase(T, C)), (enteredPIN(T, U) != pINInDatabase(T, C))]
# Ordering REQ [numberOfBills(T, C) >= desiredAmount(T, U), numberOfBills(T, C) < desiredAmount(T, U), 
#               desiredAmount(T, U) >= freeFunds(T, U), desiredAmount(T, U) < freeFunds(T, U), 
#               enteredPIN(T, U) == pINInDatabase(T, C), enteredPIN(T, U) != pINInDatabase(T, C), 
#               menuOption(T, U) == payout, menuOption(T, U) == balanceInquiry]

# ALLOWED = [[-1]*len(REQ)] # since found three unsat requests 
# compare with 0/1 and 2/3 4/5 6/7 => 00 10 01 soit 81!!!
combinations = [[-1, 0], [0, -1]]
# ALLOWED = gener_allowed([([0,1], combinations), ], len(REQ)) 
# ALLOWED = [[0, 0, -1, -1, -1, -1, -1, -1], [1, 0, -1, -1, -1, -1, -1, -1], [0, 1, -1, -1, -1, -1, -1, -1]]
### => remove first
# ALLOWED = [[0, 0, 0, 0, -1, -1, -1, -1], [1, 0, 0, 0, -1, -1, -1, -1], [0, 1, 0, 0, -1, -1, -1, -1],
#            [0, 0, 1, 0, -1, -1, -1, -1], [1, 0, 1, 0, -1, -1, -1, -1], [0, 1, 1, 0, -1, -1, -1, -1],
#            [0, 0, 0, 1, -1, -1, -1, -1], [1, 0, 0, 1, -1, -1, -1, -1], [0, 1, 0, 1, -1, -1, -1, -1] ]
#### => remove first and second
#ALLOWED = [[-1, -1, -1, -1, 0, 0, -1, -1], [-1, -1, -1, -1, 0, 1, -1, -1], [-1, -1, -1, -1, 1, 0, -1, -1]]
### remove last

ALLOWED = gener_allowed([([0,1], combinations), ([2,3], combinations), ([4,5], combinations)], len(REQ)) 
### remove all

table.compute_table(REQ, size, ALLOWED) 
    
#print (str(table))
#print (str(table.get_info()))
table.show_problems()
#table.check_problems(size)

# checking count= 99 allseen 80
# #final set of problems 1
# size= 14 time= 1
# Total number of rules 14
# number of stored 14
# number of unsafes 0
#  #normalized store 0
# number of problems 1
# 
#### NO problem in fact
