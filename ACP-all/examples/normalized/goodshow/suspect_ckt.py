# -------------------
# 23/3/2020
# GoodShow p255 Sasikumar2007
# -------------------
# -----------------

from goodshowcommon import * #@UnusedWildImport # +0

# #Rules for suspect sound ckt
# rule(spc1, suspect_sound_ckt, true, 0.7) :-      is(problem_with_sound, true).
table.add_rule(problem_with_sound(X), suspect_sound_ckt(X))
# #        Rules for suspect colour ckt
# rule(cpc1, suspect_colour_ckt, true, 0.7) :-     is(colour_problem, true),     is(colour_seen_on_screen, no).
table.add_rule(And(colour_problem(X), Not(colour_seen_on_screen(X))), suspect_colour_ckt(X))
# rule(cpc2, suspect_colour_ckt, true, 0.7) :-     is(colour_problem, true),     is(colour_seen_on_screen, yes),     is(type_of_colour_problem, pale_colours).
table.add_rule(And(colour_problem(X), colour_seen_on_screen(X), (type_of_colour_problem(X) == pale_colours)), suspect_colour_ckt(X))
# rule(cpc3, suspect_colour_ckt, true, 0.7) :-     is(colour_problem, true),     is(colour_seen_on_screen, yes),     is(type_of_colour_problem, incorrect_colours).
table.add_rule(And(colour_problem(X), colour_seen_on_screen(X), (type_of_colour_problem(X) == incorrect_colours)), suspect_colour_ckt(X))
# rule(cpc4, suspect_colour_ckt, true, 0.7) :-     is(colour_problem, true),     is(colour_seen_on_screen, yes),     is(type_of_colour_problem, intermittent_colours).
table.add_rule(And(colour_problem(X), colour_seen_on_screen(X), (type_of_colour_problem(X) == intermittent_colours)), suspect_colour_ckt(X))

# REQ =  [ (type_of_colour_problem(X) == pale_colours), (type_of_colour_problem(X) == incorrect_colours), 
#         (type_of_colour_problem(X) == intermittent_colours)]
# 
# ALLOWED = [[-1]*len(REQ)]
# # #======================================analysis
# # start = process_time()
# size = 5
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
