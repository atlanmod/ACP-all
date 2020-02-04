# -------------------
# 3/2/2019
# RBAC2 from http://www3.cs.stonybrook.edu/~stoller/ccs2007/
# -------------------
### without simplification
### encoding revoke: similar to assign
### but needs to add extra condition and discrete time
### V3 new formulation of revoke with ForAll([Q], And((Q < T), assign(Q, X, Y)) inside conditions
# -----------------

from Normalized_OK import * #@UnusedWildImport
from time import * #@UnusedWildImport
from math import * #@UnusedWildImport

# --------------------------
Person = DeclareSort('Person')
Resource = DeclareSort('Resource')

table = Normalized_Enumerate()
# Variables
table.add_variable("X", Person)
table.add_variable("R", Resource)
table.add_variable("Y", Person)
table.add_variable("T", IntSort()) # linear time
table.add_variable("P", IntSort()) # linear time
table.add_variable("Q", IntSort()) # linear time
X = table.get_variable(0)
R = table.get_variable(1)
Y = table.get_variable(2)
T = table.get_variable(3)
P = table.get_variable(4)
Q = table.get_variable(5)

### --------------------------
### predicates for roles
Employee = Function('Employee', IntSort(), Person, BoolSort()) 
Nurse = Function('Nurse', IntSort(), Person, BoolSort()) 
Doctor = Function('Doctor', IntSort(), Person, BoolSort()) 
Receptionist = Function('Receptionist', IntSort(), Person, BoolSort()) 
MedicalManager= Function('MedicalManager', IntSort(), Person, BoolSort()) 
MedicalTeam = Function('MedicalTeam', IntSort(), Person, BoolSort()) 
Manager= Function('Manager', IntSort(), Person, BoolSort()) 
Agent = Function('Agent', IntSort(), Person, BoolSort()) 
Patient = Function('Patient', IntSort(), Person, BoolSort())
PrimaryDoctor = Function('PrimaryDoctor', IntSort(), Person, BoolSort()) 
ReferredDoctor = Function('ReferredDoctor', IntSort(), Person, BoolSort()) 
ThirdParty = Function('ThirdParty', IntSort(), Person, BoolSort())
PatientWithTPC = Function('PatientWithTPC', IntSort(), Person, BoolSort())
### for action (no relation known between them)
view = Function('view', IntSort(), Person, Resource, BoolSort())
add = Function('add',  IntSort(), Person, Resource, BoolSort())
modify = Function('modify',  IntSort(), Person, Resource, BoolSort())
access = Function('access',  IntSort(), Person, Resource, BoolSort())
enter = Function('enter',  IntSort(), Person, Resource, BoolSort())
update = Function('update',  IntSort(), Person, Resource, BoolSort())
create = Function('create',  IntSort(), Person, Resource, BoolSort())
sign = Function('sign',  IntSort(), Person, Resource, BoolSort())
### for resources we do not know possible relation
OldMedicalRecords = Function('OldMedicalRecords',  IntSort(), Resource, BoolSort()) 
RecentMedicalRecords = Function('RecentMedicalRecords',  IntSort(), Resource, BoolSort()) 
PrivateNotes = Function('PrivateNotes',  IntSort(), Resource, BoolSort()) 
Prescriptions = Function('Prescriptions',  IntSort(),  Resource, BoolSort()) 
PatientPersonalInfo = Function('PatientPersonalInfo',  IntSort(), Resource, BoolSort()) 
PatientFinancialInfo = Function('PatientFinancialInfo',  IntSort(), Resource, BoolSort()) 
PatientMedicalInfo = Function('PatientMedicalInfo',  IntSort(), Resource, BoolSort()) 
CarePlan = Function('CarePlan',  IntSort(), Resource, BoolSort()) 
Appointment = Function('Appointment',  IntSort(), Resource, BoolSort()) 
ProgressNotes = Function('ProgressNotes',  IntSort(), Resource, BoolSort()) 
MedicalRecordsWithThirdPartyInfo = Function('MedicalRecordsWithThirdPartyInfo',  IntSort(), Resource, BoolSort()) 
LegalAgreement = Function('LegalAgreement',  IntSort(), Resource, BoolSort()) 
Bills = Function('Bills',  IntSort(), Resource, BoolSort()) 
### assign
assign = Function('assign',  IntSort(), Person, Person, BoolSort()) 
### revoke
revoke = Function('revoke',  IntSort(), Person, Person, BoolSort()) 

