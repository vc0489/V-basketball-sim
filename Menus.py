from StatsDisplayFunctions import *
  
def player_P40_stats_menu(game_dir):
  return
  
def player_eff_stats_menu(game_dir):
  print ("[4] Rank by FG%")
  print ("[5] Rank by 2P%")
  print ("[6] Rank by 3P%")
  print ("[7] Rank by eFG%")
  print ("[8] Rank by FT%")
   
  return
  
def player_impact_stats_menu(game_dir):
  return

def player_stats_menu(l_obj):
  chosen = False
  while chosen == False:
    print ("Please choose category:")
    print ("[1] Basic stats")
    print ("[2] Advanced stats")
    print ("[3] Efficiency stats")
    print ("[4] Game impact stats")
    print ("[5] Go back")
    reply = input("-->").rstrip()
    if reply == '1':
      basic_stats_func(l_obj)
    elif reply == '2':
      adv_stats_func(l_obj)
    elif reply == '3':
      #player_total_stats_menu
      eff_stats_func(l_obj)
    elif reply == '4':
      #player_eff_stats_menu(game_dir)
      display_impact_stat(l_obj)
    elif reply == '5':
      chosen = True
    else:
      print ("***Invalid option entered. Please try again.***" )
  return    

'''   
def between_game_menu(league_record_dict,game_dir,year):
  while 1:
    print ("Please select option:")
    print ("[0] Next match")
    print ("[1] View standings")
    print ("[2] View schedule")
    print ("[3] View results")
    print ("[4] View head-to-head results")
    print ("[5] View player stats")
    print ("[6] View team stats")
    # Include view rosters, sign/cut/(trade) players
    print ("[7] Team management")
    print ("[8] Quit game")
    reply = input("-->").rstrip()
    if reply == '0': 
      break
    elif reply == '1':
      print_standings(league_record_dict)
      input('Press any key to return to menu:')
    elif reply == '2':      
      print ('***Functionality not available yet***')
    elif reply == '3':
      print ('***Functionality not available yet***')
    elif reply == '4':
      print ('***Functionality not available yet***')
    elif reply == '5':
      player_stats_menu(game_dir,year) 
      
    elif reply == '6':
      print ('***Functionality not available yet***')
    elif reply == '7':
      print ('***Functionality not available yet***')    
    elif reply == '8':
      print ('***Functionality not available yet***')
  
  return
'''
