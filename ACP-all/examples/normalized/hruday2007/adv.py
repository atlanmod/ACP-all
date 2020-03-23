# -------------------
# 23/3/2020
# version without CF
# add a Patient parameter
# -------------------

from hrudaycommon import * #@UnusedWildImport

##### the rules -------------
# rule(a3, adv, diet, 0.90) :-      is(HD_confirmation, true),     gt(bmi, 30.0).
table.add_rule(And(HD_confirmation(X), (bmi(X) >= 30)), adv(X, diet))  # 
#rule(a301, adv, diet, 0.82) :-     is(HD_confirmation, true),     gt(bmi, 24.0),     le(bmi, 30.0).
table.add_rule(And(HD_confirmation(X), (bmi(X) >= 24), (bmi(X) < 30)), adv(X, diet))
#rule(a2, adv, hbp, 1.00) :-     is(hypertensive, true).
table.add_rule(hypertensive(X), adv(X, hpb))
#rule(a4, adv, strain, 0.95) :-     is(disease, IHD),     is(sedentary, yes),     is(managerial, yes).
table.add_rule(And((disease(X, IHD)), sedentary(X), managerial(X)), adv(X, strain))
#rule(a401, adv, strain, 0.80) :-     is(disease, IHD),     is(sedentary, no),     is(managerial, yes).
table.add_rule(And((disease(X, IHD)), Not(sedentary(X)), managerial(X)), adv(X, strain))
#rule(a5, adv, IHD_attn, 1.00) :-     is(disease, IHD).
table.add_rule(disease(X, IHD), adv(X, IHD_attn))
#rule(a602, adv, dont_smoke, 0.75) :-     isnot(disease, IHD),     is(hypertensive, true),     ge(number_of_cigs, 5.0).
table.add_rule(And(disease(X, IHD), hypertensive(X), (number_of_cigs(X) == 5)), adv(X, dont_smoke))
#rule(a601, adv, dont_smoke, 0.80) :-     is(disease, IHD),     ge(number_of_cigs, 5.0),     le(number_of_cigs, 10.0).
table.add_rule(And(disease(X, IHD), (number_of_cigs(X) > 5), (number_of_cigs(X) <= 10)), adv(X, dont_smoke))
#rule(a6, adv, dont_smoke, 0.85) :-     is(disease, IHD),     gt(number_of_cigs, 10.0).
table.add_rule(And(disease(X, IHD), (number_of_cigs(X) > 10)), adv(X, dont_smoke))
#rule(a7, adv, RHD_attn, 1.00) :-     is(disease, RHD).
table.add_rule(disease(X, RHD), adv(X, RHD_attn))
#rule(a8, adv, antibiotics, 1.00) :-     is(disease, RHD),     isnot(childhood_rfever, true).
table.add_rule(And(disease(X, RHD),  childhood_rfever(X)), adv(X, antibiotics))
#rule(a9, adv, CHD_attn, 1.00) :-     is(disease, CHD).
table.add_rule(disease(X, CHD), adv(X, CHD_attn))
#rule(a10, adv, less_salt, 0.80) :-     is(HD_confirmation, true),     is(hypertensive, true).
table.add_rule(And(HD_confirmation(X), hypertensive(X)), adv(X, less_salt))
#rule(a11, adv, diabetes_attn, 1.00) :-     is(HD_confirmation, true),     is(diabetic, yes).
table.add_rule(And(HD_confirmation(X), (diabetic(X) == diab_yes)), adv(X, diabetes_attn))
#rule(a12, adv, CARP, 1.00) :-     is(disease, CARP).
table.add_rule(disease(X, CARP), adv(X, CARP_attn))
#rule(a13, adv, no_evid, 1.00) :-      is(card_symp_present, true),     isnot(HD_confirmation, true),     isnot(disease, RHD),
#     isnot(disease, CHD),     isnot(disease, IHD),     isnot(disease, CARP).
table.add_rule(And(card_symp_present(X), HD_confirmation(X), Not(disease(X, RHD)), Not(disease(X, IHD)), Not(disease(X, CARP)), 
                   Not(disease(X, CHD))),                adv(X, no_evid))
#rule(a14, adv, watch, 1.00) :-     is(card_symp_present, true),     is(IH_risk, true),     isnot(HD_confirmation, true).
table.add_rule(And(card_symp_present(X), IH_risk(X), Not(HD_confirmation(X))),      adv(X, watch))
#rule(a15, adv, special, 1.00) :-     is(card_symp_present, true),     is(HD_confirmation, true),     isnot(disease, IHD),
#     isnot(disease, RHD),     isnot(disease, CHD),     isnot(disease, CARP).
table.add_rule(And(card_symp_present(X), HD_confirmation(X), Not(disease(X, RHD)), Not(disease(X, IHD)), 
                   Not(disease(X, CARP)), Not(disease(X, CHD))),                adv(X, special))
#rule(a16, adv, quit_alcohol, 1.00) :-      is(disease, CARP),     is(alcoholic, true).
table.add_rule(And(disease(X, CARP), alcoholic(X)),      adv(X, quit_alcohol))

# # ####  
# REQ = [(bmi(X) >= 30), (bmi(X) >= 24), (bmi(X) < 30), (number_of_cigs(X) == 5), (number_of_cigs(X) > 5), 
#        (number_of_cigs(X) <= 10), (number_of_cigs(X) > 10),
#            disease(X, IHD), disease(X, RHD), disease(X, CHD), disease(X, CARP), 
#            (diabetic(X) == diab_yes), HD_confirmation(X), hypertensive(X), sedentary(X), managerial(X), 
#            childhood_rfever(X), card_symp_present(X), IH_risk(X), alcoholic(X)]
# ALLOWED = [[-1]*len(REQ)]
# # #======================================analysis
# # start = process_time()
# size = 19
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

