from GlobalVariables import *
import copy
import os
import re

class Record:
  def __init__(self,init_year,cur_year,nick,game_dir):
    self.nick = nick
    self.name = NICK_TO_NAME[nick]
    self.own = {}
    self.h2h = {}
    self.game_dir = game_dir
    self.init_year = init_year
    self.cur_year = cur_year
    
    for y in range(self.init_year,self.cur_year+1): 
      if y == self.cur_year:
        year_dir = game_dir + os.sep + 'data' + os.sep + 'Year_' + str(y)
        conf_file = year_dir + os.sep + 'Conferences.txt'
        #print ('VC: conf_file = ' + conf_file)
        if os.path.isfile(conf_file):      
          self.alpha_teams = []
          self.beta_teams = []
          with open(conf_file,'r') as conf_f:
            for line in conf_f:
              conf_line = line.split()
              if conf_line[0][:-1] == 'ALPHA':
                for team in conf_line[1:]:
                  if team == nick:
                    self.conf_teams = self.alpha_teams
                    self.inter_conf_teams = self.beta_teams
                    self.conf = 'Alpha'
                  else:
                    self.alpha_teams.append(team)       
              elif conf_line[0][:-1] == 'BETA':
                for team in conf_line[1:]:
                  if team == nick:
                    self.conf_teams = self.beta_teams
                    self.inter_conf_teams = self.alpha_teams
                    self.conf = 'Beta'
                  else:
                    self.beta_teams.append(team)  
        else:
          print ("VC: ERROR, conf_file not found in RecordClass.py")          
      
      self.own['Y' + str(y)] = {}
      self.own['Y' + str(y)]['All'] = copy.deepcopy(YEAR_RECORD_ELEMENTS)
      self.own['Y' + str(y)]['Conf'] = copy.deepcopy(YEAR_RECORD_ELEMENTS)
      self.own['Y' + str(y)]['Inter-Conf'] = copy.deepcopy(YEAR_RECORD_ELEMENTS)
      
      self.h2h['Y' + str(y)] = {}
      for opp_nick in NICKS:
        if opp_nick == nick:
          pass
        else:
          self.h2h['Y' + str(y)][opp_nick] = copy.deepcopy(YEAR_RECORD_ELEMENTS)
      self.load_record_data(y)
    
    #All time record
    self.own['All Time'] = {}
    self.own['All Time']['All'] = copy.deepcopy(A_T_RECORD_ELEMENTS)
    self.own['All Time']['Conf'] = copy.deepcopy(A_T_RECORD_ELEMENTS)
    self.own['All Time']['Inter-Conf'] = copy.deepcopy(A_T_RECORD_ELEMENTS)
    
    self.h2h['All Time'] = {}
    for opp_nick in NICKS:
      if opp_nick == nick:
        pass
      else:
        self.h2h['All Time'][opp_nick] = copy.deepcopy(A_T_RECORD_ELEMENTS)      
    self.load_record_data('All Time')   
    
    return
  
  def load_record_data(self,year):
    if year == 'All Time':
      year_dir = self.game_dir + os.sep + 'data' + os.sep + 'All_time'
      team_dir = year_dir + os.sep + 'Teams' + os.sep + self.name 
      year_record_dict = self.own['All Time']
      h2h_record_dict = self.h2h['All Time']
    else:
      year_dir = self.game_dir + os.sep + 'data' + os.sep + 'Year_' + str(year)
      team_dir = year_dir + os.sep + 'Teams' + os.sep + self.name       
      year_record_dict = self.own['Y' + str(year)]
      h2h_record_dict = self.h2h['Y' + str(year)]
    saved_record_file = team_dir + os.sep + 'Record_data.txt' 
    if os.path.isfile(saved_record_file):
      with open(saved_record_file,'r') as f:
        for line in f:
          item = line.rstrip().split('|')
          #print ("VC: record item " + str(item))
          if item[0] in ('All','Conf','Inter-Conf'):
            stat_item = year_record_dict[item[0]]
            key_index = 1
            stat_index = 2
          elif item[0] == 'H2H':
            stat_item = h2h_record_dict[item[1]]
            key_index = 2
            stat_index = 3  
          if item[key_index] in ('L10','H L10','A L10'):
            if item[stat_index] == '':
              result_list = []
            else:
              result_list = item[stat_index].split(',')
              result_list = [int(x) for x in result_list]
            stat_item[item[key_index]] = result_list
          else:
            stat_item[item[key_index]] = int(item[stat_index])             
    else:
      print ("VC: No saved record file for " + self.name + "'s " + \
             'Year' + str(year))
    return
  
  def write_record_data(self):
    def write_single_record_data_file(file,record_own,record_h2h):
      with open(saved_record_file,'w') as f:
        for type in record_own:
          for item in record_own[type]:
            if item in ('L10','H L10','A L10'):
              stat_str = ''
              for result in record_own[type][item]:
                stat_str += str(result) + ','
              stat_str = stat_str[:-1] 
            else:
              stat_str = str(record_own[type][item])
            line = type + '|' + item + '|' + stat_str          
            f.write(line +'\n')
        for o_team in record_h2h:
          for item in record_h2h[o_team]:
            if item in ('L10','H L10','A L10'):
              stat_str = ''
              for result in record_h2h[o_team][item]:
                stat_str += str(result) + ','
              stat_str = stat_str[:-1] 
            else:
              stat_str = str(record_h2h[o_team][item])          
            line = 'H2H|' + o_team + '|' + item + '|' + stat_str
            f.write(line + '\n')
      return
    a_t_team_dir = self.game_dir + os.sep + 'data' + os.sep + 'All_time' +\
                   os.sep + 'Teams' + os.sep + self.name
    if not os.path.exists(a_t_team_dir):
      os.makedirs(a_t_team_dir)
    saved_record_file =  a_t_team_dir + os.sep + 'Record_data.txt'
    write_single_record_data_file(saved_record_file,self.own['All Time'],\
                                  self.h2h['All Time'])
                                      
    for y in range(self.init_year,self.cur_year+1):
      y_team_dir =  self.game_dir + os.sep + 'data' + os.sep + 'Year_' + \
                    str(y) + os.sep + 'Teams' + os.sep + self.name
      if not os.path.exists(y_team_dir):
        os.makedirs(y_team_dir)
      saved_record_file = y_team_dir + os.sep + 'Record_data.txt'
      write_single_record_data_file(saved_record_file,self.own['Y' + str(y)],\
                                    self.h2h['Y' + str(y)])

    return   
  
  def update_record(self,opp,home,home_pts,away_pts,same_conf,year):
    if home_pts > away_pts and home == True:
      won = True
    elif away_pts > home_pts and home == False:
      won = True
    else:
      won = False
    
    year_all = self.own['Y' + str(year)]['All']
    a_t_all = self.own['All Time']['All']
    if same_conf == True:
      year_conf_type = self.own['Y' + str(year)]['Conf']
      a_t_conf_type = self.own['All Time']['Conf']
    else:
      year_conf_type = self.own['Y' + str(year)]['Inter-Conf']
      a_t_conf_type = self.own['All Time']['Inter-Conf']
    year_h2h = self.h2h['Y' + str(year)][opp]
    a_t_h2h = self.h2h['All Time'][opp]
    
    pts_f_str = 'Pts F'
    pts_a_str = 'Pts A'
    strk_str = 'Streak'
    L10_str = 'L10'
    
    if home == True:
      h_a_type = 'H'
      own_pts = home_pts
      opp_pts = away_pts
      
    elif home == False:
      h_a_type = 'A'
      own_pts = away_pts
      opp_pts = home_pts
    
    if won == True:
      strk_factor = 1
      res_no = 1
      res_str = 'Wins'
    else:
      strk_factor = -1  
      res_no = 0
      res_str = 'Losses'
    
    h_a_pts_f_str = h_a_type + ' ' + pts_f_str
    h_a_pts_a_str = h_a_type + ' ' + pts_a_str
    h_a_res_str = h_a_type + ' ' + res_str
    h_a_L10_str = h_a_type + ' ' + L10_str
    h_a_strk_str = h_a_type + ' ' + strk_str
    
    for r_type in (year_all,year_h2h,year_conf_type,a_t_all,a_t_h2h,a_t_conf_type):
      if r_type in (year_all,year_h2h,year_conf_type):
        r_type[pts_f_str] += own_pts
        r_type[pts_a_str] += opp_pts
        r_type[h_a_pts_f_str] += own_pts
        r_type[h_a_pts_a_str] += opp_pts
      r_type[res_str] += 1
      r_type[h_a_res_str] += 1    
      if len(r_type[L10_str]) == 10:
        r_type[L10_str].pop(0)
      r_type[L10_str].append(res_no)      
      if len(r_type[h_a_L10_str]) == 10:
        r_type[h_a_L10_str].pop(0)
      r_type[h_a_L10_str].append(res_no)      
      if r_type[strk_str]*strk_factor > 0:
        r_type[strk_str] += strk_factor
      else:
        r_type[strk_str] = strk_factor    
      if r_type[h_a_strk_str]*strk_factor > 0:
        r_type[h_a_strk_str] += strk_factor
      else:
        r_type[h_a_strk_str] = strk_factor    
    self.write_record_data()
    return
    
  def print_to_screen(self,opp):
    print ('OWN:',self.own)
    print ('H2H vs. ' + opp + ':',self.h2h[opp])
    return

  '''
def det_team_streak(team_nick,opp_nick,files_dir,year,all_time,home,game_type):
  data_dir = files_dir + os.sep + 'data'
  team = NICK_TO_NAME[team_nick]  
  
  result_group = 2
  if opp_nick:
    if len(opp_nick) == 1:
      o_str = '(' + opp_nick[0] + ')'
    else:
      o_str = '([A-Z]{3,3})'
  else:
    o_str = '([A-Z]{3,3})'
  if home == True:
    p = re.compile('^ *?[0-9]*? *?' + game_type + ' v' + o_str + ' *?([LW]) ')
  elif home == False:
    p = re.compile('^ *?[0-9]*? *?' + game_type + ' @' + o_str + ' *?([LW]) ')
  elif not home:
    p = re.compile('^ *?[0-9]*? *?' + game_type + ' [v@]' + o_str + ' *?([LW]) ')
  wins = 0
  losses = 0
  
  year_str = 'Year_' + str(year)
  year_dir = data_dir + os.sep + year_str
  year_team_dir = year_dir + os.sep + 'Teams' + os.sep + team  
  year_results_file_name = year_team_dir + os.sep + 'Results.txt'
  result_list = []
  streak_found = False
  if os.path.isfile(year_results_file_name): 
    with open(year_results_file_name,'r') as year_f:
      for line in year_f:
        m = p.match(line)
        if m:
          if opp_nick and m.group(1) not in opp_nick:
            continue
          if m.group(result_group) == 'W':
            if sum(result_list) >= 0:
              result_list.append(1)
            else:
              result_list = [1]
              streak_found = True
          elif m.group(result_group) == 'L':
            if sum(result_list) <= 0:
              result_list.append(-1)
            else:
              result_list = [-1]
              streak_found = True
 
  if streak_found == True or all_time == False:
    return (sum(result_list))
  
  else:
    partial_streak = sum(result_list)
   
    while streak_found == False:
      year -= 1  
      year_str = 'Year_' + str(year)
      year_dir = data_dir + os.sep + year_str
      year_team_dir = year_dir + os.sep + 'Teams' + os.sep + team  
      year_results_file_name = year_team_dir + os.sep + 'Results.txt'      
      if not os.path.isfile(year_results_file_name):
        return (sum(result_list))
      else:
        result_list = []
        with open(year_results_file_name,'r') as year_f:
          for line in year_f:
            m = p.match(line)
            if m:
              if opp_nick and m.group(1) not in opp_nick:
                continue
              if m.group(result_group) == 'W':
                if sum(result_list) >= 0:
                  result_list.append(1)
                else:
                  result_list = [1]
                  streak_found = True
              elif m.group(result_group) == 'L':
                if sum(result_list) <= 0:
                  result_list.append(-1)
                else:
                  result_list = [-1]
                  streak_found = True        
        if sum(result_list)*partial_streak < 0:
          return (partial_streak)
        elif streak_found == True:
          return (partial_streak + sum(result_list))
        else:
          partial_streak += sum(result_list)

def det_team_last_x(team_nick,opp_nick,files_dir,year,all_time,home,game_type,x=10):
  data_dir = files_dir + os.sep + 'data'
  team = NICK_TO_NAME[team_nick]
  result_group = 2
  if opp_nick:
    if len(opp_nick) == 1:
      o_str = '(' + opp_nick[0] + ')'
    else:
      o_str = '([A-Z]{3,3})'

  else:
    o_str = '([A-Z]{3,3})'
  if home == True:
    p = re.compile('^ *?[0-9]*? *?' + game_type + ' v' + o_str + ' *?([LW]) ')
  elif home == False:
    p = re.compile('^ *?[0-9]*? *?' + game_type + ' @' + o_str + ' *?([LW]) ')
  elif not home:
    p = re.compile('^ *?[0-9]*? *?' + game_type + ' [v@]' + o_str + ' *?([LW]) ')
  wins = 0
  losses = 0
  
  year_str = 'Year_' + str(year)
  year_dir = data_dir + os.sep + year_str
  year_team_dir = year_dir + os.sep + 'Teams' + os.sep + team  
  year_results_file_name = year_team_dir + os.sep + 'Results.txt'
  result_list = []
  if os.path.isfile(year_results_file_name):
    with open(year_results_file_name,'r') as year_f:
      for line in year_f:
        m = p.match(line)
        if m:
          if opp_nick and m.group(1) not in opp_nick:
            continue
          if m.group(result_group) == 'W':
            result_list.append(1)
          elif m.group(result_group) == 'L':
            result_list.append(0)
          if len(result_list) > x:  
            result_list.pop(0)  
            
  if len(result_list) == x or all_time == False:
    return (result_list)
  
  else:
    x_found = False  
    while x_found == False:
      year -= 1  
      year_str = 'Year_' + str(year)
      year_dir = data_dir + os.sep + year_str
      year_team_dir = year_dir + os.sep + 'Teams' + os.sep + team  
      year_results_file_name = year_team_dir + os.sep + 'Results.txt'      
      if not os.path.exists(year_results_file_name):
        return (result_list)
      else:
        with open(year_results_file_name,'r') as year_f:
          for line in year_f:
            m = p.match(line)
            if opp_nick and m.group(1) not in opp_nick:
              continue
            if m:
              if m.group(result_group) == 'W':
                result_list.append(1)
              elif m.group(result_group) == 'L':
                result_list.append(0)
              if len(result_list) > x:  
                result_list.pop(0)  
                       
        if len(result_list) == x:
          return (result_list)


def det_team_wins(team_nick,opp_nick,files_dir,year,all_time,home,game_type):
  data_dir = files_dir + os.sep + 'data'
  team = NICK_TO_NAME[team_nick]
  result_group = 2
  if opp_nick:
    if len(opp_nick) == 1:
      o_str = '(' + opp_nick[0] + ')'
    else:
      o_str = '([A-Z]{3,3})'

  else:
    o_str = '([A-Z]{3,3})'
  if home == True:
    p = re.compile('^ *?[0-9]*? *?' + game_type + ' v' + o_str + ' *?([LW]) ')
  elif home == False:
    p = re.compile('^ *?[0-9]*? *?' + game_type + ' @' + o_str + ' *?([LW]) ')
  elif not home:
    p = re.compile('^ *?[0-9]*? *?' + game_type + ' [v@]' + o_str + ' *?([LW]) ')
  wins = 0
  losses = 0
  
  year_str = 'Year_' + str(year)
  year_dir = data_dir + os.sep + year_str
  year_team_dir = year_dir + os.sep + 'Teams' + os.sep + team
  year_results_file_name = year_team_dir + os.sep + 'Results.txt'

  if os.path.isfile(year_results_file_name):
    year_list = [year]
  else:
    year_list = []
    
  if all_time == True:
    year -= 1
    year_str = 'Year_' + str(year)
    year_dir = data_dir + os.sep + year_str
    year_team_dir = year_dir + os.sep + 'Teams' + os.sep + team
    year_results_file_name = year_team_dir + os.sep + 'Results.txt'    
    while os.path.isfile(year_results_file_name):
      year_list.append(year)
  
  for year in year_list:
    year_str = 'Year_' + str(year)
    year_dir = data_dir + os.sep + year_str
    year_team_dir = year_dir + os.sep + 'Teams' + os.sep + team
    year_results_file_name = year_team_dir + os.sep + 'Results.txt'
    #print ("VCVC:" + (year_results_file_name))
    with open(year_results_file_name,'r') as year_f:
      for line in year_f:     
        m = p.match(line)
        if m:
          if opp_nick and m.group(1) not in opp_nick:
            continue
          if m.group(result_group) == 'W':
            wins += 1
          elif m.group(result_group) == 'L':
            losses += 1
  return (wins,losses)

def det_team_pts(team_nick,opp_nick,files_dir,year,all_time,home,game_type,points_for):
  data_dir = files_dir + os.sep + 'data'
  team = NICK_TO_NAME[team_nick]
  if points_for == True:
    pts_group = 2
  elif points_for == False:
    pts_group = 3
  if opp_nick:
    if len(opp_nick) == 1:
      o_str = '(' + opp_nick[0] + ')'
    else:
      o_str = '([A-Z]{3,3})'

  else:
    o_str = '([A-Z]{3,3})'
  if home == True:
    p = re.compile('^ *?[0-9]*? *?' + game_type + ' v' + o_str + ' *?[LW] *?([0-9]*?)-([0-9]*?) ')
    p_str = '^ *?[0-9]*? *?' + game_type + ' v' + o_str + ' *?[LW] *?([0-9]*?)-([0-9]*?) '
  elif home == False:
    p = re.compile('^ *?[0-9]*? *?' + game_type + ' @' + o_str + ' *?[LW] *?([0-9]*?)-([0-9]*?) ')
    p_str = '^ *?[0-9]*? *?' + game_type + ' @' + o_str + ' *?[LW] *?([0-9]*?)-([0-9]*?) '
  elif not home:
    p = re.compile('^ *?[0-9]*? *?' + game_type + ' [v@]' + o_str + ' *?[LW] *?([0-9]*?)-([0-9]*?) ')
    p_str = '^ *?[0-9]*? *?' + game_type + ' [v@]' + o_str + ' *?[LW] *?([0-9]*?)-([0-9]*?) '

  points = 0
    
  year_str = 'Year_' + str(year)
  year_dir = data_dir + os.sep + year_str
  year_team_dir = year_dir + os.sep + 'Teams' + os.sep + team
  year_results_file_name = year_team_dir + os.sep + 'Results.txt'

  if os.path.isfile(year_results_file_name):
    year_list = [year]
  else:
    year_list = []
    
  if all_time == True:
    year -= 1
    year_str = 'Year_' + str(year)
    year_dir = data_dir + os.sep + year_str
    year_team_dir = year_dir + os.sep + 'Teams' + os.sep + team
    year_results_file_name = year_team_dir + os.sep + 'Results.txt'    
    while os.path.isfile(year_results_file_name):
      year_list.append(year)
  
  #print (year_list)
  for year in year_list:
    year_str = 'Year_' + str(year)
    year_dir = data_dir + os.sep + year_str
    year_team_dir = year_dir + os.sep + 'Teams' + os.sep + team
    year_results_file_name = year_team_dir + os.sep + 'Results.txt'
    #print ("VCVC:" + (year_results_file_name))
    with open(year_results_file_name,'r') as year_f:
      for line in year_f:
        if opp_nick and len(opp_nick) == 1:
          pass
        
        m = p.match(line)
        if m:
          if opp_nick and m.group(1) not in opp_nick:
            continue     
          points += int(m.group(pts_group))
  return (points)
  '''    