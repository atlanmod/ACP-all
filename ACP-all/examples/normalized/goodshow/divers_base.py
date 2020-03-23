# -------------------
# 23/3/2020
# GoodShow p255 Sasikumar2007
# -------------------
# -----------------

from goodshowcommon import * #@UnusedWildImport # +0

#Rule for size problem
# rule(id22f, size_problem, true, 1.0) :-     is(dimension_problem, true),     is(picture_size_abnormal, true).
table.add_rule(And(dimension_problem(X),   picture_size_abnormal(X)), size_problem(X))
#Rule for shift problem
# rule(id22e, shift_problem, true, 1.0) :-     is(dimension_problem, true),  is(picture_misaligned,true).
table.add_rule(And(dimension_problem(X),   picture_misaligned(X)), shift_problem(X))
#Rules for suspect picture tube
# rule(id40_2, suspect_picture_tube, true, 0.7) :-     is(brightness_problem, true).
table.add_rule(brightness_problem(X), suspect_picture_tube(X))

# #======================================analysis
 
# size = 3
#  
# REQ = [dimension_problem(X),   picture_size_abnormal(X), brightness_problem(X), picture_misaligned(X)]
#  
# ALLOWED = [[-1]*len(REQ)]
#    
# table.compute_table(REQ, size, ALLOWED)
# #======================================analysis
# start = process_time()
#
# 
#table.compute_table(REQ, size)
# print ("size= " + str(size) + " time= " + str(floor(process_time()-start)))
#       
# #print (str(table))
# print (str(table.get_info()))
# table.show_problems()
# table.check_problems(size)
#   
# #table.compare_problems(size, REQ)
