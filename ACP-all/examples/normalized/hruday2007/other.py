# -------------------
# 23/3/2020
# Hruday from Sasikumar2017
# -------------------
#### ---------------

# ------------
from hrudaycommon import * #@UnusedWildImport

# rule(ht1, hypertensive, true, 1.00) :-     is(bp_status, yes),     ge(systolic_bp, 160.0).
table.add_rule(And(bp_status(X), (systolic_bp(X) >= 160)), hypertensive(X))
# rule(ht2, hypertensive, true, 1.00) :-     is(bp_status, yes),     ge(diastolic_bp, 95.0).
table.add_rule(And(bp_status(X), (diastolic_bp(X) >= 95)), hypertensive(X))
# rule(cig1, smoker, true, 1.00) :-     gt(number_of_cigs, 19.0).
table.add_rule((number_of_cigs(X) > 0), smoker(X))
### 
# rule(cig2, smoker, true, 0.60) :-     gt(number_of_cigs, 9.0).
# rule(cig3, smoker, true, 0.30) :-     gt(number_of_cigs, 4.0).
# rule(cig4, smoker, true, 0.10) :-     le(number_of_cigs, 4.0),     gt(number_of_cigs, 0.0).
# rule(cig5, smoker, true, -1.00) :-     le(number_of_cigs, 0.0).
table.add_rule((number_of_cigs(X) == 0), Not(smoker(X)))
# rule(alco1, alcoholic, true, 1.00) :-     gt(number_of_drinks, 2.0).
# rule(alco2, alcoholic, true, 0.60) :-     gt(number_of_drinks, 1.0).
# rule(alco3, alcoholic, true, 0.30) :-     gt(number_of_drinks, 0.5).
# rule(alco4, alcoholic, true, -1.00) :-     le(number_of_drinks, 0.5).
table.add_rule((number_of_drinks(X) == 0), Not(alcoholic(X)))
table.add_rule((number_of_drinks(X) > 0), alcoholic(X))

# #### 
# REQ = [bp_status(X), (systolic_bp(X) >= 160), (diastolic_bp(X) >= 95), (number_of_cigs(X) > 0), (number_of_cigs(X) == 0), 
#              (number_of_drinks(X) == 0), (number_of_drinks(X) > 0)]
# 
# ALLOWED = [[-1]*len(REQ)]
# # # #======================================analysis
# # # start = process_time()
# size = 6
# # # 
# table.compute_table(REQ, size, ALLOWED)
# # print ("size= " + str(size) + " time= " + str(floor(process_time()-start)))
# #     
# # #print (str(table))
# # print (str(table.get_info()))
# # table.show_problems()
# # table.check_problems(size)
# # 
# # #table.compare_problems(size, REQ)
