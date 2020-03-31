# -------------------
# 27/3/2020
# GoodShow p255 Sasikumar2007
# -------------------
# -----------------

from divers_base import * #@UnusedWildImport # +3
from divers_more import * #@UnusedWildImport # +13
from suspect_ckt import * #@UnusedWildImport # +5
from suspect_more import * #@UnusedWildImport # +14

### rules
# rule(id19, faulty_module, antenna_or_tuner, 0.8) :-     is(problem_with_picture, true),     is(picture_seen_on_screen, no),     is(snowy_picture, true),     is(sound_absent, true).
table.add_rule(And(problem_with_picture(X), picture_seen_on_screen(X), snowy_picture(X), Not(sound_present(X))) , faulty_module(X, antenna_or_tuner))
# rule(id30, faulty_module, antenna_or_tuner, 0.7) :-     is(suspect_ante_tuner, true),     is(snowy_picture, true).
table.add_rule(And(suspect_ante_tuner(X), snowy_picture(X)) , faulty_module(X, antenna_or_tuner))
# rule(id35, faulty_module, antenna_or_tuner, 0.7) :-     is(contrast_problem, true),     is(snowy_picture, true).
table.add_rule(And(contrast_problem(X), snowy_picture(X)) , faulty_module(X, antenna_or_tuner))
# rule(id42, faulty_module, antenna_or_tuner, 0.8) :-     is(problem_with_picture, true),     is(picture_seen_on_screen, yes),     is(Ghosts_seen, true).
table.add_rule(And(problem_with_picture(X), picture_seen_on_screen(X), ghosts_seen(X)) , faulty_module(X, antenna_or_tuner))
# rule(id50, faulty_module, antenna_or_tuner, 0.8) :-     is(jumping_problem, true),     is(type_of_jumping, irregularly).
table.add_rule(And(jumping_problem(X), Not(type_of_jumping(X))) , faulty_module(X, antenna_or_tuner))
# rule(id13, faulty_module, mains_supply, 0.4) :-     is(TV_dead, true),     is(panel_lights, off),     isnot(plug_point_supply, true).
table.add_rule(And(TV_dead(X), Not(panel_lights(X)), Not(plug_point_supply(X))) , faulty_module(X, mains_supply))
# rule(id14, faulty_module, internal_power_supply, 0.4) :-     is(TV_dead, true),      is(panel_lights, off),     is(plug_point_supply, true).
table.add_rule(And(TV_dead(X), Not(panel_lights(X)), plug_point_supply(X)) , faulty_module(X, internal_power_supply))
# rule(id15, faulty_module, hor_sect, 0.4) :-     is(TV_dead, true),     is(panel_lights, on).
table.add_rule(And(TV_dead(X), panel_lights(X)) , faulty_module(X, hor_sect))
# rule(id18, faulty_module, hor_sect, 0.8) :-     is(problem_with_picture, true),     is(raster_present, true),     isnot(snowy_picture, true),     is(type_of_raster, black&white_lines_or_bars).
table.add_rule(And(problem_with_picture(X), raster_present(X), snowy_picture(X), (type_of_raster(X) == black_white_lines_or_bars)), faulty_module(X, hor_sect))
# rule(id21_1, faulty_module, hor_sect, 0.8) :-     is(raster_absent, true),     is(sound_present, true).
table.add_rule(And(problem_with_picture(X), Not(raster_present(X)), sound_present(X)), faulty_module(X, hor_sect))
# rule(id24, faulty_module, hor_sect, 0.7) :-     is(size_problem, true),     is(width_problem, true).
table.add_rule(And(size_problem(X), width_problem(X)), faulty_module(X, hor_sect))
# rule(id43, faulty_module, hor_sect, 0.7) :-     is(shift_problem,true),     is(horizontal_shift, true).
table.add_rule(And(shift_problem(X), horizontal_shift(X)), faulty_module(X, hor_sect))
# rule(id39, faulty_module, hor_sect, 0.25) :-     is(brightness_problem, true).
table.add_rule(brightness_problem(X), faulty_module(X, hor_sect))
# rule(id39_1, faulty_module, hor_sect, 0.5) :-     is(brightness_problem, true),     isnot(snowy_picture, true). # redundant
# rule(id46, faulty_module, hor_sect, 0.8) :-     is(rolling_problem, true),     is(rolling_direction, horizontal).
table.add_rule(And(rolling_problem(X), Not(rolling_direction(X))), faulty_module(X, hor_sect))
# rule(id23, faulty_module, vert_sect, 0.7) :-     is(size_problem, true),     is(height_problem, true).
table.add_rule(And(size_problem(X), height_problem(X)), faulty_module(X, vert_sect))
# rule(id44, faulty_module, vert_sect, 0.7) :-     is(shift_problem, true),     is(vertical_shift, true).
table.add_rule(And(shift_problem(X), vertical_shift(X)), faulty_module(X, vert_sect))
# rule(id47, faulty_module, vert_sect, 0.8) :-     is(rolling_problem, true),     is(rolling_direction, vertical).
table.add_rule(And(rolling_problem(X), rolling_direction(X)), faulty_module(X, vert_sect))
# rule(id49, faulty_module, vert_sect, 0.7) :-     is(jumping_problem, true),     is(type_of_jumping, continuously).
table.add_rule(And(jumping_problem(X), type_of_jumping(X)), faulty_module(X, vert_sect))
# rule(id17, faulty_module, sync_ckt, 0.8) :-     is(suspect_sync_ckt, true),     is(raster_present, true),     isnot(snowy_picture, true),
#      is(type_of_raster, black&white_lines_or_bars),     is(sound_absent, true).
table.add_rule(And(suspect_sync_ckt(X), raster_present(X), Not(snowy_picture(X)), (type_of_raster(X) == black_white_lines_or_bars), Not(sound_present(X))), 
               faulty_module(X, sync_ckt))
