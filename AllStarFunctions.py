import random
from GlobalFunctions import *

def choose_ASG_C(l_obj,eligible_players,eligible_stats,injured=None):
  chosen_C = None  
  for p_tuple in eligible_players:    
    if injured:
      if p_tuple[0] == injured or l_obj.players['Active'][p_tuple[1]][p_tuple[0]].status['Days Injured'] > 0:
        continue
    p = p_tuple[0]
    pos = p_tuple[1]
    ppg = p_tuple[-1]['PPG']
    rpg = p_tuple[-1]['RPG']
    apg = p_tuple[-1]['APG']
    l_imp = p_tuple[-1]['L-IMP']  
    rank_index = eligible_stats['PPG'].index(ppg) + \
                 eligible_stats['RPG'].index(rpg) + \
                 0.25*eligible_stats['APG'].index(apg) + \
                 eligible_stats['L-IMP'].index(l_imp)
    print ('C',p,rank_index)
    if not chosen_C:
      chosen_C = ([p,],[pos,],rank_index)
    elif rank_index < chosen_C[-1]:
      chosen_C = ([p,],[pos,],rank_index)
    elif rank_index == chosen_C[-1]:
      team_orig = l_obj.players['Active'][chosen_C[1][0]][chosen_C[0][0]].team_nick
      team_new = l_obj.players['Active'][pos][p].team_nick
      if team_orig == team_new:
        chosen_C[0].append(p)
        chosen_C[1].append(p)
      else:
        standings = l_obj.det_standings('League')
        if standings.index(team_orig) > standings.index(team_new):
          chosen_C = ([p,],[pos,],rank_index)
  if len(chosen_C[0]) > 1:
    p = random.choice(chosen_C[0])
    pos = chosen_C[1][chosen_C[0].index(p)]
    chosen_C = (p,pos)
  else:
    chosen_C = (chosen_C[0][0],chosen_C[1][0])
  return (chosen_C)

def choose_ASG_PF(l_obj,eligible_players,eligible_stats,injured=None):
  chosen_PF = None  
  for p_tuple in eligible_players:    
    if injured:
      if p_tuple[0] == injured or l_obj.players['Active'][p_tuple[1]][p_tuple[0]].status['Days Injured'] > 0:
        continue
    p = p_tuple[0]
    pos = p_tuple[1]
    ppg = p_tuple[-1]['PPG']
    rpg = p_tuple[-1]['RPG']
    apg = p_tuple[-1]['APG']
    l_imp = p_tuple[-1]['L-IMP']
    rank_index = eligible_stats['PPG'].index(ppg) + \
                 eligible_stats['RPG'].index(rpg) + \
                 0.25*eligible_stats['APG'].index(apg) + \
                 eligible_stats['L-IMP'].index(l_imp)
    print ('PF',p,rank_index)
    if not chosen_PF:
      chosen_PF = ([p,],[pos,],rank_index)
    elif rank_index < chosen_PF[-1]:
      chosen_PF = ([p,],[pos,],rank_index)
    elif rank_index == chosen_PF[-1]:
      team_orig = l_obj.players['Active'][chosen_PF[1][0]][chosen_PF[0][0]].team_nick
      team_new = l_obj.players['Active'][pos][p].team_nick
      if team_orig == team_new:
        chosen_PF[0].append(p)
        chosen_PF[1].append(p)
      else:
        standings = l_obj.det_standings('League')
        if standings.index(team_orig) > standings.index(team_new):
          chosen_PF = ([p,],[pos,],rank_index)
  if len(chosen_PF[0]) > 1:
    p = random.choice(chosen_PF[0])
    pos = chosen_PF[1][chosen_PF[0].index(p)]
    chosen_PF = (p,pos)
  else:
    chosen_PF = (chosen_PF[0][0],chosen_PF[1][0])
  return (chosen_PF)

def choose_ASG_SF(l_obj,eligible_players,eligible_stats,injured=None):
  chosen_SF = None  
  for p_tuple in eligible_players:    
    if injured:
      if p_tuple[0] == injured or l_obj.players['Active'][p_tuple[1]][p_tuple[0]].status['Days Injured'] > 0:
        continue
    p = p_tuple[0]
    pos = p_tuple[1]
    ppg = p_tuple[-1]['PPG']
    rpg = p_tuple[-1]['RPG']
    apg = p_tuple[-1]['APG']
    l_imp = p_tuple[-1]['L-IMP']
    rank_index = eligible_stats['PPG'].index(ppg) + \
                 0.75*eligible_stats['RPG'].index(rpg) + \
                 0.5*eligible_stats['APG'].index(apg) + \
                 eligible_stats['L-IMP'].index(l_imp)
    print ('SF',p,rank_index)
    if not chosen_SF:
      chosen_SF = ([p,],[pos,],rank_index)
    elif rank_index < chosen_SF[-1]:
      chosen_SF = ([p,],[pos,],rank_index)
    elif rank_index == chosen_SF[-1]:
      team_orig = l_obj.players['Active'][chosen_SF[1][0]][chosen_SF[0][0]].team_nick
      team_new = l_obj.players['Active'][pos][p].team_nick
      if team_orig == team_new:
        chosen_SF[0].append(p)
        chosen_SF[1].append(p)
      else:
        standings = l_obj.det_standings('League')
        if standings.index(team_orig) > standings.index(team_new):
          chosen_SF = ([p,],[pos,],rank_index)
  if len(chosen_SF[0]) > 1:
    p = random.choice(chosen_SF[0])
    pos = chosen_SF[1][chosen_SF[0].index(p)]
    chosen_SF = (p,pos)
  else:
    chosen_SF = (chosen_SF[0][0],chosen_SF[1][0])
  return (chosen_SF)

