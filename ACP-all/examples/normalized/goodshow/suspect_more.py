# -------------------
# 23/3/2020
# GoodShow p255 Sasikumar2007
# -------------------
# -----------------

from picture_module import * #@UnusedWildImport # +6

# #Rules for suspect IF amp
# rule(ifa1, suspect_IF_amp, true, 0.4) :-     is(contrast_problem, true).
table.add_rule(contrast_problem(X), suspect_IF_amp(X))
# rule(ifa2, suspect_IF_amp, true, 0.7) :-     is(colour_problem, true),     is(colour_seen_on_screen, no).
table.add_rule(And(colour_problem(X), Not(colour_seen_on_screen(X))), suspect_IF_amp(X))
# rule(ifa3, suspect_IF_amp, true, 0.7) :-     is(colour_problem, true),     is(colour_seen_on_screen, yes),     is(type_of_colour_problem, pale_colours).
table.add_rule(And(colour_problem(X), colour_seen_on_screen(X), (type_of_colour_problem(X) == pale_colours)), suspect_IF_amp(X))
# rule(ifa4, suspect_IF_amp, true, 0.7) :-     is(problem_with_picture, true),     is(picture_seen_on_screen, no).
table.add_rule(And(colour_problem(X), problem_with_picture(X), Not(picture_seen_on_screen(X))), suspect_IF_amp(X))
# #Rules for suspect sync ckt
# rule(sc1, suspect_sync_ckt, true, 0.6) :-     is(problem_with_picture, true),     is(picture_seen_on_screen, no).
table.add_rule(And(problem_with_picture(X), Not(picture_seen_on_screen(X))), suspect_sync_ckt(X))
# #Rules for suspect ante tuner
# rule(at1, suspect_ante_tuner, true, 0.5) :-     is(colour_problem, true),     is(colour_seen_on_screen, no).
table.add_rule(And(colour_problem(X), Not(colour_seen_on_screen(X))), suspect_ante_tuner(X))
# rule(at2, suspect_ante_tuner, true, 0.5) :-     is(colour_problem, true),     is(colour_seen_on_screen, yes),     is(type_of_colour_problem, pale_colours).
table.add_rule(And(colour_problem(X), colour_seen_on_screen(X), (type_of_colour_problem(X) == pale_colours)), suspect_ante_tuner(X))
# rule(at3, suspect_ante_tuner, true, 0.5) :-     is(colour_problem, true),     is(colour_seen_on_screen, yes),     is(type_of_colour_problem, intermittent_colours).
table.add_rule(And(colour_problem(X), colour_seen_on_screen(X), (type_of_colour_problem(X) == intermittent_colours)), suspect_ante_tuner(X))


# REQ = [problem_with_picture(X), picture_seen_on_screen(X), 
#        (type_of_picture_problem(X) == colour), (type_of_picture_problem(X) == dimension), 
#        (type_of_picture_problem(X) == brightness),
#              (type_of_picture_problem(X) == contrast), (type_of_picture_problem(X) == steadiness)]
# 
# ALLOWED = [[-1]*len(REQ)]
# # #======================================analysis
# # start = process_time()
# size = 6+8
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
