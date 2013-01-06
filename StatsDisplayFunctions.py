#from Menus import *
from GlobalVariables import *
import decimal
from GlobalFunctions import *
def ask_normalisation():
  reply = input("Stats per game (G), per 40 minutes (M) or totals (T)? ").rstrip()
  while 1:    
    if reply in ('G','g'):
      norm = 'PG'
      break
    elif reply in ('M','m'):
      norm = 'P40'
      break
    elif reply in ('T','t'):
      norm = 'Tot'
      break
    else:
      reply = input("Invalid input. Stats per game (G) or per 40 minutes (M)? ").rstrip()
  return (norm)

def ask_ascending():
  chosen = False
  reply = input("Ascending (A) or descending (D) order? ").rstrip()
  while chosen == False:    
    if reply in ('A','a'):
      ascending = True
      chosen = True
    elif reply in ('D','d'):
      ascending = False
      chosen = True
    else:
      reply = input("Invalid input. Ascending (A) or descending (D) order? ").rstrip()
  return (ascending)
  
def ask_qualified():
  chosen = False
  reply = input("Include qualified (Q) or all (A) players? ").rstrip()
  while chosen == False:    
    if reply in ('Q','q'):
      qualified = True
      chosen = True
    elif reply in ('A','a'):
      qualified = False
      chosen = True
    else:
      reply = input("Invalid input. Include qualified (Q) or all (A) players? ").rstrip()
  return (qualified)

def ask_career():
  chosen = False
  reply = input("Season (S) or Career (C) stats? ").rstrip()
  while chosen == False:    
    if reply in ('S','s'):
      career = False
      chosen = True
    elif reply in ('C','c'):
      career = True
      chosen = True
    else:
      reply = input("Invalid input. Season (S) or Career (C) stats? ").rstrip()
  return (career)

def player_stats_rank_options_menu():
  chosen = False
  while chosen == False:
    print ("Please select option:")
    print ("[1] Rank by name")
    print ("[2] Rank by points")
    print ("[3] Rank by total rebounds")
    print ("[4] Rank by assists")
    print ("[5] Rank by +/-")
    print ("[6] Go back")
    reply = input("-->").rstrip()
    if reply in ('1','2','3','4','5'):
      ascending = ask_ascending() 
      qualified = ask_qualified()
      career = ask_career()   
      chosen = True
      if reply == '1':
        item = 'Name'
      elif reply == '2':
        item = 'Points'
      elif reply == '3':
        item = 'Tot Reb'
      elif reply == '4':
        item = 'Assists'
      elif reply == '5':
        item = '+/-'  
    elif reply == '6':
      return (None)
    else:
      print ("***Invalid option entered. Please try again.***" )    
    
  return ({'Item':item,'Ascending':ascending,'Qualified':qualified,\
           'Career':career})

def print_rank_menu(possible_items,rank_item):
  print ("Choose Option:")
  items_list = list(possible_items)
  items_list.remove(rank_item)
  while 1:
    opt = 1
    for item in items_list:
      print ('[' + str(opt) + '] Rank by ' + item)
      opt += 1
    print ('[' + str(opt) + '] Go back')
    reply = input("-->").rstrip()  
    if reply in [str(x) for x in range(1,opt+1)]:
      if int(reply) == opt:
        return (None)
      else:
        return (items_list[int(reply)-1])
    else:
      print ("***Invalid option entered. Please try again.***" )    

def eff_stats_func(l_obj):
  qual = ask_qualified()
  possible_items = ('Name','eFG%','Pts Per Poss','Pts For P40 On Court',\
                    'Pts For P40 Off Court','Off Impact',\
                    'Pts Against P40 On Court','Pts Against P40 Off Court',
                    'Def Impact','Tot Impact')
  rank_item = 'Tot Impact'
  
  while 1:
    print_eff_stats(l_obj,False,'RS',rank_item,qual)
    input('Press ENTER to continue')
    rank_item = print_rank_menu(possible_items,rank_item)
    if not rank_item:
      break 
  return
  