def choose_ASG_SG(l_obj,eligible_players,eligible_stats,injured=None):
  chosen_SG = None  
  for p_tuple in eligible_players:    
    if injured:
      if p_tuple[0] == injured or l_obj.players['Active'][p_tuple[1]][p_tuple[0]].status['Days Injured'] > 0:
        continue
    p = p_tuple[0]
    pos = p_tuple[1]
    ppg = p_tuple[-1]['PPG']
    rpg = p_tuple[-1]['RPG']
    apg = p_tuple[-1]['APG']
    l_imp = p_tuple[-1]['L-IMP']
    rank_index = eligible_stats['PPG'].index(ppg) + \
                 0.5*eligible_stats['RPG'].index(rpg) + \
                 0.75*eligible_stats['APG'].index(apg) + \
                 eligible_stats['L-IMP'].index(l_imp)
    print ('SG',p,rank_index)
    if not chosen_SG:
      chosen_SG = ([p,],[pos,],rank_index)
    elif rank_index < chosen_SG[-1]:
      chosen_SG = ([p,],[pos,],rank_index)
    elif rank_index == chosen_SG[-1]:
      team_orig = l_obj.players['Active'][chosen_SG[1][0]][chosen_SG[0][0]].team_nick
      team_new = l_obj.players['Active'][pos][p].team_nick
      if team_orig == team_new:
        chosen_SG[0].append(p)
        chosen_SG[1].append(p)
      else:
        standings = l_obj.det_standings('League')
        if standings.index(team_orig) > standings.index(team_new):
          chosen_SG = ([p,],[pos,],rank_index)
  if len(chosen_SG[0]) > 1:
    p = random.choice(chosen_SG[0])
    pos = chosen_SG[1][chosen_SG[0].index(p)]
    chosen_SG = (p,pos)
  else:
    chosen_SG = (chosen_SG[0][0],chosen_SG[1][0])
  return (chosen_SG)

def choose_ASG_PG(l_obj,eligible_players,eligible_stats,injured=None):
  chosen_PG = None  
  for p_tuple in eligible_players:    
    if injured:
      if p_tuple[0] == injured or l_obj.players['Active'][p_tuple[1]][p_tuple[0]].status['Days Injured'] > 0:
        continue
    p = p_tuple[0]
    pos = p_tuple[1]
    ppg = p_tuple[-1]['PPG']
    rpg = p_tuple[-1]['RPG']
    apg = p_tuple[-1]['APG']
    l_imp = p_tuple[-1]['L-IMP']
    rank_index = 0.75*eligible_stats['PPG'].index(ppg) + \
                 0.25*eligible_stats['RPG'].index(rpg) + \
                 eligible_stats['APG'].index(apg) + \
                 eligible_stats['L-IMP'].index(l_imp)
    print ('PG',p,rank_index)
    if not chosen_PG:
      chosen_PG = ([p,],[pos,],rank_index)
    elif rank_index < chosen_PG[-1]:
      chosen_PG = ([p,],[pos,],rank_index)
    elif rank_index == chosen_PG[-1]:
      team_orig = l_obj.players['Active'][chosen_PG[1][0]][chosen_PG[0][0]].team_nick
      team_new = l_obj.players['Active'][pos][p].team_nick
      if team_orig == team_new:
        chosen_PG[0].append(p)
        chosen_PG[1].append(p)
      else:
        standings = l_obj.det_standings('League')
        if standings.index(team_orig) > standings.index(team_new):
          chosen_PG = ([p,],[pos,],rank_index)
  if len(chosen_PG[0]) > 1:
    p = random.choice(chosen_PG[0])
    pos = chosen_PG[1][chosen_PG[0].index(p)]
    chosen_PG = (p,pos)
  else:
    chosen_PG = (chosen_PG[0][0],chosen_PG[1][0])
  return (chosen_PG)

def choose_ASG_guard(l_obj,eligible_players,eligible_stats,chosen_players=None):
  chosen_guard = None
  for p_tuple in eligible_players:
    if l_obj.players['Active'][p_tuple[1]][p_tuple[0]].status['Days Injured'] > 0:
      continue
    p = p_tuple[0]
    if p in chosen_players:
      continue
    pos = p_tuple[1]
    ppp = p_tuple[-1]['PPP']
    ppg = p_tuple[-1]['PPG']
    rpg = p_tuple[-1]['RPG']
    apg = p_tuple[-1]['APG']
    t_imp = p_tuple[-1]['T-IMP']
    rank_index = eligible_stats['PPP'].index(ppp) + \
                 0.75*eligible_stats['PPG'].index(ppg) + \
                 0.75*eligible_stats['RPG'].index(rpg) + \
                 0.75*eligible_stats['APG'].index(apg) + \
                 eligible_stats['T-IMP'].index(t_imp)
    print ('Guard',p,rank_index)
    #print (p,rank_index)
    if not chosen_guard:
      chosen_guard = ([p,],[pos,],rank_index)
    elif rank_index < chosen_guard[-1]:
      chosen_guard = ([p,],[pos,],rank_index)
    elif rank_index == chosen_guard[-1]:
      team_orig = l_obj.players['Active'][chosen_guard[1][0]][chosen_guard[0][0]].team_nick
      team_new = l_obj.players['Active'][pos][p].team_nick
      if team_orig == team_new:
        chosen_guard[0].append(p)
        chosen_guard[1].append(p)
      else:
        standings = l_obj.det_standings('League')
        if standings.index(team_orig) > standings.index(team_new):
          chosen_guard = ([p,],[pos,],rank_index)
  if len(chosen_guard[0]) > 1:
    p = random.choice(chosen_guard[0])
    pos = chosen_guard[1][chosen_guard[0].index(p)]
    chosen_guard = (p,pos)
  else:
    chosen_guard = (chosen_guard[0][0],chosen_guard[1][0])
  return (chosen_guard)

