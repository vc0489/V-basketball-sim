import os
import copy
import decimal
import shutil
import random
from GlobalVariables import *
from GlobalFunctions import *
from MatchClass import *
from TeamClass import *
from Menus import *
from AllStarFunctions import *
import sys
#-------------------------------------------------------------------------------
# class League
#
# next_event values:
# --> Draft
# --> FA
# --> RS-G#
# --> 3PC
# --> RoSo
# --> AS
# --> AF-G#
# --> BF-G#
# --> VF-G#
#
#
# new_info_dict contains:
# --> Alpha Teams - list of teams in the Alpha conference 
# --> Beta Teams  - list of teams in the Beta conference
# --> Round Seq   - sequence of team games
#-------------------------------------------------------------------------------
class League:
  def __init__(self,name,new_league):
    self.teams = {}
    self.players = {'Active':copy.deepcopy(SIMP_POS_DICTS_IN_DICT),\
                    'Retired':copy.deepcopy(SIMP_POS_LISTS_IN_DICT),\
                    'FA':copy.deepcopy(SIMP_POS_DICTS_IN_DICT)}
    
    self.name = name
    self.game_dir = 'Season' + os.sep + name

    
    #File that contains last event info
    self.last_event_file = self.game_dir + os.sep + 'Last_event.txt'    
      
    # Determines last event that happened and also the current year and day
    self.det_prev_event()

    # Placeholder for determining the initial year of the league
    self.init_year = STARTING_YEAR
    
    self.year_dir = self.game_dir + os.sep + 'data' + os.sep + 'Year_' + \
                    str(self.cur_year)
    self.all_time_dir = self.game_dir + os.sep + 'data' + os.sep + 'All_time'
    self.draft_dir = self.game_dir + os.sep + 'Draft' + os.sep + 'Year_' + \
                     str(self.cur_year)
    self.year_league_dir = self.year_dir + os.sep + 'League'
    self.year_results_file = self.year_league_dir + os.sep + 'Results.txt'
    self.year_games_dir = self.year_dir + os.sep + 'Games'
    self.year_all_star_dir = self.year_dir + os.sep + 'All_star'
    self.transactions_file = self.year_league_dir + os.sep + 'Transactions.txt'
    self.FA_files = {}
    self.retired_files = {}
    for pos in SIMP_POS_LISTS_IN_DICT:
      FA_file = self.year_dir + os.sep + 'Free_agents' + os.sep + pos + '.txt'     
      retired_file = self.year_dir + os.sep + 'Retired_players' + os.sep + \
                     pos + '.txt'
      self.FA_files[pos] = FA_file
      self.retired_files[pos] = retired_file
    
    self.round_seq_file = self.year_dir + os.sep + 'Round_sequence.txt'
    self.sch_file = self.year_dir + os.sep + 'Schedule.txt' 
    #Conference and round sequence files for current year
    self.conf_file = self.year_dir + os.sep + 'Conferences.txt'
    
    self.all_star_results_file = self.year_all_star_dir + os.sep + 'Results.txt'
    self.three_comp_details_file = self.year_all_star_dir + os.sep + '3PC.txt'
    
                         
    self.conferences = {'Alpha':[],'Beta':[]}
    self.atts_dir = self.game_dir + os.sep + 'Attributes'
    
    self.initialise(new_league)
    
    self.backup_dir = 'Back_ups' + os.sep + name

    if os.path.isdir(self.backup_dir):
      shutil.rmtree(self.backup_dir)
    shutil.copytree(self.game_dir,self.backup_dir)    
    
    self.run_league()
    return
  
  def create_year_dir_structure(self):
    os.makedirs(self.draft_dir)
    os.makedirs(self.year_dir)
    os.makedirs(self.year_dir + os.sep + 'Teams')
    os.makedirs(self.year_dir + os.sep + 'Players')
    os.makedirs(self.year_league_dir)
    os.makedirs(self.year_games_dir)
    os.makedirs(self.year_all_star_dir)
    os.makedirs(self.year_dir + os.sep + 'Free_agents')
    os.makedirs(self.year_dir + os.sep + 'Retired_players')  
    for t_name in NAME_TO_NICK:
      os.makedirs(self.year_dir + os.sep + 'Teams' + os.sep + t_name)  
    return
    
  def create_dir_structure(self):
    os.makedirs(self.game_dir)
    os.makedirs(self.game_dir + os.sep + 'data')
    os.makedirs(self.atts_dir)
    
    self.create_year_dir_structure()
    
    os.makedirs(self.all_time_dir)
    os.makedirs(self.all_time_dir + os.sep + 'Teams')
    os.makedirs(self.all_time_dir + os.sep + 'Players')
    for t_name in NAME_TO_NICK:
      os.makedirs(self.all_time_dir + os.sep + 'Teams' + os.sep + t_name)
    return
  
  def initialise_new_year(self,new_league=False):
    for pos in SIMP_POS_DICTS_IN_DICT:
      for p in self.players['FA'][pos]:
        os.makedirs(self.players['FA'][pos][p].year_dir)
        if new_league == True:
          os.makedirs(self.players['FA'][pos][p].all_time_dir)
    
      for p in self.players['Active'][pos]:
        os.makedirs(self.players['Active'][pos][p].year_dir)
        if new_league == True:
          os.makedirs(self.players['Active'][pos][p].all_time_dir)
    
    return
  #-----------------------------------------------------------------------------
  # Function initialise
  #
  # Function to start a new season, does jobs include:
  # --> Generate conferences
  # --> Generate round sequence
  # --> Generate schedule
  # --> Create roster files
  # --> Fill players dict
  #-----------------------------------------------------------------------------
  def initialise(self,new_league):
    #If brand new league, copy over intial conference, round sequence, 
    # attribute, roster, FA and retired files.
    if new_league == True:
      self.create_dir_structure()
      init_dir = 'Initial_data' + os.sep + 'Y' + str(self.cur_year) 
      
      init_conf_file = init_dir + os.sep + 'Conferences.txt'
      shutil.copyfile(init_conf_file,self.conf_file)
      
      init_round_seq_file = init_dir + os.sep + 'Round_sequence.txt'
      shutil.copyfile(init_round_seq_file,self.round_seq_file)
       
      init_atts_dir = init_dir + os.sep + 'Attributes'
      
      for att_file in os.listdir(init_atts_dir):
        orig_file = init_atts_dir + os.sep + att_file
        dest_file = self.atts_dir + os.sep + att_file
        shutil.copyfile(orig_file,dest_file)      
          
      #Rosters 
      init_roster_dir = init_dir + os.sep + 'Rosters'
      for team_name in NAME_TO_NICK:
        team_nick = NAME_TO_NICK[team_name]
        team_dir = self.year_dir + os.sep + 'Teams' + os.sep + team_name
        orig_file = init_roster_dir + os.sep + team_name + '.txt'
        dest_file = team_dir + os.sep + 'Roster.txt'
        shutil.copyfile(orig_file,dest_file)
        
      #Copy over FA files and retired players files
      for pos in SIMP_POS_DICTS_IN_DICT:
        init_FA_file = init_dir + os.sep + 'Free_agents' + os.sep + pos + '.txt'
        shutil.copyfile(init_FA_file,self.FA_files[pos])     
        init_retired_file = init_dir + os.sep + 'Retired_players' + os.sep + \
                            pos + '.txt'
        shutil.copyfile(init_retired_file,self.retired_files[pos])
        
    #Fill FA and retired player dicts
    for pos in SIMP_POS_DICTS_IN_DICT:
      with open(self.FA_files[pos]) as FA_f:
        for line in FA_f:
          player = line.strip()
          p_obj = Player(player,self.game_dir,self.init_year,self.cur_year)
          self.players['FA'][pos][player] = p_obj                    
          
          
      with open(self.retired_files[pos]) as ret_f:
        for line in ret_f:
          player = line.strip()
          self.players['Retired'][pos].append(player)

    #Determine conferences from file and create team objects and fill league
    # player dicts
    with open(self.conf_file,'r') as conf_f:
      for line in conf_f:
        conf_list = line.split()
        if conf_list[0][:-1] == 'ALPHA':
          for team_nick in conf_list[1:]:
            self.conferences['Alpha'].append(team_nick)
            self.teams[team_nick] = Team(team_nick,self.game_dir,self.cur_year,\
                                         'Reg',None,self.init_year,'Alpha')
            for p in self.teams[team_nick].players:
              pos = self.teams[team_nick].players[p].profile['Simp Pos']
              self.players['Active'][pos][p] = self.teams[team_nick].players[p]
        elif conf_list[0][:-1] == 'BETA':
          for team_nick in conf_list[1:]:
            self.conferences['Beta'].append(team_nick)
            self.teams[team_nick] = Team(team_nick,self.game_dir,self.cur_year,\
                                         'Reg',None,self.init_year,'Beta')
            for p in self.teams[team_nick].players:
              pos = self.teams[team_nick].players[p].profile['Simp Pos']
              self.players['Active'][pos][p] = self.teams[team_nick].players[p]  
                            
    #Round sequence
    with open(self.round_seq_file,'r') as seq_f:
      seq_list = seq_f.readline().split()
      self.round_seq = tuple(team for team in seq_list)
         
    return
  
  #-----------------------------------------------------------------------------
  # Function gen_schedule
  # 
  # Generates a schedule
  #-----------------------------------------------------------------------------
  def gen_schedule(self):
    game_list = []
    intra_rounds = (1,2,3,6,7,8,13,14,15)
    inter_rounds = (4,5,9,10,11,12)
               
    def gen_rand_group(alpha_list,beta_list):
      groups = {}
      alpha = [0,1,2,3]
      beta = [0,1,2,3]
    
      alpha_first = random.choice(alpha)
      alpha.remove(alpha_first)
    
      alpha_second = random.choice(alpha)
      alpha.remove(alpha_second)
    
      beta_first = random.choice(beta)
      beta.remove(beta_first)
    
      beta_second = random.choice(beta)
      beta.remove(beta_second)
    
      groups[1] = (alpha_list[alpha_first],alpha_list[alpha_second],\
                 beta_list[beta_first],beta_list[beta_second])
      groups[2] = (alpha_list[alpha[0]],alpha_list[alpha[1]],\
                 beta_list[beta[0]],beta_list[beta[1]])
      return (groups)
  
    #Groups signify for the alpha teams which beta teams will they face at home
    # twice in the season.
    groups = gen_rand_group(self.conferences['Alpha'],\
                            self.conferences['Beta'])
                            
    home_games_left = {}
  
    for team in self.conferences['Alpha']:
      inter_left_list = []
      intra_left_list = []
      for opp_team in self.conferences['Alpha']:
        if opp_team != team:
          for i in range(3):
            intra_left_list.append(opp_team)
      for opp_team in self.conferences['Beta']:
        if (team in groups[1] and opp_team in groups[1]) or \
           (team in groups[2] and opp_team in groups[2]):
          for i in range(2):
            inter_left_list.append(opp_team)
        else:
          inter_left_list.append(opp_team)
      home_games_left[team] = {}
      home_games_left[team]['Inter'] = inter_left_list
      home_games_left[team]['Intra'] = intra_left_list
    
    for team in self.conferences['Beta']:
      inter_left_list = []
      intra_left_list = []
      for opp_team in self.conferences['Beta']:
        if opp_team != team:
          for i in range(3):
            intra_left_list.append(opp_team)
      for opp_team in self.conferences['Alpha']:
        if (team in groups[1] and opp_team in groups[1]) or \
           (team in groups[2] and opp_team in groups[2]):
          inter_left_list.append(opp_team)
        else:
          for i in range(2):
            inter_left_list.append(opp_team)    
      home_games_left[team] = {}
      home_games_left[team]['Inter'] = inter_left_list
      home_games_left[team]['Intra'] = intra_left_list
    
    game = 1
    for round in range(1,16):
      if round == 11:
        game_list.append({'Game':'AS-3P','Home':'','Away':''})
        game_list.append({'Game':'AS-RoSo','Home':'','Away':''})
        game_list.append({'Game':'ASG','Home':'','Away':''})
      for home_team in self.round_seq:
        if round in inter_rounds:
          list = home_games_left[home_team]['Inter']
        elif round in intra_rounds:
          list = home_games_left[home_team]['Intra']
        away_team = random.choice(list)
        list.remove(away_team)
        game_list.append({'Game':game,'Home':home_team,'Away':away_team})
        game += 1      
         
    with open(self.sch_file,'w') as f:
      f.write('Game Home Away\n')
      for item in game_list:
        line = str(item['Game']) + ' ' + item['Home'] + ' ' + item['Away']
        f.write(line + '\n')
    return
  
  def event_to_update_str(self,event):
    
    if event['Type'] == 'Draft':
      self.update_str = 'Y' + str(self.cur_year) + '-D' + str(self.cur_day) + \
                        '-Draft'
    elif event['Type'] == 'FA':
      self.update_str = 'Y' + str(self.cur_year) + '-D' + str(self.cur_day) + \
                        '-FA'
    elif event['Type'] == 'RS':
      self.update_str = 'Y' + str(self.cur_year) + '-D' + str(self.cur_day) + \
                        '-RSG' + str(event['Game No'])
    elif event['Type'] == 'NEW':
      self.update_str = 'Y' + str(self.cur_year) + '-D0'
    elif event['Type'] == '3PC':
      self.update_str = 'Y' + str(self.cur_year) + '-D' + str(self.cur_day) + \
                        '-AS3PC'
    elif event['Type'] == 'RoSo':
      self.update_str = 'Y' + str(self.cur_year) + '-D' + str(self.cur_day) + \
                        '-ASRoSo'    
    elif event['Type'] == 'ASG':
      self.update_str = 'Y' + str(self.cur_year) + '-D' + str(self.cur_day) + \
                        '-ASG'    
    elif event['Type'] == 'AF':
      self.update_str = 'Y' + str(self.cur_year) + '-D' + str(self.cur_day) + \
                        '-AFG' + str(event['Game No'])    
    elif event['Type'] == 'BF':
      self.update_str = 'Y' + str(self.cur_year) + '-D' + str(self.cur_day) + \
                        '-BFG' + str(event['Game No'])
    elif event['Type'] == 'VF':
      self.update_str = 'Y' + str(self.cur_year) + '-D' + str(self.cur_day) + \
                        '-VFG' + str(event['Game No'])                            
    elif event['Type'] == 'OS':
      self.update_str = 'Y' + str(self.cur_year) + '-D' + str(self.cur_day) + \
                        '-OS'       
    elif event['Type'] == 'END':
      #VC: Need to check
      pass
    return
    
  #-----------------------------------------------------------------------------
  # Function det_prev_event
  #
  # Reads from Last_Event.txt (if it exists) the last event that happened.
  # 
  # Possiblities of the last event:
  # --> Y# Draft
  # --> Y# FA
  # --> Y# RS G#
  # --> Y# 3PC
  # --> Y# RoSo
  # --> Y# ASG
  # --> Y# AF G# 
  # --> Y# BF G#
  # --> Y# VF G#
  # --> Y# OS
  # --> Y# END
  #-----------------------------------------------------------------------------
  def det_prev_event(self):

    if not os.path.isfile(self.last_event_file):
      self.prev_event = {'Type':'NEW'}
      #VC: May have a custom starting year?
      self.cur_year = STARTING_YEAR
      self.cur_day = 1
      
    else:
      with open(self.last_event_file,'r') as f:
        last_event_list = f.readline().rstrip().split('|')
        self.cur_year = int(last_event_list[0][1:])
        self.cur_day = int(last_event_list[1][1:])
        print (self.cur_day)
        if last_event_list[2] == 'Draft': 
          self.prev_event = {'Type':'Draft'}
        elif last_event_list[2] == 'FA':
          self.prev_event = {'Type':'FA','Day':int(last_event_list[-1][1:])}
        elif last_event_list[2] == 'RS':
          self.prev_event = {'Type':'RS','Game No':int(last_event_list[-1][1:])}
        elif last_event_list[2] == '3PC':
          self.prev_event = {'Type':'3PC'}
        elif last_event_list[2] == 'RoSo':
          self.prev_event = {'Type':'RoSo'}
        elif last_event_list[2] == 'ASG': 
          self.prev_event = {'Type':'AsG'}
        elif last_event_list[2] == 'AF':
          self.prev_event = {'Type':'AF','Game No':int(last_event_list[-1][1:])}
        elif last_event_list[2] == 'BF':
          self.prev_event = {'Type':'BF','Game No':int(last_event_list[-1][1:])}
        elif last_event_list[2] == 'VF':
          self.prev_event = {'Type':'VF','Game No':int(last_event_list[-1][1:])}      
        elif last_event_list[2] == 'OS':
          self.prev_event = {'Type':'OS'}
        elif last_event_list[2] == 'END':
          self.prev_event = {'Type':'END'}
    self.event_to_update_str(self.prev_event)
    return     
       
  #-----------------------------------------------------------------------------
  # Function det_next_event
  #
  # Determines the next event from the previous event.
  #-----------------------------------------------------------------------------        
  def det_next_event(self):        
    if self.prev_event['Type'] == 'NEW':
      self.next_event = {'Type':'Draft','Text':'Y' + str(self.cur_year) + \
                         ' Draft'}
    elif self.prev_event['Type'] == 'Draft':
      self.next_event = {'Type':'FA','Text':'Y' + str(self.cur_year) + \
                         ' Free Agency D1','Day':1}
    elif self.prev_event['Type'] == 'FA':
      if self.prev_event['Day'] == 16:
        self.det_next_RS_game()
      else:
        self.next_event['Day'] += 1
        self.next_event['Text'] = 'Y' + str(self.cur_year) + \
                                   ' Free Agency D' + \
                                   str(self.next_event['Day'])
    elif self.prev_event['Type'] == 'RS':
      if self.prev_event['Game No'] == 80:
        #Placeholder to generate contestants
        self.next_event = {'Type':'3PC','Text':'Y' + str(self.cur_year) + \
                           ' All Star 3-Point Shootout'}
      elif self.prev_event['Game No'] == 120:
        #Placeholder to determine playoff teams
        self.det_next_PO_game()
      else:
        self.det_next_RS_game()
    elif self.prev_event['Type'] == '3PC':
      #Placeholder to generate RoSo rosters
      self.next_event = {'Type':'RoSo','Text':'Y' + str(self.cur_year) + \
                           ' All Star Rookie-Sophomore Game'}
    elif self.prev_event['Type'] == 'RoSo':
      #Placeholder to generate AS rosters
      self.next_event = {'Type':'ASG','Text':'Y' + str(self.cur_year) + \
                           ' All Star Game'}
    elif self.prev_event['Type'] == 'ASG':
      self.det_next_RS_game()    
    elif self.prev_event['Type'] == 'AF':
      self.det_next_PO_game()
      pass
    elif self.prev_event['Type'] == 'BF':
      self.det_next_PO_game()
      pass
    elif self.prev_event['Type'] == 'VF':
      self.det_next_PO_game()
      pass
    elif self.prev_event['Type'] == 'OS':
      self.next_event = {'Type':'END','Text':'Go into Y' + \
                         str(self.cur_year + 1)}
    elif self.prev_event['Type'] == 'END':
      self.next_event = {'Type':'Draft','Text':'Y' + str(self.cur_year) + \
                         ' Draft'} 
    self.prev_event = copy.deepcopy(self.next_event)
    return 
  
  #---------------------------------------------------------------------------
  # Function: det_next_RS_game
  #
  # Operation: Looks at the league results file and determines the number of
  #            the next game.
  #---------------------------------------------------------------------------
  def det_next_RS_game(self):
    if self.prev_event['Type'] == 'FA':
      prev_game = 0
    elif self.prev_event['Type'] == 'ASG':
      prev_game = 80
    else:
      prev_game = self.prev_event['Game No']
    
    year_dir = self.game_dir + os.sep + 'data' + os.sep + 'Year_' + \
               str(self.cur_year)

    with open(self.sch_file,'r') as f:
      for line in f:
        sch_list = line.split()
        if sch_list[0] == str(prev_game + 1):
          home_nick = sch_list[1]
          away_nick = sch_list[2]
          break
    game_no = prev_game + 1      
    self.next_event = {'Type':'RS','Game No':game_no,'Home Nick':home_nick,\
                       'Away Nick':away_nick,'Text':'Y' + str(self.cur_year) + \
                       ' RS G' + str(game_no) + ':' + away_nick + '@' + \
                       home_nick}
    return 

  #---------------------------------------------------------------------------
  #
  #---------------------------------------------------------------------------
  def det_next_PO_game():
      
    return
  
  def run_day(self):
    if self.next_event['Type'] == 'Draft':
      self.run_draft()  
    elif self.next_event['Type'] == 'FA':
      self.run_FA()
    elif self.next_event['Type'] == 'RS':
      self.run_RS_game()
    elif self.next_event['Type'] == '3PC':
      self.run_3PC()
    elif self.next_event['Type'] == 'RoSo':
      self.run_RoSo_game()
    elif self.next_event['Type'] == 'ASG':
      self.run_ASG_game()
    elif self.next_event['Type'] in ('AF','BF'):
      self.run_CF_game()
    elif self.next_event['Type'] == 'VF':
      self.run_VF_game()
    elif self.next_event['Type'] == 'OS':
      self.run_OS()
    elif self.next_event['Type'] == 'END':
      self.new_season()
    with open(self.last_event_file,'w') as f:
      line = 'Y' + str(self.cur_year) + '|D' + str(self.cur_day) + '|' + self.next_event['Type']
      if self.next_event['Type'] in ('RS','AF','BF'):
        line += '|G' + str(self.next_event['Game No'])
      elif self.next_event['Type'] == 'FA':
        line += '|D' + str(self.next_event['Day'])
      f.write(line + '\n') 
    return
  
  def new_season(self):
    return
  
  def run_game(self):
  
    home_obj = self.teams[self.next_event['Home Nick']]
    away_obj = self.teams[self.next_event['Away Nick']]
    match_obj = Match(home_obj,away_obj,self)
    
    match_obj.home.record.update_record(match_obj.away.nickname,True,\
              match_obj.home.game['Stats']['Points'],\
              match_obj.away.game['Stats']['Points'],\
              match_obj.same_conf,match_obj.year)
    match_obj.away.record.update_record(match_obj.home.nickname,False,\
              match_obj.home.game['Stats']['Points'],\
              match_obj.away.game['Stats']['Points'],\
              match_obj.same_conf,match_obj.year)
    match_obj.update_player_stats()
    match_obj.store_player_data()
    match_obj.update_team_stats()
    match_obj.store_team_data()
    match_obj.store_league_data()
    return
    
  def run_RS_game(self):  
    print ('Y' + str(self.cur_year) + ' Regular Season G' + \
           str(self.next_event['Game No']) + ': ' + \
           self.next_event['Away Nick'] + '@' + self.next_event['Home Nick'])
    #self.update_str = 'Y' + str(self.cur_year) + '-D' + str(self.cur_day) + \
    #                  '-RSG' + str(self.next_event['Game No'])
    self.run_game()
    #self.update_league_players_process()
    #self.cur_day += 1
    return

  def run_RoSo_game(self):
    rosters = det_RoSo_rosters(self)
    rook_roster_list = []
    for p in rosters['Rookies']:
      rook_roster_list.append(p)
    rook_team = Team('ROOK',self.game_dir,self.cur_year,'RoSo',rosters['Rookies'])
    
    soph_roster_list = []
    for p in rosters['Sophomores']:
      soph_roster_list.append(p)
    soph_team = Team('SOPH',self.game_dir,self.cur_year,'RoSo',rosters['Sophomores'])  
    starter_info_dict = {'Home':{'Starters':copy.deepcopy(rook_roster_list),\
                                 'On Court':copy.deepcopy(rook_roster_list)},\
                         'Away':{'Starters':copy.deepcopy(soph_roster_list),\
                                 'On Court':copy.deepcopy(soph_roster_list)}\
                        }
    
    RoSo_match = Match(rook_team,soph_team,self,starter_info_dict)
    RoSo_match.store_RoSo_data()
    reply = input("-->")
    return
  
  def det_3PC_draw(self):
    eligible_players = {}
    eligible_threes_made = []
    eligible_three_per = []
    for t in NICKS:
      eligible_players[t] = []
      for p in self.teams[t].players:
        p_stats = self.teams[t].players[p].stats['Y' + str(self.cur_year)]
        if p_stats['3PFGM'] >= p_stats['Team Games'] and p_stats['3PFGM'] >= 10:
          three_fg_per = decimal.Decimal(p_stats['3PFGM']/p_stats['3PFGA']).quantize(THREE_DP)
          eligible_players[t].append((p,p_stats['3PFGM'],three_fg_per))
          eligible_threes_made.append(p_stats['3PFGM'])
          eligible_three_per.append(three_fg_per)          
    
    eligible_threes_made.sort(reverse=True)
    eligible_three_per.sort(reverse=True)
    
    draw = []
    league_standings = self.det_standings('League')
    for t in NICKS:  
      t_candidate = (t,None)
      for p_tuple in eligible_players[t]:
        p = p_tuple[0]
        #print (p_tuple)
        rank_index = eligible_threes_made.index(p_tuple[1]) + \
                     eligible_three_per.index(p_tuple[2])
        if not t_candidate[1]:
          t_candidate = [t,[p],rank_index]
        elif rank_index < t_candidate[2]:
          t_candidate = [t,[p],rank_index]
        elif rank_index == t_candidate[2]:
          t_candidate[1].append(p)
      if len(t_candidate[1]) > 1:
        t_candidate[1] = random.choice(t_candidate[1])
      else:
        t_candidate[1] = t_candidate[1][0]
      if t_candidate[1]:
        t_candidate.append(league_standings.index(t)) 
        draw.append(t_candidate)

    draw.sort(key = lambda x: (x[2],x[3]))
    for i in range(len(draw)):
      draw[i].append(i+1)
    # draw item: (team, player, rank_index, seed)
    
    return (draw)
    
  def run_3PC(self):
    draw = self.det_3PC_draw()
    rounds = 1
    while len(draw) > 2**rounds:
      rounds += 1
    matches = []
    for m in range(2**(rounds-1)):
      if len(draw) >= 2**rounds:
        matches.append([draw[m],draw[2**rounds-m-1]])
      else:
        matches.append([draw[m]])
    with open(self.three_comp_details_file,'w') as details_f: 
      for r in range(rounds,0,-1):
        if r == 3:
          round_str = 'Quarterfinals'
        elif r == 2:
          round_str = 'Semifinals'
        elif r == 1:
          round_str = 'Finals '
        winners = []
        for m in range(2**(r-1)):
          if len(matches[m]) == 1:
            print ('BYE')
            winners.append(matches[m][0])
          else:
            if matches[m][0][-1] > matches[m][1][-1]:
              player_1 = matches[m][0]
              player_2 = matches[m][1]
            else:
              player_1 = matches[m][1]
              player_2 = matches[m][0]
            
            player_1_rating = self.teams[player_1[0]].players[player_1[1]].attributes['3Pt Jumper Eff']
            player_2_rating = self.teams[player_2[0]].players[player_2[1]].attributes['3Pt Jumper Eff']
            title_str = round_str + ' ' + player_1[1] + '(' + str(player_1[-1]) + \
                        ')[' + player_1[0] + '] vs. ' + player_2[1] + '(' + \
                        str(player_2[-1]) + ')[' + player_2[0] + ']'
            print (title_str)
            details_f.write(title_str + '\n') 
            winner = run_3PC_match(player_1[1],player_1[0],player_1_rating,player_2[1],player_2[0],player_2_rating,details_f)
            print ('Winner is ' + winner + '!')
            print ('\n')
            if winner == player_1[1]:
              winners.append(player_1)
            else:
              winners.append(player_2)
        if r > 1:
          matches = []
          for i in range(2**(r-2)):
            matches.append([winners[i],winners[2**(r-1)-i-1]])
           
        else:
          winner_str = 'Winner of the 3PC is ' + winners[0][1] + ' of ' + winners[0][0] + '!'
          print (winner_str)
          details_f.write(winner_str)      
          
    input('YO!')  
    return
    
  def run_ASG_game(self):
    rosters = det_ASG_rosters(self)
    print (rosters)
    alpha_players = {}
    beta_players = {}
    for type in rosters['Alpha']:
      for p in rosters['Alpha'][type]:
        alpha_players[p] = rosters['Alpha'][type][p]
    alpha_team = Team('ALP',self.game_dir,self.cur_year,'ASG',alpha_players)
    
    for type in rosters['Beta']:
      for p in rosters['Beta'][type]:
        beta_players[p] = rosters['Beta'][type][p]
    beta_team = Team('BET',self.game_dir,self.cur_year,'ASG',beta_players)  
    
    standings = self.det_standings('League')
    alpha_starter_info_dict = {'Starters':copy.deepcopy(list(rosters['Alpha']['Starters'].keys())),\
                               'On Court':copy.deepcopy(list(rosters['Alpha']['Starters'].keys())),\
                               'Bench':copy.deepcopy(list(rosters['Alpha']['Bench'].keys())),\
                               'Unavailable':copy.deepcopy(list(rosters['Alpha']['Injured'].keys()))}
    beta_starter_info_dict = {'Starters':copy.deepcopy(list(rosters['Beta']['Starters'].keys())),\
                              'On Court':copy.deepcopy(list(rosters['Beta']['Starters'].keys())),\
                              'Bench':copy.deepcopy(list(rosters['Beta']['Bench'].keys())),\
                              'Unavailable':copy.deepcopy(list(rosters['Beta']['Injured'].keys()))}
    if standings[0] in self.conferences['Alpha']:
      home_obj = alpha_team
      away_obj = beta_team
      starter_info_dict = {'Home':alpha_starter_info_dict,\
                           'Away':beta_starter_info_dict}
    elif standings[0] in self.conferences['Beta']:
      home_obj = beta_team
      away_obj = alpha_team
      starter_info_dict = {'Home':beta_starter_info_dict,\
                           'Away':alpha_starter_info_dict}  

    ASG_match = Match(home_obj,away_obj,self,starter_info_dict)
    ASG_match.store_ASG_data()    
    
    input('-->')
    return
    
  def run_CF_game(self):
    return
    
  def run_VF_game(self):
    return
  
  def gen_draftees(self):
  
    self.draftees = {'C':{},'PF':{},'SF':{},'SG':{},'PG':{}}
    self.drafted = {}
  
    for i in range(TOT_DRAFTEES):
      draftee_pos = F_GEN_VAR_FROM_PROB_DICT(POS_PROB_DICT)
      simp_pos = SIMPLE_POS_DICT[draftee_pos]  
      draftee_name = YEAR_LETTERS[self.cur_year] + POS_TO_NAME_DICT[draftee_pos] + \
                     str(len(self.draftees[simp_pos]) + 1)
      draftee_obj = Player(draftee_name,self.game_dir,self.cur_year,self.cur_year,\
                          draftee_pos,True)
      
      self.draftees[simp_pos][draftee_name] = draftee_obj    
               
    return

  def pick_menu(self,pick_no,team_nick,draft_f):
    def choose_player(pos):
      chosen = False
      while chosen == False:
        reply = input('Enter player name to draft player or "B" to go back: ')\
                .rstrip()
        if reply in self.draftees[pos]:
          chosen = True
          return (reply)
        elif reply in ('B','b'):
          chosen = True
          return (None)
        else:
          print ('***Input invalid, please try again.***')
      return
      
    selected = False
    while selected == False:
      print ("Please choose option:")
      print ("[1] Draft a PG")
      print ("[2] Draft a SG")
      print ("[3] Draft a SF")
      print ("[4] Draft a PF")
      print ("[5] Draft a C")
      print ("[6] View all available players")
      print ("[7] View all drafted players")
      print ("[8] View roster")
      print ("[9] Forfeit pick")
      reply = input("-->").rstrip()
      reply_to_pos_dict = {'1':'PG','2':'SG','3':'SF','4':'PF','5':'C'}
      if reply in ('1','2','3','4','5'):
        pos = reply_to_pos_dict[reply]
        if len(self.draftees[pos]) == 0:
          print ("No available " + pos + "s")
        else:
          F_PRINT_P_GRADES(self.draftees[pos],'Draftees')
          draftee = choose_player(pos)
          if draftee:
            selected = True
            draft_f.write('{:<{l}}'.format(pick_no,l=4) + ' ' + \
                          '{:<{l}}'.format(team_nick,l=4) + ' ' + \
                          draftee + '\n')

            with open(self.draftees[pos][draftee].prev_atts_file,'a') as prev_f:
              prev_f.write(F_GEN_P_ATTS_LINE(self.update_str,\
                                             self.draftees[pos][draftee]) + '\n')              
            self.drafted[pick_no] = {'Name':draftee,'Team':team_nick,\
                                     'Object':self.draftees[pos][draftee]}
            del self.draftees[pos][draftee]
            self.drafted[pick_no]['Object'].profile['Pick No'] = pick_no
            self.drafted[pick_no]['Object'].team_nick = team_nick
            self.drafted[pick_no]['Object'].team_name = NICK_TO_NAME[team_nick]
            self.teams[team_nick].players[draftee] = self.drafted[pick_no]['Object']
            self.players['Active'][pos][draftee] = self.drafted[pick_no]['Object']

            with open(self.transactions_file,'a') as f:
              f.write(team_nick + ' DRAFTED ' + draftee + ' @' + self.update_str + '\n')
            with open(self.teams[team_nick].year_transactions_file,'a') as f:
              f.write('DRAFTED ' + draftee + ' @' + self.update_str + '\n')
            with open(self.players['Active'][pos][draftee].year_transactions_file,'a') as f:
              f.write('DRAFTED by ' + team_nick + ' @' + self.update_str + '\n')
            with open(self.players['Active'][pos][draftee].a_t_transactions_file,'a') as f:
              f.write('DRAFTED by ' + team_nick + ' @' + self.update_str + '\n')    
                        
            with open(self.players['Active'][pos][draftee].atts_file,'w') as cur_f:
              cur_f.write(F_GEN_P_ATTS_TITLE(False) + '\n') 
              cur_f.write(F_GEN_P_ATTS_LINE(None,\
                                         self.players['Active'][pos][draftee]))

      elif reply == '6':
        F_PRINT_P_GRADES(dict(list(self.draftees['C'].items()) + \
                              list(self.draftees['PF'].items()) + \
                              list(self.draftees['SF'].items()) + \
                              list(self.draftees['SG'].items()) + \
                              list(self.draftees['PG'].items()))\
                         ,'Draftees')
      elif reply == '7':
        if len(self.drafted) == 0:
          print ("***No players have been drafted yet!***")
        else:
          F_PRINT_P_GRADES(self.drafted,'Drafted')
        
      elif reply == '8':
        sorted_roster = self.teams[team_nick].generate_roster_list()
        F_PRINT_P_GRADES(self.teams[team_nick].players,True,sorted_roster)  
      elif reply == '9':
        selected = True
        draft_f.write('{:<{l}}'.format(pick_no,l=4) + ' ' + \
                      '{:<{l}}'.format(team_nick,l=4) + ' ' + \
                      'Forfeited\n')
      else:
        print ("***Invalid option entered. Please try again.***" )      
    return
    
  def run_draft(self):

    self.draft_file = self.draft_dir + os.sep + 'Draft.txt'
    draft_f = open(self.draft_file,'w')
    draft_f.write('Pick Team Player\n')
    #self.update_str = 'Y' + str(self.cur_year) + '-D' + str(self.cur_day) + \
    #                  '-Draft'
    
    #Generate schedule
    self.gen_schedule()
    
    #VC: Placeholder to generate draftees
    self.gen_draftees()
    
    #VC: Placeholder to run drafting process
    for r in range(2):
      pick = 1
      for team in self.round_seq:
        print ("ROUND " + str(r+1) + ", " + "PICK " + str(pick) + " - " + \
               team + " on the clock...")
        self.pick_menu(pick+r*8,team,draft_f)
        pick += 1 
    
    for pos in self.draftees:
      if pos not in self.players['FA']:
        self.players['FA'][pos] = {}
      for p in self.draftees[pos]:
        with open(self.draftees[pos][p].prev_atts_file,'a') as prev_f:
          prev_f.write(F_GEN_P_ATTS_LINE(self.update_str,\
                                         self.draftees[pos][p]) + '\n')
        
        self.draftees[pos][p].team_nick = 'FA'
        self.draftees[pos][p].team_name = 'Free Agent'
        self.players['FA'][pos][p] = self.draftees[pos][p]
        with open(self.players['FA'][pos][p].atts_file,'w') as cur_f:
          cur_f.write(F_GEN_P_ATTS_TITLE(False) + '\n') 
          cur_f.write(F_GEN_P_ATTS_LINE(None,\
                                        self.players['FA'][pos][p]))
    self.draftees = None
    draft_f.close()
    
    for t in self.teams:
      self.teams[t].update_roster_file()
    self.update_FA_files()  
    #self.update_league_players_process()
    #self.cur_day += 1
    return
  
  def update_FA_files(self):
    for pos in SIMP_POS_DICTS_IN_DICT:
      with open(self.FA_files[pos],'w') as f:
        for p in self.players['FA'][pos]:
          f.write(p + '\n')      
    return
    
  def run_FA(self):
    team_in_turn = self.round_seq[self.next_event['Day']%8]
    self.FA_menu(team_in_turn)
    '''
    for round in range(2):  
      for team in range(8):
        self.event_to_update_str(self.next_event)
        self.FA_menu(self.round_seq[team])
        #self.update_league_players_process()
        #self.cur_day += 1
    #for t in self.teams:
    #  self.teams[t].update_roster_file()
    #self.update_FA_files()  
    '''
    return

  def update_league_players_process(self):
    if self.next_event['Type'] in ('RS','AF','BF','VF'):
      for t in self.teams:
        if t in (self.next_event['Home Nick'],self.next_event['Away Nick']):
          for p in self.teams[t].players:
            self.teams[t].players[p].update_processes(self.update_str,\
                                                       self.teams[t],True)
        else:
          for p in self.teams[t].players:
            self.teams[t].players[p].update_processes(self.update_str,\
                                                       None,False)                                               
          
    elif self.next_event['Type'] in ('Draft','FA'):
      for p in self.teams[t].players:
        self.teams[t].players[p].update_processes(self.update_str,None,False)

    for pos in self.players['FA']:
      for p in self.players['FA'][pos]:
        self.players['FA'][pos][p].update_processes(self.update_str,\
                                                           None,False)   
    
    return 

  def FA_menu(self,team_nick):
    while 1:
      print ("Choose action for " + team_nick + "(roster size = " + \
             str(len(self.teams[team_nick].players)) + "):")
      print ("[1] View free agents")
      print ("[2] Sign a free agent")
      print ("[3] Propose a trade")
      print ("[4] Release a player")
      print ("[5] View roster")
      print ("[6] Finished")
      reply = input("-->").rstrip()
      if reply == '1':
        F_PRINT_P_GRADES(dict(list(self.players['FA']['C'].items()) + \
                              list(self.players['FA']['PF'].items()) + \
                              list(self.players['FA']['SF'].items()) + \
                              list(self.players['FA']['SG'].items()) + \
                              list(self.players['FA']['PG'].items()))\
                              ,'FA',None,self.teams[team_nick])  
      elif reply == '2':  
        if len(self.teams[team_nick].players) >= MAX_ROSTER_SIZE:
          print (team_nick + "'s roster size is at or larger than the " + \
                 "maximum number of players allowed. Therefore, no " + \
                 "players can be signed.")
        else:  
          while 1:
            print ("Please choose option:")
            print ("[1] View available PGs")
            print ("[2] View available SGs")
            print ("[3] View available SFs")
            print ("[4] View available PFs")
            print ("[5] View available Cs")
            print ("[6] View all available players")            
            print ("[7] Go back")
            reply_2 = input("-->").rstrip()
            reply_to_pos_dict = {'1':'PG','2':'SG','3':'SF','4':'PF','5':'C'}
            if reply_2 in reply_to_pos_dict:
              pos = reply_to_pos_dict[reply_2]
              F_PRINT_P_GRADES(self.players['FA'][pos],'FA',None,self.teams[team_nick])
              while 1:
                signed = False
                player = input('Enter player to sign or "B" to go back:').rstrip()
                if player in self.teams[team_nick].transactions['CUT'] or \
                   player in self.teams[team_nick].transactions['TRADED-AWAY']:
                  print ("***" + player + " has been cut or traded away already this season, therefore is ineligible to be signed***") 
                  break
                elif player in self.players['FA'][pos]:
                    
                  with open(self.players['FA'][pos][player].prev_atts_file,'a') as prev_f:
                    prev_f.write(F_GEN_P_ATTS_LINE(self.update_str,\
                                 self.players['FA'][pos][player]) + '\n')
                  self.players['FA'][pos][player].team_nick = team_nick
                  self.players['FA'][pos][player].team_name = NICK_TO_NAME[team_nick]
                  self.players['Active'][pos][player] = self.players['FA'][pos].pop(player)
                  self.teams[team_nick].players[player] = self.players['Active'][pos][player]
                  self.teams[team_nick].transactions['SIGNED'][player] = \
                    {'When':self.update_str}
                  signed = True
                  self.teams[team_nick].update_roster_file()
                  self.update_FA_files()    
                    
                  with open(self.transactions_file,'a') as f:
                    f.write(team_nick + ' SIGNED ' + player + ' @' + self.update_str + '\n')
                  with open(self.teams[team_nick].year_transactions_file,'a') as f:
                    f.write('SIGNED ' + player + ' @' + self.update_str + '\n')
                  with open(self.players['Active'][pos][player].year_transactions_file,'a') as f:
                    f.write('SIGNED by ' + team_nick + ' @' + self.update_str + '\n')
                  with open(self.players['Active'][pos][player].a_t_transactions_file,'a') as f:
                    f.write('SIGNED by ' + team_nick + ' @' + self.update_str + '\n')
                  with open(self.players['Active'][pos][player].atts_file,'w') as cur_f:
                    cur_f.write(F_GEN_P_ATTS_TITLE(False) + '\n') 
                    cur_f.write(F_GEN_P_ATTS_LINE(None,\
                                self.players['Active'][pos][player]))                                   
                  
                  break
                elif player in ('B','b'):
                  break
                else:
                  print ('***Invalid input, please try again***')              
              if signed == True:
                break
            elif reply_2 == '6':
              F_PRINT_P_GRADES(dict(list(self.players['FA']['C'].items()) + \
                               list(self.players['FA']['PF'].items()) + \
                               list(self.players['FA']['SF'].items()) + \
                               list(self.players['FA']['SG'].items()) + \
                               list(self.players['FA']['PG'].items()))\
                               ,'FA',None,self.teams[team_nick])            
            elif reply_2 == '7':
              break
            else:
              print ("***Invalid option entered. Please try again.***" ) 
      elif reply == '3':
        pass
      elif reply == '4':
        if len(self.teams[team_nick].players) <= MIN_ROSTER_SIZE:
          print (team_nick + "'s roster size is at or smaller than the " + \
                 "minimum number of players allowed. Therefore, no " + \
                 "players can be released.")       
        else:
          sorted_roster = self.teams[team_nick].generate_roster_list()
          F_PRINT_P_GRADES(self.teams[team_nick].players,'Team',sorted_roster)
          while 1:
            player = input('Enter player to release or "B" to go back:').rstrip()
            if player in self.teams[team_nick].players:
              with open(self.teams[team_nick].players[player].prev_atts_file,'a') as prev_f:
                prev_f.write(F_GEN_P_ATTS_LINE(self.update_str,\
                             self.teams[team_nick].players[player]) + '\n')
                    
              pos = SIMPLE_POS_DICT[self.teams[team_nick].players[player].profile['Pos']]
              self.players['FA'][pos][player] = self.teams[team_nick].players.pop(player)
              del self.players['Active'][pos][player]
              self.players['FA'][pos][player].team_nick = 'FA'
              self.players['FA'][pos][player].team_name = 'Free Agent'
              self.teams[team_nick].transactions['CUT'][player] = \
                   {'When':self.update_str}
                
              with open(self.transactions_file,'a') as f:
                f.write(team_nick + ' RELEASED ' + player + ' @' + self.update_str + '\n')
              with open(self.teams[team_nick].year_transactions_file,'a') as f:
                f.write('RELEASED ' + player + ' @' + self.update_str + '\n')
              with open(self.players['FA'][pos][player].year_transactions_file,'a') as f:
                f.write('RELEASED by ' + team_nick + ' @' + self.update_str + '\n')
              with open(self.players['FA'][pos][player].a_t_transactions_file,'a') as f:
                f.write('RELEASED by ' + team_nick + ' @' + self.update_str + '\n')
               
              with open(self.players['FA'][pos][player].atts_file,'w') as cur_f:
                cur_f.write(F_GEN_P_ATTS_TITLE(False) + '\n') 
                cur_f.write(F_GEN_P_ATTS_LINE(None,\
                            self.players['FA'][pos][player]))             
              self.teams[team_nick].update_roster_file()
              self.update_FA_files()  
              break
            elif player in ('B','b'):
              break
            else:
              print ('***Invalid input, please try again***')
      elif reply == '5':
        sorted_roster = self.teams[team_nick].generate_roster_list()
        F_PRINT_P_GRADES(self.teams[team_nick].players,'Team',sorted_roster)
      elif reply == '6':
        if len(self.teams[team_nick].players) < MIN_ROSTER_SIZE:
          print ("Too few players on the roster, please obtain more " + \
                 "players before continuing.")      
        elif len(self.teams[team_nick].players) > MAX_ROSTER_SIZE:
          print ("Too many players on the roster, please reduce the " + \
                 "number of players before continuing.")          
        else:
          break
      else:
        print ('***Invalid input, please try again***')
    return
  
  def run_OS(self):
    return
  
  def league_menu(self):
    while 1:
      print ("Choose league option:")
      print ("[1] Print standings")
      print ("[2] View stats")
      print ("[3] Team management")
      print ("[4] Next event (" + self.next_event['Text'] + ")")
      print ("[5] Save league")
      print ("[6] Exit without saving")
      reply = input("->").rstrip()
      if reply == '1':
        self.print_standings()  
      elif reply == '2':
        player_stats_menu(self)    
      elif reply == '3':
        if self.next_event['Type'] in ('FA','Draft'):
          print ("Not available until after FA period")
        else:
          while 1:
            print ("Choose team:")
            for t in range(8):
              print ("[" + str(t+1) + "] " + NICKS[t])
            print ("[9] Go back")
            reply = input("->").rstrip()
            if reply in ('1','2','3','4','5','6','7','8'):
              self.FA_menu(NICKS[int(reply)-1])
              break
            elif reply == '9':
              break
            else:  
              print ("***You did not choose a valid option, please try again***")
      elif reply == '4':
        break
      elif reply == '5':
        print ("Saving...")
        shutil.rmtree(self.backup_dir)
        shutil.copytree(self.game_dir,self.backup_dir)   
        print ("Save successful!")
      elif reply == '6':
        shutil.rmtree(self.game_dir)
        shutil.copytree(self.backup_dir,self.game_dir)
        shutil.rmtree(self.backup_dir)
        sys.exit()
      else:
        print ("***You did not choose a valid option, please try again***")      
    return

  def print_standing_to_screen(self,title,standings,sep = 2):
    seed = 1
    name_list = ('Seed','Team',' W',' L','  PCT',' GB','Home','Away',\
                 'Pts F','Pts A','Pts D','Conf',' L10','Streak')
    
    line_len = 1
    title_line = '|'
    for item in name_list:
      line_len += len(item) + 1
      if item == name_list[-1]:
        title_line += item + '|'
      else:  
        title_line += item + ' ' 
         
    head_line = '+' + '{:-^{len}}'.format(title + ' Standings',len=line_len-2) + '+'
    print (head_line)
    print (title_line)
    divider_line = '+' + '-'*(line_len - 2) + '+' 
    
    for t in standings:
      t_record = self.teams[t].record.own['Y' + str(self.cur_year)]['All']
      t_conf_record = self.teams[t].record.own['Y' + str(self.cur_year)]['Conf']
      seed_str = '(' + str(seed) + ')'
      wins = t_record['Wins']
      losses = t_record['Losses']
      if wins == 0 and losses == 0:
        win_per_str = '-'
        pts_f_str = '-'
        pts_a_str = '-'
        pts_diff_str = '-'
      else:

        win_per = decimal.Decimal(float(wins)/float(wins+losses)).quantize(THREE_DP)
        if win_per < 1:
          win_per_str = str(win_per)[1:]
        else:
          win_per_str = str(win_per)
        tot_pts_f = float(t_record['Pts F'])
        tot_pts_a = float(t_record['Pts A'])
        pts_f_str = str(decimal.Decimal(float(tot_pts_f)/(wins + losses))\
                                                        .quantize(ONE_DP))
        pts_a_str = str(decimal.Decimal(float(tot_pts_a)/(wins + losses)).\
                                                         quantize(ONE_DP))
        pts_diff_str = str(decimal.Decimal(float(tot_pts_f-tot_pts_a)/\
                                           (wins + losses)).quantize(ONE_DP))
    
      if t == standings[0]:
        GB_str = '-'
        lead_wins = t_record['Wins']
        lead_losses = t_record['Losses']
      else:
        GB = lead_wins - lead_losses -\
             t_record['Wins'] + t_record['Losses']
        if GB == 0:
          GB_str = '0.0'
        else:   
          GB_str = str(decimal.Decimal(float(GB)/2).quantize(ONE_DP))
    
      home_str = str(t_record['H Wins']) + '-' + str(t_record['H Losses'])
      away_str = str(t_record['A Wins']) + '-' + str(t_record['A Losses'])
      

      conf_record_str = str(t_conf_record['Wins']) + '-' +\
                        str(t_conf_record['Losses'])
      
      L10_str = str(sum(t_record['L10'])) + '-' + str(len(t_record['L10']) -\
                                                      sum(t_record['L10']))
    
      if t_record['Streak'] == 0:
        streak_str = '-'
      elif t_record['Streak'] > 0:
        streak_str = 'W' + str(t_record['Streak'])
      else:
        streak_str = 'L' + str(-t_record['Streak'])
      
      #'Pts F','Pts A','Diff','Conf','L10','Streak'
      print_list = ((name_list[0],str(seed_str)),\
                    (name_list[1],t),\
                    (name_list[2],str(wins)),\
                    (name_list[3],str(losses)),\
                    (name_list[4],win_per_str),\
                    (name_list[5],GB_str),\
                    (name_list[6],home_str),\
                    (name_list[7],away_str),\
                    (name_list[8],pts_f_str),\
                    (name_list[9],pts_a_str),\
                    (name_list[10],pts_diff_str),\
                    (name_list[11],conf_record_str),\
                    (name_list[12],L10_str),\
                    (name_list[13],streak_str)\
                   )
      team_line = '|'
      for item in print_list:
        if item == print_list[-1]:
          team_line += '{:>{l}}'.format(item[1],l=len(item[0]))  
        else:
          team_line += '{:>{l}}'.format(item[1],l=len(item[0])) + ' '
      team_line += '|'
      print (team_line)
      if seed == sep:
        
        print (divider_line)
      seed += 1
      
    print (divider_line) 
    return
  
  def print_standings(self):

    alpha_standings = self.det_standings('Alpha')
    beta_standings = self.det_standings('Beta')
    #+---------Alpha Standings---------+
    #|Seed Team  W  L  PCT GB Home Away|
    #| (1)  KEN 15  3 .833  -  8-1  7-2|
    #| (2)  BRE                        |
    #+---------------------------------+
    #| (3)  HAR                        |
    #| (4)  LAT                        |
    #+---------------------------------+
  
    self.print_standing_to_screen('Alpha',alpha_standings,len(alpha_standings)/2)
    self.print_standing_to_screen('Beta',beta_standings,len(beta_standings)/2)
    return
    
  def det_standings(self,t_span):
    year_str = 'Y' + str(self.cur_year)
    standings = []
    
    if t_span in ('Alpha','Beta'):
      team_list = self.conferences[t_span]
    elif t_span == 'League':
      team_list = self.conferences['Alpha'] +  self.conferences['Beta']
    for t in team_list:
      t_record = self.teams[t].record.own[year_str]['All']
      if t_record['Wins'] == 0 and t_record['Losses'] == 0:
        win_per = 0.5
      else:
        win_per = 1.0*t_record['Wins']/(t_record['Wins'] + t_record['Losses'])
      prev_per = 1
      if len(standings) > 0:
        found = False
        for per_set in standings:
          if math.fabs(per_set[0] - win_per) < 1E-6:
            per_set[1].append(t)
            found = True
            break
          elif win_per > per_set[0]:
            standings.insert(standings.index(per_set),(win_per,[t])) 
            found = True
            break
        if found == False:
          standings.append((win_per,[t]))
      else:
        standings.append((win_per,[t]))
        
    #-----------------------------------------------------
    #
    #-----------------------------------------------------
    def break_tie(tied_teams):
      wins_diff_dict = {}
      pts_diff_dict = {}
      rank = []
      print ("VC: tied_teams - " + str(tied_teams))
      for t in tied_teams:    
        wins_diff_dict[t] = 0
        pts_diff_dict[t] = 0
        
        for opp_t in tied_teams:
          
          if opp_t == t:
            continue   
          else:
            h2h_record = self.teams[t].record.h2h[year_str][opp_t] 
            wins_diff_dict[t] += h2h_record['Wins'] - h2h_record['Losses']
            pts_diff_dict[t] += h2h_record['Pts F'] - h2h_record['Pts A']
     
      for t in tied_teams:
        if len(rank) == 0:
          rank.append((t,[t]))
        else:
          for ranked_t in rank:
            if wins_diff_dict[t] > wins_diff_dict[ranked_t[0]]:
              rank.insert(rank.index(ranked_t),(t,[t]))
              break
            elif wins_diff_dict[t] == wins_diff_dict[ranked_t[0]] and \
                 pts_diff_dict[t] > pts_diff_dict[ranked_t[0]]:
              rank.insert(rank.index(ranked_t),(t,[t]))
              break
            elif wins_diff_dict[t] == wins_diff_dict[ranked_t[0]] and \
                 pts_diff_dict[t] == pts_diff_dict[ranked_t[0]]:          
              rank[rank.index(ranked_t)][-1].\
                  insert(random.randrange(len(rank[rank.index(ranked_t)][-1])+1),t)
              break
            elif ranked_t == rank[-1]:
              rank.append((t,[t]))
              break
        final_rank = []
        #print (rank)
        for t_rank in rank:
          #print (team_rank)
          if len(t_rank[-1]) == 1:
            final_rank.append(t_rank[0])
          else:
            for tied_t in sorted(t_rank[-1]):
              final_rank.append(tied_t)
      print ("VC - break_tie: ",final_rank)   
      return (final_rank)
    #-----------------------------------------------------
    
    final_standings = []
  
    for per_set in standings:
      if len(per_set[1]) > 1:
        tied_standings = break_tie(per_set[1])
        for team in tied_standings:
          final_standings.append(team)
      else:
        final_standings.append(per_set[1][0])
  
    return (final_standings)    
  
  def run_league(self):
    running = True
    while running == True:
      self.det_next_event()
      self.league_menu()
      self.event_to_update_str(self.next_event)
      self.run_day()
      self.update_league_players_process()
      self.cur_day += 1
      
   
    return