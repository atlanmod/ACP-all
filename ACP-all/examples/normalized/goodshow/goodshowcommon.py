# -------------------
# 23/3/2020
# GoodShow p 259 Sasikumar2007
# -------------------
# common type and predicates 
### change Real in IntSort()
### change CF into True/False
# level 0 attributes are variables ?
# -----------------

from Normalized_OK import * #@UnusedWildImport
from time import * #@UnusedWildImport
from math import * #@UnusedWildImport

# -------------------------- sorts
TV = DeclareSort('TV')
Type_of_picture_problem = DeclareSort('Type_of_picture_problem')
Type_of_colour_problem = DeclareSort('Type_of_colour_problem')
Type_of_raster = DeclareSort('Type_of_raster')
Faulty_module_type = DeclareSort('Faulty_module_type')

table = Normalized_Enumerate()
# Variables
table.add_variable('X', TV)
X = table.get_variable(0)

#### single predicates/functions level 0
problem_with_picture = Function('problem_with_picture', TV, BoolSort())  
problem_with_sound = Function('problem_with_sound', TV, BoolSort())  
picture_seen_on_screen = Function('picture_seen_on_screen', TV, BoolSort())  
type_of_picture_problem = Function('type_of_picture_problem', TV, Type_of_picture_problem)  
TV_age = Function('TV_age', TV, IntSort())  
dark_screen = Function('dark_screen', TV, BoolSort())  
complete_silence = Function('complete_silence', TV, BoolSort())  
snow_on_screen = Function('snow_on_screen', TV, BoolSort())  
panel_lights = Function('panel_lights', TV, BoolSort())  
picture_size_abnormal = Function('picture_size_abnormal', TV, BoolSort())  
brightness_too_low = Function('brightness_too_low', TV, BoolSort())  
contrast_too_high = Function('contrast_too_high', TV, BoolSort())  
type_of_raster = Function('type_of_raster', TV, Type_of_raster)  
picture_misaligned = Function('picture_misaligned', TV, BoolSort())  
height_problem = Function('height_problem', TV, BoolSort())  
width_problem = Function('width_problem', TV, BoolSort())  
colour_seen_on_screen = Function('colour_seen_on_screen', TV, BoolSort())  
type_of_colour_problem = Function('type_of_colour_problem', TV, Type_of_colour_problem)
lines_dots_netting_seen = Function('lines_dots_netting_seen', TV, BoolSort())  
ghosts_seen = Function('ghosts_seen', TV, BoolSort())  
horizontal_shift = Function('horizontal_shift', TV, BoolSort())  
vertical_shift = Function('vertical_shift', TV, BoolSort())  
unsteadiness = Function('unsteadiness', TV, BoolSort())  # menu(unsteadiness, [rolling_picture, jumping_picture]).
rolling_direction = Function('rolling_direction', TV, BoolSort()) # menu(rolling_direction, [vertical, horizontal]).
type_of_jumping = Function('type_of_jumping', TV, BoolSort()) # menu(type_of_jumping, [continuously, irregularly]).
sound_distorts_with_picture = Function('sound_distorts_with_picture', TV, BoolSort())  
plug_point_supply = Function('plug_point_supply', TV, BoolSort())  

#### Constants Type_of_picture_problem
# menu(type_of_picture_problem, [colour, dimension,
#                              brightness, contrast, steadiness]).
colour = Const('colour', Type_of_picture_problem)
dimension = Const('dimension', Type_of_picture_problem)
brightness = Const('brightness', Type_of_picture_problem)
contrast = Const('contrast', Type_of_picture_problem)
steadiness = Const('steadiness', Type_of_picture_problem)

#### Constants Type_of_colour_problem [may be distinct]
# menu(type_of_colour_problem, [pale_colours, incorrect_colours,
#                              intermittent_colours, colour_patch]).
pale_colours = Const('pale_colours', Type_of_colour_problem)
incorrect_colours = Const('incorrect_colours', Type_of_colour_problem)
intermittent_colours = Const('intermittent_colours', Type_of_colour_problem)
colour_patch = Const('colour_patch', Type_of_colour_problem)

### Type_of_raster
black_white_lines_or_bars = Const('black_white_lines_or_bars', Type_of_raster)
plain_white_screen = Const('plain_white_screen', Type_of_raster)
none = Const('none', Type_of_raster)
Distinct(black_white_lines_or_bars, plain_white_screen, none)

#### Constants Faulty_module_type 
antenna_or_tuner  = Const('antenna_or_tuner', Faulty_module_type)
mains_supply = Const('mains_supply', Faulty_module_type)
internal_power_supply = Const('internal_power_supply', Faulty_module_type)
hor_sect = Const('hor_sect', Faulty_module_type)
vert_sect = Const('vert_sect', Faulty_module_type)
sync_ckt = Const('sync_ckt', Faulty_module_type)
IF_amp = Const('IF_amp', Faulty_module_type)
colour_proc_ckt = Const('colour_proc_ckt', Faulty_module_type)
magnetisation = Const('magnetisation', Faulty_module_type)
luma_proc_ckt = Const('luma_proc_ckt', Faulty_module_type)
picture_tube = Const('picture_tube', Faulty_module_type)
interference = Const('interference', Faulty_module_type)
sound_proc_ckt = Const('sound_proc_ckt', Faulty_module_type)
speaker = Const('speaker', Faulty_module_type)

# ### --------------------------
#### predicates and function
raster_present = Function('raster_present', TV, BoolSort())  
sound_present = Function('sound_present', TV, BoolSort())  
snowy_picture = Function('snowy_picture', TV, BoolSort())  
TV_dead = Function('TV_dead', TV, BoolSort())  
colour_problem = Function('colour_problem', TV, BoolSort())  
dimension_problem = Function('dimension_problem', TV, BoolSort())  
brightness_problem = Function('brightness_problem', TV, BoolSort())  
contrast_problem = Function('contrast_problem', TV, BoolSort())  
rolling_problem = Function('rolling_problem', TV, BoolSort())  
jumping_problem = Function('jumping_problem', TV, BoolSort())  
suspect_sound_ckt = Function('suspect_sound_ckt', TV, BoolSort())  
suspect_colour_ckt = Function('suspect_colour_ckt', TV, BoolSort())  
suspect_IF_amp = Function('suspect_IF_amp', TV, BoolSort())  
suspect_sync_ckt  = Function('suspect_sync_ckt', TV, BoolSort())  
suspect_ante_tuner  = Function('suspect_ante_tuner', TV, BoolSort())  
size_problem  = Function('size_problem', TV, BoolSort())  
shift_problem  = Function('shift_problem', TV, BoolSort())  
suspect_picture_tube  = Function('suspect_picture_tube', TV, BoolSort())  
suspect_luma_ckt  = Function('suspect_luma_ckt', TV, BoolSort())  
faulty_module  = Function('faulty_module', TV, Faulty_module_type, BoolSort())  

# ### TV_age(X), type_of_colour_problem(X), type_of_picture_problem(X), type_of_raster(X),
# REQ = [problem_with_picture(X), problem_with_sound(X), picture_seen_on_screen(X), 
#        dark_screen(X), complete_silence(X), snow_on_screen(X), panel_lights(X), picture_size_abnormal(X), 
#        brightness_too_low(X), contrast_too_high(X), picture_misaligned(X), height_problem(X), 
#        width_problem(X), colour_seen_on_screen(X), lines_dots_netting_seen(X), 
#        ghosts_seen(X), horizontal_shift(X), vertical_shift(X), unsteadiness(X), rolling_direction(X), 
#        type_of_jumping(X), sound_distorts_with_picture(X), plug_point_supply(X)]

