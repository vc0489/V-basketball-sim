import os

def fix_possessions():
  for season in os.listdir():
    print (season)
    player_dir = season + os.sep + 'data' + os.sep + 'Year_11' + os.sep + 'Players'
    if season == 'FixPossessions.py':
      continue
    for p in os.listdir(player_dir):
      stat_file = player_dir + os.sep + p + os.sep + 'Stat_totals.txt'
      if os.path.isfile(stat_file):
        possessions = 0
        with open(stat_file,'r') as f:
          for line in f:
            line_list = line.split('|')
            #print (line_list)
            if line_list[0] == 'Fouls Drawn':
              possessions += int(line_list[-1])
            elif line_list[0] == 'FGA':
              possessions += int(line_list[-1])
        with open(stat_file,'a') as f:
          f.write('Possessions|' + str(possessions) + '\n')
  return