def choose_ASG_forward(l_obj,eligible_players,eligible_stats,chosen_players=None):
  chosen_forward = None
  for p_tuple in eligible_players:
    if l_obj.players['Active'][p_tuple[1]][p_tuple[0]].status['Days Injured'] > 0:
      continue
    p = p_tuple[0]
    if p in chosen_players:
      continue
    pos = p_tuple[1]
    ppp = p_tuple[-1]['PPP']
    ppg = p_tuple[-1]['PPG']
    rpg = p_tuple[-1]['RPG']
    apg = p_tuple[-1]['APG']
    t_imp = p_tuple[-1]['T-IMP']
    rank_index = eligible_stats['PPP'].index(ppp) + \
                 0.75*eligible_stats['PPG'].index(ppg) + \
                 eligible_stats['RPG'].index(rpg) + \
                 0.5*eligible_stats['APG'].index(apg) + \
                 eligible_stats['T-IMP'].index(t_imp)
    print ('Forward',p,rank_index)
    #print (p,rank_index)
    if not chosen_forward:
      chosen_forward = ([p,],[pos,],rank_index)
    elif rank_index < chosen_forward[-1]:
      chosen_forward = ([p,],[pos,],rank_index)
    elif rank_index == chosen_forward[-1]:
      team_orig = l_obj.players['Active'][chosen_forward[1][0]][chosen_forward[0][0]].team_nick
      team_new = l_obj.players['Active'][pos][p].team_nick
      if team_orig == team_new:
        chosen_forward[0].append(p)
        chosen_forward[1].append(p)
      else:
        standings = l_obj.det_standings('League')
        if standings.index(team_orig) > standings.index(team_new):
          chosen_forward = ([p,],[pos,],rank_index)
  if len(chosen_forward[0]) > 1:
    p = random.choice(chosen_forward[0])
    pos = chosen_forward[1][chosen_forward[0].index(p)]
    chosen_forward = (p,pos)
  else:
    chosen_forward = (chosen_forward[0][0],chosen_forward[1][0])
  return (chosen_forward)

def choose_ASG_general(l_obj,eligible_players,eligible_stats,chosen_players=None):
  chosen_general = None
  for p_tuple in eligible_players:
    if l_obj.players['Active'][p_tuple[1]][p_tuple[0]].status['Days Injured'] > 0:
      continue
    p = p_tuple[0]
    if p in chosen_players:
      continue
    pos = p_tuple[1]
    ppp = p_tuple[-1]['PPP']
    l_d_imp = p_tuple[-1]['L-DIMP']
    mpg = p_tuple[-1]['MPG']
    rank_index = eligible_stats['PPP'].index(ppp) + \
                 eligible_stats['L-DIMP'].index(l_d_imp) + \
                 eligible_stats['MPG'].index(mpg)
    print ('General',p,rank_index)
    if not chosen_general:
      chosen_general = ([p,],[pos,],rank_index)
    elif rank_index < chosen_general[-1]:
      chosen_general = ([p,],[pos,],rank_index)
    elif rank_index == chosen_general[-1]:
      team_orig = l_obj.players['Active'][chosen_general[1][0]][chosen_general[0][0]].team_nick
      team_new = l_obj.players['Active'][pos][p].team_nick
      if team_orig == team_new:
        chosen_general[0].append(p)
        chosen_general[1].append(p)
      else:
        standings = l_obj.det_standings('League')
        if standings.index(team_orig) > standings.index(team_new):
          chosen_general = ([p,],[pos,],rank_index)
  if len(chosen_general[0]) > 1:
    p = random.choice(chosen_general[0])
    pos = chosen_general[1][chosen_general[0].index(p)]
    chosen_general = (p,pos)
  else:
    chosen_general = (chosen_general[0][0],chosen_general[1][0])
  return (chosen_general)

