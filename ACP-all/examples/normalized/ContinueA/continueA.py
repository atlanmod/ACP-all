# -------------------
# 25/3/2020
# CONTINUE A from test.tspass
# -------------------

from Normalized_OK import * #@UnusedWildImport

from time import * #@UnusedWildImport
from math import * #@UnusedWildImport

# Sorts
Subject = DeclareSort('Subject')
Resource = DeclareSort('Resource')

table = Normalized_Enumerate()
#table = Enumerate()
# Variables
table.add_variable("R", Resource)
table.add_variable("X", Subject)
R = table.get_variable(0)
X = table.get_variable(1)

# predicates
### subjects
subject = Function('subject', Subject, BoolSort()) 
admin = Function('admin', Subject, BoolSort()) 
pcchair = Function('pcchair', Subject, BoolSort()) 
pcmember= Function('pcmember', Subject, BoolSort()) 
subreviewer = Function('subreviewer', Subject, BoolSort()) 
### actions
Pdelete = Function('Pdelete', Subject, Resource, BoolSort()) 
Pcreate = Function('Pcreate', Subject, Resource, BoolSort()) 
Pread = Function('Pread', Subject, Resource, BoolSort()) 
Pwrite = Function('Pwrite', Subject, Resource, BoolSort()) 
Paction = Function('Paction', Subject, Resource, BoolSort()) 
### resources 
conference = Function('conference', Resource, BoolSort()) 
conferenceInfo = Function('conferenceInfo', Resource, BoolSort()) 
PcMember = Function('PcMember', Resource, BoolSort()) 
PcMemberAssignments = Function('PcMemberAssignments', Resource, BoolSort()) 
PcMemberConflicts = Function('PcMemberConflicts', Resource, BoolSort()) 
PcMemberInfo = Function('PcMemberInfo', Resource, BoolSort()) 
PcMemberInfoPassword = Function('PcMemberInfoPassword', Resource, BoolSort()) 
Paper = Function('Paper', Resource, BoolSort()) 
PaperSubmission = Function('PaperSubmission', Resource, BoolSort()) 
PaperDecision = Function('PaperDecision', Resource, BoolSort()) 
PaperConflicts = Function('PaperConflicts', Resource, BoolSort()) 
PaperAssignments = Function('PaperAssignments', Resource, BoolSort()) 
PaperReview = Function('PaperReview', Resource, BoolSort()) 
PaperReviewInfo = Function('PaperReviewInfo', Resource, BoolSort()) 
PaperReviewContent = Function('PaperReviewContent', Resource, BoolSort()) 
PaperReviewInfoSubmission = Function('PaperReviewInfoSubmission', Resource, BoolSort()) 

#### other predicates 
PcMemberInfoischairflag = Function('PcMemberInfoischairflag', Resource, BoolSort()) 
isEQuserID = Function('isEQuserID', Subject, BoolSort()) 
isPending = Function('isPending', Subject, BoolSort()) 
isEQPaper = Function('isEQPaper', Subject, Resource, BoolSort()) 
MeetingFlag = Function('MeetingFlag', Resource, BoolSort()) 
isSubjectMeeting = Function('isSubjectMeeting', Subject, BoolSort()) 
isConflicted = Function('isConflicted', Subject, BoolSort()) 
isMeeting = Function('isMeeting', Subject, BoolSort()) 
isReviewInPlace = Function('isReviewInPlace', Subject, BoolSort()) 

REQ = [subject(X), admin(X), pcchair(X), subreviewer(X), pcmember(X), conference(R), conferenceInfo(R), PcMember(R),\
                            PcMemberAssignments(R), PcMemberConflicts(R), PcMemberInfo(R), PcMemberInfoPassword(R), \
                            Paper(R), PaperSubmission(R), PaperDecision(R), PaperConflicts(R), PaperAssignments(R), PaperReview(R),\
                            PaperReviewInfo(R), PaperReviewContent(R), PaperReviewInfoSubmission(R), PcMemberInfoischairflag(R),\
                            isEQuserID(X), isPending(X), isEQPaper(X, R), MeetingFlag(R), isSubjectMeeting(X), isConflicted(X),\
                            isMeeting(X), isReviewInPlace(X)]

