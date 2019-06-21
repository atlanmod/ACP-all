# -------------------
# 21/6/2019
# RBAC1 from http://www3.cs.stonybrook.edu/~stoller/ccs2007/
# -------------------
### Try to encode all relations even unecessary hierarchy
# assign at T+1 
# split the specification into students and employees
# remove redundancies
# -----------------

from employees import * #@UnusedWildImport
from students import * #@UnusedWildImport

REQ= REQ_students + REQ_employees

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

#======================================analysis
#### analysis ----------------
start = process_time()
# RBAC1: 9 administrative + 9 revoke + 25 + 70 (113 rules)
# size =  113
# with explicit unsafe 
size = 113 + 45 + 21 # (179 rules)

table.compute_table(REQ, size)
print ("size = " + str(size) + " time = " + str(floor(process_time()-start)))
#print (str(table))
print (str(table.get_info()))
table.show_problems()
#table.check_problems(size)

#table.compare_problems(size, REQ)