def det_ASG_rosters(l_obj):
  league_ppg = F_CALC_L_PPG(l_obj)
  eligible_alpha_p = {}
  eligible_beta_p = {}
  
  eligible_stats = {'PPG':[],'RPG':[],'APG':[],'MPG':[],'PPP':[],'L-DIMP':[],\
                    'L-IMP':[],'T-IMP':[]}
  for pos in l_obj.players['Active']:
    eligible_alpha_p[pos] = []
    eligible_beta_p[pos] = []
    for p in l_obj.players['Active'][pos]:
      p_stats = l_obj.players['Active'][pos][p].stats['Y' + str(l_obj.cur_year)]
      p_status = l_obj.players['Active'][pos][p].status
      if p_stats['Games Played'] >= p_stats['Team Games']*0.5 and \
         p_stats['Games Played'] >= 10 and \
         p_stats['Court Time']/p_stats['Games Played'] >= 1200:
        stats_dict = {}
        ppg = decimal.Decimal(p_stats['Points']/p_stats['Games Played']).quantize(ONE_DP)
        stats_dict['PPG'] = ppg
        eligible_stats['PPG'].append(ppg)
        rpg = decimal.Decimal(p_stats['Tot Reb']/p_stats['Games Played']).quantize(ONE_DP)
        stats_dict['RPG'] = rpg
        eligible_stats['RPG'].append(rpg)
        apg = decimal.Decimal(p_stats['Assists']/p_stats['Games Played']).quantize(ONE_DP)
        stats_dict['APG'] = apg
        eligible_stats['APG'].append(apg)
        mpg = decimal.Decimal((p_stats['Court Time']/60)/(p_stats['Games Played'])).quantize(ONE_DP)
        stats_dict['MPG'] = mpg
        eligible_stats['MPG'].append(mpg)
        ppp = decimal.Decimal(p_stats['Points']/p_stats['Possessions']).quantize(TWO_DP) 
        stats_dict['PPP'] = ppp
        eligible_stats['PPP'].append(ppp)
        l_d_imp = decimal.Decimal(F_CALC_P_LEAGUE_DEF_IMPACT(l_obj,p_stats)).quantize(ONE_DP)
        stats_dict['L-DIMP'] = l_d_imp
        eligible_stats['L-DIMP'].append(l_d_imp)
        l_imp = decimal.Decimal(F_CALC_P_LEAGUE_TOT_IMPACT(p_stats)).quantize(ONE_DP)
        stats_dict['L-IMP'] = l_imp
        eligible_stats['L-IMP'].append(l_imp)
        t_imp = decimal.Decimal(F_CALC_P_TEAM_TOT_IMPACT(p_stats)).quantize(ONE_DP)
        stats_dict['T-IMP'] = t_imp
        eligible_stats['T-IMP'].append(t_imp)
        if l_obj.players['Active'][pos][p].team_nick in l_obj.conferences['Alpha']:
          eligible_alpha_p[pos].append((p,pos,stats_dict))
        elif l_obj.players['Active'][pos][p].team_nick in l_obj.conferences['Beta']:
          eligible_beta_p[pos].append((p,pos,stats_dict))
    
  eligible_stats['PPG'].sort(reverse=True)
  eligible_stats['RPG'].sort(reverse=True)
  eligible_stats['APG'].sort(reverse=True)
  eligible_stats['MPG'].sort(reverse=True)
  eligible_stats['PPP'].sort(reverse=True)
  eligible_stats['L-DIMP'].sort(reverse=True)
  eligible_stats['L-IMP'].sort(reverse=True)
  eligible_stats['T-IMP'].sort(reverse=True) 
  
  alpha_injured = {}
  beta_injured = {}
  chosen_alpha_PG = choose_ASG_PG(l_obj,eligible_alpha_p['PG'],eligible_stats)
  if l_obj.players['Active'][chosen_alpha_PG[1]][chosen_alpha_PG[0]].status['Days Injured'] > 0:
    print (chosen_alpha_PG[0] + ' is injured and will be replaced')
    alpha_injured[chosen_alpha_PG[0]] = l_obj.players['Active'][chosen_alpha_PG[1]][chosen_alpha_PG[0]]
    chosen_alpha_PG = choose_ASG_PG(l_obj,eligible_alpha_p['PG'],eligible_stats,chosen_alpha_PG)
    
  chosen_alpha_SG = choose_ASG_SG(l_obj,eligible_alpha_p['SG'],eligible_stats)
  if l_obj.players['Active'][chosen_alpha_SG[1]][chosen_alpha_SG[0]].status['Days Injured'] > 0:
    print (chosen_alpha_SG[0] + ' is injured and will be replaced')
    alpha_injured[chosen_alpha_SG[0]] = l_obj.players['Active'][chosen_alpha_SG[1]][chosen_alpha_SG[0]]
    chosen_alpha_SG = choose_ASG_SG(l_obj,eligible_alpha_p['SG'],eligible_stats,chosen_alpha_SG)
    
  chosen_alpha_SF = choose_ASG_SF(l_obj,eligible_alpha_p['SF'],eligible_stats)
  if l_obj.players['Active'][chosen_alpha_SF[1]][chosen_alpha_SF[0]].status['Days Injured'] > 0:
    print (chosen_alpha_SF[0] + ' is injured and will be replaced')
    alpha_injured[chosen_alpha_SF[0]] = l_obj.players['Active'][chosen_alpha_SF[1]][chosen_alpha_SF[0]]
    chosen_alpha_SF = choose_ASG_SF(l_obj,eligible_alpha_p['SF'],eligible_stats,chosen_alpha_SF)
    
  chosen_alpha_PF = choose_ASG_PF(l_obj,eligible_alpha_p['PF'],eligible_stats)
  if l_obj.players['Active'][chosen_alpha_PF[1]][chosen_alpha_PF[0]].status['Days Injured'] > 0:
    print (chosen_alpha_PF[0] + ' is injured and will be replaced')
    alpha_injured[chosen_alpha_PF[0]] = l_obj.players['Active'][chosen_alpha_PF[1]][chosen_alpha_PF[0]]
    chosen_alpha_PF = choose_ASG_PF(l_obj,eligible_alpha_p['PF'],eligible_stats,chosen_alpha_PF)  
    
  chosen_alpha_C = choose_ASG_C(l_obj,eligible_alpha_p['C'],eligible_stats)
  if l_obj.players['Active'][chosen_alpha_C[1]][chosen_alpha_C[0]].status['Days Injured'] > 0:
    print (chosen_alpha_C[0] + ' is injured and will be replaced')
    alpha_injured[chosen_alpha_C[0]] = l_obj.players['Active'][chosen_alpha_C[1]][chosen_alpha_C[0]] 
    chosen_alpha_C = choose_ASG_PG(l_obj,eligible_alpha_p['C'],eligible_stats,chosen_alpha_C)  
    
  alpha_roster_list = [chosen_alpha_PG[0],chosen_alpha_SG[0],chosen_alpha_SF[0],\
                       chosen_alpha_PF[0],chosen_alpha_C[0]]
  
  chosen_alpha_guard = choose_ASG_guard(l_obj,\
                       eligible_alpha_p['PG']+eligible_alpha_p['SG'],\
                       eligible_stats,\
                       alpha_roster_list)
  
  alpha_roster_list.append(chosen_alpha_guard[0])                     
                       
  chosen_alpha_forward = choose_ASG_forward(l_obj,\
       eligible_alpha_p['SF']+eligible_alpha_p['PF']+eligible_alpha_p['C'],\
       eligible_stats,\
       alpha_roster_list)
  
  alpha_roster_list.append(chosen_alpha_forward[0])     
       
  chosen_alpha_general = choose_ASG_general(l_obj,\
       eligible_alpha_p['PG']+eligible_alpha_p['SG']+eligible_alpha_p['SF']+eligible_alpha_p['PF']+eligible_alpha_p['C'],\
       eligible_stats,\
       alpha_roster_list)
  
  alpha_roster_list.append(chosen_alpha_general)


  chosen_beta_PG = choose_ASG_PG(l_obj,eligible_beta_p['PG'],eligible_stats)
  if l_obj.players['Active'][chosen_beta_PG[1]][chosen_beta_PG[0]].status['Days Injured'] > 0:
    print (chosen_beta_PG[0] + ' is injured and will be replaced')
    beta_injured[chosen_beta_PG[0]] = l_obj.players['Active'][chosen_beta_PG[1]][chosen_beta_PG[0]]
    chosen_beta_PG = choose_ASG_PG(l_obj,eligible_beta_p['PG'],eligible_stats,chosen_beta_PG)
    
  chosen_beta_SG = choose_ASG_SG(l_obj,eligible_beta_p['SG'],eligible_stats)
  if l_obj.players['Active'][chosen_beta_SG[1]][chosen_beta_SG[0]].status['Days Injured'] > 0:
    print (chosen_beta_SG[0] + ' is injured and will be replaced')
    beta_injured[chosen_beta_SG[0]] = l_obj.players['Active'][chosen_beta_SG[1]][chosen_beta_SG[0]]
    chosen_beta_SG = choose_ASG_SG(l_obj,eligible_beta_p['SG'],eligible_stats,chosen_beta_SG)
    
  chosen_beta_SF = choose_ASG_SF(l_obj,eligible_beta_p['SF'],eligible_stats)
  if l_obj.players['Active'][chosen_beta_SF[1]][chosen_beta_SF[0]].status['Days Injured'] > 0:
    print (chosen_beta_SF[0] + ' is injured and will be replaced')
    beta_injured[chosen_beta_SF[0]] = l_obj.players['Active'][chosen_beta_SF[1]][chosen_beta_SF[0]]
    chosen_beta_SF = choose_ASG_SF(l_obj,eligible_beta_p['SF'],eligible_stats,chosen_beta_SF)
    
  chosen_beta_PF = choose_ASG_PF(l_obj,eligible_beta_p['PF'],eligible_stats)
  if l_obj.players['Active'][chosen_beta_PF[1]][chosen_beta_PF[0]].status['Days Injured'] > 0:
    print (chosen_beta_PF[0] + ' is injured and will be replaced')
    beta_injured[chosen_beta_PF[0]] = l_obj.players['Active'][chosen_beta_PF[1]][chosen_beta_PF[0]]
    chosen_beta_PF = choose_ASG_PF(l_obj,eligible_beta_p['PF'],eligible_stats,chosen_beta_PF)  
    
  chosen_beta_C = choose_ASG_C(l_obj,eligible_beta_p['C'],eligible_stats)
  if l_obj.players['Active'][chosen_beta_C[1]][chosen_beta_C[0]].status['Days Injured'] > 0:
    print (chosen_beta_C[0] + ' is injured and will be replaced')
    beta_injured[chosen_beta_C[0]] = l_obj.players['Active'][chosen_beta_C[1]][chosen_beta_C[0]]
    chosen_beta_C = choose_ASG_PG(l_obj,eligible_beta_p['C'],eligible_stats,chosen_beta_C)  
    

  beta_roster_list = [chosen_beta_PG[0],chosen_beta_SG[0],chosen_beta_SF[0],\
                       chosen_beta_PF[0],chosen_beta_C[0]]  
  
  chosen_beta_guard = choose_ASG_guard(l_obj,\
                      eligible_beta_p['PG']+eligible_beta_p['SG'],\
                      eligible_stats,\
                      beta_roster_list)
                      
  beta_roster_list.append(chosen_beta_guard[0])                      
                      
  chosen_beta_forward = choose_ASG_forward(l_obj,\
       eligible_beta_p['SF']+eligible_beta_p['PF']+eligible_beta_p['C'],\
       eligible_stats,\
       beta_roster_list)
  
  beta_roster_list.append(chosen_beta_forward[0])     
       
  chosen_beta_general = choose_ASG_general(l_obj,\
       eligible_beta_p['PG']+eligible_beta_p['SG']+eligible_beta_p['SF']+eligible_beta_p['PF']+eligible_beta_p['C'],\
       eligible_stats,\
       beta_roster_list)
  
  beta_roster_list.append(chosen_beta_general[0])
  
  alpha_PG_obj = l_obj.players['Active'][chosen_alpha_PG[1]][chosen_alpha_PG[0]]
  alpha_SG_obj = l_obj.players['Active'][chosen_alpha_SG[1]][chosen_alpha_SG[0]]
  alpha_SF_obj = l_obj.players['Active'][chosen_alpha_SF[1]][chosen_alpha_SF[0]]
  alpha_PF_obj = l_obj.players['Active'][chosen_alpha_PF[1]][chosen_alpha_PF[0]]
  alpha_C_obj = l_obj.players['Active'][chosen_alpha_C[1]][chosen_alpha_C[0]]
  alpha_guard_obj = l_obj.players['Active'][chosen_alpha_guard[1]][chosen_alpha_guard[0]]
  alpha_forward_obj = l_obj.players['Active'][chosen_alpha_forward[1]][chosen_alpha_forward[0]]
  alpha_general_obj = l_obj.players['Active'][chosen_alpha_general[1]][chosen_alpha_general[0]]

  beta_PG_obj = l_obj.players['Active'][chosen_beta_PG[1]][chosen_beta_PG[0]]
  beta_SG_obj = l_obj.players['Active'][chosen_beta_SG[1]][chosen_beta_SG[0]]
  beta_SF_obj = l_obj.players['Active'][chosen_beta_SF[1]][chosen_beta_SF[0]]
  beta_PF_obj = l_obj.players['Active'][chosen_beta_PF[1]][chosen_beta_PF[0]]
  beta_C_obj = l_obj.players['Active'][chosen_beta_C[1]][chosen_beta_C[0]]
  beta_guard_obj = l_obj.players['Active'][chosen_beta_guard[1]][chosen_beta_guard[0]]
  beta_forward_obj = l_obj.players['Active'][chosen_beta_forward[1]][chosen_beta_forward[0]]
  beta_general_obj = l_obj.players['Active'][chosen_beta_general[1]][chosen_beta_general[0]]
  

 
  '''      
  print (chosen_alpha_PG)
  print (chosen_alpha_SG)
  print (chosen_alpha_SF)
  print (chosen_alpha_PF)
  print (chosen_alpha_C)
  print (chosen_alpha_guard)
  print (chosen_alpha_forward)
  print (chosen_alpha_general)
  print (chosen_beta_PG)
  print (chosen_beta_SG)
  print (chosen_beta_SF)
  print (chosen_beta_PF)
  print (chosen_beta_C)
  print (chosen_beta_guard)
  print (chosen_beta_forward)
  print (chosen_beta_general)
  '''
  rosters = {\
             'Alpha':{\
                      'Starters':{\
                                  chosen_alpha_PG[0]:alpha_PG_obj,\
                                  chosen_alpha_SG[0]:alpha_SG_obj,\
                                  chosen_alpha_SF[0]:alpha_SF_obj,\
                                  chosen_alpha_PF[0]:alpha_PF_obj,\
                                  chosen_alpha_C[0]:alpha_C_obj\
                                 },\
                       'Bench':{\
                                chosen_alpha_guard[0]:alpha_guard_obj,\
                                chosen_alpha_forward[0]:alpha_forward_obj,\
                                chosen_alpha_general[0]:alpha_general_obj\
                               },\
                       'Injured':alpha_injured\
                     },\
             'Beta':{\
                      'Starters':{\
                                  chosen_beta_PG[0]:beta_PG_obj,\
                                  chosen_beta_SG[0]:beta_SG_obj,\
                                  chosen_beta_SF[0]:beta_SF_obj,\
                                  chosen_beta_PF[0]:beta_PF_obj,\
                                  chosen_beta_C[0]:beta_C_obj\
                                 },\
                       'Bench':{\
                                chosen_beta_guard[0]:beta_guard_obj,\
                                chosen_beta_forward[0]:beta_forward_obj,\
                                chosen_beta_general[0]:beta_general_obj\
                               },\
                       'Injured':beta_injured\
                     }\
                       
             }
  
  return (rosters)
  