## ThirdParties ? 
REQ= [Nurse(T, X), Doctor(T, X), Receptionist(T, X), MedicalManager(T, X), Manager(T, X), Patient(T, X), PrimaryDoctor(T, X), \
                            OldMedicalRecords(T, R), RecentMedicalRecords(T, R), PrivateNotes(T, R), Prescriptions(T, R), PatientPersonalInfo(T, R), \
                            PatientFinancialInfo(T, R), PatientMedicalInfo(T, R), CarePlan(T, R), Appointment(T, R), ProgressNotes(T, R), \
                            MedicalRecordsWithThirdPartyInfo(T, R), LegalAgreement(T, R), Bills(T, R), 
                            assign(T, X, Y), revoke(T, X, Y), ForAll([Q], And((Q < T), assign(Q, X, Y)))]

##### the rules -------------
 
### ---------------------------------------------- (8+3)
table.add_rule(Nurse(T, X), Employee(T, X))  # 0
table.add_rule(Doctor(T, X), Employee(T, X))
table.add_rule(Receptionist(T, X), Employee(T, X)) #
table.add_rule(MedicalManager(T, X), Employee(T, X))
table.add_rule(Manager(T, X), Employee(T, X))
table.add_rule(Patient(T, X), PatientWithTPC(T, X))  #
table.add_rule(Doctor(T, X), ReferredDoctor(T, X))  # 
table.add_rule(Doctor(T, X), PrimaryDoctor(T, X))   # remove it
table.add_rule(And(Patient(T, X), PrimaryDoctor(T, X)), False) #
table.add_rule(And(Receptionist(T, X), Doctor(T, X)), False) #
table.add_rule(And(Nurse(T, X), Doctor(T, X)), False) #10
### ---- 
   
# ---------------------permission assignement  (24)
table.add_rule(And(Doctor(T, X),  OldMedicalRecords(T, R)), view(T, X, R))
table.add_rule(And(Doctor(T, X),  RecentMedicalRecords(T, R)), view(T, X, R))
table.add_rule(And(Doctor(T, X),  PrivateNotes(T, R)), view(T, X, R))
table.add_rule(And(Doctor(T, X),  PrivateNotes(T, R)), add(T, X, R))
table.add_rule(And(Doctor(T, X),  RecentMedicalRecords(T, R)), add(T, X, R))
table.add_rule(And(Doctor(T, X),  Prescriptions(T, R)), view(T, X, R))
table.add_rule(And(Doctor(T, X),  Prescriptions(T, R)), modify(T, X, R))
table.add_rule(And(Manager(T, X),  PatientPersonalInfo(T, R)), access(T, X, R))
table.add_rule(And(Manager(T, X),  PatientFinancialInfo(T, R)), access(T, X, R))
table.add_rule(And(Manager(T, X),  PatientMedicalInfo(T, R)), access(T, X, R))
table.add_rule(And(Manager(T, X),  OldMedicalRecords(T, R)), enter(T, X, R))
table.add_rule(And(Manager(T, X),  RecentMedicalRecords(T, R)), enter(T, X, R))
table.add_rule(And(Manager(T, X),  CarePlan(T, R)), update(T, X, R))
table.add_rule(And(Receptionist(T, X),  Appointment(T, R)), create(T, X, R))
table.add_rule(And(Nurse(T, X),  OldMedicalRecords(T, R)), access(T, X, R))
table.add_rule(And(Nurse(T, X),  CarePlan(T, R)), view(T, X, R))
table.add_rule(And(Nurse(T, X),  ProgressNotes(T, R)), add(T, X, R))
table.add_rule(And(Nurse(T, X),  RecentMedicalRecords(T, R)), view(T, X, R))
table.add_rule(And(Patient(T, X),  OldMedicalRecords(T, R)), view(T, X, R))
table.add_rule(And(Patient(T, X),  RecentMedicalRecords(T, R)), view(T, X, R))
table.add_rule(And(PatientWithTPC(T, X),  MedicalRecordsWithThirdPartyInfo(T, R)), view(T, X, R))
table.add_rule(And(Patient(T, X),  LegalAgreement(T, R)), sign(T, X, R))
table.add_rule(And(Patient(T, X),  Prescriptions(T, R)), view(T, X, R))
table.add_rule(And(Patient(T, X),  Bills(T, R)), view(T, X, R)) # 34
# -------
  
