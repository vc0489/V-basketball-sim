import time
import os

def clock(tot_time,length=3,height=2):
  minutes = int(tot_time/60)
  seconds = tot_time - minutes * 60
  d_1 = int(minutes/10)
  d_2 = minutes%10
  d_3 = int(seconds/10)
  d_4 = seconds%10
  
  '''
  strings = (" ","  ","    ","####","# "," #","#"," # ")
  d_strings = {0:(3,5,5,3,4,4,2),\
               1:(2,5,5,2,1,1,2),\
               2:(3,5,1,3,4,1,3),\
               3:(3,5,5,3,1,1,3),\
               4:(2,5,5,2,1,4,3),\
               5:(3,1,5,3,1,4,3),\
               6:(3,1,5,3,4,4,3),\
               7:(3,5,5,2,1,1,2),\
               8:(3,5,5,3,4,4,3),\
               9:(3,5,5,3,1,4,3)}
  '''

  strings = (" ","   "," # ",\
             " "*(length+2),\
             "#"+" "*(length+1),\
             " "*(length+1)+"#",\
             "#"+" "*length+"#",\
             "#"+"#"*length+"#")
  d_strings = {0:(7,6,6,6,7),\
               1:(5,5,5,5,5),\
               2:(7,5,7,4,7),\
               3:(7,5,7,5,7),\
               4:(6,6,7,5,5),\
               5:(7,4,7,5,7),\
               6:(7,4,7,6,7),\
               7:(7,5,5,5,5),\
               8:(7,6,7,6,7),\
               9:(7,6,7,5,7)}
  
  for row in range(2*height+3):
    top_colon_row = int(height/2)
    if (top_colon_row == 0):
      top_colon_row = 1
    bottom_colon_row = 2*height + 2 - top_colon_row
    c = 1
    if ((row == top_colon_row) | (row == bottom_colon_row)):
      c = 2
    if (row == 0):
      string = strings[(d_strings[d_1])[0]] + strings[0]*2 + \
               strings[(d_strings[d_2])[0]] + strings[1] + \
               strings[(d_strings[d_3])[0]] + strings[0]*2 + \
               strings[(d_strings[d_4])[0]]
    elif (row == (height + 1)):
      string = strings[(d_strings[d_1])[2]] + strings[0]*2 + \
               strings[(d_strings[d_2])[2]] + strings[1] + \
               strings[(d_strings[d_3])[2]] + strings[0]*2 + \
               strings[(d_strings[d_4])[2]]
    elif (row == (2*height + 2)):
      string = strings[(d_strings[d_1])[4]] + strings[0]*2 + \
               strings[(d_strings[d_2])[4]] + strings[1] + \
               strings[(d_strings[d_3])[4]] + strings[0]*2 + \
               strings[(d_strings[d_4])[4]]
    elif (row < (height + 1)):
      string = strings[(d_strings[d_1])[1]] + strings[0]*2 + \
               strings[(d_strings[d_2])[1]] + strings[c] + \
               strings[(d_strings[d_3])[1]] + strings[0]*2 + \
               strings[(d_strings[d_4])[1]]
    else:
      string = strings[(d_strings[d_1])[3]] + strings[0]*2 + \
               strings[(d_strings[d_2])[3]] + strings[c] + \
               strings[(d_strings[d_3])[3]] + strings[0]*2 + \
               strings[(d_strings[d_4])[3]]
    print (string)
  
  return