# ---------------- the rules = 47
table.add_rule(Or(admin(X), pcchair(X), pcmember(X), subreviewer(X)), subject(X)) #0
table.add_rule(Paction(X, R), Or(Pdelete(X, R), Pcreate(X, R), Pread(X, R), Pwrite(X, R))) #1
table.add_rule(Or(Pdelete(X, R), Pcreate(X, R), Pread(X, R), Pwrite(X, R)), Paction(X, R)) #2
table.add_rule(And(conference(R), admin(X)), And(Pread(X, R), Pwrite(X, R))) #3
table.add_rule(And(conference(R), pcchair(X)), Pread(X, R)) #4
table.add_rule(And(conference(R), pcmember(X)), Pread(X, R)) #5
table.add_rule(And(conferenceInfo(R), subject(X)), Pread(X, R)) #6
table.add_rule(And(PcMember(R), pcmember(X)), Pread(X, R)) # 7  
table.add_rule(And(PcMember(R), admin(X)), And(Pcreate(X, R), Pwrite(X, R))) #8
table.add_rule(And(PcMember(R), pcmember(X), isEQuserID(X)), Not(Paction(X, R))) # +9 
table.add_rule(And(PcMember(R), admin(X)), Pdelete(X, R)) #10
table.add_rule(And(PcMemberAssignments(R), pcchair(X)), And(Pread(X, R), Pwrite(X, R))) # +11 
table.add_rule(And(PcMemberAssignments(R), pcmember(X), isEQuserID(X)), Pread(X, R)) #12
table.add_rule(And(PcMemberConflicts(R), pcchair(X)), And(Pread(X, R), Pwrite(X, R))) #13
table.add_rule(And(PcMemberConflicts(R), pcmember(X), isEQuserID(X)), Pread(X, R)) # 14
table.add_rule(And(PcMemberInfo(R), pcchair(X)), And(Pread(X, R), Pwrite(X, R))) # 15
table.add_rule(And(PcMemberInfo(R), pcmember(X), isEQuserID(X)), And(Pread(X, R), Pwrite(X, R))) # 16
table.add_rule(And(PcMemberInfoPassword(R), pcmember(X), isEQuserID(X)), Pwrite(X, R)) # 17
table.add_rule(And(PcMemberInfoPassword(R), admin(X), Not(isPending(X))), Pwrite(X, R))  # 18
table.add_rule(And(PcMemberInfoischairflag(R), pcmember(X)), Pread(X, R)) # 19
table.add_rule(And(PcMemberInfoischairflag(R), pcmember(X), isEQuserID(X)), Not(Paction(X, R))) # 20
table.add_rule(And(PcMemberInfoischairflag(R), admin(X)), Pwrite(X, R)) #21
table.add_rule(And(Paper(R), pcchair(X)), Pdelete(X, R)) #22
table.add_rule(And(Paper(R), pcmember(X), isEQPaper(X, R)), Pread(X, R)) #23
table.add_rule(And(Paper(R), pcmember(X)), Pcreate(X, R)) #24
table.add_rule(And(PaperSubmission(R), Or(pcmember(X), pcchair(X))), Pread(X, R)) #25
table.add_rule(And(PaperSubmission(R), subreviewer(X), isEQuserID(X)), Pread(X, R)) #26
table.add_rule(And(PaperDecision(R), pcchair(X), isSubjectMeeting(X)), And(Pread(X, R), Pwrite(X, R))) #27
table.add_rule(And(PaperConflicts(R), Or(admin(X), pcchair(X))), And(Pread(X, R), Pwrite(X, R))) #28
table.add_rule(And(PaperConflicts(R), pcmember(X), isConflicted(X)), Pread(X, R)) #29
table.add_rule(And(PaperConflicts(R), pcmember(X), isMeeting(X)), Pread(X, R)) #30
table.add_rule(And(PaperConflicts(R), subject(X), isConflicted(X)), Not(Paction(X, R))) #31
table.add_rule(And(PaperAssignments(R), Or(admin(X), pcchair(X))), And(Pread(X, R), Pwrite(X, R))) #32
table.add_rule(And(PaperAssignments(R), subject(X), isConflicted(X)), And(Not(Pread(X, R)), Not(Pwrite(X, R)), Not(Pcreate(X, R)))) #33
table.add_rule(And(PaperAssignments(R), isEQPaper(X, R), pcchair(X), isSubjectMeeting(X)), Pread(X, R)) #34
table.add_rule(And(PaperAssignments(R), subject(X), isSubjectMeeting(X)), Not(Pread(X, R))) #35
table.add_rule(And(PaperReview(R), pcchair(X), Not(isConflicted(X))), Paction(X, R))
table.add_rule(And(PaperReview(R), isEQPaper(X, R), pcchair(X), isSubjectMeeting(X)), Pread(X, R))
table.add_rule(And(PaperReview(R), pcchair(X)), And(Pdelete(X, R), Pcreate(X, R)))
table.add_rule(And(PaperReview(R), subject(X), isConflicted(X)), Not(Paction(X, R)))
table.add_rule(And(PaperReview(R), pcmember(X), Not(isConflicted(X))), Pread(X, R))
table.add_rule(And(PaperReviewInfo(R), pcchair(X)), Paction(X, R))
table.add_rule(And(PaperReviewContent(R), pcmember(X), isEQuserID(X)), And(Pcreate(X, R), Pwrite(X, R), Pdelete(X, R)))
table.add_rule(And(PaperReviewContent(R), subreviewer(X), isEQuserID(X)), Pcreate(X, R))
table.add_rule(And(PaperReviewInfoSubmission(R), pcmember(X), isEQuserID(X), isReviewInPlace(X)), Pwrite(X, R))
table.add_rule(And(MeetingFlag(R), pcchair(X)), And(Pread(X, R), Pwrite(X, R)))
table.add_rule(And(MeetingFlag(R), pcmember(X)), Pread(X, R))
#======================================

