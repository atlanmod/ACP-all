# -------------------
# 21/6/2019
# RBAC1 from http://www3.cs.stonybrook.edu/~stoller/ccs2007/
# -------------------
### part only for Employees
### Try to encode all relations even unecessary hierarchy
# assign at succ(T) 
# -----------------

from employees_declarations import * #@UnusedWildImport

##      # roles 
REQ_employees = [Staff(T, X), Employee(T, X), AdmissionsOfficer(T, X), DeanOfAdmissions(T, X), Provost(T, X), 
      Faculty(T, X), Lecturer(T, X), AssistantProf(T, X), AssociateProf(T, X), Professor(T, X),
      DeptChair(T, X), Dean(T, X), Provost(T, X), President(T, X), # TenuredFac(T, X) no
      FacilitiesDirector(T,X), FacilitiesCommittee(T, X), QualExamCommitteeHead(T,X), QualExamCommittee(T, X),
      # resources (7)
      CollegeAcct(T, R), Roster(T, R), DeptBudget(T, R), DeptAcct(T, R), EmployeeParkingPermit(T, R), 
      EmployeeHealthInsur(T, R), UniversityAcct(T, R)
      ]

##### the rules -------------
### ---------------------------------------------- roles (17-1)
table.add_rule(Staff(T, X), Employee(T, X))  #
table.add_rule(AdmissionsOfficer(T, X), Staff(T, X))  #
table.add_rule(DeanOfAdmissions(T, X), AdmissionsOfficer(T, X))
table.add_rule(Provost(T, X), DeanOfAdmissions(T, X))  #
table.add_rule(Faculty(T, X), Employee(T, X))  #
table.add_rule(Lecturer(T, X), Faculty(T, X))  #
table.add_rule(AssistantProf(T, X), Faculty(T, X))  #
table.add_rule(AssociateProf(T, X), AssistantProf(T, X))
table.add_rule(Professor(T, X), AssociateProf(T, X))
table.add_rule(DeptChair(T, X), Professor(T, X))
table.add_rule(Dean(T, X), DeptChair(T, X))
table.add_rule(Provost(T, X), Dean(T, X))
table.add_rule(President(T, X), Provost(T, X))
table.add_rule(AssociateProf(T, X), TenuredFac(T, X))
##table.add_rule(Professor(T, X), TenuredFac(T, X)) # REDUNDANT
table.add_rule(FacilitiesDirector(T,X), FacilitiesCommittee(T, X))
table.add_rule(QualExamCommitteeHead(T,X), QualExamCommittee(T, X))
### Employee < FullTimeEmployee, Faculty < QualExamCommittee, unnecessary ?
table.add_rule(FullTimeEmployee(T, X), Employee(T, X))
table.add_rule(QualExamCommittee(T, X), Faculty(T, X))
### Faculty < TenuredFac
table.add_rule(TenuredFac(T, X), Faculty(T, X))
# -------

# -------------------------------- SMER (1)
table.add_rule(And(AdmissionsOfficer(T, X), GradAdmissionsCommittee(T, X)), False)
# --------

# -------------------------------- permission assignement (16)
table.add_rule(And(Dean(T, X),  CollegeAcct(T, R)), authorizeExpenditure(T, X, R))
table.add_rule(And(Dean(T, X),  Roster(T, R)), approveLateWithdrawal(T, X, R))
table.add_rule(And(Dean(T, X),  GradeBook(T, R)), approveGradeChange(T, X, R))

table.add_rule(And(AsstForStudentAffairs(T, X),  Roster(T, R)), allowLateWithdrawal(T, X, R))
table.add_rule(And(AsstForStudentAffairs(T, X),  GradeBook(T, R)), approveGradeChange(T, X, R))

table.add_rule(And(DeptChair(T, X),  DeptBudget(T, R)), modify(T, X, R))

table.add_rule(And(FacilitiesDirector(T, X),  DeptAcct(T, R)), authorizeEquipmentPurchase(T, X, R))

table.add_rule(And(Employee(T, X),  EmployeeParkingPermit(T, R)), obtain(T, X, R))

table.add_rule(And(Faculty(T, X),  GradeBook(T, R)), assignGrade(T, X, R))
table.add_rule(And(Faculty(T, X),  GradeBook(T, R)), submitGradeChange(T, X, R))
table.add_rule(And(Faculty(T, X),  GradeBook(T, R)), submitGrades(T, X, R))
table.add_rule(And(Faculty(T, X),  GradeBook(T, R)), reviseGrade(T, X, R))
table.add_rule(And(Faculty(T, X),  GradeBook(T, R)), viewGrade(T, X, R))

table.add_rule(And(FullTimeEmployee(T, X),  EmployeeHealthInsur(T, R)), enroll(T, X, R))