def scoreboard(h_scores,a_scores,h_name="H",a_name="A",max_periods=4):
  
  #SAMPLE SCOREBOARD
  #-------------------------------------------#
  #                                           #
  #  +-----+-----+-----+-----+-----+-------+  #
  #  | VBA | Q 1 | Q 2 | Q 3 | Q 4 | TOTAL |  #
  #  +-----+-----+-----+-----+-----+-------+  #
  #  |  H  | 2 5 | 2 6 | 3 0 | 1 9 | 1 0 0 |  #
  #  +-----+–----+–----+–----+–----+–------+  #
  #  |  A  | 3 1 | 2 2 | 1 2 | 3 2 |  9 7  |  #
  #  +-----+-----+-----+-----+-----+-------+  #
  #                                           #
  #-------------------------------------------#
  h_total = sum(h_scores)
  a_total = sum(a_scores)
  length = 6*(max_periods+1) + 9 
  tot_periods = len(h_scores)
  if (tot_periods > max_periods):
    length += (tot_periods - max_periods)*6
  
  if (max_periods == 4):
    prefix = "Q"
  elif (max_periods == 2):
    prefix = "H"
  else:
    prefix = "P"
  
  if (len(h_name) == 1):
    row_h_str = "|  " + h_name + "  |"
  elif (len(h_name) == 3):
    row_h_str = "| " + h_name + " |"
  else:
    row_h_str = "|  H  |"

  if (len(a_name) == 1):
    row_a_str = "|  " + a_name + "  |"
  elif (len(a_name) == 3):
    row_a_str = "| " + a_name + " |"
  else:
    row_a_str = "|  A  |"
  
  sep_str = "+-----+"
  row_1_str = "| VBA |"
  for c in range(tot_periods):
    sep_str += "-----+"
    if (c < max_periods): 
      row_1_str += " " + prefix + " " + str(c+1) + " |"
    else:
      row_1_str += " OT" + str(c-max_periods+1) + " |"
    digit_1_h = int(h_scores[c]/10)
    digit_2_h = h_scores[c]%10
    digit_1_a = int(a_scores[c]/10)
    digit_2_a = a_scores[c]%10
      
    if (digit_1_h == 0):
      row_h_str += "   "
    else:
      row_h_str += " " + str(digit_1_h) + " "
    if (digit_1_a == 0):
      row_a_str += "   "
    else:
      row_a_str += " " + str(digit_1_a) + " "
      
    row_h_str += str(digit_2_h) + " |"
    row_a_str += str(digit_2_a) + " |"

  sep_str += "-------+"
  row_1_str += " TOTAL |"

  if (h_total > 99):
    digit_1_h = int(h_total/100)
    digit_2_h = int((h_total-100*digit_1_h)/10)
    digit_3_h = h_total%10
    row_h_str += " " + str(digit_1_h) + " " + str(digit_2_h) + " " + str(digit_3_h) + " |"
  else:
    digit_1_h = int(h_total/10)
    digit_2_h = h_total%10
    row_h_str += "  " + str(digit_1_h) + " " + str(digit_2_h) + "  |"
  if (a_total > 99):
    digit_1_a = int(a_total/100)
    digit_2_a = int((a_total-100*digit_1_a)/10)
    digit_3_a = a_total%10
    row_a_str += " " + str(digit_1_a) + " " + str(digit_2_a) + " " + str(digit_3_a) + " |"
  else:
    digit_1_a = int(a_total/10)
    digit_2_a = a_total%10
    row_a_str += "  " + str(digit_1_a) + " " + str(digit_2_a) + "  |"
  print (sep_str)
  print (row_1_str)
  print (sep_str)
  print (row_h_str)
  print (sep_str)
  print (row_a_str)
  print (sep_str)
  return

def in_game_boxscore(h_starting,h_bench,h_playing,a_starting,a_bench,a_playing):
  
  
  #------------------------------------------------------------------+--------+-----+-----+  
  # [05:30] Af4 Made 3PT Shot (22 PTS)                               |O. Stats| LAT | QUE |
  # [05:36] Ac6 Made 2 of 2 Free Throws (25 PTS) - Af4 Foul (5 PF)   |--------+-----+-----+
  # [05:45]                                                          | In Pts |  50 |  35 |
  # [06:02]                                                          | 2C Pts |  12 |   6 | 
  # [06:13]                                                          |Max Lead|   5 |   2 |
  #-----+-----+---+-----+-----+-----+--+--+--+--+--++-----+-----+---+-----+-----+-----+--+--+--+--+--+
  # LAT | Min |+/-|2P-FG|3P-FG| FTS |OR|DR|AS|FC|PT|| QUE | Min |+/-|2P-FG|3P-FG| FTS |OR|DR|AS|FC|PT|
  #-----+-----+---+-----+-----+-----+--+--+--+--+--++-----+-----+---+-----+-----+-----+--+--+--+--+--+
  #Aa13*|10:10|+20| 3-5 | 1-2 | 0-0 | 5| 7| 0| 3| 9|| Fa7*|10:10|+20| 3-5 | 1-2 | 0-0 | 5| 7| 0| 3| 9|
  # Ac6*|30:00| -5|10-17| 0-1 | 5-6 | 3| 7| 1| 1|25|| Ac4*|30:00| -5|10-17| 0-1 | 5-6 | 3| 7| 1| 1|25|
  # Be2 |29:59| +3| 8-15| 1-6 | 3-4 | 5| 5| 1| 5|22|| Af4*|29:59| +3| 8-15| 1-6 | 3-4 | 5| 5| 1| 5|22|
  # Eg3 |12:34|-15| 5-12| 4-9 | 3-3 | 2| 3| 5| 1|25|| Bg6 |12:34|-15| 5-12| 4-9 | 3-3 | 2| 3| 5| 1|25|
  # Ai2 |25:00|  0| 1-2 | 0-1 | 0-0 | 1| 4|13| 4| 2|| Ai9 |25:00|  0| 1-2 | 0-1 | 0-0 | 1| 4|13| 4| 2|
  #-----+-----+---+-----+-----+-----+--+--+--+--+--++-----+-----+---+-----+-----+-----+--+--+--+--+--+
  # Ee1*|     
  # Ee2 |
  #     |
  #     |
  #     |
  #     |
  #     |
  #-----+-----+---+-----+-----+-----+--+--+--+--+--++-----+-----+---+-----+-----+-----+--+--+--+--+--+
  # Tot |
  #  %  |-----|---|50.00|33.33|75.00|--|--|--|--|--||-----+-----+---+     +     +     +--+--+--+--+--|
  #-----+-----+---+-----+-----+-----+--+--+--+--+--++-----+-----+---+-----+-----+-----+--+--+--+--+--+

  return

def countdown(total_time):
  for i in range(total_time):
    if (os.name == 'posix'):
      os.system('clear')
    else:
      os.system('cls')
    clock(i,2,1)
    time.sleep(0.1)
  return


