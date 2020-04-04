# -------------------
# 2/4/2020
# Hruday from Sasikumar2017
# -------------------

#### TODO avoir beaucoup de redondance ...

# ------------
### from base import * #@UnusedWildImport # +11 forget it

from rfever import * #@UnusedWildImport # +3
from suspected_disease import * #@UnusedWildImport # +7
from other import * #@UnusedWildImport # +6
from IH_risk import * #@UnusedWildImport # +10
from HD import * #@UnusedWildImport # +16
from disease import * #@UnusedWildImport # +13
from chest_pain import * #@UnusedWildImport # +12
from card_symp import * #@UnusedWildImport # +7
from adv import * #@UnusedWildImport # +19

### compute (c1, bmi, (weight * 10000.0)/(height * height)). avoid it

# #### len = 58 only in conditions
# REQ = [(sex(X) == male), (sex(X) == female), (diabetic(X) == diab_yes), (diabetic(X) == diab_unknown), (diabetic(X) == diab_no),
#         cp_duration(X, half_hour), cp_duration(X, few_hours), cp_duration(X, a_few_minutes),
#         chest_pain_locn(X, center_of_chest), chest_pain_locn(X, right_side), chest_pain_locn(X, left_side), 
#     childhood_rfever(X), chronic_penicil_usr(X), fever_with_jntpain(X), 
#       cp_radiates(X),  (age(X) >= 10), (age(X) <= 40), (age(X) < 40), is_nails_blue(X), 
#       val_surgery(X), bp_status(X), (systolic_bp(X) >= 160), (diastolic_bp(X) >= 95), 
#       (number_of_cigs(X) > 0), (number_of_cigs(X) == 0), (number_of_drinks(X) == 0), (number_of_drinks(X) > 0),
#         sedentary(X), managerial(X), ambitious(X), (age(X) >= 30), (bmi(X) > 24), 
#         filariasis(X), complaint(X, syncope), epileptic(X),
#         dysp_on_exertion(X), lung_disease(X), palpitations(X), complaint(X, swelling_of_feet), 
#         pregnant(X), kidney_disease(X), face_swelling(X), (age(X) > 40), bypass_surg(X), 
#          (hb_level(X) > 15), clubbed_fingers(X), complaint(X, chest_pain), 
#             cough_linked_cp(X), sweating_linked_cp(X), exertion_linked_cp(X), complaint(X, tiredness),  
#         (bmi(X) >= 30), (bmi(X) >= 24), (bmi(X) < 30), (number_of_cigs(X) == 5), (number_of_cigs(X) > 5),
#          (number_of_cigs(X) <= 10), (number_of_cigs(X) > 10)
#                   ]
# Ordering REQ 
REQ = [diabetic(X) == diab_yes, diabetic(X) == diab_unknown,  diabetic(X) == diab_no, # 0 1 2
       chest_pain_locn(X, center_of_chest), chest_pain_locn(X, left_side), chest_pain_locn(X, right_side), # 3 4 5
       cp_duration(X, few_hours), cp_duration(X, half_hour), cp_duration(X, a_few_minutes), # 6 7 8
       sex(X) == male, sex(X) == female, pregnant(X), # 9 10 11
       childhood_rfever(X), chronic_penicil_usr(X), fever_with_jntpain(X), cp_radiates(X), # 12 13 14 15
       age(X) >= 10, age(X) <= 40, val_surgery(X), age(X) < 40, is_nails_blue(X), bp_status(X), # 16 17 18 19 20 21
       systolic_bp(X) >= 160, diastolic_bp(X) >= 95, number_of_cigs(X) > 0, number_of_cigs(X) == 0, # 22 23 24 25
       number_of_drinks(X) == 0, number_of_drinks(X) > 0, sedentary(X), managerial(X), ambitious(X), # 26 27 - 30
       age(X) >= 30, bmi(X) > 24, complaint(X, syncope), epileptic(X), dysp_on_exertion(X), # 31 32 33 34 35
       lung_disease(X), complaint(X, swelling_of_feet), kidney_disease(X), face_swelling(X), # 36 37 38 39
       filariasis(X), palpitations(X), age(X) > 40, bypass_surg(X), hb_level(X) > 15, clubbed_fingers(X), 
       # 40 41 42 43 44 45 
       complaint(X, chest_pain), cough_linked_cp(X), sweating_linked_cp(X), exertion_linked_cp(X), # 46 47 48 49 
       complaint(X, tiredness), bmi(X) >= 30, bmi(X) >= 24, bmi(X) < 30, # 50 51 52 53 
       number_of_cigs(X) == 5, number_of_cigs(X) > 5, number_of_cigs(X) <= 10, number_of_cigs(X) > 10] # 54 55 56 57