# ------------------------------- (13)
table.add_rule(And(Doctor(T, X), assign(T, X, Y)), ThirdParty(T+1, Y)) #
table.add_rule(And(Doctor(T, X), Doctor(T, Y), assign(T, X, Y)), ReferredDoctor(T+1, Y)) #
table.add_rule(And(Manager(T, X), assign(T, X, Y)), Employee(T+1, Y))  # 
table.add_rule(And(Manager(T, X), assign(T, X, Y)), Receptionist(T+1, Y)) #
table.add_rule(And(Manager(T, X), assign(T, X, Y)), Nurse(T+1, Y))  #
table.add_rule(And(Manager(T, X), assign(T, X, Y)), Doctor(T+1, Y)) #
table.add_rule(And(Patient(T, X), assign(T, X, Y)), Agent(T+1, Y)) #
table.add_rule(And(Patient(T, X), Doctor(T, Y), assign(T, X, Y)), PrimaryDoctor(T+1, Y)) # 
table.add_rule(And(Receptionist(T, X), assign(T, X, Y)), Patient(T+1, Y)) # 
table.add_rule(And(ThirdParty(T, X), Patient(T, Y), assign(T, X, Y)), PatientWithTPC(T+1, Y)) #
table.add_rule(And(MedicalManager(T, X), Doctor(T, Y), assign(T, X, Y)), MedicalTeam(T+1, Y)) #
table.add_rule(And(MedicalManager(T, X), Nurse(T, Y), assign(T, X, Y)), MedicalTeam(T+1, Y)) #
table.add_rule(And(Manager(T, X), assign(T, X, Y)), MedicalTeam(T+1, Y)) # 47
# --------------------------------------------

### ************************** new formulation revoke (13) 
table.add_rule(And(Doctor(T, X), revoke(T, X, Y), ForAll([Q], And((Q < T), assign(Q, X, Y))), Not(assign(T, X, Y))), Not(ThirdParty(T+1, Y))) # 48
table.add_rule(And(Doctor(T, X), revoke(T, X, Y), ForAll([Q], And((P < T), assign(P, X, Y))), Not(assign(T, X, Y))), Not(ReferredDoctor(T+1, Y))) # 49
table.add_rule(And(MedicalManager(T, X),  revoke(T, X, Y), ForAll([Q], And((P < T), assign(P, X, Y))), Not(assign(T, X, Y))), Not(MedicalTeam(T+1, Y)))
table.add_rule(And(MedicalManager(T, X), revoke(T, X, Y), ForAll([Q], And((P < T), assign(P, X, Y))), Not(assign(T, X, Y))),Not(MedicalTeam(T+1, Y)))
table.add_rule(And(Manager(T, X), revoke(T, X, Y), ForAll([Q], And((P < T), assign(P, X, Y))), Not(assign(T, X, Y))), Not(Employee(T+1, Y)))
table.add_rule(And(Manager(T, X), revoke(T, X, Y), ForAll([Q], And((P < T), assign(P, X, Y))), Not(assign(T, X, Y))), Not(MedicalTeam(T+1, Y)))
table.add_rule(And(Manager(T, X), revoke(T, X, Y), ForAll([Q], And((P < T), assign(P, X, Y))), Not(assign(T, X, Y))), Not(Receptionist(T+1, Y)))
table.add_rule(And(Manager(T, X), revoke(T, X, Y), ForAll([Q], And((P < T), assign(P, X, Y))), Not(assign(T, X, Y))), Not(Nurse(T+1, Y)))
table.add_rule(And(Manager(T, X), revoke(T, X, Y), ForAll([Q], And((P < T), assign(P, X, Y))), Not(assign(T, X, Y))), Not(Doctor(T+1, Y)))
table.add_rule(And(Patient(T, X), revoke(T, X, Y), ForAll([Q], And((P < T), assign(P, X, Y))), Not(assign(T, X, Y))), Not(Agent(T+1, Y)))
table.add_rule(And(Patient(T, X), revoke(T, X, Y), ForAll([Q], And((P < T), assign(P, X, Y))), Not(assign(T, X, Y))), Not(PrimaryDoctor(T+1, Y)))
table.add_rule(And(Doctor(T, X), Not(Receptionist(T, X)), revoke(T, X, Y), ForAll([Q], And((P < T), assign(P, X, Y))), Not(assign(T, X, Y))), Patient(T+1, Y))
table.add_rule(And(ThirdParty(T, X), revoke(T, X, Y), ForAll([Q], And((P < T), assign(P, X, Y))), Not(assign(T, X, Y))), Not(PatientWithTPC(T+1, Y)))
# # --------------------------------------------

