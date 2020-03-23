# -------------------
# 23/3/2020
# Hruday from Sasikumar2017
# -------------------
#### ---------------

# ------------
from hrudaycommon import * #@UnusedWildImport

# rule(sd1, suspected_disease, IHD, 0.60) :-      is(card_symp_present, true),     is(IH_risk, true).
table.add_rule(And(card_symp_present(X), IH_risk(X)), suspected_disease(X, IHD))
# rule(sd2, suspected_disease, IHD, 0.18) :-     is(cp_radiates, true).
table.add_rule(And(card_symp_present(X), cp_radiates(X)), suspected_disease(X, IHD))
# rule(sd3, suspected_disease, RHD, 0.18) :-     is(card_symp_present, true),     gt(age, 10.0),     le(age, 40.0).
table.add_rule(And(card_symp_present(X), (age(X) >= 10), (age(X) <= 40)), suspected_disease(X, RHD))
# rule(sd4, suspected_disease, RHD, 0.80) :-     is(card_symp_present, true),     is(HD_confirmation, true),     isnot(IH_risk, true),     is(val_surgery, true).
table.add_rule(And(card_symp_present(X), HD_confirmation(X), Not(IH_risk(X)), val_surgery(X)), suspected_disease(X, RHD))
# rule(sd5, suspected_disease, CHD, 0.80) :-     is(card_symp_present, true),     lt(age, 40.0),     is(nails_blue, true).
table.add_rule(And(card_symp_present(X), (age(X) < 40), is_nails_blue(X)), suspected_disease(X, CHD))
# rule(sd6, suspected_disease, CHD, 0.18) :-     is(card_symp_present, true),     lt(age, 40.0).
table.add_rule(And(card_symp_present(X), (age(X) <= 40)), suspected_disease(X, CHD))
# rule(sd7, suspected_disease, CHD, 0.18) :-     is(card_symp_present, true),     lt(age, 15.0).
table.add_rule(And(card_symp_present(X), (age(X) < 15)), suspected_disease(X, CHD))

# #### 
# REQ = [card_symp_present(X), IH_risk(X), cp_radiates(X),  (age(X) >= 10), (age(X) <= 40), 
#                  HD_confirmation(X), (age(X) < 40), is_nails_blue(X), # (age(X) < 15), since redundant
#                  val_surgery(X)]
# 
# ALLOWED = [[-1]*len(REQ)]
#  
# # #======================================analysis
# # start = process_time()
# size = 7
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

