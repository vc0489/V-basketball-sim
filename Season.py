import os
import re
import csv
import random 
import shutil
import copy
import math
from GlobalVariables import *
from LeagueClass import *
#from Menus import *

'''
def temp_create_att_files():
  att_dir = 'Teams' + os.sep + 'Attributes'
  teams = os.listdir(att_dir)
  p_att_dir = 'Attributes'
  if not os.path.exists(p_att_dir):
    os.makedirs(p_att_dir)
  
    
  for team in teams:
    file_name = att_dir + os.sep + team
    reader = csv.reader(open(file_name, newline = ''))
    players_data = [] 
    for row in reader:
      players_data.append(row)
    
    team_name = players_data[0][0]   
                
    for j in range(1,len(players_data[0])):
      name = players_data[0][j]
      
      #player_dir = att_dir + '\\' + name
      #if not os.path.exists(player_dir):
      #  os.makedirs(player_dir)
      player_file_name = p_att_dir + os.sep + name + '.txt'
      
      
      att_dict = {'Team':NAME_TO_NICK[team_name]}
      att_dict['Draft'] = players_data[1][j]
      draft_pos = players_data[1][j]
      draft_year = draft_pos.split('.')[0]
      year = 11
      y_pro = year - int(draft_year)
      att_dict['YPro'] = str(y_pro)
      att_dict['Age'] = str(y_pro + 20)
      
      att_dict['InPro'] = players_data[2][j]
      att_dict['2JPro'] = players_data[3][j]
      att_dict['3PPro'] = players_data[4][j]
      
      att_dict['InEff'] = players_data[5][j]
      att_dict['2JEff'] = players_data[6][j]
      att_dict['3PEff'] = players_data[7][j]
    
      att_dict['OReb'] = players_data[8][j]
      att_dict['DReb'] = players_data[9][j]
      att_dict['BDom'] = players_data[10][j]
      att_dict['PassR'] = players_data[11][j]
      att_dict['PassE'] = players_data[12][j]
      
      att_dict['InDef'] = players_data[13][j]
      att_dict['PerDef'] = players_data[14][j]
      att_dict['InFR'] = players_data[15][j]
      att_dict['PerFR'] = players_data[16][j]
    
      att_dict['FTEff'] = players_data[17][j]
          
      att_dict['GSus'] = players_data[18][j]
      att_dict['GInj'] = players_data[19][j]
      
  
      write_seq = ('Draft','Age','YPro','Team','InPro','2JPro','3PPro','InEff',\
                   '2JEff','3PEff','OReb','DReb','BDom','PassR','PassE',\
                   'InDef','PerDef','InFR','PerFR','FTEff','GSus','GInj')
      
      with open(player_file_name,'w') as f:
        title_line = ''
        for stat in write_seq:
          title_line += stat + ' '
        title_line = title_line[:-1]
        
        line = ''
        for stat in write_seq:
          line += '{:>{l}}'.format(att_dict[stat],l=len(stat)) + ' '
        line = line[:-1]
        
        f.write(title_line + '\n')
        f.write(line + '\n')
  return
  
  
def temp_create_rosters():
  
  roster_dir = 'Rosters'
  att_dir = 'Teams' + os.sep + 'Attributes'
  teams = os.listdir(att_dir)
  
  for team in teams:
    
    file_name = att_dir + os.sep + team
    reader = csv.reader(open(file_name, newline = ''))
    
    players = next(reader)
    team_name = players[0]  
    roster_file_name = roster_dir + os.sep + team_name + '.txt'
    with open(roster_file_name,'w') as roster_f:
      for player in sorted(players[1:]):
        roster_f.write(player + '\n')
      
  return       
    
def create_att_files(load_dir):
  att_dir = load_dir + os.sep + 'attributes' + os.sep 
  if not os.path.exists(att_dir):
    os.makedirs(att_dir)
  
  return
'''  
def choose_mode():
  chosen = False
  while chosen == False:
    print ("Choose game mode:")
    print ("[1] Single game")
    print ("[2] Season")
    print ("[3] Dynasty")
  
    reply = input("->").rstrip()
  
    if reply == '1':
      chosen = True
      single_game()
    elif reply == '2':
      chosen = True
      season()
    elif reply == '3':
      print ("***Option not available yet, please try again***")
    else:
      print ("***You did not choose a valid option, please try again***")
  return


# VC: Need fixing!
'''
def single_game(save_dir='Test'):
  load_dir = 'Free_play' + os.sep + save_dir
  teams_dir = load_dir + os.sep + "Rosters"
  teams = os.listdir(teams_dir)
  teams_dict = {}
  count = 1
  for team in teams:
    teams_dict[str(count)] = team.split('.')[0]
    count += 1
    
  def print_teams(teams_dict,away_team = None):
    print ("Teams:")
    count = 1
    for i in range(len(teams_dict)):
      if teams_dict[str(i+1)] == away_team:
        print ('[' + str(i+1) + '] ' + teams_dict[str(i+1)] + ' (AWAY)')
      else:
        print ('[' + str(i+1) + '] ' + teams_dict[str(i+1)])
      count += 1
    return 
  
  
  away_chosen = False
  while away_chosen == False:
    print_teams(teams_dict)
    reply = input("Choose away team:").rstrip()
    if reply in teams_dict:
      away_chosen = True
      away_team = teams_dict[reply]
    else:
      print ("***Invalid input, please try again***")
      
  home_chosen = False    
  while home_chosen == False:
    print_teams(teams_dict,away_team)
    reply = input("Choose home team:").rstrip()
    if teams_dict[reply] == away_team:
      print ("***" + away_team + " is the away team, please choose another team***")
    elif reply in teams_dict:  
      home_chosen = True
      home_team = teams_dict[reply]
    else:
      print ("***Invalid input, please try again***")
  
  game_type = 'RS'
  year = 0
  game = det_game(year,load_dir,game_type)
  VBA_match.game(home_team,away_team,load_dir,game_type,0,game)
  
  return
'''

#-------------------------------------------------------------------------------
# Function season
#
# Operation: Runs a season
#-------------------------------------------------------------------------------    
def season():

  saved_dir = 'Season'
  
  if os.path.exists(saved_dir):
    saved_leagues = os.listdir(saved_dir)

    if len(saved_leagues) > 0:
      chosen = False
      while chosen == False:
        print ("Please select option")
        print ("[1] Load saved league")
        print ("[2] Create new league")
        reply = input("-->").rstrip()
        if reply == '1':
          print ("Saved leagues:")
          for saved_league in saved_leagues:
            print ("-> " + saved_league)
          reply_2 = input("Please enter the league you would like to load:").rstrip()
          if reply_2 in saved_leagues:
            league_name = reply_2
            print ("Loading " + reply_2 + "...")
            chosen = True
            new_league = False
          else:
            print (reply_2 + " does not exist, please try again.\n")
        elif reply == '2':
          reply_2 = input("Enter a name for your season: ").rstrip()
          if reply_2 in saved_leagues:
            print ("League name already exists, please try again.\n")
          else:
            chosen = True
            league_name = reply_2
            new_league = True
        else:
          print ("Invalid option entered, please try again.\n")
    else:
      print ("There are no saved leagues, creating new season...")
      league_name = input("Enter a name for your league:").rstrip()
      new_league = True
  else:
    os.makedirs(saved_dir)
    print ("There are no saved seasons, creating new league...")
    league_name = input("Enter a name for your league:").rstrip()
    new_league = True   
    
  # Generate directory and schedule for new season                         
  league_obj = League(league_name,new_league)
  
  return


  
def dynasty():
  return
  
