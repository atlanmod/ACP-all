# -------------------
# 25/3/2020
# RBAC1 from http://www3.cs.stonybrook.edu/~stoller/ccs2007/
# -------------------
### Try to encode all relations even unecessary hierarchy
# assign at T+1 
# split the specification into students and employees
# remove redundancies
# -----------------
### ATTENTION version with or without explicit unsafe

from employees import * #@UnusedWildImport
from students import * #@UnusedWildImport

##### additional rules -------------
# ------------------------------- employee => student administrative (9)
table.add_rule(And(AdmissionsOfficer(T, X), Student(T, Y),assign(T, X, Y)), Undergrad(succ(T), Y)) #
table.add_rule(And(DeptChair(T, X), Grad(T, Y), assign(T, X, Y)), TA(succ(T), Y)) #
table.add_rule(And(DeptChair(T, X), Grad(T, Y), assign(T, X, Y)), GradStudOfficer(succ(T), Y)) #
table.add_rule(And(DeptChair(T, X), GradStudOfficer(T, Y), assign(T, X, Y)), GradCommittee(succ(T), Y)) #
table.add_rule(And(DeptChair(T, X), Undergrad(T, Y), assign(T, X, Y)), Grader(succ(T), Y)) #

table.add_rule(And(Faculty(T, X), Student(T, Y), assign(T, X, Y)), RA(succ(T), Y)) #

table.add_rule(And(GradAdmissionsCommittee(T, X), Student(T, Y), assign(T, X, Y)), Grad(succ(T), Y)) #

table.add_rule(And(HonorsPgmDirector(T, X), Undergrad(T, Y), assign(T, X, Y)), HonorsStudent(succ(T), Y)) #

table.add_rule(And(Faculty(T, X), Undergrad(T, Y), assign(T, X, Y)), UndergradPermittedGradClass(succ(T), Y)) #
# --------

# ----------------------- revoke admin => student (7+2)
table.add_rule(And(DeptChair(T, X), TA(T, Y), revoke(T, X, Y)), Not(TA(succ(T), Y))) #
table.add_rule(And(DeptChair(T, X), GradStudOfficer(T, Y), revoke(T, X, Y)), Not(GradStudOfficer(succ(T), Y))) #
table.add_rule(And(DeptChair(T, X), GradCommittee(T, Y), revoke(T, X, Y)), Not(GradCommittee(succ(T), Y))) #
table.add_rule(And(DeptChair(T, X), Grader(T, Y), revoke(T, X, Y)), Not(Grader(succ(T), Y))) #

table.add_rule(And(Faculty(T, X), RA(T, Y), revoke(T, X, Y)), Not(RA(succ(T), Y))) #

table.add_rule(And(HonorsPgmDirector(T, X), HonorsStudent(T, Y), revoke(T, X, Y)), Not(HonorsStudent(succ(T), Y))) #

table.add_rule(And(Faculty(T, X), UndergradPermittedGradClass(T, Y), revoke(T, X, Y)), Not(UndergradPermittedGradClass(succ(T), Y))) #

table.add_rule(And(Dean(T, X), Undergrad(T, Y), revoke(T, X, Y)), Not(Undergrad(succ(T), Y))) #
table.add_rule(And(Dean(T, X), Grad(T, Y), revoke(T, X, Y)), Not(Grad(succ(T), Y))) #
# --------

