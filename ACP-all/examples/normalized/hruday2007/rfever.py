# -------------------
# 23/3/2020
# Hruday from Sasikumar2017
# -------------------
#### ---------------

# ------------
from hrudaycommon import * #@UnusedWildImport

#rule(rf1, rfever_evidence, true, 0.60) :-     isnot(childhood_rfever, true),     is(chronic_penicil_usr, true).
table.add_rule(And(Not(childhood_rfever(X)), chronic_penicil_usr(X)),  rfever_evidence(X))
#rule(rf2, rfever_evidence, true, 0.40) :-     isnot(childhood_rfever, true),     is(fever_with_jntpain, true).
table.add_rule(And(Not(childhood_rfever(X)), fever_with_jntpain(X)),  rfever_evidence(X))
#rule(rf3, rfever_evidence, true, 0.21) :-     isnot(childhood_rfever, true),     is(fever_with_jntpain, true),     is(sore_throat_fever, true).
table.add_rule(And(Not(childhood_rfever(X)), fever_with_jntpain(X), sore_throat_fever(X)),  rfever_evidence(X))

# # #### 
# REQ = [childhood_rfever(X), chronic_penicil_usr(X), fever_with_jntpain(X)] #, sore_throat_fever(X)] since redundant
# ALLOWED = [[-1]*len(REQ)]
# # 
# # # #======================================analysis
# # # start = process_time()
# size = 3
# # # 
# table.compute_table(REQ, size, ALLOWED)
# # print ("size= " + str(size) + " time= " + str(floor(process_time()-start)))
# #     
# # #print (str(table))
# # print (str(table.get_info()))
# # table.show_problems()
# # table.check_problems(size)
# # 
# # #table.compare_problems(size, REQ)
