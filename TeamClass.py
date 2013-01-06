import decimal
import re
import copy
import os
import PlayerClass
from GlobalVariables import *
from GlobalFunctions import *
from RecordClass import *
from PlayerClass import *
def rank_from_ratings(ratings_dict,descending):
  ranked = []
  
  while (len(ratings_dict) > 0): 
    max_rating = ('',-999)
    for player in ratings_dict.keys():
      if ratings_dict[player] > max_rating[1]:
        max_rating = (player,ratings_dict[player])
      elif ratings_dict[player] == max_rating[1] and player < max_rating[0]:
        max_rating = (player,ratings_dict[player])    
    del ratings_dict[max_rating[0]]
    ranked.append(max_rating[0])
    if descending == False:
      ranked.reverse()
  return (ranked)


def print_scoreboard(h_scores,a_scores,h_name="H",a_name="A",max_periods=4):
  
  #SAMPLE SCOREBOARD
  #-------------------------------------------#
  #                                           #
  #  +-----+-----+-----+-----+-----+-------+  #
  #  | VBA | Q 1 | Q 2 | Q 3 | Q 4 | TOTAL |  #
  #  +-----+-----+-----+-----+-----+-------+  #
  #  |  H  | 2 5 | 2 6 | 3 0 | 1 9 | 1 0 0 |  #
  #  +-----+-----+-----+-----+-----+-------+  #
  #  |  A  | 3 1 | 2 2 | 1 2 | 3 2 |  9 7  |  #
  #  +-----+-----+-----+-----+-----+-------+  #
  #                                           #
  #-------------------------------------------#
  h_total = sum(h_scores)
  a_total = sum(a_scores)
  length = 6*(max_periods+1) + 9 
  tot_periods = len(h_scores)
  printed_periods = max_periods
  if (tot_periods > max_periods):
    length += (tot_periods - max_periods)*6
    printed_periods = tot_periods
  if (max_periods == 4):
    prefix = "Q"
  elif (max_periods == 2):
    prefix = "H"
  else:
    prefix = "P"
  
  if (len(h_name) == 1):
    row_h_str = "|  " + h_name + "  |"
  elif (len(h_name) in (3,4)):
    row_h_str = "| " + h_name + " |"
  else:
    row_h_str = "|  H  |"

  if (len(a_name) == 1):
    row_a_str = "|  " + a_name + "  |"
  elif (len(a_name) in (3,4)):
    row_a_str = "| " + a_name + " |"
  else:
    row_a_str = "|  A  |"
  
  if len(a_name) == 4:
    sep_str = "+------+"
    row_1_str = "|  VBA |"
  else:
    sep_str = "+-----+"
    row_1_str = "| VBA |"
  
  for c in range(printed_periods):
    sep_str += "-----+"
    if (c < max_periods): 
      row_1_str += " " + prefix + " " + str(c+1) + " |"
    else:
      row_1_str += " OT" + str(c-max_periods+1) + " |"
    
    if c+1 > len(h_scores):
      row_h_str += "  -  |"
      row_a_str += "  -  |"
    else:
      digit_1_h = int(h_scores[c]/10)
      digit_2_h = h_scores[c]%10
      digit_1_a = int(a_scores[c]/10)
      digit_2_a = a_scores[c]%10
    
      if (digit_1_h == 0):
        row_h_str += "  " + str(digit_2_h) + "  |"
      else:
        row_h_str += " " + str(digit_1_h) + " " + str(digit_2_h) + " |"
      if (digit_1_a == 0):
        row_a_str += "  " + str(digit_2_a) + "  |"
      else:
        row_a_str += " " + str(digit_1_a) + " " + str(digit_2_a) + " |"

  sep_str += "-------+"
  row_1_str += " TOTAL |"

  if (h_total > 99):
    digit_1_h = int(h_total/100)
    digit_2_h = int((h_total-100*digit_1_h)/10)
    digit_3_h = h_total%10
    row_h_str += " " + str(digit_1_h) + " " + str(digit_2_h) + " " + str(digit_3_h) + " |"
  elif (h_total > 9):
    digit_1_h = int(h_total/10)
    digit_2_h = h_total%10
    row_h_str += "  " + str(digit_1_h) + " " + str(digit_2_h) + "  |"
  else:
    row_h_str += "   " + str(h_total) + "   |"
  if (a_total > 99):
    digit_1_a = int(a_total/100)
    digit_2_a = int((a_total-100*digit_1_a)/10)
    digit_3_a = a_total%10
    row_a_str += " " + str(digit_1_a) + " " + str(digit_2_a) + " " + str(digit_3_a) + " |"
  elif (a_total > 9):
    digit_1_a = int(a_total/10)
    digit_2_a = a_total%10
    row_a_str += "  " + str(digit_1_a) + " " + str(digit_2_a) + "  |"
  else:
    row_a_str += "   " + str(a_total) + "   |"
  print (sep_str)
  print (row_1_str)
  print (sep_str)
  print (row_a_str)
  print (sep_str)
  print (row_h_str)
  print (sep_str)  
  return

