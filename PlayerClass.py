import copy
from GlobalVariables import *
import re
import os
import random
from GlobalFunctions import *
import decimal

def rating_to_grade(grade_dict,rating):
  for grade_key in sorted(grade_dict.keys()):
    if rating <= grade_key:
      return grade_dict[grade_key]
  print ("ERROR in rating_to_grade")

class Player:
  def __init__(self,name,game_dir,init_year,cur_year,pos=None,draftee=False):
    self.name = name
    self.game_dir = game_dir
    self.init_year = init_year
    self.cur_year = cur_year
    
    self.profile = {}
    self.attributes = copy.deepcopy(P_ATT_DICT)
    self.status = {}

    self.atts_file = game_dir + os.sep + 'Attributes' + os.sep + name + '.txt'
    self.prev_atts_file = game_dir + os.sep + 'Attributes' + os.sep + name + \
                          '_prev.txt'
    if os.path.isfile(self.prev_atts_file) == False:
      with open(self.prev_atts_file,'w') as f:
        f.write(F_GEN_P_ATTS_TITLE(True) + '\n')
    self.atts_change_flag = False
    
    self.year_dir = game_dir + os.sep + 'data' + os.sep + 'Year_' + \
                    str(cur_year) + os.sep + 'Players' + os.sep + name
    self.year_logs_file = self.year_dir + os.sep + 'Game_logs.txt'
    self.year_stat_totals_file = self.year_dir + os.sep + 'Stat_totals.txt'
    self.year_transactions_file = self.year_dir + os.sep + 'Transactions.txt'
    self.year_postgame_log_file = self.year_dir + os.sep + 'Postgame_log.txt'
    self.all_time_dir = game_dir + os.sep + 'data' + os.sep + 'All_time' + \
                        os.sep + 'Players' + os.sep + name
    self.a_t_logs_file = self.all_time_dir + os.sep + 'Game_logs.txt'
    self.a_t_transactions_file = self.all_time_dir + os.sep + 'Transactions.txt'
    
    if not os.path.isdir(self.year_dir):
      os.makedirs(self.year_dir)
    if not os.path.isdir(self.all_time_dir):
      os.makedirs(self.all_time_dir)
    
    if draftee == True:
      self.profile['Pos'] = pos
      
      self.gen_draftee_atts()
      self.profile['Draft Year'] = int(cur_year)
      self.profile['Pick No'] = 'U'
      self.profile['Years Pro'] = 0
      self.status['Days Injured'] = 0
      self.team_nick = 'DRA'
      self.team_name = 'Draftee' 
      draft_atts_file = game_dir + os.sep + 'Draft' + os.sep + 'Year_' + \
                        str(cur_year) + os.sep + name + '.txt'
         
      
       
      with open(draft_atts_file,'w') as d_atts_f:
        with open(self.atts_file,'w') as atts_f:
          title = F_GEN_P_ATTS_TITLE(False)
          atts_f.write(title + '\n')
          d_atts_f.write(title + '\n')
          line = F_GEN_P_ATTS_LINE(False,self)
          atts_f.write(line + '\n') 
          d_atts_f.write(line + '\n') 
                 
    elif draftee == False:  
      with open(self.atts_file,'r') as atts_f:
        title_line = atts_f.readline()
        att_seq = title_line.split()
      
        atts_line = atts_f.readline()
        att_values = atts_line.split()
      
        for i in range(len(att_seq)):
          if att_seq[i] == 'Draft':
            draft_pos_list = att_values[i].split('.')
            self.profile['Draft Year'] = int(draft_pos_list[0])
            if draft_pos_list[1] == 'U':
              self.profile['Pick No'] = 'U'
            else:
              self.profile['Pick No'] = int(draft_pos_list[1])
          elif att_seq[i] == 'Pos':
            self.profile['Pos'] = att_values[i]
          elif att_seq[i] == 'Age':
            self.profile['Age'] = int(att_values[i])
          elif att_seq[i] == 'YPro':
            self.profile['Years Pro'] = int(att_values[i])
          elif att_seq[i] == 'GInj':
            self.status['Days Injured'] = int(att_values[i])
          elif att_seq[i] in P_ATT_NAME_DICT:
            self.attributes[P_ATT_NAME_DICT[att_seq[i]]] = \
              decimal.Decimal(att_values[i]).quantize(ONE_DP)
          elif att_seq[i] == 'Team':
            if att_values[i] == 'RET':
              self.team_nick = 'RET'
              self.team_name = 'Retired'
            elif att_values[i] == 'FA':
              self.team_nick = 'FA'
              self.team_name = 'Free Agent'
            else:  
              self.team_nick = att_values[i]
              self.team_name = NICK_TO_NAME[self.team_nick]
    
    if self.profile['Age'] > 30:
      self.profile['Eff Age'] = 30
    else:
      self.profile['Eff Age'] = self.profile['Age']
    self.profile['Simp Pos'] = SIMPLE_POS_DICT[self.profile['Pos']]
    
    # VC - Maybe not needed - use atts_to_grade() when needed instead?
    self.grades = copy.deepcopy(self.attributes)
    self.atts_to_grades()
    
    # For in-game
    #self.game_attributes = copy.deepcopy(self.attributes)
    
    #Season-by-season and career stats
    self.stats = {}
    self.stats['Career'] = copy.deepcopy(P_ZERO_SEASON_STATS)
    for y in range(self.init_year,self.cur_year + 1):
      self.stats['Y' + str(y)] = copy.deepcopy(P_ZERO_SEASON_STATS)
      saved_player_data_file = game_dir + os.sep + 'data' + os.sep + 'Year_' +\
                               str(y) + os.sep + 'Players' + os.sep + name +\
                               os.sep + 'Stat_totals.txt'
      if os.path.isfile(saved_player_data_file):
        with open(saved_player_data_file,'r') as f:
          for line in f:
            item = line.rstrip().split('|')
            self.stats['Y' + str(y)][item[0]] = int(item[1])
            self.stats['Career'][item[0]] += int(item[1])
      else:    
        print ('***Y' + str(y) + ' season totals file for ' + name + \
               ' not found!***')

    return


  def gen_draftee_atts(self):
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
    
    def gen_rating(rating_set):
      low = rating_set[0]
      high = rating_set[1]
      min = rating_set[2]
      max = rating_set[3]
      pro = rating_set[4]
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
    
    shot_pros = gen_shot_pros(ATTS_RANGE_DICT[self.profile['Pos']]['InPro'],\
                              ATTS_RANGE_DICT[self.profile['Pos']]['2JPro'],\
                              ATTS_RANGE_DICT[self.profile['Pos']]['3PPro'])
    self.attributes['Inside Prop'] = shot_pros[0]
    self.attributes['2Pt Jumper Prop'] = shot_pros[1]
    self.attributes['3Pt Jumper Prop'] = shot_pros[2]       
    for att in P_ATT_NAME_DICT:
      if att in ('InPro','2JPro','3PPro'):
        pass
      else:
        self.attributes[P_ATT_NAME_DICT[att]] = \
          gen_rating(ATTS_RANGE_DICT[self.profile['Pos']][att])
  
    self.profile['Age'] = F_GEN_VAR_FROM_PROB_DICT(AGE_PROB_DICT)

    return
  
  #-----------------------------------------------------------------------------
  # Function game_initialisation
  #
  # 
  #-----------------------------------------------------------------------------
  def game_initialisation(self): 
    self.game = {'Stats':copy.deepcopy(P_ZERO_GAME_STATS),'Starter':False}
    self.game_attributes = {}
    for a in self.attributes:
      #print (a,self.attributes[a],self.name)
      self.game_attributes[a] = float(self.attributes[a])   
    #copy.deepcopy(self.attributes)
    
    #---------------------------------------------------------------------------
    # variable court_status:
    #
    #  0 - On bench and available
    #  1 - On court
    # -1 - Fouled out
    # -2 - Injured 
    #---------------------------------------------------------------------------
    if self.status['Days Injured'] > 0:
      self.game['Court Status'] = -2
    else:
      self.game['Court Status'] = 0
    return
    
  def atts_to_grades(self):
    prop_scale = {5:'X-L',15:'V-L',25:'L',40:'M-L',55:'M',\
                   70:'M-H',80:'H',90:'V-H',100:'X-H'}
    
    ball_dom_scale = {5:'X-L',10:'V-L',20:'L',30:'M-L',40:'M',\
                      60:'M-H',80:'H',100:'V-H',1000:'X-H'}
    pass_rate_scale = {10:'X-L',25:'V-L',40:'L',50:'M-L',60:'M',\
                       70:'M-H',80:'H',90:'V-H',100:'X-H'}
    
    shot_eff_scale = {50:'F',60:'E',70:'D',80:'C',90:'B',100:' A-',\
                      110:'A',1000:' A+'}
    FT_eff_scale = {50:'F',60:'E',70:'D',75:'C',80:'B',85:' A-',\
                    90:'A',100:' A+'}
                    
    off_reb_scale = {5:'F',10:'E',20:'D',30:'C',40:'B',50:' A-',\
                     60:'A',1000:' A+'}
    def_reb_scale = {20:'F',30:'E',45:'D',60:'C',75:'B',90:' A-',\
                     105:'A',1000:' A+'} 
    
    pass_eff_scale = {20:'F',30:'E',40:'D',50:'C',65:'B',80:' A-',\
                      95:'A',1000:' A+'}
    
    def_scale = {15:'F',30:'E',45:'D',60:'C',75:'B',90:' A-',\
                     105:'A',1000:' A+'}
    
    in_foul_rate_scale = {10:'F',20:'E',35:'D',50:'C',65:'B',75:' A-',\
                          85:'A',1000:' A+'}
    per_foul_rate_scale = {10:'F',20:'E',30:'D',40:'C',50:'B',60:' A-',\
                           70:'A',1000:' A+'}                       
          
    att_scale = {'Inside Prop':prop_scale,'2Pt Jumper Prop':prop_scale,\
                 '3Pt Jumper Prop':prop_scale,'Inside Eff':shot_eff_scale,\
                 '2Pt Jumper Eff':shot_eff_scale,'3Pt Jumper Eff':shot_eff_scale,\
                 'Off Reb':off_reb_scale,'Def Reb':def_reb_scale,\
                 'Ball Dom':ball_dom_scale,'Pass Rate':pass_rate_scale,\
                 'Pass Eff':pass_eff_scale,'Inside Def':def_scale,\
                 'Perimeter Def':def_scale,'Inside Foul Rate':in_foul_rate_scale,\
                 'Per Foul Rate':per_foul_rate_scale,'FT Eff':FT_eff_scale}
    
    for att in att_scale.keys():
      self.grades[att] = rating_to_grade(att_scale[att],self.attributes[att])
                          
    return
  
  def update_processes(self,update_str,t_obj,game_occurred):
    if t_obj:
      t_f = open(t_obj.year_postgame_log_file,'a')
    else:
      t_f = None
          
    with open(self.year_postgame_log_file,'a') as p_f:
    
      self.update_atts(t_obj,game_occurred,t_f,p_f,update_str)
      self.update_injury_status(t_obj,game_occurred,t_f,p_f,update_str)
    
    if t_obj:
      t_f.close()
      
    if self.atts_change_flag == True:
      with open(self.prev_atts_file,'a') as prev_f:  
        prev_f.write(F_GEN_P_ATTS_LINE(update_str,self) + '\n')        
      
      with open(self.atts_file,'w') as cur_f:
        cur_f.write(F_GEN_P_ATTS_TITLE(False) + '\n')
        cur_f.write(F_GEN_P_ATTS_LINE(None,self))  
    self.atts_change_flag = False
    return
  
  def update_injury_status(self,t_obj,game_occurred,t_log_handle,p_log_handle,update_str):
    if self.status['Days Injured'] > 0:
      inj_prob = 0.002
    elif game_occurred == True:
      inj_prob = 0.017*self.game['Stats']['Court Time']/2400 + 0.003
    else:
      inj_prob = 0.003
      
    days_missed = F_DET_INJURY(inj_prob)
    if days_missed > 0:
      if t_log_handle:
        t_log_handle.write(self.name + ' suffered a ' + str(days_missed) + \
                           ' injury @' + update_str + '\n')
      
      p_log_handle.write('Suffered a ' + str(days_missed) + \
                         ' injury @' + update_str + '\n')                   
      if self.status['Days Injured'] > 0:
        print (self.name + ' of ' + self.team_nick + ' has a suffered ' + \
             'another injury and will be out for ~' + \
             str(self.status['Days Injured'] + days_missed) + ' days!')
        
      else:
        print (self.name + ' of ' + self.team_nick + ' has a suffered an ' + \
               'injury and will be out for ~' + str(days_missed) + ' days!')
      
      self.status['Days Injured'] += days_missed
      self.atts_change_flag = True
    else:      
      if self.status['Days Injured'] > 0:
        inj_days_red = F_INJ_RECOVER()
        self.status['Days Injured'] -= inj_days_red
        if inj_days_red > 0:
          self.atts_change_flag = True
        if self.status['Days Injured'] <= 0:
          self.status['Days Injured'] = 0
          print (self.name + ' of ' + self.team_nick + ' has recovered from ' + \
                 'injury!')
    return
  
  def update_atts(self,t_obj,game_occurred,t_log_handle,p_log_handle,update_str):
    random.seed()
    eff_age = self.profile['Eff Age']
    
    if game_occurred == True:
      fac = 1
      court_time = self.game['Stats']['Court Time']
    else:
      fac = 0.2
      court_time = 0
    if self.status['Days Injured'] > 0:
      max_imp_prob = fac*POST_GAME_CHANGE_PROBS[eff_age]['Min Improve Prob']/5
      min_imp_prob = fac*POST_GAME_CHANGE_PROBS[eff_age]['Min Improve Prob']/5
      reg_prob = fac*POST_GAME_CHANGE_PROBS[eff_age]['Injury Regress Prob']
    else:
      max_imp_prob = fac*POST_GAME_CHANGE_PROBS[eff_age]['Max Improve Prob']
      min_imp_prob = fac*POST_GAME_CHANGE_PROBS[eff_age]['Min Improve Prob']
      reg_prob = fac*POST_GAME_CHANGE_PROBS[eff_age]['Regress Prob']    
    print (self.name)
    imp_prob = court_time/2400*(max_imp_prob - min_imp_prob) + min_imp_prob
    
    for a in P_ATT_NAME_DICT:
      a_name = P_ATT_NAME_DICT[a]
      X = random.random()
      if a in P_PROP_ATTS:
        chg_prob = imp_prob + reg_prob
        if X < chg_prob:
          max_chg = MAX_PROB_CHANGE[self.profile['Pos']][a]
          act_chg = decimal.Decimal(random.uniform(-max_chg,max_chg))\
                    .quantize(ONE_DP)
          self.attributes[a_name] += act_chg
          print (self.name + "'s " + a + ' changed by ' + str(act_chg))
          if t_log_handle:
            t_log_handle.write(self.name + "'s " + a + ' changed by ' + \
                               str(act_chg) + ' @' + update_str + '\n')
          p_log_handle.write(a + ' changed by ' + str(act_chg) + ' @' + \
                             update_str + '\n')
          self.atts_change_flag = True 
      else:
        if X < imp_prob:
          max_imp = (MAX_RATING[self.profile['Pos']][a] - \
                     self.attributes[a_name])/10
          act_chg = decimal.Decimal(random.uniform(0,float(max_imp)))\
                    .quantize(ONE_DP)
          if act_chg < 1:
            act_chg = 1
          self.attributes[a_name] += act_chg
          print (self.name + "'s " + a + ' improved by ' + str(act_chg))
          if t_log_handle:
            t_log_handle.write(self.name + "'s " + a + ' improved by ' + \
                               str(act_chg) + ' @' + update_str + '\n')
          p_log_handle.write(a + ' improved by ' + str(act_chg) + ' @' + \
                             update_str + '\n')
          self.atts_change_flag = True
        elif X < (imp_prob + reg_prob):
          max_reg = MAX_REGRESS[eff_age][a]
          act_chg = decimal.Decimal(random.uniform(0,-max_reg))\
                    .quantize(ONE_DP)
          if act_chg > -1:
            act_chg = -1    
          self.attributes[a_name] += act_chg
          print (self.name + "'s " + a + ' regressed by ' + str(act_chg))
          if t_log_handle:
            t_log_handle.write(self.name + "'s " + a + ' regressed by ' + \
                               str(act_chg) + ' @' + update_str + '\n')
          p_log_handle.write(a + ' regressed by ' + str(act_chg) + ' @' + \
                             update_str + '\n')
          self.atts_change_flag = True
    self.reset_atts(t_log_handle,p_log_handle,update_str)                     
    return
  
  def reset_atts(self,t_log_handle,p_log_handle,update_str):
    print (self.name + "'s orig. props: " + str(self.attributes['Inside Prop']) + ', ' + str(self.attributes['2Pt Jumper Prop']) + ', ' + str(self.attributes['3Pt Jumper Prop']))
    prop_set = ('Inside Prop','2Pt Jumper Prop','3Pt Jumper Prop')
    for prop in prop_set:
      if self.attributes[prop] < 0.2:
        self.attributes[prop] = decimal.Decimal(0.2).quantize(ONE_DP)
      elif self.attributes[prop] > 99:
        self.attributes[prop] = decimal.Decimal(99).quantize(ONE_DP)
    
    pro_sum = self.attributes['Inside Prop'] + \
              self.attributes['2Pt Jumper Prop'] + \
              self.attributes['3Pt Jumper Prop']
    
    if pro_sum != 100:
      for prop in prop_set:
        self.attributes[prop] = decimal.Decimal(float(self.attributes[prop])/\
                                float(pro_sum)*100).quantize(ONE_DP)
    
    pro_sum = self.attributes['Inside Prop'] + \
              self.attributes['2Pt Jumper Prop'] + \
              self.attributes['3Pt Jumper Prop']
    
    if pro_sum != 100:
      chg_prop = random.choice(prop_set)
      self.attributes[chg_prop] -= pro_sum - 100                          
    
    if self.attributes['Pass Rate'] > 99:
      self.attributes['Pass Rate'] = decimal.Decimal(99).quantize(ONE_DP)
    elif self.attributes['Pass Rate'] < 3:
      self.attributes['Pass Rate'] = decimal.Decimal(3).quantize(ONE_DP)
    if self.attributes['Pass Eff'] < 3:
      self.attributes['Pass Eff'] = decimal.Decimal(3).quantize(ONE_DP)
    
    elif self.attributes['Off Reb'] < 1:
      self.attributes['Off Reb'] = decimal.Decimal(1).quantize(ONE_DP)
    elif self.attributes['Def Reb'] < 1:
      self.attributes['Def Reb'] = decimal.Decimal(1).quantize(ONE_DP)      
    elif self.attributes['Ball Dom'] < 3:
      self.attributes['Ball Dom'] = decimal.Decimal(3).quantize(ONE_DP)    
    elif self.attributes['Inside Foul Rate'] < 1:
      self.attributes['Inside Foul Rate'] = decimal.Decimal(1).quantize(ONE_DP)
    elif self.attributes['Per Foul Rate'] < 1:
      self.attributes['Per Foul Rate'] = decimal.Decimal(1).quantize(ONE_DP)
    elif self.attributes['FT Eff'] > 97:
      self.attributes['FT Eff'] = decimal.Decimal(97).quantize(ONE_DP)
    print (self.name + "'s reset props: " + str(self.attributes['Inside Prop']) + ', ' + str(self.attributes['2Pt Jumper Prop']) + ', ' + str(self.attributes['3Pt Jumper Prop']))
    
    return
    
  def gen_season_stats(self):
    return
  
  def gen_career_stats(self):
    return
