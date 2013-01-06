from PossessionClass import *
from GlobalVariables import *
import math

class Period:
  def __init__(self,number,tot_number,time,home,away,misc_stats_dict,PBP_history,\
               sub_allowed,game_type):
    self.game_type = game_type
    self.number = number
    self.tot_number = tot_number
    if self.number < self.tot_number:
      self.final_period = False
    else:
      self.final_period = True
    
    self.time = time
    self.home = home
    self.away = away
    self.misc_stats_dict = misc_stats_dict
    self.PBP_history = PBP_history
    self.time_dict = {'Period':number,'Tot Period':tot_number,\
                      'Time Remaining':time}
    
    self.sub_allowed = sub_allowed
 
    #Contains attributes of player currently on court
    self.home_player_atts = {}
    self.away_player_atts = {}
    for player in self.home.players:
      if self.home.players[player].game['Court Status'] == 1:
        self.home_player_atts[player] = self.home.players[player].game_attributes
    for player in self.away.players:
      if self.away.players[player].game['Court Status'] == 1:
        self.away_player_atts[player] = self.away.players[player].game_attributes

    self.home.game['Period Scores'].append(0)
    self.away.game['Period Scores'].append(0)

 
    #------------------------------
    # variable previous_lead_team
    # 0  - Score still 0-0
    # 1  - Home team last led
    # -1 - Away team last led
    #------------------------------
    self.previous_lead_team = 0
    
    #-----------------------------------------------------------------
    # Determine which team has the ball at the start of the period
    # 
    # variable ball_possession:
    #  1 - Home team has possession
    # -1 - Away team has possession
    #-----------------------------------------------------------------
    if tot_number == 4:
      if ((number == 2) | (number == 3)):
        self.ball_possession = -1
      else:
        self.ball_possession = 1
    elif tot_number == 2:
      if (number == 2):
        self.ball_possession = -1
      else:
        self.ball_possession = 1
    else:
      print ('BUG, invalid number of periods!!')
      
    if self.number > 1:
      self.home.game['Subs'] = {'In':[],'Out':[]}
      self.away.game['Subs'] = {'In':[],'Out':[]}
      if self.sub_allowed == True:
        self.timeout(None)      
    self.print_between_period_play_by_play(False,number,tot_number)
    
    self.run_period()
    return
    
  def print_timeout_play_by_play(self,team):
    line = '[' + str(self.home.game['Stats']['Points']) + '-' +\
            str(self.away.game['Stats']['Points']) + '] '  
              
    min_left = int(self.time_dict['Time Remaining']/60)
    sec_left = int(self.time_dict['Time Remaining']%60)
      
    if min_left < 10:
      min_left = '0' + str(min_left)
    else:
      min_left = str(min_left)
      
    if sec_left < 10:
      sec_left = '0' + str(sec_left)
    else:
      sec_left = str(sec_left)
      
    line += '(' + min_left + ':' + sec_left + ') [' + team.nickname + '] ' +\
             'Timeout'
    self.PBP_history.append(line)
    return
  
  def print_sub_play_by_play(self,team,between_periods):
    if between_periods == True:
      if team.nickname:
        line = '[' + team.nickname + '] '
      else:
        line = '[' + team.name + ']'
    
      line += 'Sub(s) in: '
      for sub in team.game['Subs']['In']:
        line += sub + ' '
      line += '| Sub(s) out: '
      for sub in team.game['Subs']['Out']:
        line += sub + ' '
      self.PBP_history.append(line)
      print (line)
    else:
      sub_score_str = '[' + str(self.home.game['Stats']['Points']) + '-' +\
                      str(self.away.game['Stats']['Points']) + '] '      
      
      sub_min_left = int(self.time_dict['Time Remaining']/60)
      sub_sec_left = int(self.time_dict['Time Remaining']%60)
      
      if sub_min_left < 10:
        sub_min_left = '0' + str(sub_min_left)
      else:
        sub_min_left = str(sub_min_left)
      
      if sub_sec_left < 10:
        sub_sec_left = '0' + str(sub_sec_left)
      else:
        sub_sec_left = str(sub_sec_left)
      
      
      line = sub_score_str + '(' + sub_min_left + ':' + \
             sub_sec_left + ') [' + team.nickname + '] '
      
      line += 'Sub(s) in: '
      for sub in team.game['Subs']['In']:
        line += sub + ' '
      line += '| Sub(s) out: '
      for sub in team.game['Subs']['Out']:
        line += sub + ' '
      print (line)
      self.PBP_history.append(line)
   
    return
  
  def print_between_period_play_by_play(self,end,period_no,tot_periods):
    
    if period_no <= tot_periods:
      term = ' Period'
    else:
      term = ' Overtime'
    if end == True:
      line = '***End of the '
    else:
      line = '***Start of the '    
    line += str(period_no) + COUNT_STRINGS[period_no] + term + '***'
    
    print (line)
    self.PBP_history.append(line)
    
    return     
    
  def print_play_by_play(self,possession_obj):
    history = []
 
    p_obj = possession_obj
    foul_type_dict = {0:'Inside',1:'2Pt',2:'3Pt'}
    shot_type_dict = {0:'Inside Shot',1:'Jump Shot',2:'3Pt Shot',3:'Put Back Shot'}
        
    if self.home.nickname:
      h_name = self.home.nickname
    else:
      h_name = self.home.name
    if self.away.nickname:
      a_name = self.away.nickname
    else:
      a_name = self.away.name
    h_stats = self.home.game['Stats']
    a_stats = self.away.game['Stats']
    
    min_left = int((p_obj.time_remaining-p_obj.time)/60)

    if min_left < 10:
      min_left = '0' + str(min_left)
    else:
      min_left = str(min_left)

    sec_left = int((p_obj.time_remaining-p_obj.time)%60)
    
    if sec_left < 10:
      sec_left = '0' + str(sec_left)
    else:
      sec_left = str(sec_left)
     
    score_str = '[' + str(h_stats['Points']) + '-' + str(a_stats['Points']) + \
                '] '
    
    if (self.ball_possession == 1):
      o_team = self.home
      d_team = self.away
      o_name = score_str + '(' + min_left + ':' + sec_left + ') [' + h_name + '] '      
      d_name = score_str + '(' + min_left + ':' + sec_left + ') [' + a_name + '] '
      sub_score_str = '[' + str(h_stats['Points'] - p_obj.points_scored) +\
                      '-' + str(a_stats['Points']) + '] '
    else:
      o_team = self.away
      d_team = self.home
      o_name = score_str + '(' + min_left + ':' + sec_left + ') [' + a_name + '] '
      d_name = score_str + '(' + min_left + ':' + sec_left + ') [' + h_name + '] '
      sub_score_str = '[' + str(h_stats['Points']) + '-' + \
                       str(a_stats['Points'] - p_obj.points_scored) + '] '

    if p_obj.foul_drawn == True:
      if self.ball_possession == 1:
        prev_h_score = h_stats['Points'] - p_obj.points_scored
        score_str = '[' + str(prev_h_score) + '-' +\
                    str(a_stats['Points']) + '] '
        line = score_str + '(' + min_left + ':' + sec_left + ') [' + a_name + '] '
      elif self.ball_possession == -1:
        prev_a_score = a_stats['Points'] - p_obj.points_scored
        score_str = '[' + str(h_stats['Points']) + '-' +\
                    str(prev_a_score) + '] '
        line = score_str + '(' + min_left + ':' + sec_left + ') [' + h_name + '] '        
      
      line += p_obj.fouler + ' Shooting Foul: ' + foul_type_dict[p_obj.shot_type] +\
              ' (' + str(d_team.players[p_obj.fouler].game['Stats']['Fouls']) + ' PF)'
      print (line)
      history.append(line)
      if p_obj.fouled_out == True:
        if self.ball_possession == 1:
          line = score_str + '(' + min_left + ':' + sec_left + ') [' + a_name + '] ' 
        elif self.ball_possession == -1:
          line = score_str + '(' + min_left + ':' + sec_left + ') [' + h_name + '] '        
        line += 'Sub in: ' + p_obj.sub_in + ' | Sub out: ' + p_obj.fouler
        print (line)
        history.append(line)
      for i in range(len(p_obj.FT_result)):
        #line = o_name
        if p_obj.FT_result[i] == 1:
          if self.ball_possession == 1:
            prev_h_score += 1
            score_str = '[' + str(prev_h_score) + '-' +\
                        str(a_stats['Points']) + '] '
            line = score_str + '(' + min_left + ':' + sec_left + ') [' + h_name + '] '            
          elif self.ball_possession == -1:
            prev_a_score += 1
            score_str = '[' + str(h_stats['Points']) + '-' +\
                        str(prev_a_score) + '] '
            line = score_str + '(' + min_left + ':' + sec_left + ') [' + a_name + '] '             
          line += p_obj.shooter + ' FT ' + str(i + 1) +\
                  ' out of ' + str(len(p_obj.FT_result)) + ' (' +\
                  str(o_team.players[p_obj.shooter].game['Stats']['Points'] -\
                      sum(p_obj.FT_result) +\
                      sum(p_obj.FT_result[:(i+1)])) +\
                      ' PTS)'
          print (line)
          history.append(line)
        else:
          if self.ball_possession == 1:
            score_str = '[' + str(prev_h_score) + '-' +\
                        str(a_stats['Points']) + '] '
            line = score_str + '(' + min_left + ':' + sec_left + ') [' + h_name + '] '         
          elif self.ball_possession == -1:
            score_str = '[' + str(h_stats['Points']) + '-' +\
                        str(prev_a_score) + '] '
            line = score_str + '(' + min_left + ':' + sec_left + ') [' + a_name + '] '           
          line += p_obj.shooter + ' FT ' + str(i + 1) +\
                  ' out of ' + str(len(p_obj.FT_result)) + ' Missed'  
          print (line)
          history.append(line)
        
    else:
      line = o_name
      if p_obj.put_back == True:
        line += p_obj.shooter + ' ' + shot_type_dict[3]
      else:
        line += p_obj.shooter + ' ' + shot_type_dict[p_obj.shot_type]
      if p_obj.shot_result == True:
        line += ' Made (' + str(o_team.players[p_obj.shooter].game['Stats']['Points']) +\
                ' PTS)'
        if p_obj.assist == True:
          line += ' Assist: ' + p_obj.assister + ' (' +\
                  str(o_team.players[p_obj.assister].game['Stats']['Assists']) + \
                  ' AST)'
      elif p_obj.shot_result == False:
        line += ' Missed'
      print (line)
      history.append(line)
    
    if p_obj.reb_avail == True:
      if p_obj.off_rebound == True:
        line = o_name
        line += p_obj.rebounder + ' Off Rebound (Off:' + \
                str(o_team.players[p_obj.rebounder].game['Stats']['Off Reb']) +\
                ' Def:' + \
                str(o_team.players[p_obj.rebounder].game['Stats']['Def Reb']) +\
                ')'
       
      else:
        line = d_name
        line += p_obj.rebounder + ' Def Rebound (Off:' + \
                str(d_team.players[p_obj.rebounder].game['Stats']['Off Reb']) +\
                ' Def:' + \
                str(d_team.players[p_obj.rebounder].game['Stats']['Def Reb']) +\
                ')'
      print (line)
      history.append(line)
    for line in history:
      self.PBP_history.append(line)
    return
    
  #----------------------------------------------------------------------------
  # Function update_all_stats
  #----------------------------------------------------------------------------
  def update_all_stats(self,possession_obj):
    p_obj = possession_obj
    
    if (self.ball_possession == 1):
      o_stats = self.home.game['Stats']
      o_players = self.home.players
      d_stats = self.away.game['Stats']
      d_players = self.away.players
      o_periods = self.home.game['Period Scores']
      o_team = self.home
      o_misc_stats = self.home.game['Misc Stats']
      d_misc_stats = self.away.game['Misc Stats']
    else:
      o_stats = self.away.game['Stats']
      o_players = self.away.players
      d_stats = self.home.game['Stats']
      d_players = self.home.players
      o_periods = self.away.game['Period Scores']
      o_team = self.away
      o_misc_stats = self.away.game['Misc Stats']
      d_misc_stats = self.home.game['Misc Stats']
    
    # For all cases
    o_stats['Possessions'] += 1
    o_stats['Points'] += p_obj.points_scored
    o_players[p_obj.shooter].game['Stats']['Points'] += p_obj.points_scored
    if p_obj.shooter in o_team.game['Bench']:
      o_stats['Bench Pts'] += p_obj.points_scored
    o_periods[-1] += p_obj.points_scored
    o_players[p_obj.shooter].game['Stats']['Possessions'] += 1
    
    for player in p_obj.ball_sequence:
      o_players[player].game['Stats']['Touches'] += 1
      o_stats['Touches'] += 1
    for player in p_obj.off_player_atts.keys():
      o_players[player].game['Stats']['+/-'] += p_obj.points_scored
      o_players[player].game['Stats']['Team Points For'] += p_obj.points_scored
      o_players[player].game['Stats']['Court Time'] += p_obj.time
    for player in p_obj.def_player_atts.keys():
      d_players[player].game['Stats']['+/-'] -= p_obj.points_scored
      d_players[player].game['Stats']['Team Points Against'] += p_obj.points_scored
      d_players[player].game['Stats']['Court Time'] += p_obj.time    
    
    # Inside points
    if p_obj.inside_flag == True:       
      o_stats['Inside Pts'] += p_obj.points_scored  
      o_players[p_obj.shooter].game['Stats']['Inside Pts'] += p_obj.points_scored
    else:
      o_stats['Perimeter Pts'] += p_obj.points_scored
      o_players[p_obj.shooter].game['Stats']['Perimeter Pts'] += p_obj.points_scored
      
    # Second chance points
    if p_obj.sec_chance_flag == True:
      o_stats['2nd Chance Pts'] += p_obj.points_scored
      o_players[p_obj.shooter].game['Stats']['2nd Chance Pts'] += p_obj.points_scored
    
    if (len(p_obj.ball_sequence) > 1):
      o_stats['Passes'] += len(p_obj.ball_sequence) - 1
      for player in p_obj.ball_sequence[:-1]:
        o_players[player].game['Stats']['Passes'] += 1
    
    # If foul occurred
    if p_obj.foul_drawn == True:
      
      d_stats['Fouls'] += 1
      d_players[p_obj.fouler].game['Stats']['Fouls'] += 1
      o_stats['Fouls Drawn'] += 1
      o_players[p_obj.shooter].game['Stats']['Fouls Drawn'] += 1
      o_stats['FTA'] += len(p_obj.FT_result) 
      o_players[p_obj.shooter].game['Stats']['FTA'] += len(p_obj.FT_result) 
      o_stats['FTM'] += sum(p_obj.FT_result)
      o_players[p_obj.shooter].game['Stats']['FTM'] += sum(p_obj.FT_result)
      
      if o_stats['Points'] > d_stats['Points'] and \
         sum(p_obj.FT_result) > (o_stats['Points'] - d_stats['Points']):
        #print ("VC - Tie during FTs")
        self.misc_stats_dict['Ties'] += 1
        o_misc_stats['Ties'] += 1
        d_misc_stats['Ties'] += 1
        self.misc_stats_dict['Last Tie Score'] = (d_stats['Points'],d_stats['Points'])          
      
      if p_obj.shot_type == 0:
        d_stats['Inside Fouls'] += 1
        d_players[p_obj.fouler].game['Stats']['Inside Fouls'] += 1
        o_stats['Inside Fouls Drawn'] += 1
        o_players[p_obj.shooter].game['Stats']['Inside Fouls Drawn'] += 1
      else:
        d_stats['Per Fouls'] += 1
        d_players[p_obj.fouler].game['Stats']['Per Fouls'] += 1
        o_stats['Per Fouls Drawn'] += 1
        o_players[p_obj.shooter].game['Stats']['Per Fouls Drawn'] += 1
    else:
      o_stats['FGA'] += 1
      o_players[p_obj.shooter].game['Stats']['FGA'] += 1
      
      if p_obj.shot_type == 2:
        o_stats['3PFGA'] += 1
        o_players[p_obj.shooter].game['Stats']['3PFGA'] += 1
        
        if p_obj.shot_result == 1:
          o_stats['3PFGM'] += 1
          o_players[p_obj.shooter].game['Stats']['3PFGM'] += 1
          o_stats['FGM'] += 1
          o_players[p_obj.shooter].game['Stats']['FGM'] += 1      

      elif p_obj.shot_type == 0:
        if p_obj.put_back == True:
          o_stats['Put Backs A'] += 1
          o_players[p_obj.shooter].game['Stats']['Put Backs A'] += 1
          if p_obj.put_back_made == True:
            o_stats['Put Backs M'] += 1
            o_players[p_obj.shooter].game['Stats']['Put Backs M'] += 1       
        o_stats['2PFGA'] += 1
        o_players[p_obj.shooter].game['Stats']['2PFGA'] += 1
        o_stats['Inside FGA'] += 1
        o_players[p_obj.shooter].game['Stats']['Inside FGA'] += 1
        
        if p_obj.shot_result == 1:
          o_stats['2PFGM'] += 1
          o_players[p_obj.shooter].game['Stats']['2PFGM'] += 1        
          o_stats['Inside FGM'] += 1
          o_players[p_obj.shooter].game['Stats']['Inside FGM'] += 1
          o_stats['FGM'] += 1
          o_players[p_obj.shooter].game['Stats']['FGM'] += 1      
      else:
        o_stats['2PFGA'] += 1
        o_players[p_obj.shooter].game['Stats']['2PFGA'] += 1
        o_stats['2PJFGA'] += 1
        o_players[p_obj.shooter].game['Stats']['2PJFGA'] += 1
        
        if p_obj.shot_result == 1:
          o_stats['2PFGM'] += 1
          o_players[p_obj.shooter].game['Stats']['2PFGM'] += 1
          o_stats['2PJFGM'] += 1
          o_players[p_obj.shooter].game['Stats']['2PJFGM'] += 1
          o_stats['FGM'] += 1
          o_players[p_obj.shooter].game['Stats']['FGM'] += 1                
      
      if p_obj.assist == True:
        o_stats['Assists'] += 1
        o_players[p_obj.assister].game['Stats']['Assists'] += 1
        
    if p_obj.reb_avail == True:
      if p_obj.off_rebound == True:
        o_stats['Off Reb'] += 1
        o_stats['Tot Reb'] += 1
        o_players[p_obj.rebounder].game['Stats']['Off Reb'] += 1
        o_players[p_obj.rebounder].game['Stats']['Tot Reb'] += 1
      else:
        d_stats['Def Reb'] += 1
        d_stats['Tot Reb'] += 1
        d_players[p_obj.rebounder].game['Stats']['Def Reb'] += 1
        d_players[p_obj.rebounder].game['Stats']['Tot Reb'] += 1
    # Other misc. stats
    if (p_obj.points_scored > 0):
      
      if ((o_stats['Points'] - d_stats['Points']) >= \
                           o_misc_stats['Largest Lead']):
        o_misc_stats['Largest Lead'] = (o_stats['Points'] - d_stats['Points'])
        o_misc_stats['Largest Lead Score'] = (self.home.game['Stats']['Points'],\
                                              self.away.game['Stats']['Points'])
      
      if (self.misc_stats_dict['Team Last Scored'] == 0):
        self.misc_stats_dict['Team Last Scored'] = p_obj.ball_possession
        self.misc_stats_dict['Run'] = p_obj.points_scored
      elif (self.misc_stats_dict['Team Last Scored'] == p_obj.ball_possession):
        self.misc_stats_dict['Run'] += p_obj.points_scored
      elif (self.misc_stats_dict['Team Last Scored'] != p_obj.ball_possession):
        self.misc_stats_dict['Team Last Scored'] = p_obj.ball_possession
        self.misc_stats_dict['Run'] = p_obj.points_scored
        
      if (self.misc_stats_dict['Run'] >= o_misc_stats['Most Unanswered Pts']):
        o_misc_stats['Most Unanswered Pts'] = self.misc_stats_dict['Run']
        o_misc_stats['Most Unanswered Pts Score'] = (self.home.game['Stats']['Points'],\
                                                     self.away.game['Stats']['Points'])
    
      if (self.home.game['Stats']['Points'] == \
          self.away.game['Stats']['Points']):
        self.misc_stats_dict['Ties'] += 1
        o_misc_stats['Ties'] += 1
        d_misc_stats['Ties'] += 1
        self.misc_stats_dict['Last Tie Score'] = \
          (self.home.game['Stats']['Points'],self.away.game['Stats']['Points'])
      elif (self.misc_stats_dict['Team Last Led'] == 0):
        self.misc_stats_dict['Team Last Led'] = p_obj.ball_possession
      elif ((self.home.game['Stats']['Points'] -\
             self.away.game['Stats']['Points']) *\
             self.misc_stats_dict['Team Last Led'] < 0):
        self.misc_stats_dict['Team Last Led'] = p_obj.ball_possession
        self.misc_stats_dict['Lead Changes'] += 1
        o_misc_stats['Lead Changes'] += 1
        d_misc_stats['Lead Changes'] += 1
        self.misc_stats_dict['Last Lead Change Score'] = \
          (self.home.game['Stats']['Points'],self.away.game['Stats']['Points'])
    return
  
  def timeout(self,home_TO,end_of_match=False):
    self.home.game['Subs'] = {'In':[],'Out':[]}
    self.away.game['Subs'] = {'In':[],'Out':[]}
    
    if end_of_match == True:
      self.home.timeout(self.away,self.PBP_history,self.time_dict,\
                        self.misc_stats_dict,True)
    else:
      if home_TO == True:
        TO_caller_home = True
        opp_team_home = False
        TO_caller = self.home
        self.print_timeout_play_by_play(TO_caller)
        opp_team = self.away
        TO_caller_atts = self.home_player_atts
        opp_team_atts = self.away_player_atts
        between_periods = False
        print ('{:-^60}'.format('Timeout: ' + TO_caller.name))
      elif home_TO == False:
        TO_caller_home = False
        opp_team_home = True
        TO_caller = self.away
        self.print_timeout_play_by_play(TO_caller)
        opp_team = self.home
        TO_caller_atts = self.away_player_atts
        opp_team_atts = self.home_player_atts
        between_periods = False
        print ('{:-^60}'.format('Timeout: ' + TO_caller.name))
      elif not home_TO:
        TO_caller = self.home
        opp_team = self.away
        between_periods = True
        TO_caller_home = True
        opp_team_home = False
        TO_caller_atts = self.home_player_atts
        opp_team_atts = self.away_player_atts
        print ('***Period break***')
    
      opp_team.timeout(TO_caller,self.PBP_history,self.time_dict,\
                       self.misc_stats_dict,opp_team_home)
      TO_caller.timeout(opp_team,self.PBP_history,self.time_dict,\
                        self.misc_stats_dict,TO_caller_home)
    
      if len(opp_team.game['Subs']['In']) > 0: 
        for sub in opp_team.game['Subs']['Out']:
          del opp_team_atts[sub]
        for sub in opp_team.game['Subs']['In']:
          opp_team_atts[sub] = opp_team.players[sub].game_attributes 
        self.print_sub_play_by_play(opp_team,between_periods)
      if len(TO_caller.game['Subs']['In']) > 0: 
        for sub in TO_caller.game['Subs']['Out']:
          del TO_caller_atts[sub]
        for sub in TO_caller.game['Subs']['In']:
          TO_caller_atts[sub] = TO_caller.players[sub].game_attributes 
        self.print_sub_play_by_play(TO_caller,between_periods)
      
    return
    
    
  def run_period(self):    
    self.sec_chance_flag = False
    self.prev_off_reb = None
    self.after_TO_flag = False
    self.clutch_flag = False
    #Start of period flag (so that you can't call timeouts at the start of a
    #                      period)
    self.after_start_flag = False    
    
    while self.time_dict['Time Remaining'] > 0:
      self.score_diff = self.home.game['Stats']['Points'] - \
                        self.away.game['Stats']['Points']
      if ((self.final_period == True) & \
          (self.time_dict['Time Remaining'] < 60) & \
          (math.fabs(self.score_diff) < 10)):
        self.clutch_flag = True 
      self.home.game['Subs'] = {'In':[],'Out':[]}
      self.away.game['Subs'] = {'In':[],'Out':[]}
      
      if self.ball_possession == 1:
        off_team = self.home
        def_team = self.away
        home_pos = True
      elif self.ball_possession == -1:
        off_team = self.away
        def_team = self.home
        home_pos = False
      else:
        print ("VC:BUG! something wrong with ball_possession!")
      
      #Ask whether a timeout is to be called        
      if self.sub_allowed == True and self.after_start_flag == True and \
         off_team.game['Timeouts'] > 0:
        reply = input(off_team.name + " has " + \
                      str(off_team.game['Timeouts']) + \
                      " timeouts remaining. Call timeout(Y|N)? ")           
        reply = reply.rstrip()
        timeout_reply = False
        while timeout_reply == False:
          if reply in ['Yes','yes','Y','y']:
            timeout_reply = True      
            self.timeout(home_pos)
            self.after_TO_flag = True
            off_team.game['Timeouts'] -= 1
            self.prev_off_reb == None
            print (off_team.name + " has " + str(off_team.game['Timeouts']) +\
                   " timeouts remaining.")
          
          elif reply in ['No','no','N','n']:
            timeout_reply = True
          else:
            print ("***You did no enter a valid response.*** ")
            reply = input("Call timeout(Y|N)? ")
            reply = reply.rstrip()
        
      possession_obj = Possession(self,self.game_type)
      possession_obj.run_possession()      
      '''
      if possession_obj.foul_drawn == True:
        if def_team.players[possession_obj.fouler].game['Stats']['Fouls'] == \
                                                         FOUL_OUT_THRESHOLD - 1:
          possession_obj.fouled_out = True
      '''   
      self.after_TO_flag = False
      if self.after_start_flag == False:
         self.after_start_flag = True
      self.time_dict['Time Remaining'] -= possession_obj.time
      
      self.update_all_stats(possession_obj)
      # Play-by-play print
      self.print_play_by_play(possession_obj)
      
      if ((possession_obj.off_rebound == False) | (possession_obj.reb_avail == False)):
        self.ball_possession *= -1 
        self.sec_chance_flag = False
        self.prev_off_reb = None
      else:
        self.sec_chance_flag = True      
        self.prev_off_reb = possession_obj.rebounder
    self.print_between_period_play_by_play(True,self.number,self.tot_number)
    return