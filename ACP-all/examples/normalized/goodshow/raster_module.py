# -------------------
# 23/3/2020
# GoodShow p255 Sasikumar2007
# -------------------
# -----------------

from goodshowcommon import * #@UnusedWildImport # +0

### rules for raster_present sound_present
#rule(id01_1, raster_present, true, 1.0) :-      is(problem_with_picture, true),     is(picture_seen_on_screen, yes).
table.add_rule(And(problem_with_picture(X), picture_seen_on_screen(X)), raster_present(X))
#rule(id01_3, raster_present, true, 1.0) :-     is(problem_with_picture, true),     is(picture_seen_on_screen, no),     is(dark_screen, no).
table.add_rule(And(problem_with_picture(X), Not(picture_seen_on_screen(X)), Not(dark_screen(X))), raster_present(X))
# rule(id01_4, raster_present, true, 1.0) :-     isnot(problem_with_picture, true). ###  forget
# rule(id01_5, raster_absent, true, 1.0) :-     is(problem_with_picture, true),     is(picture_seen_on_screen, no),     is(dark_screen, yes).
table.add_rule(And(problem_with_picture(X), Not(picture_seen_on_screen(X)), dark_screen(X)), Not(raster_present(X))) # 
###table.add_rule(And(problem_with_picture, Not(picture_seen_on_screen), dark_screen), Not(raster_present))
# rule(id02_1, sound_absent, true, 1.0) :-     is(problem_with_sound, true),     is(complete_silence, yes).
table.add_rule(And(problem_with_sound(X), complete_silence(X)), Not(sound_present(X))) # 
# rule(id02_2, sound_present, true, 1.0) :-     is(problem_with_sound, true),     is(complete_silence, no).
table.add_rule(And(problem_with_sound(X), Not(complete_silence(X))), sound_present(X)) # 
# rule(id02_3, sound_present, true, 1.0) :-     isnot(problem_with_sound, true). ###  forget

# #======================================analysis
# start = process_time()
#size = 5
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
