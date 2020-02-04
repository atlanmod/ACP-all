# -------------------
# 3/2/2020
# RBAC1 from http://www3.cs.stonybrook.edu/~stoller/ccs2007/
# -------------------
### Student part only 
### Try to encode all relations even unecessary hierarchy
# -----------------

from students_declarations import * #@UnusedWildImport

##  # roles 
REQ_students = [Undergrad(T, X), Student(T, X), Grad(T, X), TA(T, X), RA(T, X), 
      Grader(T, X), GradStudOfficer(T, X), HonorsStudent(T, X), GradCommittee(T, X), UndergradPermittedGradClass(T, X),
      # resources (10)
      GradClass(T, R), StudentHealthInsur(T, R), GradeBook(T, R), RoomSchedule(T, R), UndergradHonorsClass(T, R),
      ComputerAccount(T, R), StudentParkingPermit(T, R),  Course(T, R), Tuition(T, R), UndergradClass(T, R)
      ]

##### the rules -------------
### ****************************** STUDENTS

# #### exclusivity for resources (5*9=45)
# table.add_rule(And(GradClass(T, R), StudentHealthInsur(T, R)), False)
# table.add_rule(And(GradClass(T, R), GradeBook(T, R)), False)
# table.add_rule(And(GradClass(T, R), RoomSchedule(T, R)), False)
# table.add_rule(And(GradClass(T, R), UndergradHonorsClass(T, R)), False)
# table.add_rule(And(GradClass(T, R), ComputerAccount(T, R)), False)
# table.add_rule(And(GradClass(T, R), StudentParkingPermit(T, R)), False)
# table.add_rule(And(GradClass(T, R), Course(T, R)), False)
# table.add_rule(And(GradClass(T, R), Tuition(T, R)), False)
# table.add_rule(And(GradClass(T, R), UndergradClass(T, R)), False)
# 
# table.add_rule(And(StudentHealthInsur(T, R), GradeBook(T, R)), False)
# table.add_rule(And(StudentHealthInsur(T, R), RoomSchedule(T, R)), False)
# table.add_rule(And(StudentHealthInsur(T, R), UndergradHonorsClass(T, R)), False)
# table.add_rule(And(StudentHealthInsur(T, R), ComputerAccount(T, R)), False)
# table.add_rule(And(StudentHealthInsur(T, R), StudentParkingPermit(T, R)), False)
# table.add_rule(And(StudentHealthInsur(T, R), Course(T, R)), False)
# table.add_rule(And(StudentHealthInsur(T, R), Tuition(T, R)), False)
# table.add_rule(And(StudentHealthInsur(T, R), UndergradClass(T, R)), False)
# 
# table.add_rule(And(GradeBook(T, R), RoomSchedule(T, R)), False)
# table.add_rule(And(GradeBook(T, R), UndergradHonorsClass(T, R)), False)
# table.add_rule(And(GradeBook(T, R), ComputerAccount(T, R)), False)
# table.add_rule(And(GradeBook(T, R), StudentParkingPermit(T, R)), False)
# table.add_rule(And(GradeBook(T, R), Course(T, R)), False)
# table.add_rule(And(GradeBook(T, R), Tuition(T, R)), False)
# table.add_rule(And(GradeBook(T, R), UndergradClass(T, R)), False)
# 
# table.add_rule(And(RoomSchedule(T, R), UndergradHonorsClass(T, R)), False)
# table.add_rule(And(RoomSchedule(T, R), ComputerAccount(T, R)), False)
# table.add_rule(And(RoomSchedule(T, R), StudentParkingPermit(T, R)), False)
# table.add_rule(And(RoomSchedule(T, R), Course(T, R)), False)
# table.add_rule(And(RoomSchedule(T, R), Tuition(T, R)), False)
# table.add_rule(And(RoomSchedule(T, R), UndergradClass(T, R)), False)
# 
# table.add_rule(And(UndergradHonorsClass(T, R), ComputerAccount(T, R)), False)
# table.add_rule(And(UndergradHonorsClass(T, R), StudentParkingPermit(T, R)), False)
# table.add_rule(And(UndergradHonorsClass(T, R), Course(T, R)), False)
# table.add_rule(And(UndergradHonorsClass(T, R), Tuition(T, R)), False)
# table.add_rule(And(UndergradHonorsClass(T, R), UndergradClass(T, R)), False)
# 
# table.add_rule(And(ComputerAccount(T, R), StudentParkingPermit(T, R)), False)
# table.add_rule(And(ComputerAccount(T, R), Course(T, R)), False)
# table.add_rule(And(ComputerAccount(T, R), Tuition(T, R)), False)
# table.add_rule(And(ComputerAccount(T, R), UndergradClass(T, R)), False)
# 
# table.add_rule(And(StudentParkingPermit(T, R), Course(T, R)), False)
# table.add_rule(And(StudentParkingPermit(T, R), Tuition(T, R)), False)
# table.add_rule(And(StudentParkingPermit(T, R), UndergradClass(T, R)), False)
# 
# table.add_rule(And(Course(T, R), Tuition(T, R)), False)
# table.add_rule(And(Course(T, R), UndergradClass(T, R)), False)
# 
# table.add_rule(And(Tuition(T, R), UndergradClass(T, R)), False)
# -------

