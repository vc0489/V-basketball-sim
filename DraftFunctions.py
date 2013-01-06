import random
from GlobalVariables import *
import decimal
from PlayerClass import *


                   
def gen_shot_pros(in_pro_info, two_pro_info, thr_pro_info):
    random.seed()
    X = random.random()
    Y = random.random()
    Z = random.random()
    
    in_pro_raw = X * in_pro_info[1] + in_pro_info[0]
    two_pro_raw = Y * two_pro_info[1] + two_pro_info[0]
    thr_pro_raw = Z * thr_pro_info[1] + thr_pro_info[0] 
    
    total_raw = in_pro_raw + two_pro_raw + thr_pro_raw
    
    in_pro = decimal.Decimal(100 * in_pro_raw / total_raw).quantize(ONE_DP)
    two_pro = decimal.Decimal(100 * two_pro_raw / total_raw).quantize(ONE_DP)
    thr_pro = 100 - in_pro - two_pro
    
    return (in_pro, two_pro, thr_pro)
                     
def gen_rating(low, high, min, max, pro):
    random.seed()
    range = high - low
    X = random.random()
    high_pro = pro + (1. - pro)/2
    
    if X < pro:
        rating = decimal.Decimal(X * range/pro + low).quantize(ONE_DP)
    elif X > high_pro:
        rating = decimal.Decimal((X - high_pro)*(max - high)*2/(1. - pro) + high).quantize(ONE_DP)
    else: 
        rating = decimal.Decimal((X - pro)*(low - min)*2/(1. - pro) + min).quantize(ONE_DP)
    return (rating)

def gen_draftee_atts(p_obj):
  pos = p_obj.profile['Pos']
  shot_pros = gen_shot_pros(ATTS_RANGE_DICT[pos]['InPro'],\
                            ATTS_RANGE_DICT[pos]['2JPro'],\
                            ATTS_RANGE_DICT[pos]['3PPro'])
  p_obj.attributes['Inside Prop'] = shot_pros[0]
  p_obj.attributes['2Pt Jumper Prop'] = shot_pros[1]
  p_obj.attributes['3Pt Jumper Prop'] = shot_pros[2]                          
  
  for att in P_ATT_NAME_DICT:
    if att in ('InPro,'2JPro',3PPro'):
      pass
    else:
      p_obj.attributes[P_ATT_NAME_DICT[att]] = \
        gen_rating(ATTS_RANGE_DICT[pos][att])
  
  p_obj.profile['Age'] = F_GEN_VAR_FROM_PROB_DICT(AGE_PROB_DICT)
  
  return
  
    