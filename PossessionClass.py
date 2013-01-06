import random
from GlobalFunctions import *

#------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------    
def generate_clutch_props_dict(ranking):
  prop_dict = {}
  base_prop = 5
  base_interval = 15
  interval_change = 5
  
  for i in range(len(ranking)):
    prop_dict[ranking[i]] = base_prop
    base_prop += base_interval
    base_interval += interval_change
  #print ('Prop dict:',prop_dict)
  return (prop_dict) 

def generate_clutch_pass_rate_dict(ranking):
  rate_dict = {}
  base_rate = 10
  base_interval = 10
  
  for i in range(len(ranking)):
    rate_dict[ranking[i]] = base_rate
    base_rate += base_interval
  return (rate_dict) 

def choose_thing_from_ratings(ratings_dict):
  random.seed()
  X = random.random()
  Y = 0
  tot_rating = sum(ratings_dict.values())
  for thing in ratings_dict.keys():
    if ((Y + ratings_dict[thing])/tot_rating > X):
      return (thing)  
    else:
      Y += ratings_dict[thing]
  return

class Possession:
  def __init__(self,period_obj,game_type):
    self.game_type = game_type
    if period_obj.ball_possession == 1:
      self.o_team = period_obj.home
      self.d_team = period_obj.away
      self.off_player_atts = period_obj.home_player_atts
      self.def_player_atts = period_obj.away_player_atts
         
    elif period_obj.ball_possession == -1:
      self.o_team = period_obj.away
      self.d_team = period_obj.home
      self.off_player_atts = period_obj.away_player_atts
      self.def_player_atts = period_obj.home_player_atts
    self.o_name = self.o_team.name
    self.d_name = self.d_team.name

    self.clutch = period_obj.clutch_flag
    self.sec_chance_flag = period_obj.sec_chance_flag
    self.shot_type_points_dict = {0:2,1:2,2:3}
    self.ball_possession = period_obj.ball_possession
    self.time_remaining = period_obj.time_dict['Time Remaining']
    
    self.score_diff = period_obj.score_diff
    
    self.prev_off_reb = period_obj.prev_off_reb
    self.put_back = False
    self.put_back_made = None
    self.after_TO_flag = period_obj.after_TO_flag
    #--------------------------------------------------------------------------
    # Possession info attributes: (* denotes for future)
    # --> ball_sequence   - Contains (in order) who had possession of the ball
    # --> clean*          - True  -- No turnover (shot taken/foul at the end) 
    #                     - False -- Possession ended with a turnover
    # --> stealer*        - Player who stole the ball
    # --> blocker*        - Player who blocked the shot
    # --> shooter         - Player who shot the ball/drew a foul
    # --> shot_type       - 0 - Inside shot
    #                     - 1 - 2Pt Jumper
    #                     - 2 - 3Pt Jumper
    # --> foul_drawn      - True  -- Foul drawn
    #                     - False -- No foul drawn
    # --> fouler          - Player who fouled (None -- No foul drawn)
    # --> shot_result     - None  -- No shot (either FTs or turnover)
    #                     - True  -- Made shot
    #                     - False -- Missed shot
    # --> assist          - None  -- No shot made
    #                     - False -- Shot made but no assist
    #                     - True  -- Shot made on an assist
    # --> assister        - Player with the (potential) assist
    # --> FT_result       - Contains (in order) the sequence of FT made/missed
    #                       (1 for make, 0 for miss) (None -- no FTs)
    # --> reb_avail       - True  -- Rebound available
    #                     - False -- Rebound not available
    # --> off_rebound     - True  -- Offensive player grabbed the rebound
    #                     - False -- Defensive player grabbed the rebound
    # --> rebounder       - Player who rebounded the ball
    # --> time            - Time the possession took
    # --> points_scored   - Total points scored
    # --> inside_flag     - True  -- Points (can be FTs) were a result of an 
    #                                inside shot
    #                     - False -- Points (can be FTs) were a result of a
    #                                perimeter shot
    #--------------------------------------------------------------------------
    self.ball_sequence = []
    self.shooter = None
    self.shot_type = None
    self.foul_drawn = None
    self.fouler = None
    self.fouled_out = None
    self.shot_result = None
    self.assist = None
    self.assister = None
    self.FT_result = None
    self.reb_avail = None
    self.off_rebound = None
    self.rebounder = None
    self.time = 0
    self.points_scored = 0
    self.inside_flag = None
    
    #--------------------------------------------------------------------------
    # Dict clutch_scenario
    # 
    # Variable 'Shot'
    # --> None - Any shot
    # -->    0 - 3Pt shot
    # -->    1 - 2Pt Jump shot (for intentional FTs)
    # -->    2 - Inside shot
    #         
    # Variable 'Time'
    # --> None - Normal
    # -->    X - Try to take X seconds 
    # 
    # Variable 'Time Spread'
    # --> None - Normal spread
    # -->    Y - The possession time is somewhere randomly within (X +/- Y)
    #
    # Variable 'Eff'
    # -->    0 - Normal
    # -->    1 - Higher
    # -->   -1 - Lower
    #
    # Variable 'Foul Worst'
    # -->  None - No foul
    # --> False - Foul anyone
    # -->  True - Try to foul the worst shooter 
    #--------------------------------------------------------------------------
    self.clutch_scenario = {'Shot':None,'Time':None,'Time Spread':None, \
                            'Eff':0,'Foul Worst':None}
    if (self.clutch == True):
      
      print (" ***Clutch situation***")
      init_message = 'Enter the number of the option you want executed' + \
                     '(enter "O" if you want to see the options again):'
      invalid_message = '\r\n***You did not enter a valid response.***'
      
      # Leading team has the ball
      if (self.score_diff * self.ball_possession > 0):
        
        #----------------------------------------------------------------------
        # Options (for defensive team):
        # --> 1 - To try fouling the worst FT shooter (normal time)
        # --> 2 - Quick foul with random person (quick)
        # --> 3 - Not foul
        #---------------------------------------------------------------------- 
        finished = False
        while finished == False:
          chosen = False
          print (self.d_name + ', what do you want to do?')
          print ('[1] - Try fouling the worst FT shooter')
          print ('[2] - Quick foul')
          print ('[3] - Do not foul')
          
          while chosen == False:
            reply = input(init_message)
            reply = reply.rstrip()
            
            if reply in ['O','o','0']:  
              chosen = True
            
            elif reply == '1':
              chosen = True
              finished = True
              self.clutch_scenario['Shot'] = 1
              self.clutch_scenario['Time'] = 6
              self.clutch_scenario['Time Spread'] = 5
              self.clutch_scenario['Foul Worst'] = True
                
            elif reply == '2':
              chosen = True
              finished = True
              self.clutch_scenario['Shot'] = 1
              self.clutch_scenario['Time'] = 2
              self.clutch_scenario['Time Spread'] = 1
              self.clutch_scenario['Foul Worst'] = False
                       
            elif reply == '3':
              finished = True   
              #----------------------------------------------------------------------
              # Options (for offensive team if no foul):
              # --> 1 - Waste as much time as possible (very low efficiency)
              # --> 2 - Normal possession
              #----------------------------------------------------------------------  
              print ('-------------------------------------')
              print (self.o_name + ', what do you want to do?')
              print ('[1] - Waste as much time as possible')
              print ('[2] - Normal possession')
              chosen_2 = False
              while chosen_2 == False: 
                reply_2 = input(init_message)           
                reply_2 = reply_2.rstrip()                           
            
                if reply_2 in ['O','o','0']:  
                  chosen_2 = True
            
                elif reply_2 == '1':
                  chosen = True
                  chosen_2 = True
                  self.clutch_scenario['Time'] = 21
                  self.clutch_scenario['Time Spread'] = 3
                  self.clutch_scenario['Eff'] = -1
                  self.prev_off_reb = None
                elif reply_2 == '2':
                  chosen = True
                  chosen_2 = True
  
                  self.clutch = False 
            
                else:
                  print(invalid_message)             
            
            else:
              print(invalid_message)  
        
      # Trailing team has the ball
      elif (self.score_diff * self.ball_possession < 0):
        #----------------------------------------------------------------------
        # More than a 1 possession game with more than 30 secs left
        #
        # Options (for offensive team):
        # --> 1 - Go for decent look at 3 (normal time, normal efficiency)
        # --> 2 - Go for quick 3 by good shooter (quick, lower efficiency)
        # --> 3 - Go for quick 2 by good shooter (quick, higher efficiency)
        # --> 4 - Normal possession
        #----------------------------------------------------------------------
        if abs(self.score_diff) > 3:
          finished = False
          while finished == False:
            chosen = False
            print (self.o_name + ', what do you want to do?')
            print ('[1] - Go for decent look at 3')
            print ('[2] - Go for a quick 3')
            print ('[3] - Go for a quick 2')
            print ('[4] - Normal possession')
          
            while chosen == False:
              reply = input(init_message)  
              reply = reply.rstrip()
            
              if reply in ['O','o','0']:  
                chosen = True
            
              elif reply == '1':
                chosen = True
                finished = True
                self.clutch_scenario['Shot'] = 2
                self.prev_off_reb = None
              elif reply == '2':
                chosen = True
                finished = True
                self.clutch_scenario['Shot'] = 2
                self.clutch_scenario['Time'] = 5
                self.clutch_scenario['Time Spread'] = 3
                self.clutch_scenario['Eff'] = -1
                self.prev_off_reb = None
              elif reply == '3':
                chosen = True
                finished = True 
                self.clutch_scenario['Shot'] = 0
                self.clutch_scenario['Time'] = 5
                self.clutch_scenario['Time Spread'] = 3
                self.clutch_scenario['Eff'] = 1
                
              elif reply == '4':
                chosen = True
                finished = True
                self.clutch = False                   
                                       
              else:
                print(invalid_message)    
                       
        #----------------------------------------------------------------------
        # Lead of 3 with less than 48 seconds left
        # 
        # Options (for offensive team):
        # --> 1 - Go for tying 3 by best shooter 
        #         (normal time, normal efficiency)
        # --> 2 - Go for quick 2 (normal time, normal efficiency)
        # --> 3 - Normal possession
        #----------------------------------------------------------------------
        if ((self.time_remaining < 48) & (abs(self.score_diff) == 3)):
          finished = False
          while finished == False:
            chosen = False
            print (self.o_name + ', what do you want to do?')
            print ('[1] - Go for decent look at a tying 3')
            print ('[2] - Go for a quick 2')
            print ('[3] - Normal possession')
          
            while chosen == False:
              reply = input(init_message)  
              reply = reply.rstrip()
            
              if reply in ['O','o','0']:  
                chosen = True
            
              elif reply == '1':
                chosen = True
                finished = True
                self.clutch_scenario['Shot'] = 2
                self.prev_off_reb = None
              elif reply == '2':
                chosen = True
                finished = True   
                self.clutch_scenario['Shot'] = 0
                self.clutch_scenario['Time'] = 5
                self.clutch_scenario['Time Spread'] = 3
               
              elif reply == '3':
                chosen = True
                finished = True    
                self.clutch = False
                                         
              else:
                print(invalid_message)    
                          
        #----------------------------------------------------------------------
        # Less than 3 point difference with less than 30 secs left
        #
        # Options (for offensive team):
        # --> 1 - Go for a decent look at 3 (normal time, normal efficiency)
        # --> 2 - Go for a decent look at 2 (normal time, normal efficiency)
        # --> 3 - Go for a quick 3 (lower efficiency)
        # --> 4 - Go for a quick 2 (lower efficiency)
        # --> 5 - Normal possession
        #----------------------------------------------------------------------
        elif ((self.time_remaining < 30) & (abs(self.score_diff) < 3)):      
          finished = False
          while finished == False:
            chosen = False
            print (self.o_name + ', what do you want to do?')
            print ('[1] - Go for a decent look at 3')
            print ('[2] - Go for a decent look at 2')
            print ('[3] - Go for a quick 3')
            print ('[4] - Go for a quick 2')
            print ('[5] - Normal possession')
          
            while chosen == False:
              reply = input(init_message)  
              reply = reply.rstrip()
            
              if reply in ['O','o','0']:  
                chosen = True
            
              elif reply == '1':
                chosen = True
                finished = True
                self.clutch_scenario['Shot'] = 2
                self.prev_off_reb = None
              elif reply == '2':
                chosen = True
                finished = True   
                self.clutch_scenario['Shot'] = 0
                
              elif reply == '3':
                chosen = True
                finished = True   
                self.clutch_scenario['Shot'] = 2
                self.clutch_scenario['Eff'] = -1
                self.prev_off_reb = None
              elif reply == '4':
                chosen = True
                finished = True   
                self.clutch_scenario['Shot'] = 2
                self.clutch_scenario['Eff'] = -1

              elif reply == '5':
                chosen = True
                finished = True                                   
                self.clutch = False
            
              else:
                print(invalid_message)       
     
      # Teams are tied
      else:
        #----------------------------------------------------------------------
        # Less than 30 seconds left
        #
        # Options (for offensive team):
        # --> 1 - Waste as much time as possible (lower efficiency)
        # --> 2 - Normal possession
        #----------------------------------------------------------------------
        if self.time_remaining < 30:  
          finished = False
          while finished == False:
            chosen = False
            print (self.o_name + ', what do you want to do?')
            print ('[1] - Waste as much time as possible')
            print ('[2] - Normal possession')
          
            while chosen == False:
              reply = input(init_message)  
              reply = reply.rstrip()
            
              if reply in ['O','o','0']:  
                chosen = True
            
              elif reply == '1':
                chosen = True
                finished = True
                self.clutch_scenario['Time'] = 21
                self.clutch_scenario['Time Spread'] = 3
                self.clutch_scenario['Eff'] = -1
                self.prev_off_reb = None
                
              elif reply == '2':
                chosen = True
                finished = True   
                self.clutch = False
                                            
              else:
                print(invalid_message)       

        #----------------------------------------------------------------------
        # Less than 48 seconds left
        #
        # Options (for offensive team):
        # --> 1 - Go for a 2 for 1 (lower efficiency)
        # --> 2 - Normal possession
        #----------------------------------------------------------------------
        elif self.time_remaining < 48:
     
          finished = False
          while finished == False:
            chosen = False
            print (self.o_name + ', what do you want to do?')
            print ('[1] - Go for a 2 for 1')
            print ('[2] - Normal possession')
          
            while chosen == False:
              reply = input(init_message)  
              reply = reply.rstrip()
            
              if reply in ['O','o','0']:  
                chosen = True
            
              elif reply == '1':
                chosen = True
                finished = True
                self.clutch_scenario['Time'] = self.time_remaining - 27
                self.clutch_scenario['Time Spread'] = 3
                self.clutch_scenario['Eff'] = -1
                
              elif reply == '2':
                chosen = True
                finished = True   
                self.clutch = False
                                            
              else:
                print(invalid_message)     
      #print(self.clutch_scenario)   
      

  #----------------------------------------------------------------------------
  # Function to determine who is the initial ball handler 
  #----------------------------------------------------------------------------
  def first_possession(self):
    if self.clutch_scenario['Foul Worst'] in [True,False]:
      FT_eff_dict = {}
      for player in self.off_player_atts:
        FT_eff_dict[player] = self.off_player_atts[player]['FT Eff']
      
      if self.clutch_scenario['Foul Worst'] == True:
        ranking = F_RANK_FROM_RATINGS(FT_eff_dict,descending = True)
      elif self.clutch_scenario['Foul Worst'] == False:
        ranking = F_RANK_FROM_RATINGS(FT_eff_dict,descending = False)
        
      fouled_prop_dict = generate_clutch_props_dict(ranking)      
      player = choose_thing_from_ratings(fouled_prop_dict)
      
    elif self.clutch_scenario['Shot'] in [0,2]:
      
      if self.clutch_scenario['Shot'] == 0:
        eff_dict = {}
        for player in self.off_player_atts:
          eff_dict[player] = self.off_player_atts[player]['Inside Eff']
      
      elif self.clutch_scenario['Shot'] == 2:
        eff_dict = {}
        for player in self.off_player_atts:
          eff_dict[player] = self.off_player_atts[player]['3Pt Jumper Eff']
      
      eff_ranking = F_RANK_FROM_RATINGS(eff_dict,descending = False)
      
      ball_dom_dict = generate_clutch_props_dict(eff_ranking)
      player = choose_thing_from_ratings(ball_dom_dict)
    
    elif self.sec_chance_flag == True and self.prev_off_reb:
      random.seed()
      X = random.random()
      if X < 0.333:
        self.put_back = True
        player = self.prev_off_reb
      else:
        ball_dom_dict = {}
        for player in self.off_player_atts:
          ball_dom_dict[player] = self.off_player_atts[player]['Ball Dom']
        player = choose_thing_from_ratings(ball_dom_dict)    
    else:
      ball_dom_dict = {}
      for player in self.off_player_atts:
        ball_dom_dict[player] = self.off_player_atts[player]['Ball Dom']
      player = choose_thing_from_ratings(ball_dom_dict)
    
    self.ball_sequence.append(player)
    return
  
  #----------------------------------------------------------------------------
  # Function to determine whether a pass is made or not 
  #----------------------------------------------------------------------------
  def pass_function(self):
    if self.clutch_scenario['Foul Worst'] in [True,False]:
      self.shooter = self.ball_sequence[-1]
      return
    elif self.clutch_scenario['Shot'] in [0,2]:
      if self.clutch_scenario['Shot'] == 0:
        eff_dict = {}
        for player in self.off_player_atts:
          eff_dict[player] = self.off_player_atts[player]['Inside Eff']
      
      elif self.clutch_scenario['Shot'] == 2:
        eff_dict = {}
        for player in self.off_player_atts:
          eff_dict[player] = self.off_player_atts[player]['3Pt Jumper Eff']    
    
      eff_ranking = F_RANK_FROM_RATINGS(eff_dict,descending = True)
      pass_dict = generate_clutch_pass_rate_dict(eff_ranking)
      pass_rate = pass_dict[player]
    elif self.put_back == True:
      self.shooter = self.ball_sequence[-1]
      return
    else:
      pass_rate = self.off_player_atts[self.ball_sequence[-1]]['Pass Rate']
      
    random.seed()
    X = random.random()
      
    if X*100 < pass_rate:
      self.assister = self.ball_sequence[-1]
      passee = self.assister
      while passee == self.assister:
        passee = random.choice(list(self.off_player_atts.keys()))
      self.shooter = passee
      self.ball_sequence.append(self.shooter)    
    
    else:
      self.shooter = self.ball_sequence[-1]
    
    return
  
  #----------------------------------------------------------------------------
  # Function to determine what the shot type is 
  #----------------------------------------------------------------------------
  def shot_type_function(self):
    if self.clutch_scenario['Shot'] in [0,1,2]:      
      self.shot_type = self.clutch_scenario['Shot']
    elif self.put_back == True:
      self.shot_type = 0
    else:
      shot_type_dict = {0:self.off_player_atts[self.shooter]['Inside Prop'] ,\
                        1:self.off_player_atts[self.shooter]['2Pt Jumper Prop'] ,\
                        2:self.off_player_atts[self.shooter]['3Pt Jumper Prop']}
    
      self.shot_type = choose_thing_from_ratings(shot_type_dict) 
    
    return

  #----------------------------------------------------------------------------
  # Function to determine whether a foul occurs and who the fouler is 
  #
  # Returns: 1 - Foul drawn
  #          0 - No foul drawn
  #----------------------------------------------------------------------------
  def foul_function(self): 
    
    if self.clutch_scenario['Foul Worst'] in [True,False]:
      self.foul_drawn = True
      self.fouler = random.choice(list(self.def_player_atts.keys()))
      (' Intentional foul committed by ' + self.fouler)
     
      self.check_foul_out()
      
    else:
      random.seed()
      X = 100*random.random()

      def_rating_dict = {}
      if self.shot_type == 0:
        def_rating_name = 'Inside Def'
        off_rating_name = 'Inside Foul Rate'
      elif ((self.shot_type == 1) | (self.shot_type == 2)):
        def_rating_name = 'Perimeter Def'
        off_rating_name = 'Per Foul Rate'
      else:
        print ("BUG! Invalid shot type!")
    
      for player in self.def_player_atts:
        #print (def_player_atts)
        def_rating_dict[player] = self.def_player_atts[player][def_rating_name]
    
      foul_chance = (self.off_player_atts[self.shooter][off_rating_name]/4) \
                  * (1 - (sum(def_rating_dict.values()) - 250)/275)

      if X < foul_chance:
        self.foul_drawn = True
        self.fouler = choose_thing_from_ratings(def_rating_dict)
        self.check_foul_out()
                                                      
      
    return
  
  def check_foul_out(self):
    if self.game_type not in ('RS','AF','BF','VF'):
      return
    print ('ERROR',self.game_type)
    if self.d_team.players[self.fouler].game['Stats']['Fouls'] == \
                                                       FOUL_OUT_THRESHOLD - 1:
      self.fouled_out = True
      print ('***' + self.fouler + ' has fouled out!***')
      F_PRINT_P_GRADES(self.d_team.game['Avail Subs'],'TO',None,self.d_team)
      self.sub_in = None
      while not self.sub_in:
        reply = input('Please choose substitute:').rstrip()
        if reply in self.d_team.game['Avail Subs']:
          self.sub_in = reply
          self.d_team.game['Fouled Out'].append(self.fouler)
          self.d_team.game['Avail Subs'].remove(self.sub_in)
          self.d_team.game['On Court'].append(self.sub_in)
          self.d_team.game['On Court'].remove(self.fouler)
          self.d_team.players[self.fouler].game['Court Status'] = -1
          self.d_team.players[self.sub_in].game['Court Status'] = 1
          del self.def_player_atts[self.fouler]
          self.def_player_atts[self.sub_in] = self.d_team.players[self.sub_in].game_attributes
        else:
          print ('Invalid player entered, please try again.')      
    
    return
  
  def FT_function(self):
    self.FT_result = []
    random.seed()
    Tot_FTs = self.shot_type_points_dict[self.shot_type]
   
    if self.shot_type == 0:
      self.inside_flag = True
    else:
      self.inside_flag = False
    
    for FT in range(Tot_FTs):
      X = 100*random.random()
      if X < self.off_player_atts[self.shooter]['FT Eff']:
        self.FT_result.append(1)
      else:
        self.FT_result.append(0)
    self.points_scored = sum(self.FT_result)
    if self.FT_result[-1] == 0:
      self.reb_avail = True
    else:
      self.reb_avail = False
    #print (self.FT_result,self.reb_avail,self.points_scored)
    return

  def shoot_function(self):
    random.seed()
    X = 100*random.random()
    def_sum = 0
    if self.time_remaining < 10 :
      if self.after_TO_flag == True:
        chance_factor = 1 - 0.4*(10-self.time_remaining)/10
      else:
        chance_factor = 1 - 0.8*(10-self.time_remaining)/10
      print ("VC: chance_factor = " + str(chance_factor))
    else:
      chance_factor = 1
    if self.assister:
      def_sum -= 1.2*self.off_player_atts[self.assister]['Pass Eff']
    if (self.shot_type == 0):
      self.inside_flag = True
      for player in self.def_player_atts:
        def_sum += self.def_player_atts[player]['Inside Def']
      if self.put_back == True:
        put_back_eff = self.off_player_atts[self.shooter]['Inside Eff']*1.15
        if put_back_eff < 90:
          put_back_eff = 90
        shot_chance = (put_back_eff - (def_sum / 8.5) + 16) / 1.5          
      else:
        shot_chance = chance_factor*(self.off_player_atts[self.shooter]['Inside Eff']\
                     - (def_sum / 8.5) + 16) / 1.5
    else:
      self.inside_flag = False
      for player in self.def_player_atts:
        def_sum += self.def_player_atts[player]['Perimeter Def']
      if (self.shot_type == 1):
        shot_chance = chance_factor*(self.off_player_atts[self.shooter]['2Pt Jumper Eff']\
                       - (def_sum / 8.5) + 16) / 1.8
      elif (self.shot_type == 2):
        shot_chance = chance_factor*(self.off_player_atts[self.shooter]['3Pt Jumper Eff']\
                       - (def_sum / 8.5) + 16) / 2.25
      else:
        print ("BUG! Invalid shot type!")

    if X < shot_chance:
      self.shot_result = True
      if self.put_back == True:
        self.put_back_made = True
      self.points_scored = self.shot_type_points_dict[self.shot_type]
      self.reb_avail = False
      if self.assister:
        self.assist = True
      else:
        self.assist = False
    else:
      if self.put_back == True:
        self.put_back_made = False
      self.shot_result = False
      self.reb_avail = True
    #print (self.shot_result,self.reb_avail,self.points_scored,self.assist)
    return

  def rebound_function(self):
    rebound_dict = {}
    for player in self.off_player_atts:
      rebound_dict[player] = self.off_player_atts[player]['Off Reb']
    for player in self.def_player_atts:
      rebound_dict[player] = self.def_player_atts[player]['Def Reb']
    self.rebounder = choose_thing_from_ratings(rebound_dict)
    if self.rebounder in self.off_player_atts.keys():
      self.off_rebound = True
    else:
      self.off_rebound = False
    #print (self.off_rebound,self.rebounder)
    
    return
  
  def time_function(self):
    
    random.random()
    X = random.random()
    
    if self.put_back == True:
      
      self.time = int(3*X) + 1 
    elif ((self.clutch == False) | (not self.clutch_scenario['Time'])):
      self.time = int(18*X) + 6

    else:
      self.time = int((2*self.clutch_scenario['Time Spread'] + 1)*X) + \
                  self.clutch_scenario['Time'] - self.clutch_scenario['Time Spread']
    if self.time > self.time_remaining:
      self.time = self.time_remaining
    return
  
  def adjust_eff_clutch(self,reverse):
    mag = 10
    for player in self.off_player_atts.keys():
      self.off_player_atts[player]['Inside Eff'] += mag*reverse*self.clutch_scenario['Eff']
      self.off_player_atts[player]['2Pt Jumper Eff'] += mag*reverse*self.clutch_scenario['Eff']
      self.off_player_atts[player]['3Pt Jumper Eff'] += mag*reverse*self.clutch_scenario['Eff']
    return
    
  def run_possession(self):
    
    # Adjust for clutch situations
    if ((self.clutch == True) & (self.clutch_scenario['Eff'] != 0)):
      self.adjust_eff_clutch(1)
      
    # First determine who has first possession
    self.first_possession()
    
    #self.ball_sequence.append(ball_handler)
    
    # Determine whether a pass has been made and if so who received the pass
    self.pass_function()
    
    # Determine shot type
    self.shot_type_function()

    # Determine whether a foul has occurred
    self.foul_function()
    if self.foul_drawn == True:
      self.FT_function()
    else:
      self.shoot_function()
    
    if self.reb_avail == True:
      self.rebound_function()
    
    self.time_function()
    
    # Adjust back for clutch situations
    if ((self.clutch == True) & (self.clutch_scenario['Eff'] != 0)):
      self.adjust_eff_clutch(-1)    
    
    return