#---------------------------------------------------------------------------------------------
# class: Team
#
#
#
#---------------------------------------------------------------------------------------------
class Team:
  def __init__(self,nickname,game_dir,cur_year,type='Reg',players=None,init_year=None,conf=None):
    if type == 'Reg':
      self.name = NICK_TO_NAME[nickname]
    elif type == 'RoSo':
      if nickname == 'ROOK':
        self.name = 'Rookies'
      elif nickname == 'SOPH':
        self.name = 'Sophomores'
    elif type == 'ASG':
      if nickname == 'ALP':
        self.name = 'Alpha'
      elif nickname == 'BET':
        self.name = 'Beta'    
    self.nickname = nickname
    
    self.players = {}
    self.cur_year = cur_year
    self.game_dir = game_dir 
    self.player_status = {'Available':[],'Injured':[]}
    
    if type == 'Reg':
      self.init_year = init_year
      self.conf = conf
      self.transactions = {'SIGNED':{},'CUT':{},'TRADED-FOR':{},\
                           'TRADED-AWAY':{}}                      
      self.year_dir = game_dir + os.sep + 'data' + os.sep + 'Year_' +\
                      str(cur_year) + os.sep + 'Teams' + os.sep + self.name
      self.all_time_dir = game_dir + os.sep + 'data' + os.sep + 'All_time' +\
                          os.sep + 'Teams' + os.sep + self.name
    
      self.year_stat_totals_file = self.year_dir + os.sep + 'Stat_totals.txt'
      self.year_team_logs_file = self.year_dir + os.sep + 'Team_logs.txt'
      self.a_t_team_logs_file = self.all_time_dir + os.sep + 'Team_logs.txt'
      self.year_player_logs_file = self.year_dir + os.sep + 'Player_logs.txt'
      self.year_results_file = self.year_dir + os.sep + 'Results.txt'
      self.year_transactions_file = self.year_dir + os.sep + 'Transactions.txt'
      self.year_postgame_log_file = self.year_dir + os.sep + 'Postgame_log.txt'
      #VC: Need to consider roster file containing cut or traded players
      self.roster_file = self.year_dir + os.sep + 'Roster.txt'  
      with open(self.roster_file,'r') as f:
        for line in f:
          #print (line)
          p_list = line.split()
          if len(p_list) > 1:
            last_trans = p_list[-1].split('|')[0]
            if last_trans[0] == 'CUT':
              p = None
              when = last_trans[-1]
              self.transactions['CUT'][p_list[0]] = {'When':when}
              if len(p_list) == 3:
                prev_trans = p_list[-2].split('|')
                when = prev_trans[1]
                if prev_trans[0] == 'TRADED-FOR':
                  where = prev_trans[2]
                  self.transactions['TRADED-FOR'][p_list[0]] = {'When':when,'Where':where}
                elif prev_trans[0] == 'SIGNED':
                  self.transactions['SIGNED'][p_list[0]] = {'When':when}
              pass
            elif last_trans == 'TRADED-AWAY':
              p = None
              when = last_trans[-2]
              where = last_trans[-1]
              self.transactions['TRADED-AWAY'][p_list[0]] = {'When':when}
              if len(p_list) == 3:
                prev_trans = p_list[-2].split('|')
                when = prev_trans[1]
                if prev_trans[0] == 'TRADED-FOR':
                  where = prev_trans[2]
                  self.transactions['TRADED-FOR'][p_list[0]] = {'When':when,'Where':where}
                elif prev_trans[0] == 'SIGNED':
                  self.transactions['SIGNED'][p_list[0]] = {'When':when}
              pass
            elif last_trans == 'TRADED-FOR':
              p = p_list[0]
              when = last_trans[-2]
              where = last_trans[-1]
              self.transactions['TRADED-FOR'][p] = {'When':when,'Where':where}
            elif last_trans == 'SIGNED':
              p = p_list[0]
              when = last_trans[-1]
              self.transactions['SIGNED'][p] = {'When':when}
          elif len(p_list) == 1:
            p = p_list[0]
          else:
            p = None
          if p:
            self.players[p] = Player(p,game_dir,init_year,cur_year)
    
      self.check_player_status()    
    
      self.record = Record(self.init_year,self.cur_year,self.nickname,\
                         self.game_dir)    
    
      self.stats = {}
      self.load_stats()
    elif type in ('RoSo','ASG'):
      self.players = players          
    
    return
  
  def load_stats(self):
    # Load in stats
    for y in range(self.init_year,self.cur_year+1): 
      self.stats['Y' + str(y)] = {'Games':0,'Own':{},'Opp':{}}   
      saved_team_data_file = self.game_dir + os.sep + 'data' + os.sep + 'Year_' +\
                             str(y) + os.sep + 'Teams' + os.sep + self.name + \
                             os.sep + 'Stat_totals.txt'
      if os.path.isfile(saved_team_data_file):
        with open(saved_team_data_file,'r') as f:
          for line in f:
           item = line.rstrip().split('|')
           if item[0] == 'Games':
             self.stats['Y' + str(y)][item[0]] = int(item[1])
           else:
             self.stats['Y' + str(y)][item[0]][item[1]] = int(item[2])
      else:
        print ('***Y' + str(y) + ' stat total file not found!***')
        self.stats['Y' + str(y)] = copy.deepcopy(T_ZERO_SEASON_STATS)
    return
  
  def check_player_status(self):
    self.player_status = {'Available':[],'Injured':[]}
    for p in self.players:
      p_status = self.players[p].status
      if p_status['Days Injured'] > 0:
        self.player_status['Injured'].append(p)
      else:
        self.player_status['Available'].append(p)       
    return
  
  def update_roster_file(self):
    with open(self.roster_file,'w') as f:
      for p in self.players:
        if p in self.transactions['SIGNED']:
          f.write(p + ' SIGNED|' + self.transactions['SIGNED'][p]['When'] + '\n')
        elif p in self.transactions['TRADED-FOR']:
          f.write(p + ' TRADED-FOR|' + \
                  self.transactions['TRADED-FOR'][p]['When'] + '|' + \
                  self.transactions['TRADED-FOR'][p]['Where'] + '\n')
        else:
          f.write(p + '\n')
      for p in self.transactions['CUT']:
        if p in self.transactions['SIGNED']:
          f.write(p + ' SIGNED|' + self.transactions['SIGNED'][p]['When'] + \
                  ' CUT|' + self.transations['CUT'][p]['When'] + '\n')
        elif p in self.transactions['TRADED-FOR']:
          f.write(p + ' TRADED-FOR|' + \
                  self.transactions['TRADED-FOR'][p]['When'] + '|' + \
                  self.transactions['TRADED-FOR'][p]['Where'] + \
                  ' CUT|' + self.transations['CUT'][p]['When'] + '\n') 
        else:
          f.write(p + ' CUT|' + \
                  self.transactions['CUT'][p]['When'] + '\n')
      for p in self.transactions['TRADED-AWAY']:
        if p in self.transactions['SIGNED']:
          f.write(p + ' SIGNED|' + self.transactions['SIGNED'][p]['When'] + \
                  ' TRADED-AWAY|' + \
                  self.transactions['TRADED-AWAY'][p]['When'] + '|' + \
                  self.transactions['TRADED-AWAY'][p]['Where'] + '\n')
        
        elif p in self.transactions['TRADED-FOR']:
          f.write(p + ' TRADED-FOR|' + \
                  self.transactions['TRADED-FOR'][p]['When'] + '|' + \
                  self.transactions['TRADED-FOR'][p]['Where'] + \
                  ' TRADED-AWAY|' + \
                  self.transactions['TRADED-AWAY'][p]['When'] + '|' + \
                  self.transactions['TRADED-AWAY'][p]['Where'] + '\n') 
        else:
          f.write(p + ' TRADED-AWAY|' + \
                  self.transactions['TRADED-AWAY'][p]['When'] + '|' + \
                  self.transactions['TRADED-AWAY'][p]['Where'] + '\n')
    return
    
  def game_initialisation(self,opp_nickname,game_type,game_no,home):
    self.game = {'Starters':[],'Bench':[],'On Court':[],'Avail Subs':[],\
                 'Unavailable':[],'Fouled Out':[],'Timeouts':8,\
                 'Stats':copy.deepcopy(T_ZERO_GAME_STATS),\
                 'Opp Nick':opp_nickname,'Game Type':game_type,\
                 'Game No':game_no,'Home':home,'Period Scores':[],\
                 'Subs':{'In':[],'Out':[]},\
                 'Misc Stats':copy.deepcopy(T_ZERO_MISC_GAME_STATS)}
    for p in self.players:
      #print (p,str(self.players))    
      self.players[p].game_initialisation()
      self.players[p].game_initialisation()
    return
      
  def generate_roster_list(self):
    roster = {}
    for name in self.players:
      pos = POS_TO_NUMBER_DICT[self.players[name].profile['Pos']]
      if pos not in roster.keys():
        roster[pos] = [name,]
      else:
        roster[pos].append(name)
      
      sorted_pos = sorted(roster.keys())
      #sorted_pos.reverse()
      final_list = []
      for pos in sorted_pos:
        roster[pos].sort()
        for player in roster[pos]:
          final_list.append(player)
    return (final_list)
  
  def print_player_grades(self,player_list=False,show_status=False,show_temp=False):
    # If no list of players given, list whole roster
    if player_list == False:
      player_list = self.generate_roster_list()
      
    # List of attributes to print  
    atts_to_print = ('Inside Prop','2Pt Jumper Prop','3Pt Jumper Prop',\
                     'Inside Eff','2Pt Jumper Eff','3Pt Jumper Eff',   \
                     'Off Reb','Def Reb','Ball Dom','Pass Rate',\
                     'Pass Eff','Inside Def','Perimeter Def',\
                     'Inside Foul Rate','Per Foul Rate','FT Eff')
    
    
    line = '{:<17}'.format('Player')
    for player in player_list:
      line += '{:^5}'.format(player)
    print (line)
    
    for att in atts_to_print:
      line = '{:<17}'.format(att)
      for player in player_list:
        # Temp for adjusted atts (from home court adv etc.), for debugging!
        if show_temp == False:
          init_format = '{:^3}'.format(self.players[player].grades[att])
        else:
          init_format = '{:>3}'.format(self.players[player].game_attributes[att])
        line += '{:^5}'.format(init_format)
      print (line)
    
    if show_status == True:

      line = '{:<17}'.format('Days Injured')
      for player in player_list:
        init_format = '{:^3}'.format(self.players[player].status['Days Injured'])
        line += '{:^5}'.format(init_format)
      print (line)    
  
  def print_player_atts(self,player_list=False,show_status=False,show_temp=False):
    # If no list of players given, list whole roster
    if player_list == False:
      player_list = self.generate_roster_list()
      
    # List of attributes to print  
    atts_to_print = ('Inside Prop','2Pt Jumper Prop','3Pt Jumper Prop',\
                     'Inside Eff','2Pt Jumper Eff','3Pt Jumper Eff',   \
                     'Off Reb','Def Reb','Ball Dom','Pass Rate',\
                     'Pass Eff','Inside Def','Perimeter Def',\
                     'Inside Foul Rate','Per Foul Rate','FT Eff')
    
    
    line = '{:<17}'.format('Player')
    for player in player_list:
      line += '{:^5}'.format(player)
    print (line)
    
    for att in atts_to_print:
      line = '{:<17}'.format(att)
      for player in player_list:
        # Temp for adjusted atts (from home court adv etc.), for debugging!
        if show_temp == False:
          init_format = '{:>3}'.format(self.players[player].attributes[att])
        else:
          init_format = '{:>3}'.format(self.players[player].game_attributes[att])
        line += '{:^5}'.format(init_format)
      print (line)
    
    if show_status == True:
    
      line = '{:<17}'.format('Days Injured')
      for player in player_list:
        init_format = '{:>3}'.format(self.players[player].status['Days Injured'])
        line += '{:^5}'.format(init_format)
      print (line)    
  
  def print_roster_user(self):
   
    sorted_roster = self.generate_roster_list()
    #print (sorted_roster)
    
    roster_size = len(self.players)
    total_str_len = 17 + roster_size*5
    centre_text = ' Roster of ' + self.name + ' '
    line = '{:*^{len}}'.format(centre_text,len=total_str_len)
    print (line)   
    #self.print_player_grades(sorted_roster,True)
    F_PRINT_P_GRADES(self.players,'Team',sorted_roster,None)
    print ('*'*total_str_len)
    
    return
   
  #-----------------------------------------
  # Function that handles timeouts
  #-----------------------------------------
  def timeout(self,opp_team,PBP_history,time_dict,misc_stats_dict,home_TO):
    orig_on_court = copy.deepcopy(self.game['On Court'])
    if home_TO == True:
      h_team = self
      a_team = opp_team
    elif home_TO == False:
      h_team = opp_team
      a_team = self
    elif not home_TO:
      h_team = self
      a_team = opp_team
      
    TO_complete = False
    while TO_complete == False:
      TO_option_chosen = False
      print ('Team manager for ' + self.name + '. Options:')
      print ('[1] View game overview')
      print ('[2] View basic boxscore')
      print ('[3] View advanced boxscore')
      print ('[4] View roster')
      print ('[5] Make a substitution')
      print ('[6] View play-by-play')
      print ('[7] Exit team manager')
      while TO_option_chosen == False:
        reply = input('Please enter a option number' + \
                      '(enter "O" to view options again):')
        reply = reply.rstrip()
        if reply == '7':
          TO_complete = True
          TO_option_chosen = True
        
        elif reply == '6':
          TO_option_chosen = True
          for line in PBP_history:
            print(line)
          
        elif reply == '5':
          TO_option_chosen = True
          all_subs_made = False
          
          while all_subs_made == False:
            sub_made = False
            print ('{:-^42}'.format('Players On Court'))
            #self.print_player_grades(self.game['On Court'])            
            F_PRINT_P_GRADES(self.game['On Court'],'TO',None,self)
            while sub_made == False:

              sub_out = False
              while sub_out == False:
                reply_2 = input('Who would you like to sub out ' + \
                                '(Enter "Cancel" to cancel, or "Players" to ' +\
                                'view players on court.)? ')
                reply_2 = reply_2.rstrip()
                if reply_2 in ['Cancel','C','cancel']:
                  sub_made = True
                  all_subs_made = True
                  sub_out = True
                  print ('You have not made any substitutions')
                elif reply_2 in self.game['On Court']:
                  avail_no = len(self.game['Avail Subs'])
                  total_str_len = 17 + avail_no*5
                  sub_out = True
                  player_subbed_out = reply_2
                  sub_in = False
                  while sub_in == False:
                    print ('{:-^{len}}'.format('Available Substitutes',\
                           len=total_str_len))
                    #self.print_player_grades(self.game['Avail Subs'])
                    F_PRINT_P_GRADES(self.game['Avail Subs'],'TO',None,self)
                    reply_3 = input('Who would you like to sub in ' +\
                                    '(Enter "Cancel" to cancel, or "Players" to ' +\
                                    'view available substitutes.)? ')
                    reply_3 = reply_3.rstrip()
                    
                    if reply_3 in self.game['Avail Subs']:
                      player_subbed_in = reply_3
                      print ('You have subbed in ' + player_subbed_out + ' for ' +\
                              player_subbed_in)
                      sub_in = True
                      another_sub_reply = False
                      self.game['On Court'].remove(player_subbed_out)
                      self.game['On Court'].append(player_subbed_in)
                      self.game['Avail Subs'].remove(player_subbed_in)
                      self.game['Avail Subs'].append(player_subbed_out)
                      self.players[player_subbed_out].game['Court Status'] = 0
                      self.players[player_subbed_in].game['Court Status'] = 1
                      
                      while another_sub_reply == False:
                        reply_4 = input('Would you like to make another ' + \
                                        'substitution(Y|N)? ')
                        reply_4 = reply_4.rstrip()
                        if reply_4 in ['Y','y','Yes','yes']:
                          another_sub_reply = True
                          sub_made = True
                        elif reply_4 in ['N','n','No','no']:
                          another_sub_reply = True
                          all_subs_made = True
                          sub_made = True 
                        else:
                          print ('***Invalid response***')
                          
                    elif reply_3 in ['Cancel','C','cancel']:
                      sub_out = True
                      sub_made = True
                      sub_in = True  
                      print ('You have not made a substitution')
                    else:
                      print ('***You have not enetered a player.***')
                elif reply_2 in ['Players','players','P']:
                  sub_made = True
                  sub_out = True                                  
                else:
                  print ('***You have not entered a player.***') 
        
        elif reply == '1':
          self.print_overview_to_screen(opp_team,home_TO,time_dict,\
                                        misc_stats_dict)
          reply_2 = input('Press ENTER to return to timeout menu:')                                        
          TO_option_chosen = True
        
        elif reply == '2':
          a_team.print_boxscore_to_screen(basic=True)
          h_team.print_boxscore_to_screen(basic=True)
          reply_2 = input('Press ENTER to return to timeout menu:')
          TO_option_chosen = True        
        
        elif reply == '3':
          a_team.print_boxscore_to_screen(basic=False)
          h_team.print_boxscore_to_screen(basic=False)                     
          reply_2 = input('Press ENTER to return to timeout menu:')
          TO_option_chosen = True
        
        elif reply == '4':
          a_team.print_roster_user()
          h_team.print_roster_user()
          reply_2 = input('Press ENTER to return to timeout menu:')
          TO_option_chosen = True
        
        elif reply in ['O','o','0']:
          TO_option_chosen = True
        
        else:
          print ("***You did not enter a valid option, please try again.***")
    
    #--------------------------------------------------------------------------
    # Check whether subs have been made
    #--------------------------------------------------------------------------
    for player in orig_on_court:
      if player not in self.game['On Court']:
        self.game['Subs']['Out'].append(player)
    for player in self.game['On Court']:
      if player not in orig_on_court:
        self.game['Subs']['In'].append(player)
    return
  
  #-------------------------------------------------------------------------------------------
  # function print_basic_stats
  #
  # Prints out the basic boxscore
  # 
  # team        -
  # title       -
  # player_list -
  #-------------------------------------------------------------------------------------------
  def print_basic_stats(self,title_list,player_list=None,team=False):

    top_list_str = title_list
    name_len = len(title_list[0])
    line_len = name_len
    for thing in top_list_str[1:]:
      line_len += len(thing) + 1
                    
    if team == False:
      for player in player_list:
        stats = self.players[player].game['Stats']
        line = '|'
      
        name_str = player
        if self.players[player].game['Court Status'] == -2:
          line_string = '{:<{len}}'.format(name_str,len=name_len)
          line_string += ' Unavailable - Injured'
          line_string = '{:<{len}}'.format(line_string,len=line_len)
          line += line_string + '|'
          print (line)
          continue
          
        if self.players[player].game['Court Status'] == 1:
          name_str += '*'
        line += '{:<{len}}'.format(name_str,len=name_len)
        line += ' '
        #print ("VC TEST",player,self.players[player].stats['Court Time'])
        min = str(int(stats['Court Time']/60))
        sec = stats['Court Time']%60
        if sec < 10:
          sec = "0" + str(sec)
        else:
          sec = str(sec)        
        min_str = min + ':' + sec
        line += '{:>{len}}'.format(min_str,len=len(top_list_str[1]))
        line += ' '
           
        fg_str = str(stats['FGM']) + '-' + str(stats['FGA'])
        line += '{:>{len}}'.format(fg_str,len=len(top_list_str[2]))
        line += ' '
      
        three_str = str(stats['3PFGM']) + '-' + str(stats['3PFGA'])
        line += '{:>{len}}'.format(three_str,len=len(top_list_str[3]))
        line += ' '
        
        ft_str = str(stats['FTM']) + '-' + str(stats['FTA'])
        line += '{:>{len}}'.format(ft_str,len=len(top_list_str[4]))       
        line += ' '
        
        if stats['+/-'] > 0:
          p_m_str = '+'
        else:
          p_m_str = ''
        p_m_str += str(stats['+/-'])
        line += '{:>{len}}'.format(p_m_str,len=len(top_list_str[5]))          
        line += ' '
        
        line += '{:>{len}}'.format(stats['Off Reb'],len=len(top_list_str[6]))  
        line += ' '           
                                  
        line += '{:>{len}}'.format(stats['Tot Reb'],len=len(top_list_str[7]))                                   
        line += ' '
        
        line += '{:>{len}}'.format(stats['Assists'],len=len(top_list_str[8]))
        line += ' '
        
        line += '{:>{len}}'.format(stats['Fouls'],len=len(top_list_str[9]))
        line += ' ' 
         
        line += '{:>{len}}'.format(stats['Points'],len=len(top_list_str[10]))  
        line += '|'
        print (line)  
    elif team == True:
      t_stats = self.game['Stats']
      line = '|'
      line += '{:<{len}}'.format('Team',len=len(top_list_str[0]))
      line += ' '
      line += ' '*len(top_list_str[1])
      line += ' '
      fg_str = str(t_stats['FGM']) + '-' + str(t_stats['FGA'])       
      line += '{:>{len}}'.format(fg_str,len=len(top_list_str[2]))
      line += ' '
      three_str = str(t_stats['3PFGM']) + '-' + str(t_stats['3PFGA'])      
      line += '{:>{len}}'.format(three_str,len=len(top_list_str[3]))
      line += ' '
      ft_str = str(t_stats['FTM']) + '-' + str(t_stats['FTA'])      
      line += '{:>{len}}'.format(ft_str,len=len(top_list_str[4]))
      line += ' '
      line += ' '*len(top_list_str[5])
      line += ' '
      line += '{:>{len}}'.format(t_stats['Off Reb'],len=len(top_list_str[6]))
      line += ' '
      line += '{:>{len}}'.format(t_stats['Tot Reb'],len=len(top_list_str[7]))
      line += ' '
      line += '{:>{len}}'.format(t_stats['Assists'],len=len(top_list_str[8]))
      line += ' '
      line += '{:>{len}}'.format(t_stats['Fouls'],len=len(top_list_str[9]))
      line += ' '
      line += '{:>{len}}'.format(t_stats['Points'],len=len(top_list_str[10]))
      line += '|'
      print (line)
      
      line = '|'
      line += '{:<{len}}'.format('%',len=len(top_list_str[0]))
      line += ' '
      line += ' '*len(top_list_str[1])
      line += ' '

      if t_stats['FGA'] == 0:
        fg_str = 'N/A'
      elif t_stats['FGM'] == t_stats['FGA']:
        fg_str = '1.000'
      else:    
        fg_str = str(decimal.Decimal(float(t_stats['FGM'])/\
                     t_stats['FGA']).quantize(THREE_DP))[1:]      
      line += '{:>{len}}'.format(fg_str,len=len(top_list_str[2]))
      line += ' '  
      
      if t_stats['3PFGA'] == 0:
        fg_str = 'N/A'      
      elif t_stats['3PFGM'] == t_stats['3PFGA']:
        fg_str = '1.000'
      else:          
        fg_str = str(decimal.Decimal(float(t_stats['3PFGM'])/\
                     t_stats['3PFGA']).quantize(THREE_DP))[1:]      
      line += '{:>{len}}'.format(fg_str,len=len(top_list_str[3]))
      line += ' '  

      if t_stats['FTA'] == 0:
        fg_str = 'N/A'      
      elif t_stats['FTM'] == t_stats['FTA']:
        fg_str = '1.000'
      else:          
        fg_str = str(decimal.Decimal(float(t_stats['FTM'])/\
                     t_stats['FTA']).quantize(THREE_DP))[1:]      
      line += '{:>{len}}'.format(fg_str,len=len(top_list_str[4]))
      line += ' '              
      line += ' '*len(top_list_str[5])
      line += ' '
      line += ' '*len(top_list_str[6])
      line += ' '
      line += ' '*len(top_list_str[7])
      line += ' '
      line += ' '*len(top_list_str[8])
      line += ' '
      line += ' '*len(top_list_str[9])
      line += ' '
      line += ' '*len(top_list_str[10])
      line += '|' 
      print (line)    
    return
  
  def print_adv_stats(self,title_list,player_list=None,team=False):
    top_list_str = title_list
    name_len = len(title_list[0])
    line_len = name_len
    for thing in top_list_str[1:]:
      line_len += len(thing) + 1
                      
    if team == False:
      for player in player_list:
        stats = self.players[player].game['Stats']
        line = '|'
      
        name_str = player
        if self.players[player].game['Court Status'] == -2:
          line_string = '{:<{len}}'.format(name_str,len=name_len)  
          line_string += ' Unavailable - Injured'
            
          line_string = '{:<{len}}'.format(line_string,len=line_len)
          line = line + line_string + '|'
          print (line)
          continue      
      
        if self.players[player].game['Court Status'] == 1:
          name_str += '*'
        line += '{:<{len}}'.format(name_str,len=len(top_list_str[0]))
        line += ' '
        
        pb_str = str(stats['Put Backs M']) + '-' + str(stats['Put Backs A'])
        line += '{:>{len}}'.format(pb_str,len=len(top_list_str[1]))
        line += ' '
           
        ifg_str = str(stats['Inside FGM']) + '-' + str(stats['Inside FGA'])
        line += '{:>{len}}'.format(ifg_str,len=len(top_list_str[2]))
        line += ' '
      
        jfg_str = str(stats['2PJFGM']) + '-' + str(stats['2PJFGA'])
        line += '{:>{len}}'.format(jfg_str,len=len(top_list_str[3]))
        line += ' '
        
        line += '{:>{len}}'.format(stats['Inside Pts'],len=len(top_list_str[4]))  
        line += ' '           
                                  
        line += '{:>{len}}'.format(stats['Perimeter Pts'],len=len(top_list_str[5]))
        line += ' '
        
        line += '{:>{len}}'.format(stats['2nd Chance Pts'],len=len(top_list_str[6]))
        line += ' '
        
        line += '{:>{len}}'.format(stats['Touches'],len=len(top_list_str[7]))
        line += ' ' 
         
        line += '{:>{len}}'.format(stats['Passes'],len=len(top_list_str[8]))  
        line += ' '                                     
        
        line += '{:>{len}}'.format(stats['Inside Fouls Drawn'],len=len(top_list_str[9])) 
        line += ' '   
  
        line += '{:>{len}}'.format(stats['Per Fouls Drawn'],len=len(top_list_str[10]))                                                                           
        line += '|'
        print (line)  
    elif team == True:
      t_stats = self.game['Stats']
      line = '|'
      line += '{:<{len}}'.format('Team',len=len(top_list_str[0]))
      line += ' '
      
      pb_str = str(t_stats['Put Backs M']) + '-' + str(t_stats['Put Backs A'])
      line += '{:>{len}}'.format(pb_str,len=len(top_list_str[1]))
      line += ' '
      
      ifg_str = str(t_stats['Inside FGM']) + '-' + str(t_stats['Inside FGA'])       
      line += '{:>{len}}'.format(ifg_str,len=len(top_list_str[2]))
      line += ' '
      
      jfg_str = str(t_stats['2PJFGM']) + '-' + str(t_stats['2PJFGA'])      
      line += '{:>{len}}'.format(jfg_str,len=len(top_list_str[3]))
      line += ' '
      
      line += '{:>{len}}'.format(t_stats['Inside Pts'],len=len(top_list_str[4]))
      line += ' '
      line += '{:>{len}}'.format(t_stats['Perimeter Pts'],len=len(top_list_str[5]))
      line += ' '
      line += '{:>{len}}'.format(t_stats['2nd Chance Pts'],len=len(top_list_str[6]))
      line += ' '
      line += '{:>{len}}'.format(t_stats['Touches'],len=len(top_list_str[7]))
      line += ' '
      line += '{:>{len}}'.format(t_stats['Passes'],len=len(top_list_str[8]))
      line += ' '
      line += '{:>{len}}'.format(t_stats['Inside Fouls Drawn'],len=len(top_list_str[9]))
      line += ' '
      line += '{:>{len}}'.format(t_stats['Per Fouls Drawn'],len=len(top_list_str[10]))      
      line += '|'
      print (line)
      
      line = '|'
      line += '{:<{len}}'.format('%',len=len(top_list_str[0]))
      line += ' '

      if t_stats['Put Backs A'] == 0:
        pb_str = 'N/A'
      elif t_stats['Put Backs M'] == t_stats['Put Backs A']:
        pb_str = '1.000'
      else:         
        pb_str = str(decimal.Decimal(float(t_stats['Put Backs M'])/\
                     t_stats['Put Backs A']).quantize(THREE_DP))[1:]      
      line += '{:>{len}}'.format(pb_str,len=len(top_list_str[1]))
      line += ' '  

      if t_stats['Inside FGA'] == 0:
        ifg_str = 'N/A'
      elif t_stats['Inside FGM'] == t_stats['Inside FGA']:
        ifg_str = '1.000'
      else:         
        ifg_str = str(decimal.Decimal(float(t_stats['Inside FGM'])/\
                      t_stats['Inside FGA']).quantize(THREE_DP))[1:]      
      line += '{:>{len}}'.format(ifg_str,len=len(top_list_str[2]))
      line += ' '  
      
      if t_stats['2PJFGA'] == 0:
        jfg_str = 'N/A'      
      elif t_stats['2PJFGM'] == t_stats['2PJFGA']:
        jfg_str = '1.000'
      else:         
        jfg_str = str(decimal.Decimal(float(t_stats['2PJFGM'])/\
                      t_stats['2PJFGA']).quantize(THREE_DP))[1:]      
      line += '{:>{len}}'.format(jfg_str,len=len(top_list_str[3]))
      line += ' '  

      line += ' '*len(top_list_str[4])
      line += ' '   
      line += ' '*len(top_list_str[5])
      line += ' '              
      line += ' '*len(top_list_str[6])
      line += ' '
      line += ' '*len(top_list_str[7])
      line += ' '
      line += ' '*len(top_list_str[8])
      line += ' '
      line += ' '*len(top_list_str[9])
      line += ' '
      line += ' '*len(top_list_str[10])
      line += '|' 
      print (line)     
    return
    
  #---------------------------------------------
  # Function that prints out boxscore to screen
  #---------------------------------------------
  def print_boxscore_to_screen(self,basic=True):
         
    #---------------------------------------------------------
    #-Rays *Min* *FGS* *3Pt* *FTS* *+/-* ORb TRb Ast Fls Pts- 
    #---------------------------------------------------------
    #-Ea6*  
    #-Fa3*
    #-Ge7*
    #-Dj3
    #-Ig2*
    #----------------------------------------------------------
    #-
    #-
    #-
    #-
    #-
    #-
    #-
    #----------------------------------------------------------
    #-Tot
    #-  %
    #----------------------------------------------------------

    #---------------------------------------------------------
    #-Rays InsFG 2PJFG IPts PPts 2CPt Tchs Pass IFD PFD - 
    #---------------------------------------------------------
    #-Ea6*  
    #-Fa3*
    #-Ge7*
    #-Dj3
    #-Ig2*
    #----------------------------------------------------------
    #-
    #-
    #-
    #-
    #-
    #-
    #-
    #----------------------------------------------------------
    #-Tot
    #-  %
    #----------------------------------------------------------
    
    # Ranking the starters by minutes played
    min_dict = {}
    for p in self.game['Starters']:
      min_dict[p] = self.players[p].game['Stats']['Court Time']
    starters_min_rank = rank_from_ratings(min_dict,descending = True)

    # Ranking the bench players by minutes played
    min_dict = {}
    for p in self.game['Bench']:
      min_dict[p] = self.players[p].game['Stats']['Court Time']
    bench_min_rank = rank_from_ratings(min_dict,descending = True)
    
    # For all the unavailable players
    min_dict = {}
    for p in self.game['Unavailable']:
      min_dict[p] = self.players[p].game['Stats']['Court Time']
    unavail_rank = rank_from_ratings(min_dict,descending = True)
    
    name_len = 10    
    if basic == True:
      top_list_str = ["{:<{len}}".format(self.name,len=name_len),"  Min", "   FGS", "  3Pt", "  FTS", "+/-", \
                      "ORb", "TRb", "Ast", "Fls", "Pts"]
    elif basic == False:
      top_list_str = ["{:<{len}}".format(self.name,len=name_len),"PBacks","InsFG", "2PJFG","IPts","PPts","2CPt","Tchs",\
                      "Pass","IFD","PFD"]
      
    tot_bound_len = 1
      
    title_line = "|" 
    for i in range(len(top_list_str)):
      tot_bound_len += len(top_list_str[i]) + 1
      if i == len(top_list_str) - 1:
        title_line += top_list_str[i]
      else:
        title_line += (top_list_str[i] + " ")
    title_line += "|"
    divider_line = '+' + '-'*(tot_bound_len-2) + '+'      
    
    # Printing the boxscore
    print (divider_line)
    print (title_line)
    print (divider_line)
    if basic == True:
      self.print_basic_stats(top_list_str,player_list=starters_min_rank)                                                                             
    elif basic == False:
      self.print_adv_stats(top_list_str,player_list=starters_min_rank) 
    print (divider_line)
    if basic == True:
      self.print_basic_stats(top_list_str,player_list=bench_min_rank)  
      self.print_basic_stats(top_list_str,player_list=unavail_rank)                                      
    elif basic == False:
      self.print_adv_stats(top_list_str,player_list=bench_min_rank)
      self.print_adv_stats(top_list_str,player_list=unavail_rank)  
    print (divider_line)     
    if basic == True:
      self.print_basic_stats(top_list_str,team=True) 
    elif basic == False:
      self.print_adv_stats(top_list_str,team=True) 
    print (divider_line)
            
    return
  
  #----------------------------------------------------------------------------
  # Function to print overview to screen
  #----------------------------------------------------------------------------
  def print_overview_to_screen(self,opp_team,home_TO,time_dict,\
                               misc_stats_dict): 
    #------------------------------------------------------------------
    # ****************Game overview: Kendal @ Rays****************
    #
    #
    #
    if home_TO == True:
      h_period_scores = self.game['Period Scores']
      a_period_scores = opp_team.game['Period Scores']
      home_name = self.name
      away_name = opp_team.name
      home_nick = self.nickname
      away_nick = opp_team.nickname
      home_stats = self.game['Stats']
      away_stats = opp_team.game['Stats']
      home_misc_stats = self.game['Misc Stats']
      away_misc_stats = opp_team.game['Misc Stats']
    elif home_TO == False:
      h_period_scores = opp_team.game['Period Scores']
      a_period_scores = self.game['Period Scores']    
      home_name = opp_team.name
      away_name = self.name
      home_nick = opp_team.nickname
      away_nick = self.nickname      
      home_stats = opp_team.game['Stats']
      away_stats = self.game['Stats']
      away_misc_stats = self.game['Misc Stats']
      home_misc_stats = opp_team.game['Misc Stats']
    elif not home_TO:
      h_period_scores = self.game['Period Scores']
      a_period_scores = opp_team.game['Period Scores']
      home_name = self.name
      away_name = opp_team.name
      home_nick = self.nickname
      away_nick = opp_team.nickname
      home_stats = self.game['Stats']
      away_stats = opp_team.game['Stats']
      home_misc_stats = self.game['Misc Stats']
      away_misc_stats = opp_team.game['Misc Stats']
    title_str = "***Game overview: " + away_name + " @ " + home_name + "***"
    min_str = str(int(time_dict['Time Remaining']/60))
    sec_str = time_dict['Time Remaining']%60
    if sec_str < 10:
      sec_str = "0" + str(sec_str)
    else:
      sec_str = str(sec_str)
    time_str = min_str + ":" + sec_str
    
    if time_dict['Period'] <= time_dict['Tot Period']:
      time_status_str = time_str + " remaining, period " + str(time_dict['Period']) +\
                        " out of " + str(time_dict['Tot Period'])
    else:
      time_status_str = time_str + " remaining, overtime no. " + str(time_dict['Period'] -\
                        time_dict['Tot Period'])
    name_len = 16
    mid_len = 11                  
    
    dividing_line_str = "+" + "-"*name_len + "+" + "-"*mid_len + "|" + \
                       "-"*name_len + "+"
    
    stats_title_str = "|" + '{:^{len}}'.format(away_name,len=name_len) + "|" +\
                      '{:^{len}}'.format("@",len=mid_len) + "|" +\
                      '{:^{len}}'.format(home_name,len=name_len) + "|"
    
    if away_stats['FGA'] == 0:
      a_fg_per_str = 'N/A'
    elif away_stats['FGM'] == away_stats['FGA']:
      a_fg_per_str = '100.0'
    else:  
      ONE_DP = decimal.Decimal(10) ** -1        
      a_fg_per_str = str(decimal.Decimal(float(away_stats['FGM'])/away_stats['FGA']*100).quantize(ONE_DP))      
    a_fg_str = str(away_stats['FGM']) + "-" + str(away_stats['FGA']) + " (" + a_fg_per_str + "%)"
    
    if home_stats['FGA'] == 0:
      h_fg_per_str = "N/A"
    elif home_stats['FGM'] == home_stats['FGA']:
      h_fg_per_str = '100.0'
    else:
      ONE_DP = decimal.Decimal(10) ** -1        
      h_fg_per_str = str(decimal.Decimal(float(home_stats['FGM'])/home_stats['FGA']*100).quantize(ONE_DP))      
    h_fg_str = str(home_stats['FGM']) + "-" + str(home_stats['FGA']) + " (" + h_fg_per_str + "%)"      
    
    fg_line = "|" + '{:^{len}}'.format(a_fg_str,len=name_len) + "|" + \
              '{:^{len}}'.format('FGs (%)',len=mid_len) + "|" +\
              '{:^{len}}'.format(h_fg_str,len=name_len) + "|"
    
    if away_stats['3PFGA'] == 0:
      a_thrfg_per_str = 'N/A'
    elif away_stats['3PFGM'] == away_stats['3PFGA']:
      a_thrfg_per_str = '100.0'
    else:  
      ONE_DP = decimal.Decimal(10) ** -1        
      a_thrfg_per_str = str(decimal.Decimal(float(away_stats['3PFGM'])/away_stats['3PFGA']*100).quantize(ONE_DP))      
    a_thrfg_str = str(away_stats['3PFGM']) + "-" + str(away_stats['3PFGA']) + " (" + a_thrfg_per_str + "%)"
    
    if home_stats['3PFGA'] == 0:
      h_thrfg_per_str = "N/A"
    elif home_stats['3PFGM'] == home_stats['3PFGA']:
      h_thrfg_per_str = '100.0'
    else:
      ONE_DP = decimal.Decimal(10) ** -1        
      h_thrfg_per_str = str(decimal.Decimal(float(home_stats['3PFGM'])/home_stats['3PFGA']*100).quantize(ONE_DP))      
    h_thrfg_str = str(home_stats['3PFGM']) + "-" + str(home_stats['3PFGA']) + " (" + h_thrfg_per_str + "%)"  

    thrfg_line = "|" + '{:^{len}}'.format(a_thrfg_str,len=name_len) + "|" + \
                 '{:^{len}}'.format('3Pt (%)',len=mid_len) + "|" +\
                 '{:^{len}}'.format(h_thrfg_str,len=name_len) + "|"

    if away_stats['FTA'] == 0:
      a_ft_per_str = 'N/A'
    elif away_stats['FTM'] == away_stats['FTA']:
      a_ft_per_str = '100.0'
    else:  
      ONE_DP = decimal.Decimal(10) ** -1        
      a_ft_per_str = str(decimal.Decimal(float(away_stats['FTM'])/away_stats['FTA']*100).quantize(ONE_DP))      
    a_ft_str = str(away_stats['FTM']) + "-" + str(away_stats['FTA']) + " (" + a_ft_per_str + "%)"
    
    if home_stats['FTA'] == 0:
      h_ft_per_str = "N/A"
    elif home_stats['FTM'] == home_stats['FTA']:
      h_ft_per_str = '100.0'
    else:
      ONE_DP = decimal.Decimal(10) ** -1        
      h_ft_per_str = str(decimal.Decimal(float(home_stats['FTM'])/home_stats['FTA']*100).quantize(ONE_DP))      
    h_ft_str = str(home_stats['FTM']) + "-" + str(home_stats['FTA']) + " (" + h_ft_per_str + "%)"     

    ft_line = "|" + '{:^{len}}'.format(a_ft_str,len=name_len) + "|" + \
              '{:^{len}}'.format('FTs (%)',len=mid_len) + "|" +\
              '{:^{len}}'.format(h_ft_str,len=name_len) + "|"    
    
    a_reb_str = str(away_stats['Tot Reb']) + " (" + str(away_stats['Off Reb']) + ")"
    h_reb_str = str(home_stats['Tot Reb']) + " (" + str(home_stats['Off Reb']) + ")"
    reb_line = "|" + '{:^{len}}'.format(a_reb_str,len=name_len) + "|" +\
               '{:^{len}}'.format('Reb (Off)',len=mid_len) + "|" +\
               '{:^{len}}'.format(h_reb_str,len=name_len) + "|"
    
    if away_stats['Assists'] < 10:    
      a_ast_str = ' ' + str(away_stats['Assists'])
    else:
      a_ast_str = str(away_stats['Assists'])
    
    if home_stats['Assists'] < 10:    
      h_ast_str = ' ' + str(home_stats['Assists'])
    else:
      h_ast_str = str(home_stats['Assists'])
      
    ast_line = "|" + '{:^{len}}'.format(a_ast_str,len=name_len) + "|" +\
               '{:^{len}}'.format('Assists',len=mid_len) + "|" +\
               '{:^{len}}'.format(h_ast_str,len=name_len) + "|"

    if away_stats['Inside Pts'] < 10:    
      a_in_pts_str = ' ' + str(away_stats['Inside Pts'])
    else:
      a_in_pts_str = str(away_stats['Inside Pts'])
    
    if home_stats['Inside Pts'] < 10:    
      h_in_pts_str = ' ' + str(home_stats['Inside Pts'])
    else:
      h_in_pts_str = str(home_stats['Inside Pts'])
    
    in_pts_line = "|" + '{:^{len}}'.format(a_in_pts_str,len=name_len) + "|" +\
                  '{:^{len}}'.format('Ins Pts',len=mid_len) + "|" +\
                  '{:^{len}}'.format(h_in_pts_str,len=name_len) + "|"

    if away_stats['2nd Chance Pts'] < 10:    
      a_sec_chance_pts_str = ' ' + str(away_stats['2nd Chance Pts'])
    else:
      a_sec_chance_pts_str = str(away_stats['2nd Chance Pts'])
    
    if home_stats['2nd Chance Pts'] < 10:    
      h_sec_chance_pts_str = ' ' + str(home_stats['2nd Chance Pts'])
    else:
      h_sec_chance_pts_str = str(home_stats['2nd Chance Pts'])
                  
    sec_chance_pts_line = "|" + '{:^{len}}'.format(a_sec_chance_pts_str,len=name_len) + "|" +\
                          '{:^{len}}'.format('2nd C Pts',len=mid_len) + "|" +\
                          '{:^{len}}'.format(h_sec_chance_pts_str,len=name_len) + "|"

    if away_misc_stats['Largest Lead'] < 10:    
      a_largest_lead_str = ' ' + str(away_misc_stats['Largest Lead'])
    else:
      a_largest_lead_str = str(away_misc_stats['Largest Lead'])
    
    if home_misc_stats['Largest Lead'] < 10:    
      h_largest_lead_str = ' ' + str(home_misc_stats['Largest Lead'])
    else:
      h_largest_lead_str = str(home_misc_stats['Largest Lead'])
                       
    largest_lead_line = "|" + '{:^{len}}'.format(a_largest_lead_str,len=name_len) + "|" +\
                        '{:^{len}}'.format('Lgst Lead',len=mid_len) + "|" +\
                        '{:^{len}}'.format(h_largest_lead_str,len=name_len) + "|"

    if away_misc_stats['Most Unanswered Pts'] < 10:    
      a_max_run_str = ' ' + str(away_misc_stats['Most Unanswered Pts'])
    else:
      a_max_run_str = str(away_misc_stats['Most Unanswered Pts'])
    
    if home_misc_stats['Most Unanswered Pts'] < 10:    
      h_max_run_str = ' ' + str(home_misc_stats['Most Unanswered Pts'])
    else:
      h_max_run_str = str(home_misc_stats['Most Unanswered Pts'])
    
    max_run_line = "|" + '{:^{len}}'.format(a_max_run_str,len=name_len) + "|" +\
                   '{:^{len}}'.format('Max Run',len=mid_len) + "|" +\
                   '{:^{len}}'.format(h_max_run_str,len=name_len) + "|"

    if away_stats['Bench Pts'] < 10:    
      a_bench_pts_str = ' ' + str(away_stats['Bench Pts'])
    else:
      a_bench_pts_str = str(away_stats['Bench Pts'])
    
    if home_stats['Bench Pts'] < 10:    
      h_bench_pts_str = ' ' + str(home_stats['Bench Pts'])
    else:
      h_bench_pts_str = str(home_stats['Bench Pts'])
    
    bench_pts_line = "|" + '{:^{len}}'.format(a_bench_pts_str,len=name_len) + "|" +\
                     '{:^{len}}'.format('Bench Pts',len=mid_len) + "|" +\
                     '{:^{len}}'.format(h_bench_pts_str,len=name_len) + "|"
    
    
    #Print full overview
    print (title_str)
    print (time_status_str)
    print_scoreboard(h_period_scores,a_period_scores,home_nick,away_nick,\
                     time_dict['Tot Period'])
    print (dividing_line_str)
    print (stats_title_str)
    print (dividing_line_str)
    print (fg_line)
    print (thrfg_line)
    print (ft_line)
    print (reb_line)
    print (ast_line)
    print (in_pts_line)
    print (sec_chance_pts_line)
    print (largest_lead_line)
    print (max_run_line)
    print (bench_pts_line)
    print (dividing_line_str)
    
    #------------------------------------------
    #
    # +-----------------+
    # |   Misc. Stats   |
    # +------------+----+
    # | Lead Chgs  |    |
    # | Ties       |    |
    # +------------+----+
    #
    #------------------------------------------
    def print_misc_stats(misc_stats_dict):
      
      title_len = 17
      top_line = '+' + title_len*'-' + '+'
      title_str = '{:^{len}}'.format('Misc. Stats',len=17)
      title_line = '|' + title_str + '|'
      left_seg_len = title_len - 5
      right_seg_len = 4
      mid_line = '|' + left_seg_len*'-' + '+' + right_seg_len*'-' + '+'
      lead_chgs_line = '|' + '{:<{len}}'.format(' Lead Chgs',len=left_seg_len) + '|' +\
                       '{:^{len}}'.format(str(misc_stats_dict['Lead Changes']),len=right_seg_len) + '|'
      ties_line = '|' + '{:<{len}}'.format(' Ties',len=left_seg_len) + '|' +\
                  '{:^{len}}'.format(str(misc_stats_dict['Ties']),len=right_seg_len) + '|'
      
      print (top_line)
      print (title_line)                 
      print (mid_line)
      print (lead_chgs_line)
      print (ties_line)
      print (mid_line)
      
      return
      
    print_misc_stats(misc_stats_dict)
    return
  
  #-----------------------------------------------------------------------------
  # Function print_team_stats
  #
  # VC: Add H2H functionality?
  # VC: Game type functionality?
  #-----------------------------------------------------------------------------
  def print_team_stats(self,career,game_type):
    #team_stats_dict = {}
    team_basic_pg_dict = {}
    
    basic_stats = ('Court Time','FGM','FGA','3PFGM','3PFGA','FTM','FTA',\
                   '+/-','Off Reb','Tot Reb','Assists','Fouls','Points')
    #adv_stats = ()
    result_p = re.compile('^[WL]\(([0-9]*?)-([0-9]*?)\)$')
    players_appeared = []
    players_not_appeared = []

    ppg_dict = {}
    no_ppg_dict = {}
    
    for p in self.players: 
      if career == True:
        y_str = 'Career'
      else:
        y_str = 'Y' + str(self.cur_year)
      
      p_stats = self.players[p].stats[y_str]
      #print (player,player_stats_dict)          
      #team_stats_dict[player] = player_stats_dict
      if p_stats['Court Time'] > 0:
        players_appeared.append(p)
        basic_pg_dict = {}
        ppg_dict[p] = 1.0*p_stats['Points']/p_stats['Games Played']
        for s in basic_stats:
          basic_pg_dict[s] = 1.0*p_stats[s]/p_stats['Games Played']
        basic_pg_dict['Games Played'] = p_stats['Games Played']
        basic_pg_dict['Games Started'] = p_stats['Games Started']
        team_basic_pg_dict[p] = basic_pg_dict  
      else:
        players_not_appeared.append(p)
        no_ppg_dict[p] = 0
      
    
    basic_title_str = ('Player','Pos','  G',' GS',' Min','  FGM-A  ',' FG% ','  3PM-A  ',\
                       ' 3P% ','  FTM-A  ',' FT% ',' +/- ','OReb','TReb',' Ast',\
                       ' Fls',' Pts')  
    title_line = ''
    line_len = 0
    for s in basic_title_str:
      title_line += s + ' '
      line_len += len(s) + 1
    line_len -= 1
    print ('{:-^{l}}'.format(self.name + ' stats: ',l=line_len))
    print (title_line)
    
    player_print_seq = F_RANK_FROM_RATINGS(ppg_dict,True)
    
    
    for p in player_print_seq:
      line = '{:<{l}}'.format(p,l=len(basic_title_str[0])) + ' '
      
      pos_str = SIMPLE_POS_DICT[self.players[p].profile['Pos']]
      line += '{:>{l}}'.format(pos_str,l=len(basic_title_str[1])) + ' '
      
      g_str = str(team_basic_pg_dict[p]['Games Played'])
      line += '{:>{l}}'.format(g_str,l=len(basic_title_str[2])) + ' '
      
      gs_str = str(team_basic_pg_dict[p]['Games Started'])
      line += '{:>{l}}'.format(gs_str,l=len(basic_title_str[3])) + ' '
      
      min_str = str(decimal.Decimal(team_basic_pg_dict[p]['Court Time']/60)\
                    .quantize(ONE_DP))
      line += '{:>{l}}'.format(min_str,l=len(basic_title_str[4])) + ' '
      
      fgm_str = str(decimal.Decimal(team_basic_pg_dict[p]['FGM'])\
                    .quantize(ONE_DP))
      fga_str = str(decimal.Decimal(team_basic_pg_dict[p]['FGA'])\
                    .quantize(ONE_DP))                 
      fg_str = '{:>4}'.format(fgm_str) + '-' + '{:<4}'.format(fga_str)
      line += fg_str + ' '
      
      if team_basic_pg_dict[p]['FGA'] == 0:
        fg_per_str = ' N/A '
      else:
        fg_per_str = str(decimal.Decimal(team_basic_pg_dict[p]['FGM']/ \
                     team_basic_pg_dict[p]['FGA']).quantize(THREE_DP))
      line += fg_per_str + ' '
      
      thr_m_str = str(decimal.Decimal(team_basic_pg_dict[p]['3PFGM'])\
                    .quantize(ONE_DP))
      thr_a_str = str(decimal.Decimal(team_basic_pg_dict[p]['3PFGA'])\
                    .quantize(ONE_DP))
      thr_str = '{:>4}'.format(thr_m_str) + '-' + '{:<4}'.format(thr_a_str)
      line += thr_str + ' '
      
      if team_basic_pg_dict[p]['3PFGA'] == 0:
        thr_per_str = ' N/A '
      else:
        thr_per_str = str(decimal.Decimal(team_basic_pg_dict[p]['3PFGM']/ \
                     team_basic_pg_dict[p]['3PFGA']).quantize(THREE_DP))
      line += thr_per_str + ' '
      
      ftm_str = str(decimal.Decimal(team_basic_pg_dict[p]['FTM'])\
                    .quantize(ONE_DP))
      fta_str = str(decimal.Decimal(team_basic_pg_dict[p]['FTA'])\
                    .quantize(ONE_DP))
      ft_str = '{:>4}'.format(ftm_str) + '-' + '{:<4}'.format(fta_str)
      line += ft_str + ' '
     
      if team_basic_pg_dict[p]['FTA'] == 0:
        ft_per_str = ' N/A '
      else:
        ft_per_str = str(decimal.Decimal(team_basic_pg_dict[p]['FTM']/ \
                   team_basic_pg_dict[p]['FTA']).quantize(THREE_DP))
      line += ft_per_str + ' '
      
      if team_basic_pg_dict[p]['+/-'] >= 0:
        p_m_str = '+' + str(decimal.Decimal(team_basic_pg_dict[p]['+/-'])\
                            .quantize(ONE_DP))
      else:
        p_m_str = str(decimal.Decimal(team_basic_pg_dict[p]['+/-'])\
                            .quantize(ONE_DP))
      line += '{:>{l}}'.format(p_m_str,l=len(basic_title_str[11])) + ' '
      
      o_reb_str = str(decimal.Decimal(team_basic_pg_dict[p]['Off Reb'])\
                      .quantize(ONE_DP))
      line += '{:>{l}}'.format(o_reb_str,l=len(basic_title_str[12])) + ' '                
                      
      t_reb_str = str(decimal.Decimal(team_basic_pg_dict[p]['Tot Reb'])\
                      .quantize(ONE_DP))
      line += '{:>{l}}'.format(t_reb_str,l=len(basic_title_str[13])) + ' '
      
      ast_str = str(decimal.Decimal(team_basic_pg_dict[p]['Assists'])\
                      .quantize(ONE_DP))
      line += '{:>{l}}'.format(ast_str,l=len(basic_title_str[14])) + ' '                
                      
      fls_str = str(decimal.Decimal(team_basic_pg_dict[p]['Fouls'])\
                      .quantize(ONE_DP))
      line += '{:>{l}}'.format(fls_str,l=len(basic_title_str[15])) + ' '                
                      
      pts_str = str(decimal.Decimal(team_basic_pg_dict[p]['Points'])\
                      .quantize(ONE_DP))
      line += '{:>{l}}'.format(pts_str,l=len(basic_title_str[16])) + ' '                 
                      
      print (line) 
    player_print_seq = F_RANK_FROM_RATINGS(no_ppg_dict,True) 
    for p in player_print_seq:  
      line = '{:<{l}}'.format(p,l=len(basic_title_str[0])) + ' '
      line += 'Yet to appear this season'
      print (line)
    
    print ('-'*(line_len))  
    return
  
  def pre_match(self,game_type,starter_info_dict=None):
    print ('***' + self.name + ' Pre-Game***')
    #VC: Fix later
    if game_type in ('RS','AF','BF','VF'):
      self.team_stats_viewer()
    
    self.choose_starting_lineup(game_type,starter_info_dict)
    return
    
  def team_stats_viewer(self):
    viewer_complete = False
    while viewer_complete == False:
      option_chosen = False
      print ('Options:')
      print ('[1] See season stats')
      print ('[2] See season H2H stats')
      print ('[3] See career stats')
      print ('[4] See career H2H stats')
      print ('[5] Choose starting lineup')
      while option_chosen == False:
        reply = input('Please enter a option number' + \
                      '(enter "O" to view options again):').rstrip()
        if reply == '1':
          option_chosen = True
          self.print_team_stats(False,self.game['Game Type'])
        elif reply == '2':
          option_chosen = True
          print ('Functionality not available yet')
        elif reply == '3':
          option_chosen = True
          print ('Functionality not available yet')
        elif reply == '4':
          option_chosen = True
          print ('Functionality not available yet')
        elif reply == '5':
          viewer_complete = True
          option_chosen = True
        elif reply in ('o','O','0'):
          option_chosen = True
        else:
          print ("***You did not enter a valid option, please try again.***")                
           
    return
    
  #---------------------------------------------
  # Function for user to choose starting lineup
  #---------------------------------------------
  def choose_starting_lineup(self,type,starter_info_dict):
    if type == 'Reg':
      init_message = 'Choose starters for ' + self.name + ':'
      satisfied = False
      starters = []
      while satisfied == False:
        self.print_roster_user()     
        print (init_message)    
        for i in range(5):     
          player = None   
          while not player:
            if (i > 0):
              line = 'Starters picked: '
              for j in range(i):
                line += starters[j] + ' '
              print (line)
            reply = input('Enter name of starter no. ' + str(i+1) + \
                            ' (enter "Roster" to view roster again):')    
            reply = reply.rstrip()
            if reply in starters:
              print ('***' + reply + " is already chosen, please choose a different player.***")
            elif reply in self.players.keys():
              if self.players[reply].game['Court Status'] == -3:
                print ('***' + reply + " is injured and suspended, please choose a different player.***")
              elif self.players[reply].game['Court Status'] == -2:
                print ('***' + reply + " is injured, please choose a different player.***")
              elif self.players[reply].game['Court Status'] == -1:
                print ('***' + reply + " is suspended, please choose a different player.***")
              else:
                player = reply
            elif reply == 'Roster':
              self.print_roster_user()
            else:
              print ("***You did not enter a player's name, please try again.***")
            print ('\n')
                
          starters.append(player)
        F_PRINT_P_GRADES(self.players,'Team',starters,None)  
        #self.print_player_grades(starters)
        confirmed = False
      
        while confirmed == False:
          message =  'This is your selected starting lineup, do you want go ahead with it? (Y|N)'
          print (message)
          reply = input('-->')
          reply = reply.rstrip()
          if reply in ('Yes','Y','YES'):
            confirmed = True
            satisfied = True
          elif reply in ('No','N','NO'):
            init_message = 'Please repick starters for ' + self.name + ':'
            starters = []
            confirmed = True
          else:
            message = 'Invalid reply. Do you want go ahead with your chosen starting lineup? (Y|N)'
    
      self.game['Starters'] = copy.deepcopy(starters)
      self.game['On Court'] = copy.deepcopy(starters)
    else:
      self.game['Starters'] = starter_info_dict['Starters']
      self.game['On Court'] = starter_info_dict['On Court']

    for s in self.game['Starters']:
      self.players[s].game['Court Status'] = 1
      self.players[s].game['Starter'] = True
    for p in self.players:
      if self.players[p].game['Court Status'] == 0:
        self.game['Avail Subs'].append(p)
        self.game['Bench'].append(p)
      elif self.players[p].game['Court Status'] < 0:
        self.game['Unavailable'].append(p)
    return  
    
