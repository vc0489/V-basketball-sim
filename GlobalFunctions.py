from GlobalVariables import *
import random

def F_CALC_P_PTS_FOR_P40_ON(p_stats):
  return (p_stats['Team Points For']*2400/p_stats['Court Time'])
  
def F_CALC_P_PTS_FOR_P40_OFF(p_stats):
  return ((p_stats['All Team Points F'] - p_stats['Team Points For'])*2400/\
         (p_stats['Team Court Time'] - p_stats['Court Time']))
  
def F_CALC_P_PTS_AGAINST_P40_ON(p_stats):
  return (p_stats['Team Points Against']*2400/p_stats['Court Time'])
  
def F_CALC_P_PTS_AGAINST_P40_OFF(p_stats):
  return ((1.0*p_stats['All Team Points A'] - p_stats['Team Points Against'])*2400/\
         (p_stats['Team Court Time'] - p_stats['Court Time']))

def F_CALC_P_TEAM_OFF_IMPACT(p_stats):
  return (F_CALC_P_PTS_FOR_P40_ON(p_stats) - F_CALC_P_PTS_FOR_P40_OFF(p_stats))
  
def F_CALC_P_TEAM_DEF_IMPACT(p_stats):
  return (F_CALC_P_PTS_AGAINST_P40_OFF(p_stats) - F_CALC_P_PTS_AGAINST_P40_ON(p_stats))
  
def F_CALC_P_TEAM_TOT_IMPACT(p_stats):
  return (F_CALC_P_TEAM_OFF_IMPACT(p_stats) + F_CALC_P_TEAM_DEF_IMPACT(p_stats))
  
def F_CALC_L_PPG(l_obj):
  tot_l_pts = 0
  tot_l_games = 0
  for t in NICKS:
    t_stats = l_obj.teams[t].stats['Y' + str(l_obj.cur_year)]
    tot_l_pts += t_stats['Own']['Points']
    tot_l_games += t_stats['Games']
  #print ('League PPG: ' + str(tot_l_pts/tot_l_games))
  return (tot_l_pts/tot_l_games)

def F_CALC_P_LEAGUE_OFF_IMPACT(l_obj,p_stats):
   
  return
  
def F_CALC_P_LEAGUE_DEF_IMPACT(l_obj,p_stats):
  return (F_CALC_L_PPG(l_obj) - F_CALC_P_PTS_AGAINST_P40_ON(p_stats) + F_CALC_P_TEAM_DEF_IMPACT(p_stats)/2)

def F_CALC_P_LEAGUE_TOT_IMPACT(p_stats):
  return (p_stats['+/-']*2400/p_stats['Court Time'] + F_CALC_P_TEAM_TOT_IMPACT(p_stats)/2)
  

def F_DET_INJURY(inj_prob):
  def formula(days):
    return (1/(days*days + 50))
  random.seed()
  I = random.random()
  if I < inj_prob:
    while 1:   
      X = random.random()*formula(1)
      Y = random.randrange(1,201)
      if X < formula(Y):
        days_missed = Y
        break
  else:
    days_missed = 0
  return (days_missed)
  
def F_INJ_RECOVER():
  random.seed()
  X = random.random()
  if X < 0.5:
    inj_reduction = 1
  elif X < 0.75:
    inj_reduction = 0
  elif X < 0.99:
    inj_reduction = 2
  else:
    inj_reduction = 3
  return (inj_reduction)
  
def F_RANK_FROM_RATINGS(ratings_dict,descending):
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
  
def F_GEN_P_ATTS_TITLE(prev):
  title = ''
  for att in P_ATT_WRITE_SEQ:
    if att not in ('Age','Pos','YPro','Draft','GInj','Team') and len(att) < 5:
      l_att = 5
    else:
      l_att = len(att)
    title += '{:>{l}}'.format(att,l=l_att) + ' '
  if prev == True:
    title += 'Updated'
  return (title)
  
def F_GEN_P_ATTS_LINE(update_str,p_obj):
  line = ''
  draft_str = str(p_obj.profile['Draft Year']) + '.' + \
              str(p_obj.profile['Pick No'])
      
  for att in P_ATT_WRITE_SEQ:
    if att == 'Age':
      line += '{:>{l}}'.format(str(p_obj.profile['Age']),l=len(att)) + ' '
    elif att == 'Pos':
      line += '{:>{l}}'.format(str(p_obj.profile['Pos']),l=len(att)) + ' '
    elif att == 'YPro':
      line += '{:>{l}}'.format(str(p_obj.profile['Years Pro']),l=len(att)) + ' '
    elif att == 'Draft':
      line += '{:>{l}}'.format(draft_str,l=len(att)) + ' '
    elif att == 'GInj':
      line += '{:>{l}}'.format(str(p_obj.status['Days Injured']),l=len(att)) + ' '
    elif att == 'Team':
      line += '{:>{l}}'.format(p_obj.team_nick,l=len(att)) + ' '
    elif att in P_ATT_NAME_DICT:
      if len(att) < 5:
        l_att = 5
      else:
        l_att = len(att)
      line += '{:>{l}}'.format(str(p_obj.attributes[P_ATT_NAME_DICT[att]]),l=l_att) + ' '
         
  if update_str:
    line += '{:<{l}}'.format(update_str,l=7)

  return (line)

def F_GEN_VAR_FROM_PROB_DICT(prob_dict):
  random.seed()
  X = random.random() 
  chance_bound = 0
  for var in prob_dict:
    chance_bound += prob_dict[var]
    if X <= chance_bound:
      return (var)  
  print ("VC - ERROR in F_GEN_VAR_FROM_PROB_DICT")
  return 