table.add_rule(And(President(T, X),  UniversityAcct(T, R)), authorizeExpenditure(T, X, R))

table.add_rule(And(Provost(T, X),  UniversityAcct(T, R)), authorizeExpenditure(T, X, R))
# --------

# -------------------------------- administrative (19)
table.add_rule(And(Dean(T, X), Professor(T, Y), Not(Dean(T, Y)), Not(Provost(T, Y)), assign(T, X, Y)), DeptChair(succ(T), Y)) #

table.add_rule(And(Dean(T, X), Staff(T, Y), assign(T, X, Y)), AsstForStudentAffairs(succ(T), Y)) #

table.add_rule(And(DeanOfAdmissions(T, X), Staff(T, Y), assign(T, X, Y)), AdmissionsOfficer(succ(T), Y)) #

table.add_rule(And(DeptChair(T, X), Faculty(T, Y), assign(T, X, Y)), GradAdmissionsCommittee(succ(T), Y)) #
table.add_rule(And(DeptChair(T, X), Faculty(T, Y), assign(T, X, Y)), GradCommittee(succ(T), Y)) #
table.add_rule(And(DeptChair(T, X), Faculty(T, Y), assign(T, X, Y)), HonorsPgmDirector(succ(T), Y)) #
table.add_rule(And(DeptChair(T, X), Employee(T, Y), assign(T, X, Y)), FacilitiesCommittee(succ(T), Y)) #
table.add_rule(And(DeptChair(T, X), Faculty(T, Y), assign(T, X, Y)), FacilitiesDirector(succ(T), Y)) #
table.add_rule(And(DeptChair(T, X), Faculty(T, Y), assign(T, X, Y)), QualExamCommittee(succ(T), Y)) #
table.add_rule(And(DeptChair(T, X), GradCommittee(T, Y), assign(T, X, Y)), QualExamCommitteeHead(succ(T), Y)) #

table.add_rule(And(President(T, X), Employee(T, Y), assign(T, X, Y)), Staff(succ(T), Y)) #
table.add_rule(And(President(T, X), Employee(T, Y), assign(T, X, Y)), DeanOfAdmissions(succ(T), Y)) #
table.add_rule(And(President(T, X), Employee(T, Y), assign(T, X, Y)), Lecturer(succ(T), Y)) #
table.add_rule(And(President(T, X), Employee(T, Y), assign(T, X, Y)), AssistantProf(succ(T), Y)) #
table.add_rule(And(President(T, X), Employee(T, Y), assign(T, X, Y)), AssociateProf(succ(T), Y)) #
table.add_rule(And(President(T, X), Employee(T, Y), assign(T, X, Y)), Professor(succ(T), Y)) #

table.add_rule(And(President(T, X), Employee(T, Y), assign(T, X, Y)), FullTimeEmployee(succ(T), Y)) #

table.add_rule(And(President(T, X), Professor(T, Y), Not(DeptChair(T, Y)), assign(T, X, Y)), Provost(succ(T), Y)) #

table.add_rule(And(Provost(T, X), Professor(T, Y), Not(DeptChair(T, Y)), assign(T, X, Y)), Dean(succ(T), Y)) #
# --------

### add exclusivity of revoke and assign
table.add_rule(And(revoke(T, X, Y), assign(T, X, Y)), False)

# -------------------------------- revoke (19-5)
# in general, each administrator can revoke users from the same roles to
# which he can assign users.  in order words, for each rule can_assign(r_a,
# c, r), there is usually a corresponding rule can_revoke(r_a, r).  
### New encoding: 
#### A cond assign => newrole becomes
#### A newrole revoke => Not(newrole) 

table.add_rule(And(Dean(T, X), DeptChair(T, Y), revoke(T, X, Y)), DeptChair(succ(T), Y)) #

table.add_rule(And(Dean(T, X), AsstForStudentAffairs(T, Y), revoke(T, X, Y)), Not(AsstForStudentAffairs(succ(T), Y))) #

table.add_rule(And(DeanOfAdmissions(T, X), AdmissionsOfficer(T, Y), revoke(T, X, Y)), Not(AdmissionsOfficer(succ(T), Y))) #

table.add_rule(And(DeptChair(T, X), GradAdmissionsCommittee(T, Y), revoke(T, X, Y)), Not(GradAdmissionsCommittee(succ(T), Y))) #
table.add_rule(And(DeptChair(T, X), GradCommittee(T, Y), revoke(T, X, Y)), Not(GradCommittee(succ(T), Y))) #
table.add_rule(And(DeptChair(T, X), HonorsPgmDirector(T, Y), revoke(T, X, Y)), Not(HonorsPgmDirector(succ(T), Y))) #
table.add_rule(And(DeptChair(T, X), FacilitiesCommittee(T, Y), revoke(T, X, Y)), Not(FacilitiesCommittee(succ(T), Y))) #