def print_eff_stats(l_obj,career,game_type,rank_item,qual):  

  appeared = []
  not_appeared = []
  for pos in l_obj.players['Active']:
    for p in l_obj.players['Active'][pos]: 
      is_qual = False
      if career == True:
        y_str = 'Career'
      else:
        y_str = 'Y' + str(l_obj.cur_year)
      p_stats = l_obj.players['Active'][pos][p].stats[y_str]

      if rank_item == 'Name':
        rank_stat = p
        if p_stats['Games Played']*2 >= p_stats['Team Games']:
          is_qual = True
      elif rank_item == 'eFG%':
        if p_stats['FGA'] >= p_stats['Team Games']*4:
          is_qual = True
        if p_stats['FGA'] == 0:
          rank_stat = -1
        else:
          rank_stat = (p_stats['2PFGM']+1.5*p_stats['3PFGM'])/p_stats['FGA']
      elif rank_item == 'Pts Per Poss':
        if (p_stats['FGA'] + p_stats['Fouls Drawn']) >= p_stats['Team Games']*5:
         is_qual = True
        if (p_stats['FGA'] + p_stats['Fouls Drawn']) == 0:
          rank_stat = -1
        else:
          rank_stat = p_stats['Points']/(p_stats['FGA'] + p_stats['Fouls Drawn'])
        '''
        if p_stats['Possessions'] >= p_stats['Team Games']*5:
          is_qual = True
        if p_stats['Possessions'] == 0:
          rank_stat = -1
        else: 
          rank_stat = p_stats['Points']/p_stats['Possessions']
        '''
      elif rank_item == 'Pts For P40 On Court':
        if p_stats['Games Played']*2 >= p_stats['Team Games']:
          is_qual = True
        if p_stats['Court Time'] == 0:
          rank_stat = -1
        else:
          rank_stat = F_CALC_P_PTS_FOR_P40_ON(p_stats)
      elif rank_item == 'Pts For P40 Off Court':
        if p_stats['Games Played']*2 >= p_stats['Team Games']:
          is_qual = True
        if (p_stats['Team Court Time'] - p_stats['Court Time']) == 0:
          rank_stat = -1
        else:
          rank_stat = F_CALC_P_PTS_FOR_P40_OFF(p_stats)
      elif rank_item == 'Off Impact':
        if p_stats['Games Played']*2 >= p_stats['Team Games']:
          is_qual = True
        if p_stats['Court Time'] == 0 or (p_stats['Team Court Time'] - p_stats['Court Time']) == 0:
          rank_stat = -1
        else:
          rank_stat = F_CALC_P_TEAM_OFF_IMPACT(p_stats)    
      elif rank_item == 'Pts Against P40 On Court':
        if p_stats['Games Played']*2 >= p_stats['Team Games']:
          is_qual = True
        if p_stats['Court Time'] == 0:
          rank_stat = -1
        else:
          rank_stat = F_CALC_P_PTS_AGAINST_P40_ON(p_stats)
      elif rank_item == 'Pts Against P40 Off Court':
        if p_stats['Games Played']*2 >= p_stats['Team Games']:
          is_qual = True
        if (p_stats['Team Court Time'] - p_stats['Court Time']) == 0:
          rank_stat = -1
        else:
          rank_stat = F_CALC_P_PTS_AGAINST_P40_OFF(p_stats)
      elif rank_item == 'Def Impact':
        if p_stats['Games Played']*2 >= p_stats['Team Games']:
          is_qual = True
        if p_stats['Court Time'] == 0 or (p_stats['Team Court Time'] - p_stats['Court Time']) == 0:
          rank_stat = -1
        else:
          rank_stat = F_CALC_P_TEAM_DEF_IMPACT(p_stats)
      elif rank_item == 'Tot Impact':
        if p_stats['Games Played']*2 >= p_stats['Team Games']:
          is_qual = True
        if p_stats['Court Time'] == 0 or (p_stats['Team Court Time'] - p_stats['Court Time']) == 0:
          rank_stat = -1
        else:
          rank_stat = F_CALC_P_TEAM_TOT_IMPACT(p_stats)
            
            
      if p_stats['Court Time'] > 0:
        if qual == True and is_qual == False:
          not_appeared.append(p)
          continue
        basic_pg_dict = {}
        if len(appeared) == 0:
          i = 0
        else:
          for other_p_item in appeared: 
            if rank_stat > other_p_item[1]:
              i = appeared.index(other_p_item)
              break
            elif rank_stat == other_p_item[1]:
              if p < other_p_item[0]:
                i = appeared.index(other_p_item)
                break
              elif other_p_item == appeared[-1]:
                i = len(appeared)
                break
              else:
                continue  
            elif other_p_item == appeared[-1]:
              i = len(appeared)
              break
            
        appeared.insert(i,(p,rank_stat,{}))
        for s in ('Court Time','Possessions','Points','2PFGM','3PFGM','FGA',\
                  'Team Points For','Team Points Against','All Team Points F',\
                  'All Team Points A','Team Court Time','Fouls Drawn'):
          appeared[i][2][s] = p_stats[s]
        appeared[i][2]['Games Played'] = p_stats['Games Played']
        appeared[i][2]['Games Started'] = p_stats['Games Started']
        appeared[i][2]['Pos'] = pos
        appeared[i][2]['Team Nick'] = l_obj.players['Active'][pos][p].team_nick
      else:
        not_appeared.append(p)
  
  titles = ('Player','Pos','Team','  G',' GS',' Min',' eFG%',\
            'Pt/Po','PtF/40-ON','PtF/40-OFF','Off-Imp','PtA/40-ON',\
            'PtA/40-OFF','Def-Imp','Tot-Imp')
  title_line = 'Rank '
  line_len = 5
  for s in titles:
    title_line += s + ' '
    line_len += len(s) + 1
  line_len -= 1
  print ('{:-^{l}}'.format(l_obj.name + ' stats: ',l=line_len))
  print (title_line)
  
  rank = 1  
  for p_item in appeared:
    line = '{:>{l}}'.format(rank,l=4) + ' '
    name = p_item[0]
    stats = p_item[2]
    line += '{:<{l}}'.format(name,l=len(titles[0])) + ' '
    
    pos_str = p_item[2]['Pos']
    line += '{:>{l}}'.format(pos_str,l=len(titles[1])) + ' '
        
    t_str = p_item[2]['Team Nick']
    line += '{:>{l}}'.format(t_str,l=len(titles[2])) + ' '
      
    g_str = str(stats['Games Played'])
    line += '{:>{l}}'.format(g_str,l=len(titles[3])) + ' '
      
    gs_str = str(stats['Games Started'])
    line += '{:>{l}}'.format(gs_str,l=len(titles[4])) + ' '
    

    min_str = str(decimal.Decimal(stats['Court Time']/stats['Games Played']/60)\
                  .quantize(ONE_DP))
    line += '{:>{l}}'.format(min_str,l=len(titles[5])) + ' '
      
    
     
    if stats['FGA'] == 0:
      efg_per_str = ' N/A '
    else:
      efg_per = (stats['2PFGM']+1.5*stats['3PFGM'])/stats['FGA']
      efg_per_str = str(decimal.Decimal(efg_per).quantize(THREE_DP))
    line += efg_per_str + ' '
    
    if (stats['FGA'] + stats['Fouls Drawn']) == 0:
      p_per_pos_str = ' N/A '
    else:
      p_per_pos_str = str(decimal.Decimal(stats['Points']/stats['Possessions']).quantize(THREE_DP))
    '''
    if stats['Possessions'] == 0:
      p_per_pos_str = ' N/A '
    else:
      p_per_pos_str = str(decimal.Decimal(stats['Points']/stats['Possessions']).quantize(THREE_DP))
    '''
    line += p_per_pos_str + ' '
    
    if stats['Court Time'] == 0:
      pf_p40_on_str = '   N/A   '
    else:
      pf_p40_on = decimal.Decimal(F_CALC_P_PTS_FOR_P40_ON(stats)).quantize(TWO_DP)
      pf_p40_on_str = '{:^{l}}'.format(pf_p40_on,l=len(titles[8]))
    line += pf_p40_on_str + ' '
    
    if (stats['Team Court Time'] - stats['Court Time']) == 0:
      pf_p40_off_str = '    N/A   '
    else:
      pf_p40_off = decimal.Decimal(F_CALC_P_PTS_FOR_P40_OFF(stats)).quantize(TWO_DP)
      pf_p40_off_str = '{:^{l}}'.format(pf_p40_off,l=len(titles[9]))
    line += pf_p40_off_str + ' '
    
    if stats['Court Time'] == 0 or (stats['Team Court Time'] - stats['Court Time']) == 0:
      off_imp_str = '  N/A  '
    else:
      off_imp = pf_p40_on - pf_p40_off
      if off_imp >= 0:
        off_imp_str = '+' + str(off_imp)
      else:
        off_imp_str = str(off_imp)
      off_imp_str = '{:^{l}}'.format(off_imp_str,l=len(titles[10]))
    line += off_imp_str + ' '
    
    if stats['Court Time'] == 0:
      pa_p40_on_str = '   N/A   '
    else:
      pa_p40_on = decimal.Decimal(F_CALC_P_PTS_AGAINST_P40_ON(stats)).quantize(TWO_DP)
      pa_p40_on_str = '{:^{l}}'.format(pa_p40_on,l=len(titles[11]))
    line += pa_p40_on_str + ' '
    
    if (stats['Team Court Time'] - stats['Court Time']) == 0:
      pa_p40_off_str = '    N/A   '
    else:
      pa_p40_off = decimal.Decimal(F_CALC_P_PTS_AGAINST_P40_OFF(stats)).quantize(TWO_DP)
      pa_p40_off_str = '{:^{l}}'.format(pa_p40_off,l=len(titles[12]))
    line += pa_p40_off_str + ' '
    
    if stats['Court Time'] == 0 or (stats['Team Court Time'] - stats['Court Time']) == 0:
      def_imp_str = '  N/A  '
    else:
      def_imp = pa_p40_off - pa_p40_on
      if def_imp < 0:
        def_imp_str = str(def_imp)
      else:
        def_imp_str = '+' + str(def_imp)
      def_imp_str = '{:^{l}}'.format(def_imp_str,l=len(titles[13]))      
    line += def_imp_str + ' '
              
    if stats['Court Time'] == 0 or (stats['Team Court Time'] - stats['Court Time']) == 0:
      tot_imp_str = '  N/A  '
    else:
      tot_imp = off_imp + def_imp
      if tot_imp < 0:
        tot_imp_str = str(tot_imp)
      else:
        tot_imp_str = '+' + str(tot_imp)
      tot_imp_str = '{:^{l}}'.format(tot_imp_str,l=len(titles[14]))      
    line += tot_imp_str + ' '
                                                                                                
    print (line) 
    rank += 1
  
  print ('-'*(line_len))  
  return