### ------------------------- (12+) relation on resources ? (6*13)
table.add_rule(And(OldMedicalRecords(T, R), RecentMedicalRecords(T, R)), False)
table.add_rule(And(OldMedicalRecords(T, R), PrivateNotes(T, R)), False)
table.add_rule(And(OldMedicalRecords(T, R), Prescriptions(T, R)), False)
table.add_rule(And(OldMedicalRecords(T, R), PatientPersonalInfo(T, R)), False) 
table.add_rule(And(OldMedicalRecords(T, R), PatientFinancialInfo(T, R)), False)
table.add_rule(And(OldMedicalRecords(T, R), PatientMedicalInfo(T, R)), False)
table.add_rule(And(OldMedicalRecords(T, R), CarePlan(T, R)), False)
table.add_rule(And(OldMedicalRecords(T, R), Appointment(T, R)), False)
table.add_rule(And(OldMedicalRecords(T, R), ProgressNotes(T, R)), False)
table.add_rule(And(OldMedicalRecords(T, R), MedicalRecordsWithThirdPartyInfo(T, R)), False)
table.add_rule(And(OldMedicalRecords(T, R), LegalAgreement(T, R)), False)
table.add_rule(And(OldMedicalRecords(T, R), Bills(T, R)), False) 

table.add_rule(And(RecentMedicalRecords(T, R), PrivateNotes(T, R)), False)
table.add_rule(And(RecentMedicalRecords(T, R), Prescriptions(T, R)), False)
table.add_rule(And(RecentMedicalRecords(T, R), PatientPersonalInfo(T, R)), False) 
table.add_rule(And(RecentMedicalRecords(T, R), PatientFinancialInfo(T, R)), False)
table.add_rule(And(RecentMedicalRecords(T, R), PatientMedicalInfo(T, R)), False)
table.add_rule(And(RecentMedicalRecords(T, R), CarePlan(T, R)), False)
table.add_rule(And(RecentMedicalRecords(T, R), Appointment(T, R)), False)
table.add_rule(And(RecentMedicalRecords(T, R), ProgressNotes(T, R)), False)
table.add_rule(And(RecentMedicalRecords(T, R), MedicalRecordsWithThirdPartyInfo(T, R)), False)
table.add_rule(And(RecentMedicalRecords(T, R), LegalAgreement(T, R)), False)
table.add_rule(And(RecentMedicalRecords(T, R), Bills(T, R)), False) 

table.add_rule(And(PrivateNotes(T, R), Prescriptions(T, R)), False)
table.add_rule(And(PrivateNotes(T, R), PatientPersonalInfo(T, R)), False) 
table.add_rule(And(PrivateNotes(T, R), PatientFinancialInfo(T, R)), False)
table.add_rule(And(PrivateNotes(T, R), PatientMedicalInfo(T, R)), False)
table.add_rule(And(PrivateNotes(T, R), CarePlan(T, R)), False)
table.add_rule(And(PrivateNotes(T, R), Appointment(T, R)), False)
table.add_rule(And(PrivateNotes(T, R), ProgressNotes(T, R)), False)
table.add_rule(And(PrivateNotes(T, R), MedicalRecordsWithThirdPartyInfo(T, R)), False)
table.add_rule(And(PrivateNotes(T, R), LegalAgreement(T, R)), False)
table.add_rule(And(PrivateNotes(T, R), Bills(T, R)), False) 

table.add_rule(And(Prescriptions(T, R), PatientPersonalInfo(T, R)), False) 
table.add_rule(And(Prescriptions(T, R), PatientFinancialInfo(T, R)), False)
table.add_rule(And(Prescriptions(T, R), PatientMedicalInfo(T, R)), False)
table.add_rule(And(Prescriptions(T, R), CarePlan(T, R)), False)
table.add_rule(And(Prescriptions(T, R), Appointment(T, R)), False)
table.add_rule(And(Prescriptions(T, R), ProgressNotes(T, R)), False)
table.add_rule(And(Prescriptions(T, R), MedicalRecordsWithThirdPartyInfo(T, R)), False)
table.add_rule(And(Prescriptions(T, R), LegalAgreement(T, R)), False)
table.add_rule(And(Prescriptions(T, R), Bills(T, R)), False) 