### also on actions ?
#============ add few explicit unsafe representing disjunctions on resources (16)= 8*15=120
table.add_rule(And(conference(R), conferenceInfo(R)), False)
table.add_rule(And(conference(R), PcMember(R)), False)
table.add_rule(And(conference(R), PcMemberAssignments(R)), False)
table.add_rule(And(conference(R), PcMemberConflicts(R)), False)
table.add_rule(And(conference(R), PcMemberInfo(R)), False)
table.add_rule(And(conference(R), PcMemberInfoPassword(R)), False)
table.add_rule(And(conference(R), Paper(R)), False)
table.add_rule(And(conference(R), PaperSubmission(R)), False)
table.add_rule(And(conference(R), PaperDecision(R)), False)
table.add_rule(And(conference(R), PaperConflicts(R)), False)
table.add_rule(And(conference(R), PaperAssignments(R)), False)
table.add_rule(And(conference(R), PaperReview(R)), False)
table.add_rule(And(conference(R), PaperReviewInfo(R)), False)
table.add_rule(And(conference(R), PaperReviewContent(R)), False)
table.add_rule(And(conference(R), PaperReviewInfoSubmission(R)), False)

table.add_rule(And(conferenceInfo(R), PcMember(R)), False)
table.add_rule(And(conferenceInfo(R), PcMemberAssignments(R)), False)
table.add_rule(And(conferenceInfo(R), PcMemberConflicts(R)), False)
table.add_rule(And(conferenceInfo(R), PcMemberInfo(R)), False)
table.add_rule(And(conferenceInfo(R), PcMemberInfoPassword(R)), False)
table.add_rule(And(conferenceInfo(R), Paper(R)), False)
table.add_rule(And(conferenceInfo(R), PaperSubmission(R)), False)
table.add_rule(And(conferenceInfo(R), PaperDecision(R)), False)
table.add_rule(And(conferenceInfo(R), PaperConflicts(R)), False)
table.add_rule(And(conferenceInfo(R), PaperAssignments(R)), False)
table.add_rule(And(conferenceInfo(R), PaperReview(R)), False)
table.add_rule(And(conferenceInfo(R), PaperReviewInfo(R)), False)
table.add_rule(And(conferenceInfo(R), PaperReviewContent(R)), False)
table.add_rule(And(conferenceInfo(R), PaperReviewInfoSubmission(R)), False)

