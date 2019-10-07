# -------------------
# 22/8/2019
# RBAC1 from http://www3.cs.stonybrook.edu/~stoller/ccs2007/
# -------------------
### Student part only 
### Try to encode all relations even unecessary hierarchy
# -----------------

#from Enumerate import * #@UnusedWildImport
from Normalized_OK_V2 import * #@UnusedWildImport
from time import * #@UnusedWildImport
from math import * #@UnusedWildImport

# --------------------------
Person = DeclareSort('Person')
Resource = DeclareSort('Resource')
Time = DeclareSort('Time')

table = Normalized_enumerate()
#table = Enumerate()
# Variables
table.add_variable("X", Person)
table.add_variable("R", Resource)
table.add_variable("Y", Person)
table.add_variable("T", Time) # linear time
X = table.get_variable(0)
R = table.get_variable(1)
Y = table.get_variable(2)
T = table.get_variable(3)

### for discrete time
succ = Function('succ', Time, Time)

### --------------------------
### predicates for roles (10)
Student = Function('Student', Time, Person, BoolSort()) 
Undergrad = Function('Undergrad', Time, Person, BoolSort())  
Grad = Function('Grad', Time, Person, BoolSort())  
TA = Function('TA', Time, Person, BoolSort())  
RA = Function('RA', Time, Person, BoolSort())  
Grader = Function('Grader', Time, Person, BoolSort())  
GradStudOfficer = Function('GradStudOfficer', Time, Person, BoolSort())  
HonorsStudent = Function('HonorsStudent', Time, Person, BoolSort())  
GradCommittee = Function('GradCommittee', Time, Person, BoolSort()) 
UndergradPermittedGradClass = Function('UndergradPermittedGradClass', Time, Person, BoolSort()) 

### for action (no relation known between them) (9)
register = Function('register', Time, Person, Resource, BoolSort())
enroll = Function('enroll',  Time, Person, Resource, BoolSort())
withdraw = Function('withdraw',  Time, Person, Resource, BoolSort())
assignGrade = Function('assignGrade',  Time, Person, Resource, BoolSort())
viewGrade = Function('viewGrade',  Time, Person, Resource, BoolSort())
reserveRoom = Function('reserveRoom',  Time, Person, Resource, BoolSort())
create = Function('create',  Time, Person, Resource, BoolSort())
obtain = Function('obtain',  Time, Person, Resource, BoolSort())
pay = Function('pay',  Time, Person, Resource, BoolSort())

### for resources we do not know possible relation (10)
GradClass = Function('GradClass',  Time, Resource, BoolSort()) 
StudentHealthInsur = Function('StudentHealthInsur',  Time, Resource, BoolSort()) 
UndergradHonorsClass = Function('UndergradHonorsClass',  Time, Resource, BoolSort()) 
GradeBook = Function('GradeBook',  Time,  Resource, BoolSort()) 
RoomSchedule = Function('RoomSchedule',  Time, Resource, BoolSort()) 
StudentParkingPermit = Function('StudentParkingPermit',  Time, Resource, BoolSort()) 
ComputerAccount = Function('ComputerAccount',  Time, Resource, BoolSort()) 
Tuition = Function('Tuition',  Time, Resource, BoolSort()) 
UndergradClass = Function('UndergradClass',  Time, Resource, BoolSort()) 
Course = Function('Course',  Time, Resource, BoolSort()) 

### assign
assign = Function('assign',  Time, Person, Person, BoolSort()) 
### revoke
revoke = Function('revoke',  Time, Person, Person, BoolSort()) 