### REDUNDANT
# table.add_rule(And(DeptChair(T, X), FacilitiesDirector(T, Y), revoke(T, X, Y)), Not(FacilitiesDirector(succ(T), Y))) #
# table.add_rule(And(DeptChair(T, X), QualExamCommittee(T, Y), revoke(T, X, Y)), Not(QualExamCommittee(succ(T), Y))) #

table.add_rule(And(DeptChair(T, X), QualExamCommitteeHead(T, Y), revoke(T, X, Y)), Not(QualExamCommitteeHead(succ(T), Y))) #

table.add_rule(And(President(T, X), Staff(T, Y), revoke(T, X, Y)), Not(Staff(succ(T), Y))) #
table.add_rule(And(President(T, X), Lecturer(T, Y), revoke(T, X, Y)), Not(Lecturer(succ(T), Y))) #
table.add_rule(And(President(T, X), AssistantProf(T, Y), revoke(T, X, Y)), Not(AssistantProf(succ(T), Y))) #

### REDUNDANT
#table.add_rule(And(President(T, X), DeanOfAdmissions(T, Y), revoke(T, X, Y)), Not(DeanOfAdmissions(succ(T), Y))) #
#table.add_rule(And(President(T, X), AssociateProf(T, Y), revoke(T, X, Y)), Not(AssociateProf(succ(T), Y))) #
#table.add_rule(And(President(T, X), Professor(T, Y), revoke(T, X, Y)), Not(Professor(succ(T), Y))) #

table.add_rule(And(President(T, X), FullTimeEmployee(T, Y), revoke(T, X, Y)), Not(FullTimeEmployee(succ(T), Y))) #

table.add_rule(And(President(T, X), Provost(T, Y), revoke(T, X, Y)), Not(Provost(succ(T), Y))) #

table.add_rule(And(Provost(T, X), Dean(T, Y), revoke(T, X, Y)), Not(Dean(succ(T), Y))) #
# --------

### ------------------ resources exclusivity (7*3 = 21)
table.add_rule(And(CollegeAcct(T, R), Roster(T, R)), False)
table.add_rule(And(CollegeAcct(T, R), DeptBudget(T, R)), False)
table.add_rule(And(CollegeAcct(T, R), DeptAcct(T, R)), False)
table.add_rule(And(CollegeAcct(T, R), EmployeeParkingPermit(T, R)), False) 
table.add_rule(And(CollegeAcct(T, R), EmployeeHealthInsur(T, R)), False)
table.add_rule(And(CollegeAcct(T, R), UniversityAcct(T, R)), False)

table.add_rule(And(Roster(T, R), DeptBudget(T, R)), False)
table.add_rule(And(Roster(T, R), DeptAcct(T, R)), False)
table.add_rule(And(Roster(T, R), EmployeeParkingPermit(T, R)), False) 
table.add_rule(And(Roster(T, R), EmployeeHealthInsur(T, R)), False)
table.add_rule(And(Roster(T, R), UniversityAcct(T, R)), False)

table.add_rule(And(DeptBudget(T, R), DeptAcct(T, R)), False)
table.add_rule(And(DeptBudget(T, R), EmployeeParkingPermit(T, R)), False) 
table.add_rule(And(DeptBudget(T, R), EmployeeHealthInsur(T, R)), False)
table.add_rule(And(DeptBudget(T, R), UniversityAcct(T, R)), False)

table.add_rule(And(DeptAcct(T, R), EmployeeParkingPermit(T, R)), False) 
table.add_rule(And(DeptAcct(T, R), EmployeeHealthInsur(T, R)), False)
table.add_rule(And(DeptAcct(T, R), UniversityAcct(T, R)), False)

table.add_rule(And(EmployeeParkingPermit(T, R), EmployeeHealthInsur(T, R)), False)
table.add_rule(And(EmployeeParkingPermit(T, R), UniversityAcct(T, R)), False)

table.add_rule(And(EmployeeHealthInsur(T, R), UniversityAcct(T, R)), False)
# --------
      
#======================================analysis
# #### analysis ----------------
# start = process_time()
# # employees:  17+3 roles + 1 SMER +  16 permissions + 1 +  19 administrative + 19 revoke (75 rules)
# ### 3 redundant rules
# # employees:  16+3 roles + 1 SMER +  16 permissions + 1 +  19 administrative + 14 revoke (70 rules)
# ### + 21 explicit unsafe
# size =  16+3+1+16+ 1 + 19+14 +21
#  
# table.compute_table(REQ_employees, size)
# print ("size = " + str(size) + " time = " + str(floor(process_time()-start)))
# #print (str(table))
# print (str(table.get_info()))
# table.show_problems()
# #table.check_problems(size)

#table.compare_problems(size, REQ)