def F_RATING_TO_GRADE(grade_dict,rating):
  for grade_key in sorted(grade_dict.keys()):
    if rating <= grade_key:
      return grade_dict[grade_key]
  print ("ERROR in F_RATING_TO_GRADE")


#def F_PRINT_P_ATTS_TITLE(print_seq,p_dict,draft):
#  return
def F_PRINT_DRAFTED_GRADES(drafted_dict):
  name_len = 5
  title = 'Pick Name '
  for att in P_ATT_WRITE_SEQ:
    if att in ('YPro','GInj','Draft'):
      continue
    else:
      title += P_ATT_ABBREV_DICT[att] + ' '
  print (title)

  for p in sorted(drafted_dict.keys()):
    line = '{:>{l}}'.format(p,l=4) + ' ' + \
           '{:<{l}}'.format(drafted_dict[p]['Name'],l=name_len) + ' '
    for att in P_ATT_WRITE_SEQ:
      if att in ('YPro','GInj','Draft'):
        continue
      elif att == 'Pos':
        line += '{:>{l}}'.format(drafted_dict[p]['Object'].profile['Pos'],\
                                 l=len(P_ATT_ABBREV_DICT[att])) + ' '
      elif att == 'Age':
        line += '{:>{l}}'.format(drafted_dict[p]['Object'].profile['Age'],\
                                 l=len(P_ATT_ABBREV_DICT[att])) + ' '
      elif att == 'Team':
        line += '{:>{l}}'.format(drafted_dict[p]['Object'].team_nick,\
                                 l=len(P_ATT_ABBREV_DICT[att])) + ' '
      else:
        grade = F_RATING_TO_GRADE(ATTS_GRADE_SCALE[att],\
                drafted_dict[p]['Object'].attributes[P_ATT_NAME_DICT[att]])
        line += '{:>{l}}'.format(grade,l=len(P_ATT_ABBREV_DICT[att])) + ' '
    print (line)  
  
  return
  
  
def F_PRINT_P_GRADES(p_container,mode,seq=None,t_obj=None):
  
  if mode == 'Draftees':
    atts_to_skip = ('Draft','YPro','Team','GInj')
    p_dict = p_container
  elif mode == 'Team':
    atts_to_skip = ('Team')
    p_dict = p_container
  elif mode == 'Drafted': 
    atts_to_skip = ('Draft','YPro','GInj')
    p_dict = p_container
  elif mode == 'FA':
    atts_to_skip = ()
    p_dict = p_container
  elif mode == 'TO':
    atts_to_skip = ('GInj','Team')
    p_dict = {}
    for p in p_container:
      p_dict[p] = t_obj.players[p]
    
  else:
    atts_to_skip = ()
    p_dict = p_container
  name_len = 5
  
  if mode == 'Drafted':
    title = 'Pick '
  else:
    title =  ''
    
  title += '{:<{l}}'.format('Name',l=name_len) + ' '
  for att in P_ATT_WRITE_SEQ:
    if att in atts_to_skip:
      continue
    else:
      title += P_ATT_ABBREV_DICT[att] + ' '
  print (title)
  if not seq:
    seq = sorted(p_dict.keys())
  for p in seq:
    if mode == 'Drafted':
      line = '{:>{l}}'.format(p,l=4) + ' ' + \
             '{:<{l}}'.format(p_dict[p]['Name'],l=name_len) + ' '
      p_obj = p_dict[p]['Object']
    else:
      if mode == 'FA':
        
        if p in t_obj.transactions['CUT'] or \
           p in t_obj.transactions['TRADED-AWAY']:
          line = '{:<{l}}'.format(p + '*', l=name_len) + ' '
        else:
          line = '{:<{l}}'.format(p,l=name_len) + ' '
      else:
        line = '{:<{l}}'.format(p,l=name_len) + ' '
      p_obj = p_dict[p]
    for att in P_ATT_WRITE_SEQ:
      if att in atts_to_skip:
        continue
      elif att == 'Draft':
        draft_str = '{:>{l}}'.format(p_obj.profile['Draft Year'],l=2) + \
                    '.' + '{:<{l}}'.format(p_obj.profile['Pick No'],l=2)
        line += '{:>{l}}'.format(draft_str,\
                                 l=len(P_ATT_ABBREV_DICT[att])) + ' '
      elif att == 'Team':
        line += '{:>{l}}'.format(p_obj.team_nick,\
                                 l=len(P_ATT_ABBREV_DICT[att])) + ' '
      elif att == 'YPro':
        line += '{:>{l}}'.format(p_obj.profile['Years Pro'],\
                                 l=len(P_ATT_ABBREV_DICT[att])) + ' '
      elif att == 'Pos':
        line += '{:>{l}}'.format(p_obj.profile['Pos'],\
                                 l=len(P_ATT_ABBREV_DICT[att])) + ' '
      elif att == 'Age':
        line += '{:>{l}}'.format(p_obj.profile['Age'],\
                                 l=len(P_ATT_ABBREV_DICT[att])) + ' '
      elif att == 'GInj':
        line += '{:>{l}}'.format(p_obj.status['Days Injured'],\
                                 l=len(P_ATT_ABBREV_DICT[att])) + ' '
      else:
        grade = F_RATING_TO_GRADE(ATTS_GRADE_SCALE[att],\
                                  p_obj.attributes[P_ATT_NAME_DICT[att]])
        line += '{:>{l}}'.format(grade,l=len(P_ATT_ABBREV_DICT[att])) + ' '
    print (line)  
  
  return
  
def F_PRINT_PLAYER_ATTS():
  return