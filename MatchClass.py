import random
import array
import math
import copy
import decimal
import os
import re
from PlayerClass import *
from TeamClass import *
from GlobalVariables import *
from PeriodClass import *

#-------------------------------------------------------------------------------
# Class Match
#
#
#-------------------------------------------------------------------------------
class Match:
  def __init__(self,home_obj,away_obj,l_obj,starter_info_dict=None):
    self.away = away_obj
    self.home = home_obj
    self.l_obj = l_obj

    self.year = home_obj.cur_year
    self.overtimes = 0
    self.game_dir = home_obj.game_dir       
    self.game_type = l_obj.next_event['Type']
    self.team_players_on_court = 5
    if self.game_type == 'RS':
      if home_obj.conf == away_obj.conf:
        self.same_conf = True
      else:
        self.same_conf = False
      self.playoffs = False
      self.game_no = l_obj.next_event['Game No']
      self.overtime_time = 300
      self.period_time = 600
      self.tot_periods = 4
    elif self.game_type == 'AF':
      self.playoffs = True
      self.game_no = l_obj.next_event['Game No']
      self.overtime_time = 300
      self.period_time = 600
      self.tot_periods = 4
    elif self.game_type == 'BF':
      self.playoffs = True
      self.game_no = l_obj.next_event['Game No']
      self.overtime_time = 300
      self.period_time = 600
      self.tot_periods = 4
    elif self.game_type == 'VF':
      self.playoffs = True
      self.game_no = l_obj.next_event['Number']
      self.overtime_time = 300
      self.period_time = 600
      self.tot_periods = 4
    elif self.game_type == 'ASG':
      self.playoffs = False
      self.game_no = None
      self.overtime_time = 300
      self.period_time = 600
      self.tot_periods = 4
    elif self.game_type == 'RoSo':
      self.playoffs = False
      self.game_no = None
      self.overtime_time = 300
      self.period_time = 900
      self.tot_periods = 2    
      self.team_players_on_court = 3
      
    #VC: Move to function variable?
    mode_chosen = False
    while mode_chosen == False:
      print ("Choose a game mode:")
      print ("[1] Normal")
      print ("[2] No substitutions")
      reply = input().rstrip()
      if reply == '1':
        mode_chosen = True
        self.sub_allowed = True
      elif reply == '2':
        mode_chosen = True
        self.sub_allowed = False
      else:
        print ("***Invalid choice, try again.***\n")
     
    self.pre_match(starter_info_dict)
    self.adjust_atts()

    self.period = 1
    self.PBP_history = []
    start_line = '***Start of the match***'
    self.PBP_history.append(start_line)
    
    self.misc_stats_dict = {'Team Last Scored':0,'Run':0,'Team Last Led':0,\
                            'Last Tie Score':(0,0),'Last Lead Change Score':(0,0),\
                            'Lead Changes':0,'Ties':0}
    self.winner = None
    
    self.run_match()
    #This is in LeagueClass
    #self.post_match()
    return
  
  #-----------------------------------------------------------------------------
  # Function pre_match
  #
  # 
  #-----------------------------------------------------------------------------
  def pre_match(self,starter_info_dict):
    self.away.game_initialisation(self.home.nickname,self.game_type,\
                                  self.game_no,False)
    self.home.game_initialisation(self.away.nickname,self.game_type,\
                                  self.game_no,True)
   
    self.away.pre_match(self.game_type,starter_info_dict['Away'])
    self.home.pre_match(self.game_type,starter_info_dict['Home'])
    '''
    else:
      self.away.game['Starters'] = starter_info_dict['Away']['Starters']
      self.away.game['On Court'] = starter_info_dict['Away']['On Court']
      self.home.game['Starters'] = starter_info_dict['Home']['Starters']
      self.home.game['On Court'] = starter_info_dict['Home']['On Court']
      if self.game_type in 'ASG':
        self.away.game['Bench'] = starter_info_dict['Away']['Bench']
        self.away.game['Avail Subs'] = starter_info_dict['Away']['Avail Subs']
        self.home.game['Bench'] = starter_info_dict['Home']['Bench']
        self.home.game['Avail Subs'] = starter_info_dict['Home']['Avail Subs']
    '''
    return
  

  #--------------------------------------------------------------------
  # function adjust_atts
  # 
  # Function to adjust attributes for homecourt advantage, and also to
  # adjust the Off Reb attribute. 
  #
  # game_type variable:
  # --> 'RS' - Regular Season
  # --> 'AFG#' - Alpha Conference Finals Game #
  # --> 'BFG#' - Beta Conference Finals Game #
  # --> 'VFG#' - VBA Finals Game #
  # --> 'AS' - All Star
  # --> 'RoSo' - Rook-Soph (3 vs.3) 
  #
  #
  # Changes are made in:
  # --> Inside Eff
  # --> 2Pt Eff
  # --> 3Pt Eff
  # --> FT Eff
  # --> Off Reb (if needed)
  #------------------------------------------------------------------
  def adjust_atts(self):
    if self.game_type in ('RS','AF','BF','VF'):
      home_shot_adv = 3
      home_FT_adv = 2
    elif self.game_type == 'RoSo':
      home_shot_adv = 3
      home_FT_adv = 2      
      rook_soph_def_adj = 33
    elif self.game_type == 'ASG':
      home_shot_adv = 3
      home_FT_adv = 2
    
    
    for p in self.home.players:
      self.home.players[p].game_attributes['Inside Eff'] += home_shot_adv
      self.home.players[p].game_attributes['2Pt Jumper Eff'] += home_shot_adv
      self.home.players[p].game_attributes['3Pt Jumper Eff'] += home_shot_adv
      self.home.players[p].game_attributes['FT Eff'] += home_FT_adv
      if self.game_type in 'RoSo':
        self.home.players[p].game_attributes['Perimeter Def'] += 33
        self.home.players[p].game_attributes['Inside Def'] += 33
      if (self.home.players[p].game_attributes['Off Reb'] > 30):
        x = self.home.players[p].game_attributes['Off Reb']
        if x > 60:
          x -= int(10 + x - 60 * 2 / 3)
        else:
          x -= int((x - 30) / 3)
        self.home.players[p].game_attributes['Off Reb'] = x

    if self.game_type in ('ASG','RoSo'):
      home_shot_adv *= -1
      home_FT_adv *= -1
  
    for p in self.away.players:
      self.away.players[p].game_attributes['Inside Eff'] -= home_shot_adv
      self.away.players[p].game_attributes['2Pt Jumper Eff'] -= home_shot_adv
      self.away.players[p].game_attributes['3Pt Jumper Eff'] -= home_shot_adv
      self.away.players[p].game_attributes['FT Eff'] -= home_FT_adv
      if self.game_type in 'RoSo':
        self.away.players[p].game_attributes['Perimeter Def'] += 33
        self.away.players[p].game_attributes['Inside Def'] += 33      
      if (self.away.players[p].game_attributes['Off Reb'] > 30):
        x = self.away.players[p].game_attributes['Off Reb']
        if x > 60:
          x -= int(10 + x - 60 * 2 / 3)
        else:
          x -= int((x - 30) / 3)
        self.away.players[p].game_attributes['Off Reb'] = x

    return

  def run_match(self):
    finished = False
    while finished == False:
      if self.period <= self.tot_periods: 
        period_time = self.period_time
        if self.period == self.tot_periods:
          if self.home.game['Timeouts'] > 3:
            self.home.game['Timeouts'] = 3
          if self.away.game['Timeouts'] > 3:
            self.away.game['Timeouts'] = 3
            
      else: 
        self.overtimes = self.period - self.tot_periods
        period_time = self.overtime_time
        self.home.game['Timeouts'] = 2
        self.away.game['Timeouts'] = 2
      
      #Run period  
      period_obj = Period(self.period,self.tot_periods,period_time,\
                          self.home,self.away,self.misc_stats_dict,self.PBP_history,\
                          self.sub_allowed,self.game_type)
      
      if self.period >= self.tot_periods and \
        self.home.game['Stats']['Points'] != self.away.game['Stats']['Points']:
        period_obj.timeout(None,True)                 
        if self.home.game['Stats']['Points'] > self.away.game['Stats']['Points']:
          self.winner = self.home.name
        else:
          self.winner = self.away.name
        finished = True
        end_line = '***End of the match***'
        print (end_line)
        self.PBP_history.append(end_line)
      self.period += 1
    
    self.away.print_boxscore_to_screen(basic = True)    
    self.home.print_boxscore_to_screen(basic = True)
    self.match_time = self.period_time*self.tot_periods + \
                      self.overtime_time*self.overtimes
    return    
  
  '''
  def post_match(self):
    
    for t in self.l_obj.teams:
      if t in (self.home.nickname,self.away.nickname):
        game_occurred = True
      else:
        game_occurred = False
      for p in self.l_obj.teams[t].players:
        self.l_obj.teams[t].players[p].update_processes(self.l_obj.update_str,\
                                                       self.l_obj.teams[t],game_occurred)
      self.l_obj.teams[t].check_player_status()
    
    for pos in self.l_obj.players['FA']:
      for p in self.l_obj.players['FA'][pos]:
        self.l_obj.players['FA'][pos][p].update_processes(self.l_obj.update_str,\
                                                            None,False)   
    return 
  '''
  
  #-----------------------------------------------------------------------------
  # Function store_RoSo_data
  #
  # 1. Writes boxscore, play-by-play
  # 2. Writes rosters
  #-----------------------------------------------------------------------------
  def store_RoSo_data(self):
    self.gen_boxscore_file()
    self.gen_PBP_file()
    roster_file = self.l_obj.year_all_star_dir + os.sep + 'RoSo_rosters.txt'
    with open (roster_file,'w') as f:
      f.write('Sophomores [SOPH]\n')
      for p in self.away.players:
        line = p + ' ' + self.away.players[p].profile['Pos'] + ' ' + self.away.players[p].team_nick       
        f.write(line + '\n')
      f.write('\n')
      f.write('Rookies [ROOK]\n')
      for p in self.home.players:
        line = p + ' ' + self.home.players[p].profile['Pos'] + ' ' + self.home.players[p].team_nick       
        f.write(line + '\n')        
    return
    
  def store_ASG_data(self):
    self.gen_boxscore_file()
    self.gen_PBP_file()
    roster_file = self.l_obj.year_all_star_dir + os.sep + 'RoSo_rosters.txt'
    with open (roster_file,'w') as f:
      away_title = self.away.name + '[' + self.away.nickname + ']\n'
      f.write(away_title)
      for p in self.away.players:
        line = p + ' ' + self.away.players[p].profile['Pos'] + ' ' + self.away.players[p].team_nick       
        if self.away.players[p].status['Days Injured'] > 0:
          line += ' (Injured)'
        f.write(line + '\n')
      f.write('\n')
      home_title = self.home.name + '[' + self.home.nickname + ']\n'
      f.write(home_title)
      for p in self.home.players:
        line = p + ' ' + self.home.players[p].profile['Pos'] + ' ' + self.home.players[p].team_nick       
        if self.home.players[p].status['Days Injured'] > 0:
          line += ' (Injured)'
        f.write(line + '\n')      
    
    return
  
      
  #-----------------------------------------------------------------------------
  # Function update_player_stats
  #
  #
  #-----------------------------------------------------------------------------
  def update_player_stats(self):
    for t in (self.home,self.away):
      t_game_stats = t.game['Stats']
      if t == self.home:
        opp_game_stats = self.away.game['Stats']
      else:
        opp_game_stats = self.home.game['Stats']
        
      for p in t.players:
        
        p_year_stats = t.players[p].stats['Y' + str(self.year)]
        #print ('VC: Prev ' + p + ' stats: ' + str(p_year_stats))
        p_career_stats = t.players[p].stats['Career']
        p_game_stats = t.players[p].game['Stats']
        
        for s in p_game_stats:
          p_year_stats[s] += p_game_stats[s] 
          p_career_stats[s] += p_game_stats[s]
        
        p_year_stats['All Team Points A'] += opp_game_stats['Points']
        p_year_stats['All Team Points F'] += t_game_stats['Points']
        p_career_stats['All Team Points A'] += opp_game_stats['Points']
        p_career_stats['All Team Points F'] += t_game_stats['Points']
        
        if p_game_stats['Court Time'] > 0:
          p_year_stats['Games Played'] += 1
          p_career_stats['Games Played'] += 1
        if p in t.game['Starters']:
          p_year_stats['Games Started'] += 1
          p_career_stats['Games Started'] += 1
        
        p_year_stats['Team Court Time'] += self.match_time
        p_year_stats['Team Games'] += 1
        p_career_stats['Team Court Time'] += self.match_time
        p_career_stats['Team Games'] += 1
        
        #print ('VC: Updated ' + p + ' stats: ' + str(p_year_stats))
    return  
  
  #-----------------------------------------------------------------------------
  # Function store_player_data
  #
  # Updates:
  # 1. Year stat totals ([year_player_dir]/Stat_toals.txt)
  # 2. Year logs        ([year_player_dir]/Game_logs.txt)
  # 3. All time logs    ([a_t_player_dir]/Game_logs.txt)
  #-----------------------------------------------------------------------------
  def store_player_data(self):
 
    for t in (self.home,self.away):
      for p in t.players:           
        
        if not os.path.exists(t.players[p].year_dir):
          os.makedirs(t.players[p].year_dir)
        if not os.path.exists(t.players[p].all_time_dir):
          os.makedirs(t.players[p].all_time_dir)
          
        #1. Year stat totals
        with open (t.players[p].year_stat_totals_file,'w') as f:
          for s in t.players[p].stats['Y' + str(self.year)]:
            line = s + '|' + str(t.players[p].stats['Y' + str(self.year)][s])
            f.write(line + '\n')
        
        #2. Year player logs     
        if os.path.isfile(t.players[p].year_logs_file):
          with open(t.players[p].year_logs_file,'a') as f:
            year_stat_line = self.create_player_line(p,'Year',False)
            f.write(year_stat_line + '\n') 
        else:
          with open(t.players[p].year_logs_file,'w') as f:
            year_title_line = self.create_player_line(p,'Year',True)
            f.write(year_title_line + '\n')
            year_stat_line = self.create_player_line(p,'Year',False)
            f.write(year_stat_line + '\n')   
        
        #3. All time logs
        if os.path.isfile(t.players[p].a_t_logs_file):
          with open(t.players[p].a_t_logs_file,'a') as f:
            a_t_stat_line = self.create_player_line(p,'All Time',False)
            f.write(a_t_stat_line + '\n') 
        else:
          with open(t.players[p].a_t_logs_file,'w') as f:
            a_t_title_line = self.create_player_line(p,'All Time',True)
            f.write(a_t_title_line + '\n')
            a_t_stat_line = self.create_player_line(p,'All Time',False)
            f.write(a_t_stat_line + '\n') 
               
    return

  #-------------------------------------------------------------------------------
  # Function create_player_line
  #-------------------------------------------------------------------------------
  def create_player_line(self,player,line_type,title): 
    line = ''
    
    if player:
      if player in self.home.players:
        p_obj = self.home.players[player]
        team_name = self.home.name
        o_team_nick = self.away.nickname
        vs_str = 'v'
        team_score = self.home.game['Stats']['Points']
        opp_team_score = self.away.game['Stats']['Points']
        
      elif player in self.away.players:
        team_name = self.away.name
        p_obj = self.away.players[player]
        o_team_nick = self.home.nickname
        vs_str = '@'
        team_score = self.away.game['Stats']['Points']
        opp_team_score = self.home.game['Stats']['Points']          
      p_stats = p_obj.game['Stats']
      if p_obj.game['Starter'] == True:
        starter_str = '1'
      else:
        starter_str = '0'    
      if self.winner == team_name:
        WL_str = 'W'
      else:
        WL_str = 'L'
    else:
      starter_str = ''
      o_team_nick = ''
      WL_str = ''
      vs_str = ''
      team_score = ''
      opp_team_score = ''
       
    if line_type == 'All Time':
      head_seq = (('Year',str(self.year)),\
                  ('Team',o_team_nick))        
    elif line_type == 'Team':
      head_seq = (('Player',player),)
    elif line_type == 'Boxscore':
      head_seq = ((team_name,player),)
    elif line_type == 'Year':
      head_seq = ()
    if title == True:
      for s in head_seq:
        line += s[0] + ' '
    else:
      for s in head_seq:
        line += '{:>{l}}'.format(s[1],l=len(s[0])) + ' '
    
    if line_type != 'Boxscore':
      opp_str = vs_str + o_team_nick
      result_str = WL_str + '(' + str(team_score) + '-' +\
                   str(opp_team_score) + ')'

      print_seq = (('Game',self.game_no),\
                   ('Type',self.game_type),\
                   ('Opp.',opp_str),\
                   ('    Result',result_str),\
                   ('OT',self.overtimes),\
                   ('St',starter_str))
                   
      if title == True:
        for s in print_seq:
          line += s[0] + ' '
      else:
        for s in print_seq:
          line += '{:>{l}}'.format(s[1],l=len(s[0])) + ' '
                   
    for s in P_STATS_WRITE_SEQ:
      if title == True:
        line += STAT_NAME_TO_ABBREV[s] + ' '
      else:
        line += '{:>{l}}'.format(str(p_stats[s]),\
                                 l=len(STAT_NAME_TO_ABBREV[s])) + ' '
      
    if line_type != 'Boxscore':
      if not player:
        status_str = ''
      elif p_obj.game['Court Status'] >= 0:
        status_str = 'A'
      elif p_obj.game['Court Status'] == -1:
        status_str = 'A'
      elif p_obj.game['Court Status'] == -2:
        status_str = 'I'
      end_seq = (('CS',status_str),)
      if title == True:
        for s in end_seq:
          line += s[0] + ' '
      else:
        for s in end_seq:
          line += '{:>{l}}'.format(s[1],l=len(s[0])) + ' '
      
    line = line[:-1]
    return (line)
    
  #-----------------------------------------------------------------------------
  # Function update_team_stats
  #
  #
  #-----------------------------------------------------------------------------  
  def update_team_stats(self):
    for t in (self.home,self.away):
      t_game_stats = t.game['Stats']
      t_year_stats = t.stats['Y' + str(self.year)]
      if t == self.home:
        opp_game_stats = self.away.game['Stats']
      else:
        opp_game_stats = self.home.game['Stats']
      
      for s in t_game_stats:
        t_year_stats['Own'][s] += t_game_stats[s]
        t_year_stats['Opp'][s] += opp_game_stats[s]
      t_year_stats['Games'] += 1
    return
  
  #-----------------------------------------------------------------------------
  # Function store_team_data
  #
  # Updates:
  # 1. Year stat totals ([year_team_dir]/Stat_toals.txt)
  # 2. Year logs        ([year_team_dir]/Team_logs.txt)
  # 3. All time logs    ([a_t_team_dir]/Team_logs.txt)
  # 4. Year player logs ([year_team_dir]/Player_logs.txt)
  # 5. Year results     ([year_team_dir]/Results.txt)
  #-----------------------------------------------------------------------------
  def store_team_data(self):
                    
    for t in (self.home,self.away): 

      #1. Year stat totals
      with open (t.year_stat_totals_file ,'w') as f:
        line = 'Games|' + str(t.stats['Y' + str(self.year)]['Games'])
        f.write(line + '\n')
        for type in ('Own','Opp'):
          for s in t.stats['Y' + str(self.year)][type]:
            line = type + '|' + s + '|' + \
                   str(t.stats['Y' + str(self.year)][type][s])
            f.write(line + '\n')
      
      #2. Year logs 
      if os.path.isfile(t.year_team_logs_file):
        with open(t.year_team_logs_file,'a') as f:
          year_stat_line = self.create_team_line(t.name,'Year',False)
          f.write(year_stat_line + '\n') 
      else:
        with open(t.year_team_logs_file,'w') as f:
          year_title_line = self.create_team_line(t.name,'Year',True)
          f.write(year_title_line + '\n')
          year_stat_line = self.create_team_line(t.name,'Year',False)
          f.write(year_stat_line + '\n')  
               
      #3. All time logs 
      if os.path.isfile(t.a_t_team_logs_file):
        with open(t.a_t_team_logs_file,'a') as f:
          a_t_stat_line = self.create_team_line(t.name,'All Time',False)
          f.write(a_t_stat_line + '\n') 
      else:
        with open(t.a_t_team_logs_file,'w') as f:
          a_t_title_line = self.create_team_line(t.name,'All Time',True)
          f.write(a_t_title_line + '\n')
          a_t_stat_line = self.create_team_line(t.name,'All Time',False)
          f.write(a_t_stat_line + '\n')  
      
      #4. Year player logs
      if os.path.isfile(t.year_player_logs_file):
        with open(t.year_player_logs_file,'a') as f:
          for p in t.players:  
            team_line = self.create_player_line(p,'Team',False)
            f.write(team_line + '\n')    
      else:
        with open(t.year_player_logs_file,'w') as f:
          team_title_line = self.create_player_line(None,'Team',True)
          f.write(team_title_line + '\n')
          for p in t.players:  
            team_line = self.create_player_line(p,'Team',False)
            f.write(team_line + '\n')    
        
      #5 Year results
      if os.path.isfile(t.year_results_file):
        with open(t.year_results_file,'a') as f:  
          results_line = self.create_team_results_line(t.name,False)
          f.write(results_line + '\n')
      else:
        with open(t.year_results_file,'w') as f:  
          results_title_line = self.create_team_results_line(t.name,True)
          f.write(results_title_line + '\n')
          results_line = self.create_team_results_line(t.name,False)
          f.write(results_line + '\n')
    return

  #---------------------------------------------------------------------------
  # function create_team_results_line
  #---------------------------------------------------------------------------
  def create_team_results_line(self,team_name,title):
    if team_name == self.home.name:
      t_obj = self.home
      opp_obj = self.away
      vs_str = 'v'
      HA_str = 'H'
      opp_HA_str = 'A'
    else:
      t_obj = self.away
      opp_obj = self.home
      vs_str = '@'
      HA_str = 'A'
      opp_HA_str = 'H'
    
    t_stats = t_obj.game['Stats']
    opp_stats = opp_obj.game['Stats']
    
    opp_nick = opp_obj.nickname
    year_str = 'Y' + str(self.year)
    
    t_year_record = t_obj.record.own[year_str]['All']
    t_a_t_record = t_obj.record.own['All Time']['All']
    opp_year_record = opp_obj.record.own[year_str]['All']
    opp_a_t_record = opp_obj.record.own['All Time']['All']
    h2h_year_record = t_obj.record.h2h[year_str][opp_nick]
    h2h_a_t_record = t_obj.record.h2h['All Time'][opp_nick]
    
    if self.winner == team_name:
      WL_str = 'W'
      opp_WL_str = 'L'
      strk_factor = 1
    else:
      WL_str = 'L'   
      opp_WL_str = 'W'
      strk_factor = -1   
    
    opp_str = vs_str + opp_obj.nickname
    score_str = str(t_stats['Points']) + '-' + str(opp_stats['Points'])
    
    if self.same_conf == True:
      same_conf_str = 'Intra'
      conf_type_record = t_obj.record.own[year_str]['Conf'] 
    else: 
      same_conf_str = 'Inter'
      conf_type_record = t_obj.record.own[year_str]['Inter-Conf']
      
    record_str = str(t_year_record['Wins']) + '-' + \
                 str(t_year_record['Losses']) + '(' + HA_str + ':' + \
                 str(t_year_record[HA_str + ' Wins']) + '-' + \
                 str(t_year_record[HA_str + ' Losses']) + ')'
    
    opp_record_str = str(opp_year_record['Wins']) + '-' + \
                     str(opp_year_record['Losses']) + '(' + opp_HA_str + ':' + \
                     str(opp_year_record[opp_HA_str + ' Wins']) + '-' + \
                     str(opp_year_record[opp_HA_str + ' Losses']) + ')'
    
    a_t_record_str = str(t_a_t_record['Wins']) + '-' + \
                     str(t_a_t_record['Losses']) + '(' + HA_str + ':' + \
                     str(t_a_t_record[HA_str + ' Wins']) + '-' + \
                     str(t_a_t_record[HA_str + ' Losses']) + ')'
    
    conf_type_record_str = str(conf_type_record['Wins']) + '-' + \
                           str(conf_type_record['Losses']) + '(' + HA_str + ':' + \
                           str(conf_type_record[HA_str + ' Wins']) + '-' + \
                           str(conf_type_record[HA_str + ' Losses']) + ')'
    
    year_h2h_str = str(h2h_year_record['Wins']) + '-' + \
                   str(h2h_year_record['Losses']) + '(' + HA_str + ':' + \
                   str(h2h_year_record[HA_str + ' Wins']) + '-' + \
                   str(h2h_year_record[HA_str + ' Losses']) + ')'
    
    a_t_h2h_str = str(h2h_a_t_record['Wins']) + '-' + \
                  str(h2h_a_t_record['Losses']) + '(' + HA_str + ':' + \
                  str(h2h_a_t_record[HA_str + ' Wins']) + '-' + \
                  str(h2h_a_t_record[HA_str + ' Losses']) + ')'
    
    L10_str = ''
    for x in t_year_record['L10']:
      if x == 1:
        L10_str += 'W'
      else:
        L10_str += 'L'    
    
    strk_str = WL_str + str(strk_factor*t_year_record['Streak'])

    h2h_L10_str = ''
    for x in h2h_a_t_record['L10']:
      if x == 1:
        h2h_L10_str += 'W'
      else:
        h2h_L10_str += 'L'
    
    a_t_strk_str = WL_str + str(strk_factor*t_a_t_record['Streak'])
    h2h_strk_str = WL_str + str(strk_factor*h2h_a_t_record['Streak'])
   
    stat_seq = (('Game',str(self.game_no)),\
                ('Type',self.game_type),\
                ('Conf-Type',same_conf_str),\
                ('Opp.',opp_str),\
                ('Res.',WL_str),\
                ('  Score',score_str),\
                ('OTs',str(self.overtimes)),\
                ('        Record',record_str),\
                ('    Opp.Record',opp_record_str),\
                ('    All-TimeRecord',a_t_record_str),\
                ('Conf-TypeRecord',conf_type_record_str),\
                ('     SeasonH2H',year_h2h_str),\
                ('       All-TimeH2H',a_t_h2h_str),\
                (' SeasonL10',L10_str),\
                ('Streak',strk_str),\
                ('    H2HL10',h2h_L10_str),\
                ('A-TStreak',a_t_strk_str),\
                ('H2HStreak',h2h_strk_str))
    
    line = ''
    for s in stat_seq:
      if title == True:
        line += s[0] + ' '
      else:
        line += '{:>{l}}'.format(s[1],l=len(s[0])) + ' '
    
    return (line)  

  #-----------------------------------------------------------------------------
  # Function create_team_line
  #
  #
  #-----------------------------------------------------------------------------
  def create_team_line(self,team_name,line_type,title):
    if team_name == self.home.name:
      t_obj = self.home
      opp_obj = self.away
      vs_str = 'v'
    else:
      t_obj = self.away
      opp_obj = self.home
      vs_str = '@'
    
    t_stats = t_obj.game['Stats']
    opp_stats = opp_obj.game['Stats']
    t_misc_stats = t_obj.game['Misc Stats']
    opp_misc_stats = opp_obj.game['Misc Stats']
    
    if self.winner == team_name:
      WL_str = 'W'
    else:
      WL_str = 'L'
    
    #---------------------------------------------------------------------
    # Leading columns: Game #, game_type, (v./@)opp, result, overtimes  
    opp_str = vs_str + opp_obj.nickname  
    result_str = WL_str +'(' + str(t_stats['Points']) + '-' +\
                 str(opp_stats['Points']) + ')'
    
    if line_type == 'All Time':
      head_seq = (('Year',self.year),\
                  ('Game',self.game_no),\
                  ('Type',self.game_type),\
                  ('Opp.',opp_str),\
                  ('    Result',result_str),\
                  ('OT',self.overtimes),\
                  ('Ties',self.misc_stats_dict['Ties']),\
                  ('LChgs',self.misc_stats_dict['Lead Changes']))    
      
    elif line_type == 'Year':             
      head_seq = (('Game',self.game_no),\
                  ('Type',self.game_type),\
                  ('Opp.',opp_str),\
                  ('    Result',result_str),\
                  ('OT',self.overtimes),\
                  ('Ties',self.misc_stats_dict['Ties']),\
                  ('LChgs',self.misc_stats_dict['Lead Changes']))   
    
    line = ''
    if title == True:
      for s in head_seq:
        line += s[0] + ' '
    else:
      for s in head_seq:
        line += '{:>{l}}'.format(s[1],l=len(s[0])) + ' '

    for s in T_STATS_WRITE_SEQ:
      if title == True:
        line += STAT_NAME_TO_ABBREV[s] + ' '
      else:
        line += '{:>{l}}'.format(str(t_stats[s]),\
                                 l=len(STAT_NAME_TO_ABBREV[s])) + ' '
   
    for s in T_MISC_STATS_WRITE_SEQ:
      if title == True:
        line += STAT_NAME_TO_ABBREV[s] + ' '
      else:
        line += '{:>{l}}'.format(str(t_misc_stats[s]),\
                                      l=len(STAT_NAME_TO_ABBREV[s])) + ' '
    
    for s in T_STATS_WRITE_SEQ:
      if title == True:
        line += 'o' + STAT_NAME_TO_ABBREV[s] + ' '
      else:
        line += '{:>{l}}'.format(str(opp_stats[s]),\
                                 l=len(STAT_NAME_TO_ABBREV[s])+1) + ' '
   
    for s in T_MISC_STATS_WRITE_SEQ:
      if title == True:
        line += 'o' + STAT_NAME_TO_ABBREV[s] + ' '
      else:
        line += '{:>{l}}'.format(str(opp_misc_stats[s]),\
                                 l=len(STAT_NAME_TO_ABBREV[s])+1) + ' '
    
    # Period scores
    periods_str = ''
    for i in range(self.tot_periods + self.overtimes):
      if i > 0:
        periods_str += ','
      periods_str += str(t_obj.game['Period Scores'][i]) + '-' + \
                    str(opp_obj.game['Period Scores'][i])
    
    if title == True:
      line += 'PeriodScores'
    else:
      line += periods_str  
            
    return (line)
  
  #---------------------------------------------------------------------------
  # Function store_league_data
  #
  # Operation
  # 1. Creates boxscore file
  # 2. Creates PBP file
  # 3. Updates year results file
  #---------------------------------------------------------------------------
  def store_league_data(self):   
    
    #1. Create boxscore file
    self.gen_boxscore_file()
    
    #2. Create PBP file
    self.gen_PBP_file()
    
    #3. Update year results file
    if os.path.isfile(self.l_obj.year_results_file):
      with open(self.l_obj.year_results_file,'a') as f:  
        results_line = self.create_league_results_line(False)
        f.write(results_line + '\n')
    else:
      with open(self.l_obj.year_results_file,'w') as f:  
        results_title_line = self.create_league_results_line(True)
        f.write(results_title_line + '\n')
        results_line = self.create_league_results_line(False)
        f.write(results_line + '\n')    
    
    return
  
  #-----------------------------------------------------------------------------------
  # Function gen_PBP_file
  #-----------------------------------------------------------------------------------
  def gen_PBP_file(self):
    if self.game_type == 'RS':
      PBP_file_name = self.l_obj.year_games_dir + os.sep + 'Game_' + \
                      str(self.game_no) + '_PBP.txt'
    elif self.game_type == 'RoSo':
      PBP_file_name = self.l_obj.year_all_star_dir + os.sep + 'RoSo_PBP.txt'
    elif self.game_type == 'ASG':
      PBP_file_name = self.l_obj.year_all_star_dir + os.sep + 'ASG_PBP.txt'
    with open(PBP_file_name,'w') as f:
      title_line = 'Year:' + str(self.year) + ' Game:' + str(self.game_no) + \
                   ' Type:' + self.game_type + ' ' + self.away.nickname + '@' +\
                    self.home.nickname    
      f.write(title_line + '\n')         
      for line in self.PBP_history:
        f.write(line + '\n')
     
    return
    
  #-----------------------------------------------------------------------------------
  # Function gen_boxscore_file
  #-----------------------------------------------------------------------------------
  def gen_boxscore_file(self):
    if self.game_type == 'RS':
      box_file_name = self.l_obj.year_games_dir + os.sep + 'Game_' + \
                      str(self.game_no) + '_stats.txt'
    elif self.game_type == 'RoSo':
      box_file_name = self.l_obj.year_all_star_dir + os.sep + 'RoSo_stats.txt'
    elif self.game_type == 'ASG':
      box_file_name = self.l_obj.year_all_star_dir + os.sep + 'ASG_stats.txt'
    else:
      print ("VC needs to add gen_boxscore_file functionality for non RS/AS games!")
    
    with open(box_file_name,'w') as f:
      title_line = 'Year:' + str(self.year) + ' Game:' + str(self.game_no) + \
                   ' Type:' + self.game_type + ' ' + self.away.nickname + '@' +\
                    self.home.nickname    
      f.write(title_line + '\n')     
      
      for t in (self.away,self.home):
        title_line = self.create_player_line(t.game['Starters'][0],'Boxscore',True)
        f.write(title_line + '\n')    
        f.write('STARTERS\n')
      
        # Ranking the starters by minutes played
        min_dict = {}
        for p in t.game['Starters']:
          min_dict[p] = t.players[p].game['Stats']['Court Time']
        starters_min_rank = F_RANK_FROM_RATINGS(min_dict,descending = True)
      
        for p in starters_min_rank:     
          line = self.create_player_line(p,'Boxscore',False)
          f.write(line + '\n')
        
        if len(t.game['Bench']) > 0:
          
          f.write('BENCH\n')
      
          # Ranking the bench players by minutes played
          min_dict = {}
          for p in t.game['Bench']:
            min_dict[p] = t.players[p].game['Stats']['Court Time']
          bench_min_rank = rank_from_ratings(min_dict,descending = True)    
    
          for p in bench_min_rank:
            if t.players[p].game['Stats']['Court Time'] == 0:
              line = '{:>{l}}'.format(p,l=len(t.name)) + ' DNP-CD'
            else:
              line = self.create_player_line(p,'Boxscore',False)
            f.write(line + '\n')
        
          for p in sorted(t.game['Unavailable']):
            DNP_str = 'Injured'
            line = '{:>{l}}'.format(p,l=len(t.name)) + ' DNP-' + DNP_str

            f.write(line + '\n')
                
      return
      
  #---------------------------------------------------------------------------
  # Function create_league_results_line
  #---------------------------------------------------------------------------
  def create_league_results_line(self,title):
    year_str = 'Y' + str(self.year)
    
    H_nick = self.home.nickname
    A_nick = self.away.nickname
    
    H_stats = self.home.game['Stats']
    A_stats = self.away.game['Stats']
    
    H_year_record = self.home.record.own[year_str]['All']
    H_a_t_record = self.home.record.own['All Time']['All']
    A_year_record = self.away.record.own[year_str]['All']
    A_a_t_record = self.away.record.own['All Time']['All']
    
    H_h2h_year_record = self.home.record.h2h[year_str][A_nick]
    H_h2h_a_t_record = self.home.record.h2h['All Time'][A_nick]
    A_h2h_year_record = self.away.record.h2h[year_str][H_nick]
    A_h2h_a_t_record = self.away.record.h2h['All Time'][H_nick]
    
    if self.winner == self.home.name:
      H_WL_str = 'W'
      A_WL_str = 'L'
      H_strk_factor = 1    
    else:
      H_WL_str = 'L'   
      A_WL_str = 'W'
      H_strk_factor = -1   
    
    score_str = str(H_stats['Points']) + '-' + str(A_stats['Points'])
    
    if self.same_conf == True:
      same_conf_str = 'Intra'
      H_conf_type_record = self.home.record.own[year_str]['Conf'] 
      A_conf_type_record = self.away.record.own[year_str]['Conf']
    else: 
      same_conf_str = 'Inter'
      H_conf_type_record = self.home.record.own[year_str]['Inter-Conf']
      A_conf_type_record = self.away.record.own[year_str]['Inter-Conf']
      
    H_record_str = str(H_year_record['Wins']) + '-' + \
                   str(H_year_record['Losses']) + '(H:' + \
                   str(H_year_record['H Wins']) + '-' + \
                   str(H_year_record['H Losses']) + ')'
    
    A_record_str = str(A_year_record['Wins']) + '-' + \
                   str(A_year_record['Losses']) + '(A:' + \
                   str(A_year_record['A Wins']) + '-' + \
                   str(A_year_record['A Losses']) + ')'
     
    H_conf_type_record_str = str(H_conf_type_record['Wins']) + '-' + \
                             str(H_conf_type_record['Losses']) + '(H:' + \
                             str(H_conf_type_record['H Wins']) + '-' + \
                             str(H_conf_type_record['H Losses']) + ')'
    
    A_conf_type_record_str = str(A_conf_type_record['Wins']) + '-' + \
                             str(A_conf_type_record['Losses']) + '(A:' + \
                             str(A_conf_type_record['A Wins']) + '-' + \
                             str(A_conf_type_record['A Losses']) + ')'

    if H_h2h_year_record['Wins'] >= H_h2h_year_record['Losses']:
      year_h2h_str = H_nick + ':' + \
                     str(H_h2h_year_record['Wins']) + '-' + \
                     str(H_h2h_year_record['Losses']) + '(H:' + \
                     str(H_h2h_year_record['H Wins']) + '-' + \
                     str(H_h2h_year_record['H Losses']) + ')' 
    else:
      year_h2h_str = A_nick + ':' + \
                     str(A_h2h_year_record['Wins']) + '-' + \
                     str(A_h2h_year_record['Losses']) + '(H:' + \
                     str(A_h2h_year_record['H Wins']) + '-' + \
                     str(A_h2h_year_record['H Losses']) + ')'
    
    if H_h2h_a_t_record['Wins'] >= H_h2h_a_t_record['Losses']:
      a_t_h2h_str = H_nick + ':' + \
                    str(H_h2h_a_t_record['Wins']) + '-' + \
                    str(H_h2h_a_t_record['Losses']) + '(H:' + \
                    str(H_h2h_a_t_record['H Wins']) + '-' + \
                    str(H_h2h_a_t_record['H Losses']) + ')' 
    else:
      a_t_h2h_str = A_nick + ':' + \
                    str(A_h2h_a_t_record['Wins']) + '-' + \
                    str(A_h2h_a_t_record['Losses']) + '(H:' + \
                    str(A_h2h_a_t_record['H Wins']) + '-' + \
                    str(A_h2h_a_t_record['H Losses']) + ')'
    
    H_strk_str = H_WL_str + str(H_strk_factor*H_year_record['Streak'])
    A_strk_str = A_WL_str + str(-H_strk_factor*H_year_record['Streak'])

    home_h2h_L10_W = sum(H_h2h_a_t_record['L10'])
    home_h2h_L10_L = len(H_h2h_a_t_record['L10']) - home_h2h_L10_W
                       
    if home_h2h_L10_W >= home_h2h_L10_L:        
      h2h_L10_str = H_nick + ':' + str(home_h2h_L10_W) + '-' + \
                    str(home_h2h_L10_L)
    else:
      h2h_L10_str = A_nick + ':' + str(home_h2h_L10_L) + '-' + \
                    str(home_h2h_L10_W)
    
    if H_h2h_a_t_record['Streak'] > 0:
      h2h_strk_str = H_nick + ':W' + str(H_h2h_a_t_record['Streak'])
    else:
      h2h_strk_str = A_nick + ':W' + str(A_h2h_a_t_record['Streak'])
              
    H_L10_str = ''
    for x in H_year_record['L10']:
      if x == 1:
        H_L10_str += 'W'
      else:
        H_L10_str += 'L'    
    
    A_L10_str = ''
    for x in A_year_record['L10']:
      if x == 1:
        A_L10_str += 'W'
      else:
        A_L10_str += 'L'    
    
    if H_h2h_a_t_record['Streak'] > 0:
      h2h_strk_str = H_nick
    else:
      h2h_strk_str = A_nick
    h2h_strk_str += ':W' + str(H_strk_factor*H_h2h_a_t_record['Streak'])
    
    stat_seq = (('Game',str(self.game_no)),\
                ('Type',self.game_type),\
                ('Conf-Type',same_conf_str),\
                ('Home',H_nick),\
                ('Away',A_nick),\
                ('  Score',score_str),\
                ('OT',str(self.overtimes)),\
                ('      HomeRecord',H_record_str),\
                ('     H-L10',H_L10_str),\
                ('H-Streak',H_strk_str),\
                ('H-Conf-TypeRecord',H_conf_type_record_str),\
                ('      AwayRecord',A_record_str),\
                ('     A-L10',A_L10_str),\
                ('A-Conf-TypeRecord',A_conf_type_record_str),\
                ('A-Streak',A_strk_str),\
                ('       SeasonH2H',year_h2h_str),\
                ('  H2HL10',h2h_L10_str),\
                ('H2HStreak',h2h_strk_str),\
                ('          AllTimeH2H',a_t_h2h_str))   
    
    line = ''
    for s in stat_seq:
      if title == True:
        line += s[0] + ' '
      else:
        line += '{:>{l}}'.format(s[1],l=len(s[0])) + ' '
    
    return (line) 