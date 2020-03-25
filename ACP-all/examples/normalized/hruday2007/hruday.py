# -------------------
# 23/3/2020
# Hruday from Sasikumar2017
# -------------------

#### TODO avoir beaucoup de redondance ...

# ------------
from base import * #@UnusedWildImport # +11
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

#### len = 58 only in conditions
REQ = [(sex(X) == male), (sex(X) == female), (diabetic(X) == diab_yes), (diabetic(X) == diab_unknown), (diabetic(X) == diab_no),
        cp_duration(X, half_hour), cp_duration(X, few_hours), cp_duration(X, a_few_minutes),
        chest_pain_locn(X, center_of_chest), chest_pain_locn(X, right_side), chest_pain_locn(X, left_side), 
    childhood_rfever(X), chronic_penicil_usr(X), fever_with_jntpain(X), 
      cp_radiates(X),  (age(X) >= 10), (age(X) <= 40), (age(X) < 40), is_nails_blue(X), 
      val_surgery(X), bp_status(X), (systolic_bp(X) >= 160), (diastolic_bp(X) >= 95), 
      (number_of_cigs(X) > 0), (number_of_cigs(X) == 0), (number_of_drinks(X) == 0), (number_of_drinks(X) > 0),
        sedentary(X), managerial(X), ambitious(X), (age(X) >= 30), (bmi(X) > 24), 
        filariasis(X), complaint(X, syncope), epileptic(X),
        dysp_on_exertion(X), lung_disease(X), palpitations(X), complaint(X, swelling_of_feet), 
        pregnant(X), kidney_disease(X), face_swelling(X), (age(X) > 40), bypass_surg(X), 
         (hb_level(X) > 15), clubbed_fingers(X), complaint(X, chest_pain), 
            cough_linked_cp(X), sweating_linked_cp(X), exertion_linked_cp(X), complaint(X, tiredness),  
        (bmi(X) >= 30), (bmi(X) >= 24), (bmi(X) < 30), (number_of_cigs(X) == 5), (number_of_cigs(X) > 5),
         (number_of_cigs(X) <= 10), (number_of_cigs(X) > 10)
                  ]

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

ALLOWED = [[-1]*len(REQ)]

print(str(len(REQ)))
#======================================analysis
start = process_time()
size = 11+3+7+6+10+16+13+12+7+19  # total = 104

table.compute_table(REQ, size, ALLOWED)
# number of stored 93
# number of unsafes 11
# number of normalized store 93
# number of problems 0
# number of unsafe problems 11


# print ("size= " + str(size) + " time= " + str(floor(process_time()-start)))
    
#print (str(table))
# print (str(table.get_info()))
# table.show_problems()
#table.check_problems(size)

#table.compare_problems(size, REQ)