def adv_stats_func(l_obj):
  norm = ask_normalisation()
  qual = ask_qualified()
  if norm == 'PG':
    possible_items = ('Name','Court Time','Put Backs M','Put Backs A','PB%',\
                      'Inside FGM','Inside FGA','Inside FG%','2PJFGM','2PJFGA',\
                      '2PJFG%','Inside Pts','Perimeter Pts','2nd Chance Pts',\
                      'Touches','Passes','Inside Fouls','Per Fouls',\
                      'Inside Fouls Drawn','Per Fouls Drawn')
  else:
    possible_items = ('Name','Put Backs M','Put Backs A','PB%',\
                      'Inside FGM','Inside FGA','Inside FG%','2PJFGM','2PJFGA',\
                      '2PJFG%','Inside Pts','Perimeter Pts','2nd Chance Pts',\
                      'Touches','Passes','Inside Fouls','Per Fouls',\
                      'Inside Fouls Drawn','Per Fouls Drawn')
  
  rank_item = 'Court Time'
  print_adv_stats(l_obj,False,'RS',rank_item,norm,qual)
  while 1:
    reply = input('Press ENTER to continue')
    rank_item = print_rank_menu(possible_items,rank_item)
    if not rank_item:
      break
    else:
      print_adv_stats(l_obj,False,'RS',rank_item,norm,qual)
  return
  
