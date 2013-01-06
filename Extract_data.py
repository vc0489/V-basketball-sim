import re
import csv
import decimal
import operator

def print_rank(rank_tuples,min=0,max_rank=None):
  rank_len = 4
  name_len = 5
  value_len = 3
  rank = 0
  prev_value = None
  for item in rank_tuples:
    rank += 1
    
    if item[1] < min:
      break
    if item[1] == prev_value:
      print (' '*rank_len + '{:<{len}}'.format(item[0],len=name_len) +\
             '{:>{len}}'.format(str(item[1]),len=value_len))
    else:
      if max_rank and rank > max_rank:
        break
      print ('{:^{len}}'.format(str(rank),len=rank_len) + \
             '{:<{len}}'.format(item[0],len=name_len) +\
             '{:>{len}}'.format(str(item[1]),len=value_len))
    prev_value = item[1]
  return
  

def extract_team_data():
  ONE_DP = decimal.Decimal(10) ** -1
  stats_names = ('Player','2PM','2PA','3PM','3PA','FTM','FTA','OReb','DReb',\
                 'Assists','Fouls','Points')  
  output_stats_order = ('FGM','FGA','FG%','2PM','2PA','2P%','3PM','3PA',\
                        '3P%','FTM','FTA','FT%','OReb','DReb','TReb','Assists',\
                        'Fouls','Points')
  output_HtH_order = ('v. WIL','v. LAT','v. CRO','v. QUE','v. BRE','v. HAR','v. KEN','v. RAY',\
                      '@ WIL','@ LAT','@ CRO','@ QUE','@ BRE','@ HAR','@ KEN','@ RAY')
  forty_pt_games = {}
  thirty_pt_games = {}
  twenty_reb_games = {}
  twenty_ast_games = {}
  five_threes_games = {}
  ten_fta_games = {}
  triple_double_games = {}
  games_suspended = {}
  twenty_twenty_games = {}
  all_games_file = 'All_Games.txt'
  output_all = open(all_games_file,'w')
  for year in range(1,11): 
    #file = 'Year_' + str(year) + '_Season_Schedule.txt'
    file = 'Year_' + str(year) + '_Playoff_Schedule.txt'
    data_dir = 'C:\\Users\\shchen\\Dropbox\\VBA\\Year ' + str(year) + '\\VBA Results\\'
    
    
    '''
    output_file = 'Year_' + str(year) + '_Stats.txt'
    output = open(output_file,'w')
    line = 'Team'
    for stat in output_stats_order:
      line += ' ' + stat
    line += ' Opp'
    for stat in output_stats_order:
      line += ' ' + stat    
    output.write(line)
    '''
    
    
    league_data = {}

    for line in open(file,'r'):
      #print (year)
      game,home,away = line.split()
      print (year,game,home,away)
      #game_file = data_dir + 'Boxscore_' + str(game) + '.csv'
      game_file = data_dir + 'Boxscore_P_' + str(game) + '.csv'
      game_reader = csv.reader(open(game_file, newline=''))
      
      home_flag = -1
      if home not in league_data:
        league_data[home] = {}
      if away not in league_data:
        league_data[away] = {}

        
      league_data[home][game] = {'Home':True,'Opponent':away,\
                                  'Team Stats':{},'Opp Stats':{}}
      league_data[away][game] = {'Home':False,'Opponent':home,\
                                  'Team Stats':{},'Opp Stats':{}}
      home_totals = {}
      away_totals = {}
      home_stats = {'2PM':0,'2PA':0,'3PM':0,'3PA':0,'FTM':0,'FTA':0,\
                    'OReb':0,'DReb':0,'Assists':0,'Fouls':0,'Points':0,\
                    'FGM':0,'FGA':0,'TReb':0}
      away_stats = {'2PM':0,'2PA':0,'3PM':0,'3PA':0,'FTM':0,'FTA':0,\
                    'OReb':0,'DReb':0,'Assists':0,'Fouls':0,'Points':0,\
                    'FGM':0,'FGA':0,'TReb':0}

      for row in game_reader:
        
        if len(row) > 10 and row[-1] != '':
          if row[0] == 'Player':
            home_flag *= -1
          else:
            player = row[0]
            line = player + ' ' + str(year) + ' ' + str(game) + ' ' + str(home_flag) + ' '
            if home_flag == 1:
              league_data[home][game][player] = {}
              line += home + ' ' + away + ' '
              for i in range(1,len(stats_names)):
                stat = stats_names[i]
                league_data[home][game][player][stat] = row[i]
                
                home_stats[stat] += int(row[i])
                line += row[i] + ' '
                #print (player,stat,row[i])
               
              if int(league_data[home][game][player]['Points']) >= 40:
                if player in forty_pt_games:
                  forty_pt_games[player] += 1
                else:
                  forty_pt_games[player] = 1 
                   
              if int(league_data[home][game][player]['Points']) >= 35:                
                if player in thirty_pt_games:
                  thirty_pt_games[player] += 1
                else:
                  thirty_pt_games[player] = 1  
              TReb = int(league_data[home][game][player]['OReb']) + \
                 int(league_data[home][game][player]['DReb'])
              if TReb >= 20:                
                if player in twenty_reb_games:
                  twenty_reb_games[player] += 1
                else:
                  twenty_reb_games[player] = 1  

              if int(league_data[home][game][player]['Assists']) >= 20:                
                if player in twenty_ast_games:
                  twenty_ast_games[player] += 1
                else:
                  twenty_ast_games[player] = 1  

              if int(league_data[home][game][player]['3PM']) >= 5:                
                if player in five_threes_games:
                  five_threes_games[player] += 1
                else:
                  five_threes_games[player] = 1  

              if int(league_data[home][game][player]['FTA']) >= 10:                
                if player in ten_fta_games:
                  ten_fta_games[player] += 1
                else:
                  ten_fta_games[player] = 1  

              if int(league_data[home][game][player]['Points']) >= 10 and\
                 TReb >= 10 and\
                 int(league_data[home][game][player]['Assists']) >= 10:                
                if player in triple_double_games:
                  triple_double_games[player] += 1
                else:
                  triple_double_games[player] = 1  
                  
              if int(league_data[home][game][player]['Fouls']) >= 4:                
                if player in games_suspended:
                  games_suspended[player] += \
                    int(league_data[home][game][player]['Fouls']) - 3
                else:
                  games_suspended[player] = \
                    int(league_data[home][game][player]['Fouls']) - 3                   

              if int(league_data[home][game][player]['Points']) >= 20 and\
                 (TReb >= 20 or\
                 int(league_data[home][game][player]['Assists']) >= 20):                
                if player in twenty_twenty_games:
                  twenty_twenty_games[player] += 1
                else:
                  twenty_twenty_games[player] = 1
              
            else:
              league_data[away][game][player] = {}
              line += away + ' ' + home + ' '
              for i in range(1,len(stats_names)):
                stat = stats_names[i]
                league_data[away][game][player][stat] = row[i]
                away_stats[stat] += int(row[i])
                line += row[i] + ' '
                #print (player,stat,row[i])
             
              
              if int(league_data[away][game][player]['Points']) >= 40:
                if player in forty_pt_games:
                  forty_pt_games[player] += 1
                else:
                  forty_pt_games[player] = 1   

              if int(league_data[away][game][player]['Points']) >= 35:                  
                if player in thirty_pt_games:
                  thirty_pt_games[player] += 1
                else:
                  thirty_pt_games[player] = 1  
              TReb = int(league_data[away][game][player]['OReb']) + \
                 int(league_data[away][game][player]['DReb'])    
              if TReb >= 20:                
                if player in twenty_reb_games:
                  twenty_reb_games[player] += 1
                else:
                  twenty_reb_games[player] = 1  

              if int(league_data[away][game][player]['Assists']) >= 20:                
                if player in twenty_ast_games:
                  twenty_ast_games[player] += 1
                else:
                  twenty_ast_games[player] = 1  

              if int(league_data[away][game][player]['3PM']) >= 5:                
                if player in five_threes_games:
                  five_threes_games[player] += 1
                else:
                  five_threes_games[player] = 1  

              if int(league_data[away][game][player]['FTA']) >= 10:              
                if player in ten_fta_games:
                  ten_fta_games[player] += 1
                else:
                  ten_fta_games[player] = 1  

              if int(league_data[away][game][player]['Points']) >= 10 and\
                 TReb >= 10 and\
                 int(league_data[away][game][player]['Assists']) >= 10:                
                if player in triple_double_games:
                  triple_double_games[player] += 1
                else:
                  triple_double_games[player] = 1
                  
              if int(league_data[away][game][player]['Fouls']) >= 4:                
                if player in games_suspended:
                  games_suspended[player] += \
                    int(league_data[away][game][player]['Fouls']) - 3
                else:
                  games_suspended[player] = \
                    int(league_data[away][game][player]['Fouls']) - 3                    

              if int(league_data[away][game][player]['Points']) >= 20 and\
                 (TReb >= 20 or\
                 int(league_data[away][game][player]['Assists']) >= 20):                
                if player in twenty_twenty_games:
                  twenty_twenty_games[player] += 1
                else:
                  twenty_twenty_games[player] = 1
               
            line += '\n'
            output_all.write(line)                                
      home_stats['FGM'] = home_stats['2PM'] + home_stats['3PM']
      home_stats['FGA'] = home_stats['2PA'] + home_stats['3PA']
      home_stats['TReb'] = home_stats['OReb'] + home_stats['DReb']
      away_stats['FGM'] = away_stats['2PM'] + away_stats['3PM']
      away_stats['FGA'] = away_stats['2PA'] + away_stats['3PA']    
      away_stats['TReb'] = away_stats['OReb'] + away_stats['DReb']    
          
      league_data[home][game]['Team Stats'] = home_stats   
      league_data[home][game]['Opp Stats'] = away_stats  
      league_data[away][game]['Team Stats'] = away_stats  
      league_data[away][game]['Opp Stats'] = home_stats  
      #print (home_stats,away_stats)
      
    for team in league_data:
      
      season_stats = {'2PM':0,'2PA':0,'3PM':0,'3PA':0,'FTM':0,'FTA':0,\
                     'OReb':0,'DReb':0,'Assists':0,'Fouls':0,'Points':0,\
                     'FGM':0,'FGA':0,'TReb':0}  
      opp_season_stats = {'2PM':0,'2PA':0,'3PM':0,'3PA':0,'FTM':0,'FTA':0,\
                          'OReb':0,'DReb':0,'Assists':0,'Fouls':0,'Points':0,\
                          'FGM':0,'FGA':0,'TReb':0}                
      for game in league_data[team]:
        for stat in season_stats:
          season_stats[stat] += league_data[team][game]['Team Stats'][stat]
          opp_season_stats[stat] += league_data[team][game]['Opp Stats'][stat]
      
      season_stats['FG%'] = str(decimal.Decimal(float(100*season_stats['FGM'])/\
                                 season_stats['FGA']).quantize(ONE_DP))
      season_stats['2P%'] = str(decimal.Decimal(float(100*season_stats['2PM'])/\
                                 season_stats['2PA']).quantize(ONE_DP))
      season_stats['3P%'] = str(decimal.Decimal(float(100*season_stats['3PM'])/\
                                 season_stats['3PA']).quantize(ONE_DP))
      season_stats['FT%'] = str(decimal.Decimal(float(100*season_stats['FTM'])/\
                                 season_stats['FTA']).quantize(ONE_DP))                                 

      opp_season_stats['FG%'] = str(decimal.Decimal(float(100*opp_season_stats['FGM'])/\
                                 opp_season_stats['FGA']).quantize(ONE_DP))
      opp_season_stats['2P%'] = str(decimal.Decimal(float(100*opp_season_stats['2PM'])/\
                                 opp_season_stats['2PA']).quantize(ONE_DP))
      opp_season_stats['3P%'] = str(decimal.Decimal(float(100*opp_season_stats['3PM'])/\
                                 opp_season_stats['3PA']).quantize(ONE_DP))
      opp_season_stats['FT%'] = str(decimal.Decimal(float(100*opp_season_stats['FTM'])/\
                                 opp_season_stats['FTA']).quantize(ONE_DP)) 
      
      '''
      output.write('\n')
      line = team
      for stat in output_stats_order:
        line += ' ' + str(season_stats[stat])
      line += ' --'
      for stat in output_stats_order:
        line += ' ' + str(opp_season_stats[stat])      
      output.write(line)                                                                                               
      #print (team, season_stats, opp_season_stats)
      '''

    #output.close()
  output_all.close()
  forty_pt_rank = sorted(forty_pt_games.items(),key=operator.itemgetter(0))
  forty_pt_rank = sorted(forty_pt_rank,key=operator.itemgetter(1),reverse = True)
  print_rank(forty_pt_rank)
  print ('\n')
  thirty_pt_rank = sorted(thirty_pt_games.items(),key=operator.itemgetter(0))
  thirty_pt_rank = sorted(thirty_pt_rank,key=operator.itemgetter(1),reverse = True)
  print_rank(thirty_pt_rank)  
  print ('\n')
  twenty_reb_rank = sorted(twenty_reb_games.items(),key=operator.itemgetter(0))
  twenty_reb_rank = sorted(twenty_reb_rank,key=operator.itemgetter(1),reverse = True)
  print_rank(twenty_reb_rank) 
  print ('\n')
  twenty_ast_rank = sorted(twenty_ast_games.items(),key=operator.itemgetter(0))
  twenty_ast_rank = sorted(twenty_ast_rank,key=operator.itemgetter(1),reverse = True)
  print_rank(twenty_ast_rank) 
  print ('\n')
  five_threes_rank = sorted(five_threes_games.items(),key=operator.itemgetter(0))
  five_threes_rank = sorted(five_threes_rank,key=operator.itemgetter(1),reverse = True)
  print_rank(five_threes_rank) 
  print ('\n')
  ten_fta_rank = sorted(ten_fta_games.items(),key=operator.itemgetter(0))
  ten_fta_rank = sorted(ten_fta_rank,key=operator.itemgetter(1),reverse = True)
  print_rank(ten_fta_rank)    
  print ('\n')
  triple_double_rank = sorted(triple_double_games.items(),key=operator.itemgetter(0))
  triple_double_rank = sorted(triple_double_rank,key=operator.itemgetter(1),reverse = True)
  print_rank(triple_double_rank)   
  
  '''
  print ('\n')
  games_suspended_rank = sorted(games_suspended.items(),key=operator.itemgetter(0))
  games_suspended_rank = sorted(games_suspended_rank,key=operator.itemgetter(1),reverse = True)
  print_rank(games_suspended_rank,min=10,max_rank=50)     
  '''
  print ('\n')
  twenty_twenty_rank = sorted(twenty_twenty_games.items(),key=operator.itemgetter(0))
  twenty_twenty_rank = sorted(twenty_twenty_rank,key=operator.itemgetter(1),reverse = True)
  print_rank(twenty_twenty_rank)     
  return 
  