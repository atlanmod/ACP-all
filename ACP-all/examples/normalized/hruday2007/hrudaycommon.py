# -------------------
# 23/3/2020
# -------------------
# utile type and predicates 
### change Real in IntSort()
# -----------------

### resort it

from Normalized_OK import * #@UnusedWildImport
from time import * #@UnusedWildImport
from math import * #@UnusedWildImport

# --------------------------
Patient = DeclareSort('Patient')
Adv = DeclareSort('Adv')
Disease = DeclareSort('Disease')
Suspected_disease = DeclareSort('Suspected_disease') #m
Chest_pain_type = DeclareSort('Chest_pain_type') #m
Diabetic = DeclareSort('Diabetic') #p
Complaint = DeclareSort('Complaint') #m
Chest_pain_locn = DeclareSort('Chest_pain_locn') #m
Sex = DeclareSort('Sex') #p
Status = DeclareSort('Status') #p
Pregnant = DeclareSort('Pregnant') #p
Cp_duration = DeclareSort('Cp_duration') #p

table = Normalized_Enumerate()
# Variables
table.add_variable("X", Patient)

### 
X = table.get_variable(0) # 

#### Constants Adv not necessarily exclusive
diet = Const('diet', Adv)
hpb = Const('hpb', Adv)
strain = Const('strain', Adv)
IHD_attn = Const('IHD_attn', Adv)
dont_smoke = Const('dont_smoke', Adv)
RHD_attn = Const('RHD_attn', Adv)
antibiotics = Const('antibiotics', Adv)
CHD_attn = Const('CHD_attn', Adv)
less_salt = Const('less_salt', Adv)
diabetes_attn = Const('diabetes_attn', Adv)
CARP_attn = Const('CARP_attn', Adv)
no_evid = Const('no_evid', Adv)
watch = Const('watch', Adv)
special = Const('special', Adv)
quit_alcohol = Const('quit_alcohol', Adv)

few_hours = Const('few_hours', Cp_duration)
half_hour = Const('half_hour', Cp_duration)
a_few_minutes  = Const('a_few_minutes', Cp_duration)

# diseases not necessarily exclusive
IHD = Const('IHD', Disease) # Ischaemic Heart Disease (IHD)
RHD = Const('RHD', Disease) # Rheumatic Heart Disease (RHD)
CHD = Const('CHD', Disease) # Congenital Heart Disease (CHD)
CARP = Const('CARP', Disease) # Cor Pulmonale (CARP)

# diabetic exclusive
diab_yes = Const('diab_yes', Diabetic)
diab_no = Const('diab_no', Diabetic)
diab_unknown = Const('diab_unknwon', Diabetic)
diabetic  = Function('diabetic', Patient, Diabetic)

# pains not necessarily exclusive
swelling_of_feet = Const('swelling_of_feet', Complaint)
tiredness = Const('tiredness', Complaint)
syncope = Const('syncope', Complaint)
chest_pain = Const('chest_pain', Complaint)

# chest_pain_type
cardiac = Const('cardiac', Chest_pain_type)

# Chest_pain_locn exclusive
center_of_chest = Const('center_of_chest', Chest_pain_locn)
left_side  = Const('left_side', Chest_pain_locn)
right_side   = Const('right_side', Chest_pain_locn)
#Distinct(center_of_chest, left_side, right_side)
chest_pain_locn = Function('chest_pain_locn', Patient, Chest_pain_locn, BoolSort()) 

# ### --------------------------
### predicates and functions
sex = Function('sex', Patient, Sex) 
male =  Const('male', Sex)
female =  Const('female', Sex)
pregnant = Function('pregnant', Patient, BoolSort()) 

cp_duration = Function('cp_duration', Patient, Cp_duration, BoolSort()) 

adv = Function('adv', Patient, Adv, BoolSort()) 
bmi = Function('bmi', Patient, IntSort()) 
age = Function('age', Patient, IntSort()) 
hb_level = Function('hb_level', Patient, IntSort()) 
systolic_bp = Function('systolic_bp', Patient, IntSort()) 
diastolic_bp = Function('diastolic_bp', Patient, IntSort())
number_of_drinks = Function('number_of_drinks', Patient, IntSort())

HD_confirmation = Function('HD_confirmation', Patient, BoolSort()) 
hypertensive = Function('hypertensive', Patient, BoolSort()) 
disease = Function('disease', Patient, Disease, BoolSort()) 
sedentary = Function('sedentary', Patient, BoolSort()) 
managerial = Function('managerial', Patient, BoolSort())
number_of_cigs = Function('number_of_cigs', Patient, IntSort())
IH_risk  = Function('IH_risk', Patient, BoolSort())
alcoholic = Function('alcoholic', Patient, BoolSort())
childhood_rfever = Function('childhood_rfever', Patient, BoolSort())
card_symp_present = Function('card_symp_present', Patient, BoolSort()) 
complaint = Function('complaint', Patient, Complaint, BoolSort()) 
is_nails_blue  = Function('is_nails_blue', Patient, BoolSort()) 
chest_pain_type = Function('chest_pain_type', Patient, Chest_pain_type, BoolSort()) 
cp_radiates = Function('cp_radiates', Patient, BoolSort()) 
cough_linked_cp = Function('cough_linked_cp', Patient, BoolSort()) 
sweating_linked_cp   = Function('sweating_linked_cp', Patient, BoolSort()) 
exertion_linked_cp = Function('exertion_linked_cp', Patient, BoolSort()) 
breath_linked_cp  = Function('breath_linked_cp', Patient, BoolSort()) 
suspected_disease = Function('suspected_disease', Patient, Disease, BoolSort()) 
val_surgery = Function('val_surgery', Patient, BoolSort()) 
ambitious = Function('ambitious', Patient, BoolSort()) 
smoker = Function('smoker', Patient, BoolSort()) 
lung_disease  = Function('lung_disease', Patient, BoolSort()) 
bypass_surg = Function('bypass_surg', Patient, BoolSort()) 
rfever_evidence  = Function('rfever_evidence', Patient, BoolSort()) 
clubbed_fingers = Function('clubbed_fingers', Patient, BoolSort()) 
chorea = Function('chorea', Patient, BoolSort()) 
epileptic = Function('epileptic', Patient, BoolSort()) 
dysp_on_exertion  = Function('dysp_on_exertion', Patient, BoolSort()) 
palpitations  = Function('palpitations', Patient, BoolSort()) 
dysp_at_rest = Function('dysp_at_rest', Patient, BoolSort()) 
PND = Function('PND', Patient, BoolSort()) 
kidney_disease  = Function('kidney_disease', Patient, BoolSort()) 
face_swelling = Function('face_swelling', Patient, BoolSort())
orthopnoea  = Function('orthopnoea', Patient, BoolSort())
filariasis  = Function('filariasis', Patient, BoolSort())
bp_status  = Function('bp_status', Patient, BoolSort())
fever_with_jntpain  = Function('fever_with_jntpain', Patient, BoolSort())
chronic_penicil_usr  = Function('chronic_penicil_usr', Patient, BoolSort())
sore_throat_fever  = Function('sore_throat_fever ', Patient, BoolSort())
