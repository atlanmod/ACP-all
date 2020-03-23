# -------------------
# 23/3/2020
# Hruday from Sasikumar2017
# -------------------
#### ---------------

# ------------
from hrudaycommon import * #@UnusedWildImport

# rule(ch1, chest_pain_type, cardiac, 0.25) :-     is(complaint, chest_pain),     is(chest_pain_locn, center_of_chest).
table.add_rule(And(complaint(X, chest_pain), chest_pain_locn(X, center_of_chest)), chest_pain_type(X, cardiac))
# rule(ch2, chest_pain_type, cardiac, 0.25) :-     is(complaint, chest_pain),     is(chest_pain_locn, left_side).
table.add_rule(And(complaint(X, chest_pain), chest_pain_locn(X, left_side)), chest_pain_type(X, cardiac))
# rule(ch3, chest_pain_type, cardiac, -0.18) :-     is(complaint, chest_pain),     is(chest_pain_locn, right_side).
table.add_rule(And(complaint(X, chest_pain), chest_pain_locn(X, right_side)), chest_pain_type(X, cardiac))
# rule(ch5, chest_pain_type, cardiac, 0.35) :-     is(complaint, chest_pain),     is(cp_radiates, true).
table.add_rule(And(complaint(X, chest_pain), cp_radiates(X)), chest_pain_type(X, cardiac))
# -- use Not ?
# rule(ch6, chest_pain_type, cardiac, -0.18) :-     is(complaint, chest_pain),     is(cough_linked_cp, true).
table.add_rule(And(complaint(X, chest_pain), cough_linked_cp(X)), Not(chest_pain_type(X, cardiac)))
# rule(ch7, chest_pain_type, cardiac, 0.40) :-     is(complaint, chest_pain),     is(sweating_linked_cp, true).
table.add_rule(And(complaint(X, chest_pain), sweating_linked_cp(X)), chest_pain_type(X, cardiac))
# rule(ch8, chest_pain_type, cardiac, 0.40) :-     is(complaint, chest_pain),     is(exertion_linked_cp, true).
table.add_rule(And(complaint(X, chest_pain), exertion_linked_cp(X)), chest_pain_type(X, cardiac))
# rule(ch9, chest_pain_type, cardiac, -0.20) :-     is(complaint, chest_pain),     is(breath_linked_cp, true).
table.add_rule(And(complaint(X, chest_pain), breath_linked_cp(X)), Not(chest_pain_type(X, cardiac)))
# rule(ch10, chest_pain_type, cardiac, -0.20) :-     is(complaint, chest_pain),     is(lung_disease, true).
table.add_rule(And(complaint(X, chest_pain), lung_disease(X)), Not(chest_pain_type(X, cardiac)))
# rule(ch11, chest_pain_type, cardiac, 0.10) :-     is(complaint, chest_pain),     is(cp_duration, few_hours).
table.add_rule(And(complaint(X, chest_pain), cp_duration(X, few_hours)), chest_pain_type(X, cardiac))
# rule(ch12, chest_pain_type, cardiac, 0.25) :-     is(complaint, chest_pain),     is(cp_duration, half_hour).
table.add_rule(And(complaint(X, chest_pain), cp_duration(X, half_hour)), chest_pain_type(X, cardiac))
# rule(ch4, chest_pain_type, cardiac, 0.10) :-     is(complaint, chest_pain),     is(cp_duration, a_few_minutes).
table.add_rule(And(complaint(X, chest_pain), cp_duration(X, a_few_minutes)), chest_pain_type(X, cardiac))

# #### 
# REQ = [complaint(X, chest_pain), chest_pain_locn(X, center_of_chest), chest_pain_locn(X, left_side), chest_pain_locn(X, right_side),
#             cough_linked_cp(X), sweating_linked_cp(X), exertion_linked_cp(X), 
#             cp_duration(X, few_hours), cp_duration(X, half_hour), cp_duration(X, a_few_minutes), lung_disease(X)]
# ALLOWED = [[-1]*len(REQ)]
# # #======================================analysis
# # start = process_time()
# size = 12
# # 
# table.compute_table(REQ, size, ALLOWED)
# # print ("size= " + str(size) + " time= " + str(floor(process_time()-start)))
# #     
# # #print (str(table))
# # print (str(table.get_info()))
# # table.show_problems()
# # table.check_problems(size)
# # 
# # #table.compare_problems(size, REQ)