table.add_rule(And(PcMember(R), PcMemberAssignments(R)), False)
table.add_rule(And(PcMember(R), PcMemberConflicts(R)), False)
table.add_rule(And(PcMember(R), PcMemberInfo(R)), False)
table.add_rule(And(PcMember(R), PcMemberInfoPassword(R)), False)
table.add_rule(And(PcMember(R), Paper(R)), False)
table.add_rule(And(PcMember(R), PaperSubmission(R)), False)
table.add_rule(And(PcMember(R), PaperDecision(R)), False)
table.add_rule(And(PcMember(R), PaperConflicts(R)), False)
table.add_rule(And(PcMember(R), PaperAssignments(R)), False)
table.add_rule(And(PcMember(R), PaperReview(R)), False)
table.add_rule(And(PcMember(R), PaperReviewInfo(R)), False)
table.add_rule(And(PcMember(R), PaperReviewContent(R)), False)
table.add_rule(And(PcMember(R), PaperReviewInfoSubmission(R)), False)

table.add_rule(And(PcMemberAssignments(R), PcMemberConflicts(R)), False)
table.add_rule(And(PcMemberAssignments(R), PcMemberInfo(R)), False)
table.add_rule(And(PcMemberAssignments(R), PcMemberInfoPassword(R)), False)
table.add_rule(And(PcMemberAssignments(R), Paper(R)), False)
table.add_rule(And(PcMemberAssignments(R), PaperSubmission(R)), False)
table.add_rule(And(PcMemberAssignments(R), PaperDecision(R)), False)
table.add_rule(And(PcMemberAssignments(R), PaperConflicts(R)), False)
table.add_rule(And(PcMemberAssignments(R), PaperAssignments(R)), False)
table.add_rule(And(PcMemberAssignments(R), PaperReview(R)), False)
table.add_rule(And(PcMemberAssignments(R), PaperReviewInfo(R)), False)
table.add_rule(And(PcMemberAssignments(R), PaperReviewContent(R)), False)
table.add_rule(And(PcMemberAssignments(R), PaperReviewInfoSubmission(R)), False)

table.add_rule(And(PcMemberConflicts(R), PcMemberInfo(R)), False)
table.add_rule(And(PcMemberConflicts(R), PcMemberInfoPassword(R)), False)
table.add_rule(And(PcMemberConflicts(R), Paper(R)), False)
table.add_rule(And(PcMemberConflicts(R), PaperSubmission(R)), False)
table.add_rule(And(PcMemberConflicts(R), PaperDecision(R)), False)
table.add_rule(And(PcMemberConflicts(R), PaperConflicts(R)), False)
table.add_rule(And(PcMemberConflicts(R), PaperAssignments(R)), False)
table.add_rule(And(PcMemberConflicts(R), PaperReview(R)), False)
table.add_rule(And(PcMemberConflicts(R), PaperReviewInfo(R)), False)
table.add_rule(And(PcMemberConflicts(R), PaperReviewContent(R)), False)
table.add_rule(And(PcMemberConflicts(R), PaperReviewInfoSubmission(R)), False)

table.add_rule(And(PcMemberInfo(R), PcMemberInfoPassword(R)), False)
table.add_rule(And(PcMemberInfo(R), Paper(R)), False)
table.add_rule(And(PcMemberInfo(R), PaperSubmission(R)), False)
table.add_rule(And(PcMemberInfo(R), PaperDecision(R)), False)
table.add_rule(And(PcMemberInfo(R), PaperConflicts(R)), False)
table.add_rule(And(PcMemberInfo(R), PaperAssignments(R)), False)
table.add_rule(And(PcMemberInfo(R), PaperReview(R)), False)
table.add_rule(And(PcMemberInfo(R), PaperReviewInfo(R)), False)
table.add_rule(And(PcMemberInfo(R), PaperReviewContent(R)), False)
table.add_rule(And(PcMemberInfo(R), PaperReviewInfoSubmission(R)), False)