# ##  # roles 
# REQ_students = [Undergrad(T, X), Student(T, X), Grad(T, X), TA(T, X), RA(T, X), 
#       Grader(T, X), GradStudOfficer(T, X), HonorsStudent(T, X), GradCommittee(T, X), UndergradPermittedGradClass(T, X),
#       # resources (10)
#       GradClass(T, R), StudentHealthInsur(T, R), GradeBook(T, R), RoomSchedule(T, R), UndergradHonorsClass(T, R),
#       ComputerAccount(T, R), StudentParkingPermit(T, R),  Course(T, R), Tuition(T, R), UndergradClass(T, R)
#       ]
# ##      # roles 
# REQ_employees = [Staff(T, X), Employee(T, X), AdmissionsOfficer(T, X), DeanOfAdmissions(T, X), Provost(T, X), 
#       Faculty(T, X), Lecturer(T, X), AssistantProf(T, X), AssociateProf(T, X), Professor(T, X),
#       DeptChair(T, X), Dean(T, X), Provost(T, X), President(T, X), # TenuredFac(T, X) no
#       FacilitiesDirector(T,X), FacilitiesCommittee(T, X), QualExamCommitteeHead(T,X), QualExamCommittee(T, X),
#       # resources (7)
#       CollegeAcct(T, R), Roster(T, R), DeptBudget(T, R), DeptAcct(T, R), EmployeeParkingPermit(T, R), 
#       EmployeeHealthInsur(T, R), UniversityAcct(T, R)
#       ]
# REQ= REQ_students + REQ_employees

