# -------------------
# 23/3/2020
# RBAC1 from http://www3.cs.stonybrook.edu/~stoller/ccs2007/
# -------------------
### part only for Employees
### Try to encode all relations even unecessary hierarchy
# assign at T+1 
# -----------------

from students_declarations import * #@UnusedWildImport

### --------------------------
### predicates for roles (22)
Employee = Function('Employee', Time, Person, BoolSort()) 
AdmissionsOfficer = Function('AdmissionsOfficer', Time, Person, BoolSort()) 
AssistantProf = Function('AssistantProf', Time, Person, BoolSort()) 
AssociateProf = Function('AssociateProf', Time, Person, BoolSort()) 
Dean = Function('Dean', Time, Person, BoolSort()) 
DeanOfAdmissions = Function('DeanOfAdmissions', Time, Person, BoolSort()) 
DeptChair = Function('DeptChair', Time, Person, BoolSort()) 
FacilitiesCommittee = Function('FacilitiesCommittee', Time, Person, BoolSort()) 
FacilitiesDirector = Function('FacilitiesDirector', Time, Person, BoolSort()) 
Faculty = Function('Faculty', Time, Person, BoolSort()) 
FullTimeEmployee = Function('FullTimeEmployee', Time, Person, BoolSort()) # ? deduction
GradAdmissionsCommittee = Function('GradAdmissionsCommittee', Time, Person, BoolSort()) 
HonorsPgmDirector = Function('HonorsPgmDirector', Time, Person, BoolSort()) # ?
Lecturer = Function('Lecturer', Time, Person, BoolSort()) 
President = Function('President', Time, Person, BoolSort())  
Professor = Function('Professor', Time, Person, BoolSort()) 
Provost = Function('Provost', Time, Person, BoolSort()) 
QualExamCommittee = Function('QualExamCommittee', Time, Person, BoolSort()) 
QualExamCommitteeHead = Function('QualExamCommitteeHead', Time, Person, BoolSort()) 
Staff = Function('Staff', Time, Person, BoolSort()) 
TenuredFac = Function('TenuredFac', Time, Person, BoolSort()) # ? deduction
AsstForStudentAffairs = Function('AsstForStudentAffairs', Time, Person, BoolSort()) # ?

### predicates for resources (7)
CollegeAcct = Function('CollegeAcct',  Time, Resource, BoolSort())
Roster = Function('Roster',  Time, Resource, BoolSort())
DeptBudget = Function('DeptBudget',  Time, Resource, BoolSort())
DeptAcct = Function('DeptAcct',  Time, Resource, BoolSort())
EmployeeParkingPermit = Function('EmployeeParkingPermit',  Time, Resource, BoolSort())
EmployeeHealthInsur = Function('EmployeeHealthInsur',  Time, Resource, BoolSort())
UniversityAcct = Function('UniversityAcct',  Time, Resource, BoolSort())

### for action (no relation known between them) (10)
authorizeExpenditure = Function('authorizeExpenditure',  Time, Person, Resource, BoolSort())
approveLateWithdrawal = Function('approveLateWithdrawal',  Time, Person, Resource, BoolSort())
approveGradeChange = Function('approveGradeChange',  Time, Person, Resource, BoolSort())
allowLateWithdrawal = Function('allowLateWithdrawal',  Time, Person, Resource, BoolSort())
modify = Function('modify',  Time, Person, Resource, BoolSort())
authorizeEquipmentPurchase = Function('authorizeEquipmentPurchase',  Time, Person, Resource, BoolSort())
submitGradeChange = Function('submitGradeChange',  Time, Person, Resource, BoolSort())
submitGrades = Function('submitGrades',  Time, Person, Resource, BoolSort())
reviseGrade = Function('reviseGrade',  Time, Person, Resource, BoolSort())
authorizeExpenditure = Function('authorizeExpenditure',  Time, Person, Resource, BoolSort())