#Requires p_tuples in eligible_players to be in form (p,pos,p_stats)
def choose_RoSo_general(l_obj,eligible_players,eligible_stats,chosen_players=None):
  print (chosen_players)
  chosen_general = None
  for p_tuple in eligible_players:
    p = p_tuple[0]
    if p in chosen_players:
      continue
    pos = p_tuple[1]
    mpg = p_tuple[-1]['MPG']
    t_imp = p_tuple[-1]['T-IMP']
    rank_index = eligible_stats['MPG'].index(mpg) + \
                 eligible_stats['T-IMP'].index(t_imp)
    print (p,rank_index)
    if not chosen_general:
      chosen_general = ([p,],[pos,],rank_index)
    elif rank_index < chosen_general[-1]:
      chosen_general = ([p,],[pos,],rank_index)
    elif rank_index == chosen_general[-1]:
      team_orig = l_obj.players['Active'][chosen_general[1][0]][chosen_general[0][0]].team_nick
      team_new = l_obj.players['Active'][pos][p].team_nick
      if team_orig == team_new:
        chosen_general[0].append(p)
        chosen_general[1].append(p)
      else:
        standings = l_obj.det_standings('League')
        if standings.index(team_orig) > standings.index(team_new):
          chosen_general = ([p,],[pos,],rank_index)
  if len(chosen_general[0]) > 1:
    p = random.choice(chosen_general[0])
    pos = chosen_general[1][chosen_general[0].index(p)]
    chosen_general = (p,pos)
  else:
    chosen_general = (chosen_general[0][0],chosen_general[1][0])
  return (chosen_general)

