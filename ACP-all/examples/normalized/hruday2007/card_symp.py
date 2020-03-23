# -------------------
# 23/3/2020
# Hruday from Sasikumar2017
# -------------------
#### ---------------

# ------------
from hrudaycommon import * #@UnusedWildImport

# rule(cs3, card_symp_present, true, 0.30) :-      is(complaint, swelling_of_feet).
table.add_rule(complaint(X, swelling_of_feet), card_symp_present(X))
# rule(cs1, card_symp_present, true, 0.40) :-      is(dysp_on_exertion, true).
table.add_rule(dysp_on_exertion(X), card_symp_present(X))
# rule(cs2, card_symp_present, true, 0.40) :-     is(palpitations, true).
table.add_rule(palpitations(X), card_symp_present(X))
# rule(cs4, card_symp_present, true, 0.08) :-     is(complaint, tiredness).
table.add_rule(complaint(X, tiredness), card_symp_present(X))
# rule(cs5, card_symp_present, true, 0.40) :-     is(nails_blue, true). 
table.add_rule(is_nails_blue(X), card_symp_present(X))
# rule(cs6, card_symp_present, true, 0.18) :-     is(complaint, syncope).
table.add_rule(complaint(X, syncope), card_symp_present(X))
# rule(cs8, card_symp_present, true, 0.40) :-     is(complaint, chest_pain).
table.add_rule(complaint(X, chest_pain), card_symp_present(X))

# #### 
# REQ = [complaint(X, swelling_of_feet), 
#             complaint(X, tiredness), is_nails_blue(X), complaint(X, syncope), complaint(X, chest_pain)]
# ALLOWED = [[-1]*len(REQ)]
# #======================================analysis
# start = process_time()
# size = 7
#   
# table.compute_table(REQ, size, ALLOWED)
# # print ("size= " + str(size) + " time= " + str(floor(process_time()-start)))
#      
# #print (str(table))
# print (str(table.get_info()))
# table.show_problems()
# table.check_problems(size)