#-----------------------------------------------------------------------------
# Function print_adv_stats
#
# VC: Game type functionality?
#-----------------------------------------------------------------------------
def print_adv_stats(l_obj,career,game_type,rank_item,norm,qual):
  stat_seq = ('Court Time','Put Backs M','Put Backs A',\
              'Inside FGM','Inside FGA','2PJFGM','2PJFGA',\
              'Inside Pts','Perimeter Pts','2nd Chance Pts',\
              'Touches','Passes','Inside Fouls','Per Fouls',\
              'Inside Fouls Drawn','Per Fouls Drawn')

  appeared = []
  not_appeared = []
  for pos in l_obj.players['Active']:
    for p in l_obj.players['Active'][pos]: 
      is_qual = False
      if career == True:
        y_str = 'Career'
      else:
        y_str = 'Y' + str(l_obj.cur_year)
      p_stats = l_obj.players['Active'][pos][p].stats[y_str]
      if norm == 'PG':
        if p_stats['Games Played'] == 0:
          norm_fac = None
        else:
          norm_fac = 1.0/p_stats['Games Played']
      elif norm == 'P40':
        if p_stats['Court Time'] == 0:
          norm_fac = None
        else:
          norm_fac = 2400.0/p_stats['Court Time'] 
      elif norm == 'Tot':
        if p_stats['Court Time'] == 0:
          norm_fac == None
        else:
          norm_fac = 1
      if rank_item == 'Name':
        rank_stat = p
        if p_stats['Games Played']*2 >= p_stats['Team Games']:
          is_qual = True
      elif rank_item == 'PB%':
        if p_stats['Put Backs A'] >= p_stats['Team Games']*0.5:
          is_qual = True
        if p_stats['Put Backs A'] == 0:
          rank_stat = -1
        else:
          rank_stat = 1.0*p_stats['Put Backs M']/p_stats['Put Backs A']
      elif rank_item == 'Inside FG%':
        if p_stats['Inside FGA'] >= p_stats['Team Games']*2:
          is_qual = True
        if p_stats['Inside FGA'] == 0:
          rank_stat = -1
        else: 
          rank_stat = 1.0*p_stats['Inside FGM']/p_stats['Inside FGA']
      elif rank_item == '2PJFG%':
        if p_stats['2PJFGA'] >= p_stats['Team Games']*2:
          is_qual = True
        if p_stats['2PJFGA'] == 0:
          rank_stat = -1
        else:
          rank_stat = 1.0*p_stats['2PJFGM']/p_stats['2PJFGA']
      else:
        if p_stats['Games Played']*2 >= p_stats['Team Games']:
          is_qual = True
        if p_stats['Court Time'] > 0:
          rank_stat = p_stats[rank_item]*norm_fac
        else: 
          pass
      if p_stats['Court Time'] > 0:
        if qual == True and is_qual == False:
          not_appeared.append(p)
          continue
        basic_pg_dict = {}
        if len(appeared) == 0:
          i = 0
        else:
          for other_p_item in appeared: 
            if rank_stat > other_p_item[1]:
              i = appeared.index(other_p_item)
              break
            elif rank_stat == other_p_item[1]:
              if p < other_p_item[0]:
                i = appeared.index(other_p_item)
                break
              elif other_p_item == appeared[-1]:
                i = len(appeared)
                break
              else:
                continue  
            elif other_p_item == appeared[-1]:
              i = len(appeared)
              break
            
        appeared.insert(i,(p,rank_stat,{}))
        for s in stat_seq:
          appeared[i][2][s] = 1.0*p_stats[s]*norm_fac
        appeared[i][2]['Games Played'] = p_stats['Games Played']
        appeared[i][2]['Games Started'] = p_stats['Games Started']
        appeared[i][2]['Pos'] = pos
        appeared[i][2]['Team Nick'] = l_obj.players['Active'][pos][p].team_nick
      else:
        not_appeared.append(p)
      
  titles = ('Player','Pos','Team','  G',' GS',' Min','  PBM-A  ',' PB% ',\
            ' InFGM-A ',' IFG%',' 2JFGM-A ','2JFG%','IPts','PPts',\
            '2CPt','Tchs','Pass','IFC','PFC','IFD','PFD')  
  title_line = 'Rank '
  line_len = 5
  for s in titles:
    if s == ' Min' and norm == 'P40':
      continue
    title_line += s + ' '
    line_len += len(s) + 1
  line_len -= 1
  print ('{:-^{l}}'.format(l_obj.name + ' stats: ',l=line_len))
  print (title_line)
  
  rank = 1  
  for p_item in appeared:
    line = '{:>{l}}'.format(rank,l=4) + ' '
    name = p_item[0]
    stats = p_item[2]
    line += '{:<{l}}'.format(name,l=len(titles[0])) + ' '
    
    pos_str = p_item[2]['Pos']
    line += '{:>{l}}'.format(pos_str,l=len(titles[1])) + ' '
        
    t_str = p_item[2]['Team Nick']
    line += '{:>{l}}'.format(t_str,l=len(titles[2])) + ' '
      
    g_str = str(stats['Games Played'])
    line += '{:>{l}}'.format(g_str,l=len(titles[3])) + ' '
      
    gs_str = str(stats['Games Started'])
    line += '{:>{l}}'.format(gs_str,l=len(titles[4])) + ' '
    
    if norm == 'P40':  
      pass
    else:
      min_str = str(decimal.Decimal(stats['Court Time']/60)\
                    .quantize(ONE_DP))
      line += '{:>{l}}'.format(min_str,l=len(titles[5])) + ' '
      
    pbm_str = str(decimal.Decimal(stats['Put Backs M']).quantize(ONE_DP))
    pba_str = str(decimal.Decimal(stats['Put Backs A']).quantize(ONE_DP))
    pb_str = '{:>4}'.format(pbm_str) + '-' + '{:<4}'.format(pba_str)
    line += pb_str + ' '
      
    if stats['Put Backs A'] == 0:
      pb_per_str = ' N/A '
    else:
      pb_per_str = str(decimal.Decimal(stats['Put Backs M']/stats['Put Backs A'])\
                                              .quantize(THREE_DP))
    line += pb_per_str + ' '
      
    in_m_str = str(decimal.Decimal(stats['Inside FGM']).quantize(ONE_DP))
    in_a_str = str(decimal.Decimal(stats['Inside FGA']).quantize(ONE_DP))
    in_str = '{:>4}'.format(in_m_str) + '-' + '{:<4}'.format(in_a_str)
    line += in_str + ' '
      
    if stats['Inside FGA'] == 0:
      in_per_str = ' N/A '
    else:
      in_per_str = str(decimal.Decimal(stats['Inside FGM']/stats['Inside FGA'])\
                                                   .quantize(THREE_DP))
    line += in_per_str + ' '
      
    jump_m_str = str(decimal.Decimal(stats['2PJFGM']).quantize(ONE_DP))
    jump_a_str = str(decimal.Decimal(stats['2PJFGA']).quantize(ONE_DP))
    jump_str = '{:>4}'.format(jump_m_str) + '-' + '{:<4}'.format(jump_a_str)
    line += jump_str + ' '
     
    if stats['2PJFGA'] == 0:
      jump_per_str = ' N/A '
    else:
      jump_per_str = str(decimal.Decimal(stats['2PJFGM']/stats['2PJFGA'])\
                                              .quantize(THREE_DP))
    line += jump_per_str + ' '
  
    in_pts_str = str(decimal.Decimal(stats['Inside Pts']).quantize(ONE_DP))
    line += '{:>{l}}'.format(in_pts_str,l=len(titles[12])) + ' '
      
    per_pts_str = str(decimal.Decimal(stats['Perimeter Pts']).quantize(ONE_DP))
    line += '{:>{l}}'.format(per_pts_str,l=len(titles[13])) + ' '                
                     
    sec_chance_str = str(decimal.Decimal(stats['2nd Chance Pts']).quantize(ONE_DP))
    line += '{:>{l}}'.format(sec_chance_str,l=len(titles[14])) + ' '
      
    tch_str = str(decimal.Decimal(stats['Touches']).quantize(ONE_DP))
    line += '{:>{l}}'.format(tch_str,l=len(titles[15])) + ' '                
                    
    pass_str = str(decimal.Decimal(stats['Passes']).quantize(ONE_DP))
    line += '{:>{l}}'.format(pass_str,l=len(titles[16])) + ' '                
                      
    in_foul_str = str(decimal.Decimal(stats['Inside Fouls']).quantize(ONE_DP))
    line += '{:>{l}}'.format(in_foul_str,l=len(titles[17])) + ' '                 
                      
    per_foul_str = str(decimal.Decimal(stats['Per Fouls']).quantize(ONE_DP))
    line += '{:>{l}}'.format(per_foul_str,l=len(titles[18])) + ' '                                       

    in_foul_c_str = str(decimal.Decimal(stats['Inside Fouls Drawn']).quantize(ONE_DP))
    line += '{:>{l}}'.format(in_foul_c_str,l=len(titles[19])) + ' '                 

    per_foul_c_str = str(decimal.Decimal(stats['Per Fouls Drawn']).quantize(ONE_DP))
    line += '{:>{l}}'.format(per_foul_c_str,l=len(titles[20])) + ' '                 
                                                                                        
    print (line) 
    rank += 1
  #for p in sorted(not_appeared):  
  #  line = '{:<{l}}'.format(p,l=len(basic_title_str[0])) + ' '
  #  line += 'Yet to appear this season'
  #  print (line)
  
  print ('-'*(line_len))  
  return  
  
