# -------------------
# 23/3/2020
# GoodShow p255 Sasikumar2007
# -------------------
# -----------------

from raster_module import * #@UnusedWildImport # +5

# #Rules for snowy picture
# rule(id03_1, snowy_picture, true, 1.0) :-     is(problem_with_picture, true),     is(raster_present, true),     is(snow_on_screen, true).
table.add_rule(And(raster_present(X), snow_on_screen(X)), snowy_picture(X))
# rule(id03_2, snowy_picture, true, -1.0) :-     is(problem_with_picture, true),     is(raster_present, true),     isnot(snow_on_screen, true).
table.add_rule(And(raster_present(X), Not(snow_on_screen(X))), Not(snowy_picture(X)))
# rule(id03_3, snowy_picture, true, -1.0) :-     isnot(problem_with_picture, true).
table.add_rule(Not(problem_with_picture(X)), Not(snowy_picture(X)))
# #Rules for TV dead
# rule(id12, TV_dead, true, 1.0) :-     is(raster_absent, true),     is(sound_absent, true).
table.add_rule(And(Not(sound_present(X)), Not(raster_present(X))), TV_dead(X))
# rule(id12_1, TV_dead, true, -1.0) :-     is(raster_present, true).
table.add_rule(raster_present(X), Not(TV_dead(X)))
# rule(id12_2, TV_dead, true, -1.0) :-     is(sound_present, true).
table.add_rule(sound_present(X), Not(TV_dead(X)))
# #Rules for suspect luma ckt
# rule(lpc1, suspect_luma_ckt, true, 0.5) :-     is(contrast_problem, true).
table.add_rule(contrast_problem(X), suspect_luma_ckt(X))
# rule(lpc2, suspect_luma_ckt, true, 0.5) :-     is(brightness_problem, true).
table.add_rule(brightness_problem(X), suspect_luma_ckt(X))

# REQ = [raster_present(X), snow_on_screen(X), problem_with_picture(X), sound_present(X), 
#         contrast_problem(X),  brightness_problem(X), picture_seen_on_screen(X), dark_screen(X),
#         problem_with_sound(X), complete_silence(X)]
#         
# ALLOWED = [[-1]*len(REQ)]
# 
# # #======================================analysis
# # start = process_time()
# size = 5+8
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
