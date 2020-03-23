# -------------------
# 23/3/2020
# GoodShow p255 Sasikumar2007
# -------------------
# -----------------

from goodshowcommon import * #@UnusedWildImport # 

# rule(id22b, colour_problem, true, 1.0) :-      is(problem_with_picture, true),     is(picture_seen_on_screen, yes),     is(type_of_picture_problem, colour).
table.add_rule(And(problem_with_picture(X), picture_seen_on_screen(X), (type_of_picture_problem(X) == colour)), colour_problem(X))
# rule(id22a, dimension_problem, true, 1.0) :-     is(problem_with_picture, true),     is(picture_seen_on_screen, yes),     is(type_of_picture_problem, dimension).
table.add_rule(And(problem_with_picture(X), picture_seen_on_screen(X), (type_of_picture_problem(X) == dimension)), dimension_problem(X))
# rule(id22c, brightness_problem, true, 1.0) :-     is(problem_with_picture, true),     is(picture_seen_on_screen, yes),     is(type_of_picture_problem, brightness).
table.add_rule(And(problem_with_picture(X), picture_seen_on_screen(X), (type_of_picture_problem(X) == brightness)), brightness_problem(X))
# rule(id22d, contrast_problem, true, 1.0) :-     is(problem_with_picture, true),     is(picture_seen_on_screen, yes),     is(type_of_picture_problem, contrast).
table.add_rule(And(problem_with_picture(X), picture_seen_on_screen(X), (type_of_picture_problem(X) == contrast)), contrast_problem(X))
# rule(id45, rolling_problem, true, 1.0) :-     is(problem_with_picture, true),     is(picture_seen_on_screen, yes),     is(type_of_picture_problem, steadiness),     is(unsteadiness, rolling_picture).
table.add_rule(And(problem_with_picture(X), picture_seen_on_screen(X), (type_of_picture_problem(X) == steadiness), unsteadiness(X)), rolling_problem(X))
# rule(id48, jumping_problem, true, 1.0) :-     is(problem_with_picture, true),     is(picture_seen_on_screen, yes),     is(type_of_picture_problem, steadiness),     is(unsteadiness, jumping_picture).
table.add_rule(And(problem_with_picture(X), picture_seen_on_screen(X), (type_of_picture_problem(X) == steadiness), Not(unsteadiness(X))), jumping_problem(X))


# #======================================analysis
# start = process_time()
#size = 6
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