def choose_RoSo_forward(l_obj,eligible_players,eligible_stats,ineligible_players):
  chosen_forward = None  
  for p_tuple in eligible_players:    
    p = p_tuple[0]
    pos = p_tuple[1]
    ppg = p_tuple[-1]['PPG']
    rpg = p_tuple[-1]['RPG']
    l_imp = p_tuple[-1]['L-IMP']
    rank_index = eligible_stats['PPG'].index(ppg) + \
                 eligible_stats['RPG'].index(rpg) + \
                 eligible_stats['L-IMP'].index(l_imp)
    if not chosen_forward:
      chosen_forward = ([p,],[pos,],rank_index)
    elif rank_index < chosen_forward[-1]:
      chosen_forward = ([p,],[pos,],rank_index)
    elif rank_index == chosen_forward[-1]:
      team_orig = l_obj.players['Active'][chosen_forward[1][0]][chosen_forward[0][0]].team_nick
      team_new = l_obj.players['Active'][pos][p].team_nick
      if team_orig == team_new:
        chosen_forward[0].append(p)
        chosen_forward[1].append(p)
      else:
        standings = l_obj.det_standings('League')
        if standings.index(team_orig) > standings.index(team_new):
          chosen_forward = ([p,],[pos,],rank_index)
  if not chosen_forward:
    for p_tuple in ineligible_players:
      p = p_tuple[0]
      pos = p_tuple[1]
      mpg = p_tuple[-1]['MPG']
      if not chosen_forward:
        chosen_forward = ([p,],[pos,],mpg)
      elif mpg > chosen_forward[-1]:
        chosen_forward = ([p,],[pos,],mpg)
      elif mpg == chosen_forward[-1]:
        team_orig = l_obj.players['Active'][chosen_forward[1][0]][chosen_forward[0][0]].team_nick
        team_new = l_obj.players['Active'][pos][p].team_nick
        if team_orig == team_new:
          chosen_rook_guard[0].append(p)
          chosen_rook_guard[1].append(p)
        else:
          standings = l_obj.det_standings('League')
          if standings.index(team_orig) > standings.index(team_new):
            chosen_forward = ([p,],[pos,],mpg) 

  if len(chosen_forward[0]) > 1:
    p = random.choice(chosen_forward[0])
    pos = chosen_forward[1][chosen_forward[0].index(p)]
    chosen_forward = (p,pos)
  else:
    chosen_forward = (chosen_forward[0][0],chosen_forward[1][0])
  return (chosen_forward)