# rule(id20, faulty_module, IF_amp, 0.8) :-     is(suspect_IF_amp, true),     is(raster_present, true),     isnot(snowy_picture, true),     is(type_of_raster, plain_white_screen).
table.add_rule(And(suspect_IF_amp(X), raster_present(X), Not(snowy_picture(X)), (type_of_raster(X) == plain_white_screen)), faulty_module(X, sync_ckt))
# rule(id20_1, faulty_module, IF_amp, 0.5) :-     is(suspect_IF_amp, true),     is(raster_present, true),     is(sound_present, true).
table.add_rule(And(suspect_IF_amp(X), raster_present(X), sound_present(X)), faulty_module(X, sync_ckt))
# rule(id21_2, faulty_module, IF_amp, 0.4) :-     is(suspect_IF_amp, true),     is(raster_absent, true),     is(sound_present, true).
table.add_rule(And(suspect_IF_amp(X), Not(raster_present(X)), sound_present(X)), faulty_module(X, sync_ckt))
# rule(id28, faulty_module, IF_amp, 0.4) :-     is(suspect_IF_amp, true),     isnot(snowy_picture, true).
table.add_rule(And(suspect_IF_amp(X), Not(snowy_picture(X))), faulty_module(X, sync_ckt))
# rule(id29, faulty_module, colour_proc_ckt, 0.8) :-     is(suspect_colour_ckt, true),     isnot(snowy_picture, true).
table.add_rule(And(suspect_colour_ckt(X), Not(snowy_picture(X))), faulty_module(X, colour_proc_ckt))
# rule(id34, faulty_module, magnetisation, 0.9) :-     is(colour_problem, true),     is(colour_seen_on_screen, yes),     is(type_of_colour_problem, colour_patch).
table.add_rule(And(colour_problem(X), colour_seen_on_screen(X), (type_of_colour_problem(X) == colour_patch)), faulty_module(X, magnetisation))
# rule(id36_1, faulty_module, luma_proc_ckt, 0.4) :-     is(suspect_luma_ckt, true),     isnot(snowy_picture, true).
table.add_rule(And(suspect_luma_ckt(X), Not(snowy_picture(X))), faulty_module(X, luma_proc_ckt))
# rule(id37, faulty_module, luma_proc_ckt, 0.6) :-     is(suspect_luma_ckt, true),     isnot(snowy_picture, true),     is(contrast_too_high, true). # redundant
# rule(id40_0, faulty_module, picture_tube, 0.5) :-     is(suspect_picture_tube, true),     isnot(snowy_picture, true),     is(brightness_too_low, true).
table.add_rule(And(suspect_picture_tube(X), Not(snowy_picture(X)), brightness_too_low(X)), faulty_module(X, picture_tube))
# rule(id53_1, faulty_module, picture_tube, 0.25) :-     is(suspect_picture_tube, true),     isnot(snowy_picture, true),     ge(TV_age, 8.0).
table.add_rule(And(suspect_picture_tube(X), Not(snowy_picture(X)), (TV_age(X) >= 8)), faulty_module(X, picture_tube))
# redundant
# rule(id40_1, faulty_module, picture_tube, 0.7) :-     is(suspect_picture_tube, true),isnot(snowy_picture, true),     is(brightness_too_low, true),     ge(TV_age, 8.0).
# rule(id41, faulty_module, interference, 0.8) :-     is(problem_with_picture, true),     is(picture_seen_on_screen, yes),     is(Lines_dots_Netting_seen, true).
table.add_rule(And(problem_with_picture(X), picture_seen_on_screen(X), lines_dots_netting_seen(X)), faulty_module(X, interference))
# rule(id52, faulty_module, interference, 0.8) :-     is(problem_with_sound, true),     is(sound_present, true),     is(raster_present, true),     is(sound_distorts_with_picture, true).
table.add_rule(And(problem_with_sound(X), sound_present(X), raster_present(X), sound_distorts_with_picture(X)), faulty_module(X, interference))
# rule(id51_2, faulty_module, sound_proc_ckt, 0.8) :-     is(suspect_sound_ckt, true),     is(sound_present, true),     is(raster_present, true),     isnot(sound_distorts_with_picture, true).
table.add_rule(And(suspect_sound_ckt(X), sound_present(X), raster_present(X), Not(sound_distorts_with_picture(X))), faulty_module(X, sound_proc_ckt))
# rule(id51_3, faulty_module, sound_proc_ckt, 0.6) :-     is(suspect_sound_ckt, true),     is(sound_absent, true),     is(raster_present, true).
table.add_rule(And(suspect_sound_ckt(X), Not(sound_present(X)), raster_present(X)), faulty_module(X, sound_proc_ckt))
# rule(id51_4, faulty_module, speaker, 0.5) :-     is(problem_with_sound, true),     is(sound_absent, true),     is(raster_present, true).
table.add_rule(And(problem_with_sound(X), Not(sound_present(X)), raster_present(X)), faulty_module(X, speaker))