def basic_stats_func(l_obj):
  norm = ask_normalisation()
  qual = ask_qualified()
  if norm == 'PG':
    possible_items = ('Name','Court Time','FGM','FGA','FG%','3PFGM','3PFGA',\
                      '3PFG%','FTM','FTA','FT%','+/-','Off Reb','Tot Reb',\
                      'Assists','Fouls','Points')
  else:
    possible_items = ('Name','FGM','FGA','FG%','3PFGM','3PFGA',\
                      '3PFG%','FTM','FTA','FT%','+/-','Off Reb','Tot Reb',\
                      'Assists','Fouls','Points')
  
  rank_item = 'Points'
  print_basic_stats(l_obj,False,'RS',rank_item,norm,qual)
  while 1:
    reply = input('Press ENTER to continue')
    rank_item = print_rank_menu(possible_items,rank_item)
    if not rank_item:
      break
    else:
      print_basic_stats(l_obj,False,'RS',rank_item,norm,qual)
  return

#-----------------------------------------------------------------------------
# Function print_basic_stats
#
# VC: Game type functionality?
#-----------------------------------------------------------------------------
def print_basic_stats(l_obj,career,game_type,rank_item,norm,qual):
  stat_seq = ('Court Time','FGM','FGA','3PFGM','3PFGA','FTM','FTA',\
              '+/-','Off Reb','Tot Reb','Assists','Fouls','Points')

  appeared = []
  not_appeared = []
  for pos in l_obj.players['Active']:
    for p in l_obj.players['Active'][pos]: 

      is_qual = False
      if career == True:
        y_str = 'Career'
      else:
        y_str = 'Y' + str(l_obj.cur_year)
      p_stats = l_obj.players['Active'][pos][p].stats[y_str]
      if norm == 'PG':
        if p_stats['Games Played'] == 0:
          norm_fac = None
        else:
          norm_fac = 1.0/p_stats['Games Played']
      elif norm == 'P40':
        if p_stats['Court Time'] == 0:
          norm_fac = None
        else:
          norm_fac = 2400.0/p_stats['Court Time'] 
      elif norm == 'Tot':
        if p_stats['Court Time'] == 0:
          norm_fac == None
        else:
          norm_fac = 1          
      if rank_item == 'Name':
        rank_stat = p
        if p_stats['Games Played']*2 >= p_stats['Team Games']:
          is_qual = True
      elif rank_item == 'FG%':
        if p_stats['FGA'] >= p_stats['Team Games']*4:
          is_qual = True
        if p_stats['FGA'] == 0:
          rank_stat = -1
        else:
          rank_stat = 1.0*p_stats['FGM']/p_stats['FGA']
      elif rank_item == '3PFG%':
        if p_stats['3PFGA'] >= p_stats['Team Games']*2:
          is_qual = True
        if p_stats['3PFGA'] == 0:
          rank_stat = -1
        else: 
          rank_stat = 1.0*p_stats['3PFGM']/p_stats['3PFGA']
      elif rank_item == 'FT%':
        if p_stats['FTA'] >= p_stats['Team Games']*2:
          is_qual = True
        if p_stats['FTA'] == 0:
          rank_stat = -1
        else:
          rank_stat = 1.0*p_stats['FTM']/p_stats['FTA']
      else:
        if p_stats['Games Played']*2 >= p_stats['Team Games']:
          is_qual = True
        if p_stats['Court Time'] > 0:
          rank_stat = p_stats[rank_item]*norm_fac
        else: 
          pass
      if p_stats['Court Time'] > 0:
        if qual == True and is_qual == False:
          not_appeared.append(p)
          continue
        basic_pg_dict = {}
        if len(appeared) == 0:
          i = 0
        else:
          for other_p_item in appeared: 
            if rank_stat > other_p_item[1]:
              i = appeared.index(other_p_item)
              break
            elif rank_stat == other_p_item[1]:
              if p < other_p_item[0]:
                i = appeared.index(other_p_item)
                break
              elif other_p_item == appeared[-1]:
                i = len(appeared)
                break
              else:
                continue  
            elif other_p_item == appeared[-1]:
              i = len(appeared)
              break
            
        appeared.insert(i,(p,rank_stat,{}))
        for s in stat_seq:
          appeared[i][2][s] = 1.0*p_stats[s]*norm_fac
        appeared[i][2]['Games Played'] = p_stats['Games Played']
        appeared[i][2]['Games Started'] = p_stats['Games Started']
        appeared[i][2]['Pos'] = pos
        appeared[i][2]['Team Nick'] = l_obj.players['Active'][pos][p].team_nick
      else:
        not_appeared.append(p)
      
  titles = ('Player','Pos','Team','  G',' GS',' Min','  FGM-A  ',' FG% ',\
            '  3PM-A  ',' 3P% ','  FTM-A  ',' FT% ',' +/- ','OReb',\
            'TReb',' Ast',' Fls',' Pts')  
  title_line = 'Rank '
  line_len = 5
  for s in titles:
    if s == ' Min' and norm == 'P40':
      continue
    title_line += s + ' '
    line_len += len(s) + 1
  line_len -= 1
  print ('{:-^{l}}'.format(l_obj.name + ' stats: ',l=line_len))
  print (title_line)
  
  rank = 1  
  for p_item in appeared:
    line = '{:>{l}}'.format(rank,l=4) + ' '
    name = p_item[0]
    stats = p_item[2]
    
    line += '{:<{l}}'.format(name,l=len(titles[0])) + ' '
    
    pos_str = p_item[2]['Pos']
    line += '{:>{l}}'.format(pos_str,l=len(titles[1])) + ' '
      
    t_str = p_item[2]['Team Nick']
    line += '{:>{l}}'.format(t_str,l=len(titles[2])) + ' '
      
    g_str = str(stats['Games Played'])
    line += '{:>{l}}'.format(g_str,l=len(titles[3])) + ' '
      
    gs_str = str(stats['Games Started'])
    line += '{:>{l}}'.format(gs_str,l=len(titles[4])) + ' '
    
    if norm == 'P40':  
      pass
    else:
      min_str = str(decimal.Decimal(stats['Court Time']/60)\
                    .quantize(ONE_DP))
      line += '{:>{l}}'.format(min_str,l=len(titles[5])) + ' '
      
    fgm_str = str(decimal.Decimal(stats['FGM']).quantize(ONE_DP))
    fga_str = str(decimal.Decimal(stats['FGA']).quantize(ONE_DP))
    fg_str = '{:>4}'.format(fgm_str) + '-' + '{:<4}'.format(fga_str)
    line += fg_str + ' '
      
    if stats['FGA'] == 0:
      fg_per_str = ' N/A '
    else:
      fg_per_str = str(decimal.Decimal(stats['FGM']/stats['FGA'])\
                                              .quantize(THREE_DP))
    line += fg_per_str + ' '
      
    thr_m_str = str(decimal.Decimal(stats['3PFGM']).quantize(ONE_DP))
    thr_a_str = str(decimal.Decimal(stats['3PFGA']).quantize(ONE_DP))
    thr_str = '{:>4}'.format(thr_m_str) + '-' + '{:<4}'.format(thr_a_str)
    line += thr_str + ' '
      
    if stats['3PFGA'] == 0:
      thr_per_str = ' N/A '
    else:
      thr_per_str = str(decimal.Decimal(stats['3PFGM']/stats['3PFGA'])\
                                                   .quantize(THREE_DP))
    line += thr_per_str + ' '
      
    ftm_str = str(decimal.Decimal(stats['FTM']).quantize(ONE_DP))
    fta_str = str(decimal.Decimal(stats['FTA']).quantize(ONE_DP))
    ft_str = '{:>4}'.format(ftm_str) + '-' + '{:<4}'.format(fta_str)
    line += ft_str + ' '
     
    if stats['FTA'] == 0:
      ft_per_str = ' N/A '
    else:
      ft_per_str = str(decimal.Decimal(stats['FTM']/stats['FTA'])\
                                              .quantize(THREE_DP))
    line += ft_per_str + ' '
      
    if stats['+/-'] >= 0:
      p_m_str = '+' + str(decimal.Decimal(stats['+/-']).quantize(ONE_DP))
    else:
      p_m_str = str(decimal.Decimal(stats['+/-']).quantize(ONE_DP))
    line += '{:>{l}}'.format(p_m_str,l=len(titles[12])) + ' '
      
    o_reb_str = str(decimal.Decimal(stats['Off Reb']).quantize(ONE_DP))
    line += '{:>{l}}'.format(o_reb_str,l=len(titles[13])) + ' '                
                     
    t_reb_str = str(decimal.Decimal(stats['Tot Reb']).quantize(ONE_DP))
    line += '{:>{l}}'.format(t_reb_str,l=len(titles[14])) + ' '
      
    ast_str = str(decimal.Decimal(stats['Assists']).quantize(ONE_DP))
    line += '{:>{l}}'.format(ast_str,l=len(titles[15])) + ' '                
                    
    fls_str = str(decimal.Decimal(stats['Fouls']).quantize(ONE_DP))
    line += '{:>{l}}'.format(fls_str,l=len(titles[16])) + ' '                
                      
    pts_str = str(decimal.Decimal(stats['Points']).quantize(ONE_DP))
    line += '{:>{l}}'.format(pts_str,l=len(titles[17])) + ' '                 
                      
    print (line) 
    rank += 1
  #for p in sorted(not_appeared):  
  #  line = '{:<{l}}'.format(p,l=len(basic_title_str[0])) + ' '
  #  line += 'Yet to appear this season'
  #  print (line)
  
  print ('-'*(line_len))  
  return  