#### from OrderedDict all 
# definitions OrderedDict([(P_0(T, X), Staff(T, X)), (P_1(T, X), Employee(T, X)), (P_2(T, X), AdmissionsOfficer(T, X)), (P_3(T, X), 
# DeanOfAdmissions(T, X)), (P_4(T, X), Provost(T, X)), (P_5(T, X), Faculty(T, X)), (P_6(T, X), Lecturer(T, X)), (P_7(T, X), AssistantProf(T, X)), 
# (P_8(T, X), AssociateProf(T, X)), (P_9(T, X), Professor(T, X)), (P_10(T, X), DeptChair(T, X)), (P_11(T, X), Dean(T, X)), (P_12(T, X), President(T, X)), 
# (P_13(T, X), TenuredFac(T, X)), (P_14(T, X), FacilitiesDirector(T, X)), (P_15(T, X), FacilitiesCommittee(T, X)), (P_16(T, X), QualExamCommitteeHead(T, X)),
# (P_17(T, X), QualExamCommittee(T, X)), (P_18(T, X), FullTimeEmployee(T, X)), (P_19(T, X), GradAdmissionsCommittee(T, X)), (P_20(T, R), CollegeAcct(T, R)),
# (P_21(T, X, R), authorizeExpenditure(T, X, R)), (P_22(T, R), Roster(T, R)), (P_23(T, X, R), approveLateWithdrawal(T, X, R)), (P_24(T, R), GradeBook(T, R)),
# (P_25(T, X, R), approveGradeChange(T, X, R)), (P_26(T, X), AsstForStudentAffairs(T, X)), (P_27(T, X, R), allowLateWithdrawal(T, X, R)), 
# (P_28(T, R), DeptBudget(T, R)), (P_29(T, X, R), modify(T, X, R)), (P_30(T, R), DeptAcct(T, R)), (P_31(T, X, R), authorizeEquipmentPurchase(T, X, R)), 
# (P_32(T, R), EmployeeParkingPermit(T, R)), (P_33(T, X, R), obtain(T, X, R)), (P_34(T, X, R), assignGrade(T, X, R)), 
# (P_35(T, X, R), submitGradeChange(T, X, R)), (P_36(T, X, R), submitGrades(T, X, R)), (P_37(T, X, R), reviseGrade(T, X, R)), 
# (P_38(T, X, R), viewGrade(T, X, R)), (P_39(T, R), EmployeeHealthInsur(T, R)), (P_40(T, X, R), enroll(T, X, R)), (P_41(T, R), UniversityAcct(T, R)),
# (P_42(T, Y), Professor(T, Y)), (P_43(T, Y), Dean(T, Y)), (P_44(T, Y), Provost(T, Y)), (P_45(T, X, Y), assign(T, X, Y)), 
# (P_46(T, Y), DeptChair(succ(T), Y)), (P_47(T, Y), Staff(T, Y)), (P_48(T, Y), AsstForStudentAffairs(succ(T), Y)), 
# (P_49(T, Y), AdmissionsOfficer(succ(T), Y)), (P_50(T, Y), Faculty(T, Y)), (P_51(T, Y), GradAdmissionsCommittee(succ(T), Y)), 
# (P_52(T, Y), GradCommittee(succ(T), Y)), (P_53(T, Y), HonorsPgmDirector(succ(T), Y)), (P_54(T, Y), Employee(T, Y)), 
# (P_55(T, Y), FacilitiesCommittee(succ(T), Y)), (P_56(T, Y), FacilitiesDirector(succ(T), Y)), (P_57(T, Y), QualExamCommittee(succ(T), Y)), 
# (P_58(T, Y), GradCommittee(T, Y)), (P_59(T, Y), QualExamCommitteeHead(succ(T), Y)), (P_60(T, Y), Staff(succ(T), Y)), 
# (P_61(T, Y), DeanOfAdmissions(succ(T), Y)), (P_62(T, Y), Lecturer(succ(T), Y)), (P_63(T, Y), AssistantProf(succ(T), Y)), 
# (P_64(T, Y), AssociateProf(succ(T), Y)), (P_65(T, Y), Professor(succ(T), Y)), (P_66(T, Y), FullTimeEmployee(succ(T), Y)),
# (P_67(T, Y), DeptChair(T, Y)), (P_68(T, Y), Dean(succ(T), Y)), (P_69(T, X, Y), revoke(T, X, Y)), (P_70(T, Y), AsstForStudentAffairs(T, Y)), 
# (P_71(T, Y), AdmissionsOfficer(T, Y)), (P_72(T, Y), GradAdmissionsCommittee(T, Y)), (P_73(T, Y), HonorsPgmDirector(T, Y)), 
# (P_74(T, Y), FacilitiesCommittee(T, Y)), (P_75(T, Y), QualExamCommitteeHead(T, Y)), (P_76(T, Y), Lecturer(T, Y)), (P_77(T, Y), AssistantProf(T, Y)), 
# (P_78(T, Y), FullTimeEmployee(T, Y)), (P_79(T, X), Undergrad(T, X)), (P_80(T, X), Student(T, X)), (P_81(T, X), Grad(T, X)), (P_82(T, X), TA(T, X)), 
# (P_83(T, X), RA(T, X)), (P_84(T, X), Grader(T, X)), (P_85(T, R), GradClass(T, R)), (P_86(T, X, R), register(T, X, R)), (P_87(T, X, R), withdraw(T, X, R)),
# (P_88(T, R), StudentHealthInsur(T, R)), (P_89(T, X), GradStudOfficer(T, X)), (P_90(T, R), RoomSchedule(T, R)), (P_91(T, X, R), reserveRoom(T, X, R)), 
# (P_92(T, X), HonorsStudent(T, X)), (P_93(T, R), UndergradHonorsClass(T, R)), (P_94(T, R), ComputerAccount(T, R)), (P_95(T, X, R), create(T, X, R)), 
# (P_96(T, R), StudentParkingPermit(T, R)), (P_97(T, R), Course(T, R)), (P_98(T, R), Tuition(T, R)), (P_99(T, X, R), pay(T, X, R)), 
# (P_100(T, R), UndergradClass(T, R)), (P_101(T, X), UndergradPermittedGradClass(T, X)), (P_102(T, Y), Student(T, Y)),
# (P_103(T, Y), Undergrad(succ(T), Y)), (P_104(T, Y), Grad(T, Y)), (P_105(T, Y), TA(succ(T), Y)), (P_106(T, Y), GradStudOfficer(succ(T), Y)),
# (P_107(T, Y), GradStudOfficer(T, Y)), (P_108(T, Y), Undergrad(T, Y)), (P_109(T, Y), Grader(succ(T), Y)), (P_110(T, Y), RA(succ(T), Y)), 
# (P_111(T, Y), Grad(succ(T), Y)), (P_112(T, X), HonorsPgmDirector(T, X)), (P_113(T, Y), HonorsStudent(succ(T), Y)), 
# (P_114(T, Y), UndergradPermittedGradClass(succ(T), Y)), (P_115(T, Y), TA(T, Y)), (P_116(T, Y), Grader(T, Y)), (P_117(T, Y), RA(T, Y)), 
# (P_118(T, Y), HonorsStudent(T, Y)), (P_119(T, Y), UndergradPermittedGradClass(T, Y))])
# size= 120 REQ-pos [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 20, 22, 24, 28, 30, 32, 39, 41, 79, 80, 81, 82, 83, 84, 85, 88, 89, 90, 92, 93, 94, 96, 97, 98, 100, 101] mapping {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 14: 13, 15: 14, 16: 15, 17: 16, 20: 17, 22: 18, 24: 19, 28: 20, 30: 21, 32: 22, 39: 23, 41: 24, 79: 25, 80: 26, 81: 27, 82: 28, 83: 29, 84: 30, 85: 31, 88: 32, 89: 33, 90: 34, 92: 35, 93: 36, 94: 37, 96: 38, 97: 39, 98: 40, 100: 41, 101: 42}
#### print REQ defs
# [Staff(T, X), Employee(T, X), AdmissionsOfficer(T, X), DeanOfAdmissions(T, X), Provost(T, X), Faculty(T, X), Lecturer(T, X), AssistantProf(T, X), 
# AssociateProf(T, X), Professor(T, X), DeptChair(T, X), Dean(T, X), President(T, X), FacilitiesDirector(T, X), FacilitiesCommittee(T, X), 
# QualExamCommitteeHead(T, X), QualExamCommittee(T, X), CollegeAcct(T, R), Roster(T, R), GradeBook(T, R), DeptBudget(T, R), DeptAcct(T, R), 
# EmployeeParkingPermit(T, R), EmployeeHealthInsur(T, R), UniversityAcct(T, R), Undergrad(T, X), Student(T, X), Grad(T, X), TA(T, X), RA(T, X), 
# Grader(T, X), GradClass(T, R), StudentHealthInsur(T, R), GradStudOfficer(T, X), RoomSchedule(T, R), HonorsStudent(T, X), UndergradHonorsClass(T, R), 
# ComputerAccount(T, R), StudentParkingPermit(T, R), Course(T, R), Tuition(T, R), UndergradClass(T, R), UndergradPermittedGradClass(T, X)]
REQ = [Staff(T, X), Employee(T, X), AdmissionsOfficer(T, X), DeanOfAdmissions(T, X), Provost(T, X), Faculty(T, X), 
       Lecturer(T, X), AssistantProf(T, X), AssociateProf(T, X), Professor(T, X), DeptChair(T, X), Dean(T, X), 
       President(T, X), FacilitiesDirector(T, X), FacilitiesCommittee(T, X), QualExamCommitteeHead(T, X), QualExamCommittee(T, X),
       CollegeAcct(T, R), Roster(T, R), DeptBudget(T, R), DeptAcct(T, R), EmployeeParkingPermit(T, R), 
       EmployeeHealthInsur(T, R), UniversityAcct(T, R), Undergrad(T, X), Student(T, X), Grad(T, X), TA(T, X), RA(T, X), 
       Grader(T, X),  GradClass(T, R), StudentHealthInsur(T, R), GradeBook(T, R), GradStudOfficer(T, X), RoomSchedule(T, R), HonorsStudent(T, X),
       UndergradHonorsClass(T, R), ComputerAccount(T, R), StudentParkingPermit(T, R), Course(T, R), Tuition(T, R), 
       UndergradClass(T, R), UndergradPermittedGradClass(T, X)]

### TODO et ceux avec des Y ? les succ non si conclusions 
####il doit manque pleins d'atomes et donc aussi des relations 
ALLOWED = [[-1]*len(REQ)]
#NOTRELREQ = []

#======================================analysis
#### analysis ----------------
# RBAC1: 9 administrative + 9 revoke + 25 + 70 (113 rules)
size =  113

table.compute_table(REQ, size, ALLOWED) #, NOTRELREQ)
table.show_problems()