table.add_rule(And(PcMemberInfoPassword(R), Paper(R)), False)
table.add_rule(And(PcMemberInfoPassword(R), PaperSubmission(R)), False)
table.add_rule(And(PcMemberInfoPassword(R), PaperDecision(R)), False)
table.add_rule(And(PcMemberInfoPassword(R), PaperConflicts(R)), False)
table.add_rule(And(PcMemberInfoPassword(R), PaperAssignments(R)), False)
table.add_rule(And(PcMemberInfoPassword(R), PaperReview(R)), False)
table.add_rule(And(PcMemberInfoPassword(R), PaperReviewInfo(R)), False)
table.add_rule(And(PcMemberInfoPassword(R), PaperReviewContent(R)), False)
table.add_rule(And(PcMemberInfoPassword(R), PaperReviewInfoSubmission(R)), False)

table.add_rule(And(Paper(R), PaperSubmission(R)), False)
table.add_rule(And(Paper(R), PaperDecision(R)), False)
table.add_rule(And(Paper(R), PaperConflicts(R)), False)
table.add_rule(And(Paper(R), PaperAssignments(R)), False)
table.add_rule(And(Paper(R), PaperReview(R)), False)
table.add_rule(And(Paper(R), PaperReviewInfo(R)), False)
table.add_rule(And(Paper(R), PaperReviewContent(R)), False)
table.add_rule(And(Paper(R), PaperReviewInfoSubmission(R)), False)

table.add_rule(And(PaperSubmission(R), PaperDecision(R)), False)
table.add_rule(And(PaperSubmission(R), PaperConflicts(R)), False)
table.add_rule(And(PaperSubmission(R), PaperAssignments(R)), False)
table.add_rule(And(PaperSubmission(R), PaperReview(R)), False)
table.add_rule(And(PaperSubmission(R), PaperReviewInfo(R)), False)
table.add_rule(And(PaperSubmission(R), PaperReviewContent(R)), False)
table.add_rule(And(PaperSubmission(R), PaperReviewInfoSubmission(R)), False)

table.add_rule(And(PaperDecision(R), PaperConflicts(R)), False)
table.add_rule(And(PaperDecision(R), PaperAssignments(R)), False)
table.add_rule(And(PaperDecision(R), PaperReview(R)), False)
table.add_rule(And(PaperDecision(R), PaperReviewInfo(R)), False)
table.add_rule(And(PaperDecision(R), PaperReviewContent(R)), False)
table.add_rule(And(PaperDecision(R), PaperReviewInfoSubmission(R)), False)

table.add_rule(And(PaperConflicts(R), PaperAssignments(R)), False)
table.add_rule(And(PaperConflicts(R), PaperReview(R)), False)
table.add_rule(And(PaperConflicts(R), PaperReviewInfo(R)), False)
table.add_rule(And(PaperConflicts(R), PaperReviewContent(R)), False)
table.add_rule(And(PaperConflicts(R), PaperReviewInfoSubmission(R)), False)

table.add_rule(And(PaperAssignments(R), PaperReview(R)), False)
table.add_rule(And(PaperAssignments(R), PaperReviewInfo(R)), False)
table.add_rule(And(PaperAssignments(R), PaperReviewContent(R)), False)
table.add_rule(And(PaperAssignments(R), PaperReviewInfoSubmission(R)), False)

table.add_rule(And(PaperReview(R), PaperReviewInfo(R)), False)
table.add_rule(And(PaperReview(R), PaperReviewContent(R)), False)
table.add_rule(And(PaperReview(R), PaperReviewInfoSubmission(R)), False)

table.add_rule(And(PaperReviewInfo(R), PaperReviewContent(R)), False)
table.add_rule(And(PaperReviewInfo(R), PaperReviewInfoSubmission(R)), False)

table.add_rule(And(PaperReviewContent(R), PaperReviewInfoSubmission(R)), False)
# ------------

ALLOWED = [[-1]*len(REQ)]
#### analysis ----------------
start = process_time()
size = 47 # without
#### with few explicit unsafe representing disjunction
#size = 167 # 47+ 120 

table.compute_table(REQ, size, ALLOWED)
# print ("size = " + str(size) + " time = " + str(floor(process_time()-start)))
# #print (str(table))
# print (str(table.get_info()))
#table.show_problems()
#table.check_problems(size)

#table.compare_problems(REQ, size)