REQ = [dimension_problem(X),   picture_size_abnormal(X), brightness_problem(X), picture_misaligned(X), 
       raster_present(X), snow_on_screen(X), problem_with_picture(X), sound_present(X), 
       contrast_problem(X),  picture_seen_on_screen(X), dark_screen(X),
       problem_with_sound(X), complete_silence(X),
       (type_of_colour_problem(X) == pale_colours), (type_of_colour_problem(X) == incorrect_colours), 
       (type_of_colour_problem(X) == intermittent_colours),
       (type_of_picture_problem(X) == colour), (type_of_picture_problem(X) == dimension), 
       (type_of_picture_problem(X) == brightness),
       (type_of_picture_problem(X) == contrast), (type_of_picture_problem(X) == steadiness),
       (type_of_raster(X) == black_white_lines_or_bars), (type_of_raster(X) == plain_white_screen),
       (type_of_colour_problem(X) == colour_patch),              (TV_age(X) >= 8)]

ALLOWED = [[-1]*len(REQ)]
# #======================================analysis
start = process_time()
size = 3+13+5+14+33 # (Total= 68)
  
table.compute_table(REQ, size, ALLOWED)
#print ("size= " + str(size) + " time= " + str(floor(process_time()-start)))
      
# #print (str(table))
# print (str(table.get_info()))
# table.show_problems()
# table.check_problems(size)
  
#table.compare_problems(size, REQ)

