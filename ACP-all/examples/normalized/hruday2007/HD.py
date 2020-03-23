# -------------------
# 23/3/2020
# Hruday from Sasikumar2017
# -------------------
#### ---------------

# ------------
from hrudaycommon import * #@UnusedWildImport

# rule(cf1, HD_confirmation, true, 0.75) :-     is(card_symp_present, true),     is(chest_pain_type, cardiac).
table.add_rule(And(card_symp_present(X), chest_pain_type(X, cardiac)), HD_confirmation(X))
# rule(cf2, HD_confirmation, true, -0.20) :-     is(complaint, syncope),     is(epileptic, true).
table.add_rule(And(complaint(X, syncope), epileptic(X)), Not(HD_confirmation(X)))
# rule(cf3, HD_confirmation, true, -0.20) :-     is(complaint, syncope),     is(diabetic, yes).
table.add_rule(And(complaint(X, syncope), (diabetic(X) == diab_yes)), Not(HD_confirmation(X)))
# rule(cf4, HD_confirmation, true, -0.40) :-     is(complaint, syncope),     is(hypertensive, true).
table.add_rule(And(complaint(X, syncope), hypertensive(X)), Not(HD_confirmation(X)))
# rule(cf5, HD_confirmation, true, 0.60) :-     is(dysp_on_exertion, true).
table.add_rule(dysp_on_exertion(X), HD_confirmation(X))
# rule(cf6, HD_confirmation, true, 0.60) :-     is(dysp_on_exertion, true),     is(dysp_at_rest, true).
table.add_rule(And(dysp_on_exertion(X), dysp_at_rest(X)), HD_confirmation(X))
# rule(cf7, HD_confirmation, true, 0.60) :-     is(dysp_on_exertion, true),     is(PND, true).
table.add_rule(And(dysp_on_exertion(X), dysp_at_rest(X), PND(X)), HD_confirmation(X))
# rule(cf8, HD_confirmation, true, -0.40) :-     is(dysp_on_exertion, true),     is(lung_disease, true).
table.add_rule(And(dysp_on_exertion(X), lung_disease(X)), Not(HD_confirmation(X)))
# rule(cf12, HD_confirmation, true, -0.40) :-     is(complaint, swelling_of_feet),     is(kidney_disease, true).
table.add_rule(And(complaint(X, swelling_of_feet), kidney_disease(X)), Not(HD_confirmation(X)))
# rule(cf13, HD_confirmation, true, -0.40) :-     is(complaint, swelling_of_feet),     is(face_swelling, true).
table.add_rule(And(complaint(X, swelling_of_feet), face_swelling(X)), Not(HD_confirmation(X)))
# rule(cf15, HD_confirmation, true, -0.40) :-     is(PND, true),     is(lung_disease, true).
table.add_rule(And(PND(X), lung_disease(X)), Not(HD_confirmation(X)))
# rule(cf16, HD_confirmation, true, -0.40) :-     is(complaint, swelling_of_feet),     is(filariasis, true).
table.add_rule(And(complaint(X, swelling_of_feet), filariasis(X)), Not(HD_confirmation(X)))

# rule(cf9, HD_confirmation, true, 0.40) :-     is(palpitations, true).
table.add_rule(palpitations(X), HD_confirmation(X))
# rule(cf10, HD_confirmation, true, 0.20) :-     is(complaint, swelling_of_feet).
table.add_rule(complaint(X, swelling_of_feet), HD_confirmation(X))
# rule(cf11, HD_confirmation, true, 0.20) :-     is(complaint, swelling_of_feet),     is(sex, female),
#      gt(age, 15.0),     lt(age, 45.0),     isnot(pregnant, yes).
table.add_rule(And(complaint(X, swelling_of_feet), (sex(X) == female), (age(X) > 15), (age(X) < 45), Not(pregnant(X))), 
               HD_confirmation(X))
# rule(cf14, HD_confirmation, true, 0.20) :-     is(dysp_on_exertion, true),     is(orthopnoea, true).
table.add_rule(And(dysp_on_exertion(X), orthopnoea(X)), HD_confirmation(X))



# # #### 
# REQ = [card_symp_present(X), chest_pain_type(X, cardiac), filariasis(X), complaint(X, syncope), epileptic(X),
#           hypertensive(X), palpitations(X), #lung_disease(X), dysp_on_exertion(X), complaint(X, swelling_of_feet), 
#           kidney_disease(X), face_swelling(X), #(age(X) > 15), (age(X) < 45), pregnant(X), orthopnoea(X),
#           lung_disease(X)] #(sex(X) == female),  dysp_at_rest(X), PND(X), ]
# ALLOWED = [[-1]*len(REQ)]
# # #======================================analysis
# # start = process_time()
# size = 16
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