table.add_rule(And(PatientPersonalInfo(T, R), PatientFinancialInfo(T, R)), False)
table.add_rule(And(PatientPersonalInfo(T, R), PatientMedicalInfo(T, R)), False)
table.add_rule(And(PatientPersonalInfo(T, R), CarePlan(T, R)), False)
table.add_rule(And(PatientPersonalInfo(T, R), Appointment(T, R)), False)
table.add_rule(And(PatientPersonalInfo(T, R), ProgressNotes(T, R)), False)
table.add_rule(And(PatientPersonalInfo(T, R), MedicalRecordsWithThirdPartyInfo(T, R)), False)
table.add_rule(And(PatientPersonalInfo(T, R), LegalAgreement(T, R)), False)
table.add_rule(And(PatientPersonalInfo(T, R), Bills(T, R)), False) 

table.add_rule(And(PatientFinancialInfo(T, R), PatientMedicalInfo(T, R)), False)
table.add_rule(And(PatientFinancialInfo(T, R), CarePlan(T, R)), False)
table.add_rule(And(PatientFinancialInfo(T, R), Appointment(T, R)), False)
table.add_rule(And(PatientFinancialInfo(T, R), ProgressNotes(T, R)), False)
table.add_rule(And(PatientFinancialInfo(T, R), MedicalRecordsWithThirdPartyInfo(T, R)), False)
table.add_rule(And(PatientFinancialInfo(T, R), LegalAgreement(T, R)), False)
table.add_rule(And(PatientFinancialInfo(T, R), Bills(T, R)), False) 

table.add_rule(And(PatientMedicalInfo(T, R), CarePlan(T, R)), False)
table.add_rule(And(PatientMedicalInfo(T, R), Appointment(T, R)), False)
table.add_rule(And(PatientMedicalInfo(T, R), ProgressNotes(T, R)), False)
table.add_rule(And(PatientMedicalInfo(T, R), MedicalRecordsWithThirdPartyInfo(T, R)), False)
table.add_rule(And(PatientMedicalInfo(T, R), LegalAgreement(T, R)), False)
table.add_rule(And(PatientMedicalInfo(T, R), Bills(T, R)), False)

table.add_rule(And(CarePlan(T, R), Appointment(T, R)), False)
table.add_rule(And(CarePlan(T, R), ProgressNotes(T, R)), False)
table.add_rule(And(CarePlan(T, R), MedicalRecordsWithThirdPartyInfo(T, R)), False)
table.add_rule(And(CarePlan(T, R), LegalAgreement(T, R)), False)
table.add_rule(And(CarePlan(T, R), Bills(T, R)), False)

table.add_rule(And(Appointment(T, R), ProgressNotes(T, R)), False)
table.add_rule(And(Appointment(T, R), MedicalRecordsWithThirdPartyInfo(T, R)), False)
table.add_rule(And(Appointment(T, R), LegalAgreement(T, R)), False)
table.add_rule(And(Appointment(T, R), Bills(T, R)), False)

table.add_rule(And(ProgressNotes(T, R), MedicalRecordsWithThirdPartyInfo(T, R)), False)
table.add_rule(And(ProgressNotes(T, R), LegalAgreement(T, R)), False)
table.add_rule(And(ProgressNotes(T, R), Bills(T, R)), False)

table.add_rule(And(MedicalRecordsWithThirdPartyInfo(T, R), LegalAgreement(T, R)), False)
table.add_rule(And(MedicalRecordsWithThirdPartyInfo(T, R), Bills(T, R)), False)

table.add_rule(And(LegalAgreement(T, R), Bills(T, R)), False)
## -------
#======================================analysis
start = process_time()
# original version (59)
#size = 11+24+1+13+10
### with some disjunction (137)
size = 11+24+1+13+10 + 6*13

table.compute_table(REQ, size)
print ("size= " + str(size) + " time= " + str(floor(process_time()-start)))
    
#print (str(table))
print (str(table.get_info()))
table.show_problems()
#table.check_problems(size)

#table.compare_problems(REQ, size)

