# -------------------
# 23/3/2020
# -------------------
# some exclusive rules 
# -----------------

from hrudaycommon import * #@UnusedWildImport

## first version
table.add_rule(And((diabetic(X) == diab_yes), (diabetic(X) == diab_no)), False)
table.add_rule(And((diabetic(X) == diab_yes), (diabetic(X) == diab_unknown)), False)
table.add_rule(And((diabetic(X) == diab_no), (diabetic(X) == diab_unknown)), False)
### alternative 
# table.add_rule((diab_yes == diab_no), False)
# table.add_rule((diab_yes == diab_unknown), False)
# table.add_rule((diab_no == diab_unknown), False)
# third version
#Distinct(diab_yes, diab_no, diab_unknown)

table.add_rule(And(chest_pain_locn(X, center_of_chest), chest_pain_locn(X, left_side)), False)
table.add_rule(And(chest_pain_locn(X, center_of_chest), chest_pain_locn(X, right_side)), False)
table.add_rule(And(chest_pain_locn(X, left_side), chest_pain_locn(X, right_side)), False)

# Cp_duration exclusive
#Distinct(few_hours, half_hour, a_few_minutes)
table.add_rule(And(cp_duration(X, few_hours), cp_duration(X, half_hour)), False)
table.add_rule(And(cp_duration(X, few_hours), cp_duration(X, a_few_minutes)), False)
table.add_rule(And(cp_duration(X, half_hour), cp_duration(X, a_few_minutes)), False)

# Sex 
table.add_rule(And((sex(X) == male), (sex(X) == female)), False)
#Distinct(male, female)
table.add_rule(pregnant(X), (sex(X) == female))
 
# REQ = [(sex(X) == male), (sex(X) == female), pregnant(X), (diabetic(X) == diab_yes), (diabetic(X) == diab_unknown), (diabetic(X) == diab_no),
#        cp_duration(X, half_hour), cp_duration(X, few_hours), cp_duration(X, a_few_minutes),
#        chest_pain_locn(X, center_of_chest), chest_pain_locn(X, right_side), chest_pain_locn(X, left_side)
#        ]
# 
# ALLOWED = [[-1]*len(REQ)]
# #  
# # #======================================analysis
# # start = process_time()
# size = 11 
# #   
# table.compute_table(REQ, size, ALLOWED)
# print ("size= " + str(size) + " time= " + str(floor(process_time()-start)))
#       
# #print (str(table))
# print (str(table.get_info()))
# table.show_problems()
# table.check_problems(size)
#   
# #table.compare_problems(size, REQ)