ALLOWED = [[-1]*len(REQ)] # without restrictions
### many restrictions not simple to express !
three_exclu = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
# 8 9 10 
sex_exclu = [[1, 0, 0], [0, 1, 0], [0, 1, 1]]
# 16 17 19 43 
# 24 25 
two_exclu = [[1, 0], [0, 1]]
# 54 55 56 57 mais aussi avec 24 25 ?

ALLOWED = gener_allowed([([0,1,2], three_exclu), ([3,4,5], three_exclu), ([6, 7, 8], three_exclu),
                         ([8,9,10], sex_exclu),  ([24, 25], two_exclu)], len(REQ))

#======================================analysis
#size = 11+3+7+6+10+16+13+12+7+19  # total = 104
size = 3+7+6+10+16+13+12+7+19  # total = 93

table.compute_table(REQ, size, ALLOWED)

# print ("size= " + str(size) + " time= " + str(floor(process_time()-start)))
    
#print (str(table))
# print (str(table.get_info()))
table.show_problems()
#table.check_problems(size)

###############===========================Normalized_OK
### pour avoir une idee avec _OK
# start = process_time()
# truc = minimizing(table.normalized_problems)
# print (str(len(truc)) + " time= " + str(floor(process_time()-start)))


# Heuristic says sufficient level is 4
# end #level= 4 #problems here 81 time = 5354
# checking checking= 184404 allseen 218550
# #total number of problems 81
# time PLA simplify sur 81 PBs = 0 ? TODO refaire

###############=============================
### with Normalized_BDD and all allowed
#level= 2 time = 2878
#checking checking= 1426 allseen 1383
# +temps long de simplification 

#### restrict allowed 
# end #level= 2 time = 101
# checking checking= 1357 allseen 1318
# simplif semble potable en temps = 57 elements
### time simplif espresso time= 298

#### ============ keep it 
### len=72 too much
# REQ = [(diabetic(X) == diab_yes), (diabetic(X) == diab_unknown), (sex(X) == male), (sex(X) == female), pregnant(X), 
#        (diabetic(X) == diab_no), cp_duration(X, half_hour), cp_duration(X, few_hours), cp_duration(X, a_few_minutes),
#         chest_pain_locn(X, center_of_chest), chest_pain_locn(X, right_side), chest_pain_locn(X, left_side),
#         childhood_rfever(X), chronic_penicil_usr(X), fever_with_jntpain(X), 
#        card_symp_present(X), IH_risk(X), cp_radiates(X),  (age(X) >= 10), (age(X) <= 40), 
#         HD_confirmation(X), (age(X) < 40), is_nails_blue(X), val_surgery(X),
#         bp_status(X), (systolic_bp(X) >= 160), (diastolic_bp(X) >= 95), (number_of_cigs(X) > 0), (number_of_cigs(X) == 0), 
#              (number_of_drinks(X) == 0), (number_of_drinks(X) > 0),
#         sedentary(X), managerial(X), ambitious(X), hypertensive(X), (age(X) >= 30), (bmi(X) > 24), 
#           chest_pain_type(X, cardiac), filariasis(X), complaint(X, syncope), epileptic(X),
#           palpitations(X), kidney_disease(X), face_swelling(X), lung_disease(X), 
#        suspected_disease(X, IHD), suspected_disease(X, CHD), suspected_disease(X, RHD), 
#                (age(X) > 40), bypass_surg(X), smoker(X), 
#                (hb_level(X) > 15), (age(X) < 15), clubbed_fingers(X), 
#                complaint(X, chest_pain),  
#             cough_linked_cp(X), sweating_linked_cp(X), exertion_linked_cp(X), 
#             complaint(X, swelling_of_feet), complaint(X, tiredness), 
#             (bmi(X) >= 30), (bmi(X) >= 24), (bmi(X) < 30), (number_of_cigs(X) == 5), (number_of_cigs(X) > 5), 
#        (number_of_cigs(X) <= 10), (number_of_cigs(X) > 10),
#            disease(X, IHD), disease(X, RHD), disease(X, CHD), disease(X, CARP), 
#            alcoholic(X)                                                 
#         ]