### ---------------------------------------------- student roles (5)
table.add_rule(Undergrad(T, X), Student(T, X))  #
table.add_rule(Grad(T, X), Student(T, X))  # 
table.add_rule(TA(T, X), Grad(T, X))  # 
table.add_rule(RA(T, X), Grad(T, X))  # 
table.add_rule(Grader(T, X), Undergrad(T, X))  # 
# -------

# -------------------------------- SMER (1)
table.add_rule(And(Undergrad(T, X), Grad(T, X)), False)
# ------
 
# ---------------------student permission assignement  (19)

table.add_rule(And(Grad(T, X), GradClass(T, R)), register(T, X, R))
table.add_rule(And(Grad(T, X), GradClass(T, R)), withdraw(T, X, R))
table.add_rule(And(Grad(T, X), StudentHealthInsur(T, R)), enroll(T, X, R))

table.add_rule(And(Grader(T, X), GradeBook(T, R)), assignGrade(T, X, R))
table.add_rule(And(Grader(T, X), GradeBook(T, R)), viewGrade(T, X, R))

table.add_rule(And(GradStudOfficer(T, X), RoomSchedule(T, R)), reserveRoom(T, X, R))

table.add_rule(And(HonorsStudent(T, X), UndergradHonorsClass(T, R)), register(T, X, R))
table.add_rule(And(HonorsStudent(T, X), UndergradHonorsClass(T, R)), withdraw(T, X, R))

table.add_rule(And(Student(T, X), GradeBook(T, R)), viewGrade(T, X, R))
table.add_rule(And(Student(T, X), ComputerAccount(T, R)), create(T, X, R))
table.add_rule(And(Student(T, X), StudentParkingPermit(T, R)), obtain(T, X, R))
table.add_rule(And(Student(T, X), Course(T, R)), register(T, X, R))
table.add_rule(And(Student(T, X), Tuition(T, R)), pay(T, X, R))

table.add_rule(And(TA(T, X), GradeBook(T, R)), assignGrade(T, X, R))
table.add_rule(And(TA(T, X), GradeBook(T, R)), viewGrade(T, X, R))

table.add_rule(And(Undergrad(T, X), UndergradClass(T, R)), register(T, X, R))
table.add_rule(And(Undergrad(T, X), UndergradClass(T, R)), withdraw(T, X, R))
table.add_rule(And(UndergradPermittedGradClass(T, X), GradClass(T, R)), withdraw(T, X, R))
table.add_rule(And(UndergradPermittedGradClass(T, X), GradClass(T, R)), withdraw(T, X, R))
# -------

#======================================analysis
# #### analysis ----------------
# start = process_time()
# # student: 5 roles + 1 SMER + 19 permissions (25 rules) + 45 explicit unsafe
# size =  5+1+19 + 45
#    
# table.compute_table(REQ_students, size)
# print ("size = " + str(size) + " time = " + str(floor(process_time()-start)))
# #print (str(table))
# print (str(table.get_info()))
# table.show_problems()
#table.check_problems(size)
#  
# #table.compare_problems(REQ, size)

