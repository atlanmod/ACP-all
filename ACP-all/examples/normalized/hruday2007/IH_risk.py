# -------------------
# 23/3/2020
# Hruday from Sasikumar2017
# -------------------
#### ---------------

# ------------
from hrudaycommon import * #@UnusedWildImport

# rule(ihr2, IH_risk, true, 0.15) :-      is(sedentary, yes).
table.add_rule(sedentary(X), IH_risk(X))
# rule(ihr3, IH_risk, true, 0.10) :-     is(managerial, yes).
table.add_rule(managerial(X), IH_risk(X))
# rule(ihr4, IH_risk, true, 0.15) :-     is(ambitious, true).
table.add_rule(ambitious(X), IH_risk(X))
# rule(ihr5, IH_risk, true, 0.20) :-     is(smoker, true).
table.add_rule(smoker(X), IH_risk(X))
# rule(ihr6, IH_risk, true, 0.20) :-     is(hypertensive, true).
table.add_rule(hypertensive(X), IH_risk(X))
# rule(ihr7, IH_risk, true, 0.10) :-     is(sex, male).
table.add_rule((sex(X) == male), IH_risk(X))
### rules ???
# rule(ihr9, IH_risk, true, 0.10) :-     gt(age, 30.0).
table.add_rule((age(X) >= 30), IH_risk(X))
# rule(ihr10, IH_risk, true, 0.10) :-     gt(age, 50.0).
table.add_rule((age(X) >= 50), IH_risk(X))
# rule(ihr11, IH_risk, true, 0.10) :-     is(sex, female),     gt(age, 55.0).
table.add_rule(And((age(X) >= 55), (sex(X) == female)), IH_risk(X))
# rule(ihr12, IH_risk, true, 0.20) :-     gt(bmi, 24.0).
table.add_rule((bmi(X) > 24), IH_risk(X))

# #### 
# REQ = [sedentary(X), managerial(X), ambitious(X), (sex(X) == male), # (age(X) >= 55), (sex(X) == female),
#           hypertensive(X), (age(X) >= 30), (bmi(X) > 24)] # age(X) >= 50
#  
# ALLOWED = [[-1]*len(REQ)]
# # #======================================analysis
# # start = process_time()
# size = 10
# # 
# table.compute_table(REQ, size, ALLOWED)
# # # print ("size= " + str(size) + " time= " + str(floor(process_time()-start)))
# # #     
# # # #print (str(table))
# # # print (str(table.get_info()))
# # # table.show_problems()
# # # table.check_problems(size)
# # # 
# # # #table.compare_problems(size, REQ)
