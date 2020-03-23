# -------------------
# 23/3/2020
# Hruday from Sasikumar2017
# -------------------
#### ---------------

# ------------
from hrudaycommon import * #@UnusedWildImport

# rule(dis1, disease, IHD, 1.00) :-      is(suspected_disease, IHD),     is(HD_confirmation, true).
table.add_rule(And(HD_confirmation(X), suspected_disease(X, IHD)), disease(X, IHD))
# rule(dis2, disease, IHD, 1.00) :-     is(suspected_disease, IHD),     isnot(IH_risk, true),     gt(age, 40.0),     is(bypass_surg, true).
table.add_rule(And(Not(IH_risk(X)), suspected_disease(X, IHD), (age(X) > 40), bypass_surg(X)), disease(X, IHD))
# rule(dis3, disease, RHD, 1.00) :-     is(suspected_disease, RHD),     is(HD_confirmation, true).
table.add_rule(And(suspected_disease(X, RHD), HD_confirmation(X)), disease(X, RHD))
# rule(dis4, disease, RHD, 0.40) :-     is(suspected_disease, RHD),     is(childhood_rfever, true).
table.add_rule(And(suspected_disease(X, RHD), childhood_rfever(X)), disease(X, RHD))
# rule(dis5, disease, RHD, 0.18) :-     is(suspected_disease, RHD),     isnot(HD_confirmation, true).
table.add_rule(And(suspected_disease(X, RHD), Not(HD_confirmation(X))), disease(X, RHD))
# rule(dis6, disease, RHD, 0.60) :-     is(suspected_disease, RHD),     is(rfever_evidence, true).
table.add_rule(And(suspected_disease(X, RHD), rfever_evidence(X)), disease(X, RHD))
# rule(dis7, disease, RHD, 0.40) :-     is(suspected_disease, RHD),     is(chorea, true).
table.add_rule(And(suspected_disease(X, RHD), chorea(X)), disease(X, RHD))
# rule(dis8, disease, CHD, 0.60) :-     lt(age, 15.0),     is(HD_confirmation, true),     gt(hb_level, 15.0).
table.add_rule(And((age(X) < 15), HD_confirmation(X), (hb_level(X) > 15)), disease(X, CHD))
# rule(dis9, disease, CHD, 0.60) :- lt(age, 15.0),     is(HD_confirmation, true),     is(nails_blue, true).
table.add_rule(And((age(X) < 15), HD_confirmation(X), is_nails_blue(X)), disease(X, CHD))
# rule(dis10, disease, CHD, 0.35) :-     is(suspected_disease, CHD),     is(clubbed_fingers, true).
table.add_rule(And(suspected_disease(X, CHD), clubbed_fingers(X)), disease(X, CHD))
# rule(dis11, disease, CHD, -0.21) :-     is(nails_blue, true),     gt(age, 40.0),     is(lung_disease, true).
table.add_rule(And(is_nails_blue(X), (age(X) > 40), lung_disease(X)), Not(disease(X, CHD)))
# rule(dis12, disease, CARP, 0.45) :-     gt(age, 40.0),     is(HD_confirmation, true),     is(nails_blue, true).
table.add_rule(And(HD_confirmation(X), (age(X) > 40), is_nails_blue(X)), disease(X, CARP))
# rule(dis13, disease, CHD, -0.11) :-     is(nails_blue, true),     gt(age, 40.0),     is(smoker, true).
table.add_rule(And(smoker(X), (age(X) > 40), is_nails_blue(X)), Not(disease(X, CHD)))

#### 
# REQ = [HD_confirmation(X), suspected_disease(X, IHD), suspected_disease(X, CHD), suspected_disease(X, RHD), 
#                IH_risk(X), (age(X) > 40), bypass_surg(X), childhood_rfever(X), smoker(X), # rfever_evidence(X), 
#                (hb_level(X) > 15), is_nails_blue(X), (age(X) < 15), clubbed_fingers(X), lung_disease(X)] # chorea(X), 
# 
# ALLOWED = [[-1]*len(REQ)]
# # #======================================analysis
# # start = process_time()
# size = 13
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