def choose_RoSo_guard(l_obj,eligible_players,eligible_stats,ineligible_players):
  chosen_guard = None  
  for p_tuple in eligible_players:
    p = p_tuple[0]
    pos = p_tuple[1]
    ppg = p_tuple[-1]['PPG']
    apg = p_tuple[-1]['APG']
    l_imp = p_tuple[-1]['L-IMP']
    rank_index = eligible_stats['PPG'].index(ppg) + \
                 eligible_stats['APG'].index(apg) + \
                 eligible_stats['L-IMP'].index(l_imp)
    if not chosen_guard:
      chosen_guard = ([p,],[pos,],rank_index)
    elif rank_index < chosen_guard[-1]:
      chosen_guard = ([p,],[pos,],rank_index)
    elif rank_index == chosen_guard[-1]:
      team_orig = l_obj.players['Active'][chosen_rook_guard[1][0]][chosen_rook_guard[0][0]].team_nick
      team_new = l_obj.players['Active'][pos][p].team_nick
      if team_orig == team_new:
        chosen_guard[0].append(p)
        chosen_guard[1].append(p)
      else:
        standings = l_obj.det_standings('League')
        if standings.index(team_orig) > standings.index(team_new):
          chosen_guard = ([p,],[pos,],rank_index)
  
  if not chosen_guard:
    for p_tuple in ineligible_players:
      p = p_tuple[0]
      pos = p_tuple[1]
      mpg = p_tuple[-1]['MPG']
      if not chosen_guard:
        chosen_guard = ([p,],[pos,],mpg)
      elif mpg > chosen_guard[-1]:
        chosen_guard = ([p,],[pos,],mpg)
      elif mpg == chosen_guard[-1]:
        team_orig = l_obj.players['Active'][chosen_guard[1][0]][chosen_guard[0][0]].team_nick
        team_new = l_obj.players['Active'][pos][p].team_nick
        if team_orig == team_new:
          chosen_guard[0].append(p)
          chosen_guard[1].append(p)
        else:
          standings = l_obj.det_standings('League')
          if standings.index(team_orig) > standings.index(team_new):
            chosen_guard = ([p,],[pos,],mpg)      
  
  if len(chosen_guard[0]) > 1:
    p = random.choice(chosen_guard[0])
    pos = chosen_rook_guard[1][chosen_guard[0].index(p)]
    chosen_guard = (p,pos)
  else:
    chosen_guard = (chosen_guard[0][0],chosen_guard[1][0])
  
  return (chosen_guard)
  
def det_RoSo_rosters(l_obj):
  league_ppg = F_CALC_L_PPG(l_obj)
  eligible_rookies = {}
  eligible_sophomores = {}
  ineligible_rookies = {}
  ineligible_sophomores = {}
  
  eligible_stats = {'PPG':[],'RPG':[],'APG':[],'MPG':[],'L-IMP':[],'T-IMP':[]}
  for pos in l_obj.players['Active']:
    eligible_rookies[pos] = []
    ineligible_rookies[pos] = []
    eligible_sophomores[pos] = []
    ineligible_sophomores[pos] = []
    for p in l_obj.players['Active'][pos]:
      p_stats = l_obj.players['Active'][pos][p].stats['Y' + str(l_obj.cur_year)]
      p_status = l_obj.players['Active'][pos][p].status
      p_years_pro = l_obj.players['Active'][pos][p].profile['Years Pro']
      if p_years_pro == 0:
        print (p,p_stats['Court Time'])
      if p_stats['Court Time'] >= 3600 and p_years_pro == 0 and p_status['Days Injured'] == 0:
        stats_dict = {}
        ppg = decimal.Decimal(p_stats['Points']/p_stats['Games Played']).quantize(ONE_DP)
        stats_dict['PPG'] = ppg
        eligible_stats['PPG'].append(ppg)
        rpg = decimal.Decimal(p_stats['Tot Reb']/p_stats['Games Played']).quantize(ONE_DP)
        stats_dict['RPG'] = rpg
        eligible_stats['RPG'].append(rpg)
        apg = decimal.Decimal(p_stats['Assists']/p_stats['Games Played']).quantize(ONE_DP)
        stats_dict['APG'] = apg
        eligible_stats['APG'].append(apg)
        mpg = decimal.Decimal((p_stats['Court Time']/60)/(p_stats['Games Played'])).quantize(ONE_DP)
        stats_dict['MPG'] = mpg
        eligible_stats['MPG'].append(mpg)
        l_imp = decimal.Decimal(F_CALC_P_LEAGUE_TOT_IMPACT(p_stats)).quantize(ONE_DP)
        stats_dict['L-IMP'] = l_imp
        eligible_stats['L-IMP'].append(l_imp)
        t_imp = decimal.Decimal(F_CALC_P_TEAM_TOT_IMPACT(p_stats)).quantize(ONE_DP)
        stats_dict['T-IMP'] = t_imp
        eligible_stats['T-IMP'].append(t_imp)
        eligible_rookies[pos].append((p,pos,stats_dict))
      elif p_years_pro == 0 and p_status['Days Injured'] == 0:
        ineligible_rookies[pos].append((p,p_stats['Court Time']))
      elif p_stats['Court Time'] >= 7200 and p_years_pro == 1 and p_status['Days Injured'] == 0:
        stats_dict = {}
        ppg = decimal.Decimal(p_stats['Points']/p_stats['Games Played']).quantize(ONE_DP)
        stats_dict['PPG'] = ppg
        eligible_stats['PPG'].append(ppg)
        rpg = decimal.Decimal(p_stats['Tot Reb']/p_stats['Games Played']).quantize(ONE_DP)
        stats_dict['RPG'] = rpg
        eligible_stats['RPG'].append(rpg)
        apg = decimal.Decimal(p_stats['Assists']/p_stats['Games Played']).quantize(ONE_DP)
        stats_dict['APG'] = apg
        eligible_stats['APG'].append(apg)
        mpg = decimal.Decimal((p_stats['Court Time']/60)/(p_stats['Games Played'])).quantize(ONE_DP)
        stats_dict['MPG'] = mpg
        eligible_stats['MPG'].append(mpg)
        l_imp = decimal.Decimal(F_CALC_P_LEAGUE_TOT_IMPACT(p_stats)).quantize(ONE_DP)
        stats_dict['L-IMP'] = l_imp
        eligible_stats['L-IMP'].append(l_imp)
        t_imp = decimal.Decimal(F_CALC_P_TEAM_TOT_IMPACT(p_stats)).quantize(ONE_DP)
        stats_dict['T-IMP'] = t_imp
        eligible_stats['T-IMP'].append(t_imp)
        eligible_sophomores[pos].append((p,pos,stats_dict))          
      elif p_years_pro == 1 and p_status['Days Injured'] == 0:
        ineligible_sophomores[pos].append((p,p_stats['Court Time']))
  eligible_stats['PPG'].sort(reverse=True)
  eligible_stats['RPG'].sort(reverse=True)
  eligible_stats['APG'].sort(reverse=True)
  eligible_stats['MPG'].sort(reverse=True)
  eligible_stats['L-IMP'].sort(reverse=True)
  eligible_stats['T-IMP'].sort(reverse=True) 
  
  chosen_rook_guard = choose_RoSo_guard(l_obj,\
      eligible_rookies['PG']+eligible_rookies['SG'],\
      eligible_stats,\
      ineligible_rookies['PG']+ineligible_rookies['SG'])
  chosen_rook_forward = choose_RoSo_forward(l_obj,\
      eligible_rookies['SF']+eligible_rookies['PF']+eligible_rookies['C'],\
      eligible_stats,\
      ineligible_rookies['SF']+ineligible_rookies['PF']+ineligible_rookies['C'])
  chosen_rook_general = choose_RoSo_general(l_obj,eligible_rookies['PG']+eligible_rookies['SG']+eligible_rookies['SF']+eligible_rookies['PF']+eligible_rookies['C'],eligible_stats,(chosen_rook_guard[0],chosen_rook_forward[0]))
  
  chosen_soph_guard = choose_RoSo_guard(l_obj,\
      eligible_sophomores['PG']+eligible_sophomores['SG'],\
      eligible_stats,\
      ineligible_sophomores['PG']+ineligible_sophomores['SG'])
  chosen_soph_forward = choose_RoSo_forward(l_obj,\
      eligible_sophomores['SF']+eligible_sophomores['PF']+eligible_sophomores['C'],\
      eligible_stats,\
      ineligible_sophomores['SF']+ineligible_sophomores['PF']+ineligible_sophomores['C']
      )
  chosen_soph_general = choose_RoSo_general(l_obj,eligible_sophomores['PG']+eligible_sophomores['SG']+eligible_sophomores['SF']+eligible_sophomores['PF']+eligible_sophomores['C'],eligible_stats,(chosen_soph_guard[0],chosen_soph_forward[0]))
  
  rook_guard_obj = l_obj.players['Active'][chosen_rook_guard[1]][chosen_rook_guard[0]]
  rook_forward_obj = l_obj.players['Active'][chosen_rook_forward[1]][chosen_rook_forward[0]]
  rook_general_obj = l_obj.players['Active'][chosen_rook_general[1]][chosen_rook_general[0]]
  soph_guard_obj = l_obj.players['Active'][chosen_soph_guard[1]][chosen_soph_guard[0]]
  soph_forward_obj = l_obj.players['Active'][chosen_soph_forward[1]][chosen_soph_forward[0]]
  soph_general_obj = l_obj.players['Active'][chosen_soph_general[1]][chosen_soph_general[0]]
        
  print (eligible_rookies)
  print (chosen_rook_guard)
  print (chosen_rook_forward)
  print (chosen_rook_general)
  print (chosen_soph_guard)
  print (chosen_soph_forward)
  print (chosen_soph_general)
  rosters = {'Rookies':{chosen_rook_guard[0]:rook_guard_obj,\
                        chosen_rook_forward[0]:rook_forward_obj,\
                        chosen_rook_general[0]:rook_general_obj\
                       },\
             'Sophomores':{chosen_soph_guard[0]:soph_guard_obj,\
                           chosen_soph_forward[0]:soph_forward_obj,\
                           chosen_soph_general[0]:soph_general_obj\
                          }\
             }
  
  return (rosters)

def run_3PC_match(p_1_name,p_1_team,p_1_rating,p_2_name,p_2_team,p_2_rating,output_f=None):
  random.seed()
  name_len = 8
  shots_1 = []
  shots_2 = []
  score_1 = 0
  score_2 = 0
  three_per_1 = p_1_rating / 2
  three_per_2 = p_2_rating / 2
  
  rack = 1
  sudden_death = False
  rack_line_1 = '| ' + '{:<{l}}'.format(p_1_name,l=name_len) + ' ||'
  rack_line_2 = '| ' + '{:<{l}}'.format(p_2_name,l=name_len) + ' ||'
  divider = '+-' + (name_len)*'-' + '-++'
  while (rack <= 5):
    ball = 1
    while (ball <= 5):
      if ball == 5:
        made_str = 'O'
        missed_str = 'X'
        points = 2
      else:
        made_str = 'o'
        missed_str = 'x'
        points = 1
      X_1 = random.random()*100
      X_2 = random.random()*100
      if (X_1 < three_per_1):
        rack_line_1 += ' ' + made_str 
        score_1 += points
      else:
        rack_line_1 += ' ' + missed_str 
      if (X_2 < three_per_2):
        rack_line_2 += ' ' + made_str
        score_2 += points
      else:
        rack_line_2 += ' ' + missed_str
      divider += '--'
      ball += 1
    rack_line_1 += ' |'
    rack_line_2 += ' |' 
    divider += '-+'
    rack += 1
        
  rack_line_1 += '|'
  rack_line_2 += '|'
  divider += '+'
    
     
  while score_1 == score_2:
    sudden_death = True
    made_str = 'o'
    missed_str = 'x'
    points = 1       
    X_1 = random.random()*100
    X_2 = random.random()*100
    if X_1 < three_per_1:
      rack_line_1 += ' ' + made_str
      score_1 += points
    else:
      rack_line_1 += ' ' + missed_str
    if X_2 < three_per_2:    
      rack_line_2 += ' ' + made_str
      score_2 += points
    else:
      rack_line_2 += ' ' + missed_str
    divider += '--'
  if sudden_death == True:
    rack_line_1 += ' ||'
    rack_line_2 += ' ||' 
    divider += '-++'
  rack_line_1 += ' Total ' + '{:>{l}}'.format(score_1,l=2) + ' |'
  rack_line_2 += ' Total ' + '{:>{l}}'.format(score_2,l=2) + ' |'
  divider += '----------+'
  if score_1 > score_2:
    winner = p_1_name
  else:
    winner = p_2_name
  print (divider)
  print (rack_line_1)
  print (divider) 
  print (rack_line_2)  
  print (divider)
  print ('\n')
  
  if output_f:
    output_f.write(divider + '\n')
    output_f.write(rack_line_1 + '\n')
    output_f.write(divider + '\n')
    output_f.write(rack_line_2 + '\n')
    output_f.write(divider + '\n')
    output_f.write('\n')  
  return (winner)