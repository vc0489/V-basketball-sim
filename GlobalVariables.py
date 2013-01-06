import decimal

NICKS = ('BRE','CRO','HAR','KEN','LAT','QUE','RAY','WIL')

NICK_TO_NAME = {'BRE':'Breton','CRO':'Cromwell','HAR':'Hartford',\
                'KEN':'Kendal','LAT':'Latymer','QUE':'Queens',\
                'RAY':'Rays','WIL':'Wilson'}
                
NAME_TO_NICK = {'Breton':'BRE',\
                 'Cromwell':'CRO',\
                 'Hartford':'HAR',\
                 'Kendal':'KEN',\
                 'Latymer':'LAT',\
                 'Queens':'QUE',\
                 'Rays':'RAY',\
                 'Wilson':'WIL'}
                
ONE_DP = decimal.Decimal(10)**-1             
TWO_DP = decimal.Decimal(10)**-2
THREE_DP = decimal.Decimal(10)**-3

SEASON_QUALIFYING_GAMES_PROP = 0.5
SEASON_QUALIFYING_3PA_TOTAL = 60
SEASON_QUALIFYING_FTA_TOTAL = 60
SEASON_QUALIFYING_2PA_TOTAL = 120
SEASON_QUALIFYING_FGA_TOTAL = 120
SEASON_QUALIFYING_STARTS_PROP = 0.35

FOUL_OUT_THRESHOLD = 4

P_ATT_WRITE_SEQ = ('Draft','Pos','Age','YPro','Team','InPro','2JPro','3PPro',\
                   'InEff','2JEff','3PEff','OReb','DReb','BDom','PassR','PassE',\
                   'InDef','PerDef','InFR','PerFR','FTEff','GInj')
                   
P_ATT_DICT = {'Inside Prop':None,'2Pt Jumper Prop':None,'3Pt Jumper Prop':None,\
              'Inside Eff':None,'2Pt Jumper Eff':None,'3Pt Jumper Eff':None,\
              'Off Reb':None,'Def Reb':None,'Ball Dom':None,'Pass Rate':None,\
              'Pass Eff':None,'Inside Def':None,'Perimeter Def':None,\
              'Inside Foul Rate':None,'Per Foul Rate':None,'FT Eff':None}
              
P_ATT_NAME_DICT = {'InPro':'Inside Prop','2JPro':'2Pt Jumper Prop',\
                   '3PPro':'3Pt Jumper Prop','InEff':'Inside Eff',\
                   '2JEff':'2Pt Jumper Eff','3PEff':'3Pt Jumper Eff',\
                   'OReb':'Off Reb','DReb':'Def Reb','BDom':'Ball Dom',\
                   'PassR':'Pass Rate','PassE':'Pass Eff','InDef':'Inside Def',\
                   'PerDef':'Perimeter Def','InFR':'Inside Foul Rate',\
                   'PerFR':'Per Foul Rate','FTEff':'FT Eff'}
                   
P_ATT_ABBREV_DICT = {'InPro':'IP','2JPro':'2P','3PPro':'3P','InEff':'IE',\
                   '2JEff':'2E','3PEff':'3E','OReb':'OR','DReb':'DR',\
                   'BDom':'BD','PassR':'PR','PassE':'PE','InDef':'ID',\
                   'PerDef':'PD','InFR':'IF','PerFR':'PF','FTEff':'FT',\
                   'Draft':'Draft','Pos':'Pos','Age':'Age','YPro':'YP',\
                   'Team':'Team','GInj':'DI'}

P_PROP_ATTS = ('InPro','2JPro','3PPro','BDom','PassR')

P_ZERO_GAME_STATS = {'Inside FGM':0,'Inside FGA':0,'2PJFGM':0,'2PJFGA':0,\
                     '2PFGM':0,'2PFGA':0,'3PFGM':0,'3PFGA':0,'FTM':0,'FTA':0,\
                     'Off Reb':0,'Def Reb':0,'Tot Reb':0,'Assists':0,'Fouls':0,\
                     '+/-':0,'Fouls Drawn':0,'Inside Pts':0,'2nd Chance Pts':0,\
                     'Points':0,'Court Time':0,'Team Points For':0,\
                     'Team Points Against':0,'Touches':0,'Perimeter Pts':0,\
                     'FGM':0,'FGA':0,'Passes':0,'Inside Fouls Drawn':0,\
                     'Inside Fouls':0,'Per Fouls Drawn':0,'Per Fouls':0,\
                     'Put Backs M':0,'Put Backs A':0,'Possessions':0}

P_ZERO_SEASON_STATS = {'Inside FGM':0,'Inside FGA':0,'2PJFGM':0,'2PJFGA':0,\
                       '2PFGM':0,'2PFGA':0,'3PFGM':0,'3PFGA':0,'FTM':0,'FTA':0,\
                       'Off Reb':0,'Def Reb':0,'Tot Reb':0,'Assists':0,'Fouls':0,\
                       '+/-':0,'Fouls Drawn':0,'Inside Pts':0,'2nd Chance Pts':0,\
                       'Points':0,'Court Time':0,'Team Points For':0,\
                       'Team Points Against':0,'Touches':0,'Perimeter Pts':0,\
                       'FGM':0,'FGA':0,'Passes':0,'Inside Fouls Drawn':0,\
                       'Inside Fouls':0,'Per Fouls Drawn':0,'Per Fouls':0,\
                       'Put Backs M':0,'Put Backs A':0,'Team Games':0,\
                       'Games Played':0,'Games Started':0,'All Team Points F':0,\
                       'All Team Points A':0,'Team Court Time':0,'Possessions':0}

T_ZERO_SEASON_STATS = {'Games':0,\
                       'Own':{'2nd Chance Pts':0,'Inside Pts':0,'Points':0,'Fouls':0,\
                       'Fouls Drawn':0,'Off Reb':0,'Def Reb':0,'Tot Reb':0,\
                       'Inside FGM':0,'Inside FGA':0,'2PJFGM':0,'2PJFGA':0,\
                       '3PFGM':0,'3PFGA':0,'FTM':0,'FTA':0,'Possessions':0,\
                       '2PFGA':0,'2PFGM':0,'Perimeter Pts':0,'Assists':0,\
                       'FGA':0,'FGM':0,'Passes':0,'Touches':0,'Inside Fouls':0,\
                       'Per Fouls':0,'Inside Fouls Drawn':0,'Per Fouls Drawn':0,\
                       'Put Backs M':0,'Put Backs A':0,'Bench Pts':0},\
                       'Opp':{'2nd Chance Pts':0,'Inside Pts':0,'Points':0,'Fouls':0,\
                       'Fouls Drawn':0,'Off Reb':0,'Def Reb':0,'Tot Reb':0,\
                       'Inside FGM':0,'Inside FGA':0,'2PJFGM':0,'2PJFGA':0,\
                       '3PFGM':0,'3PFGA':0,'FTM':0,'FTA':0,'Possessions':0,\
                       '2PFGA':0,'2PFGM':0,'Perimeter Pts':0,'Assists':0,\
                       'FGA':0,'FGM':0,'Passes':0,'Touches':0,'Inside Fouls':0,\
                       'Per Fouls':0,'Inside Fouls Drawn':0,'Per Fouls Drawn':0,\
                       'Put Backs M':0,'Put Backs A':0,'Bench Pts':0}} 

T_ZERO_GAME_STATS = {'2nd Chance Pts':0,'Inside Pts':0,'Points':0,'Fouls':0,\
                     'Fouls Drawn':0,'Off Reb':0,'Def Reb':0,'Tot Reb':0,\
                     'Inside FGM':0,'Inside FGA':0,'2PJFGM':0,'2PJFGA':0,'3PFGM':0,\
                     '3PFGA':0,'FTM':0,'FTA':0,'Possessions':0,'2PFGA':0,'2PFGM':0,\
                     'Perimeter Pts':0,'Assists':0,'FGA':0,'FGM':0,'Passes':0,\
                     'Touches':0,'Inside Fouls':0,'Per Fouls':0,'Inside Fouls Drawn':0,\
                     'Per Fouls Drawn':0,'Put Backs M':0,'Put Backs A':0,'Bench Pts':0}

T_ZERO_MISC_GAME_STATS = {'Largest Lead Score':(0,0),'Most Unanswered Pts Score':(0,0),\
                          'Largest Lead':0,'Most Unanswered Pts':0,'Ties':0,\
                          'Lead Changes':0}

STAT_NAME_TO_ABBREV = {'+/-':'+/-',\
                       '2nd Chance Pts':'2CP',\
                       '2PFGA':'2PA',\
                       '2PFGM':'2PM',\
                       '2PJFGA':'2JA',\
                       '2PJFGM':'2JM',\
                       '3PFGA':'3PA',\
                       '3PFGM':'3PM',\
                       'All Team Points A':'ATPA',\
                       'All Team Points F':'ATPF',\
                       'Assists':'Ast',\
                       'Bench Pts':'BPts',\
                       'Court Time':'CTime',\
                       'Def Reb':'DF',\
                       'FGA':'FGA',\
                       'FGM':'FGM',\
                       'Fouls':'FC',\
                       'Fouls Drawn':'FD',\
                       'FTA':'FTA',\
                       'FTM':'FTM',\
                       'Games Played':'GP',\
                       'Games Started':'GS',\
                       'Inside FGA':'InA',\
                       'Inside FGM':'InM',\
                       'Inside Fouls':'IFC',\
                       'Inside Fouls Drawn':'IFD',\
                       'Inside Pts':'InP',\
                       'Largest Lead':'MaxL',\
                       'Lead Changes':'LChgs',\
                       'Most Unanswered Pts':'MUPt',\
                       'Off Reb':'OR',\
                       'Passes':'Pass',\
                       'Perimeter Pts':'PerP',\
                       'Per Fouls':'PFC',\
                       'Per Fouls Drawn':'PFD',\
                       'Points':'Pts',\
                       'Possessions':'Poss',\
                       'Put Backs A':'PBA',\
                       'Put Backs M':'PBM',\
                       'Team Court Time':'TCTime',\
                       'Team Games':'TG',\
                       'Team Points Against':'TPA',\
                       'Team Points For':'TPF',\
                       'Ties':'Ties',\
                       'Touches':'Tchs',\
                       'Tot Reb':'TR'\
                      }
                      
T_STATS_WRITE_SEQ = ('FGM',\
                     'FGA',\
                     '2PFGM',\
                     '2PFGA',\
                     '3PFGM',\
                     '3PFGA',\
                     'FTM',\
                     'FTA',\
                     'Put Backs M',\
                     'Put Backs A',\
                     'Inside FGM',\
                     'Inside FGA',\
                     '2PJFGM',\
                     '2PJFGA',\
                     'Off Reb',\
                     'Def Reb',\
                     'Tot Reb',\
                     'Assists',\
                     'Fouls',\
                     'Points',\
                     'Inside Pts',\
                     '2nd Chance Pts',\
                     'Possessions',\
                     'Touches',\
                     'Passes',\
                     'Inside Fouls',\
                     'Per Fouls',\
                     'Bench Pts'\
                     )
                     
T_MISC_STATS_WRITE_SEQ = ('Largest Lead',\
                          'Most Unanswered Pts')
                          
                      
P_STATS_WRITE_SEQ = ('Court Time',\
                     'FGM',\
                     'FGA',\
                     '2PFGM',\
                     '2PFGA',\
                     '3PFGM',\
                     '3PFGA',\
                     'FTM',\
                     'FTA',\
                     'Put Backs M',\
                     'Put Backs A',\
                     'Inside FGM',\
                     'Inside FGA',\
                     '2PJFGM',\
                     '2PJFGA',\
                     'Off Reb',\
                     'Def Reb',\
                     'Tot Reb',\
                     'Assists',\
                     'Fouls',\
                     'Fouls Drawn',\
                     'Points',\
                     'Inside Pts',\
                     '2nd Chance Pts',\
                     '+/-',\
                     'Team Points For',\
                     'Team Points Against',\
                     'Touches',\
                     'Passes',\
                     'Inside Fouls',\
                     'Per Fouls',\
                     'Inside Fouls Drawn',\
                     'Per Fouls Drawn')                       
                       

STAT_ABBREV_TO_NAME = {}

STARTING_YEAR = 11     

YEAR_RECORD_ELEMENTS = {'Wins':0,\
                        'Losses':0,\
                        'H Wins':0,\
                        'H Losses':0,\
                        'A Wins':0,\
                        'A Losses':0,\
                        'L10':[],\
                        'H L10':[],\
                        'A L10':[],\
                        'Streak':0,\
                        'H Streak':0,\
                        'A Streak':0,\
                        'Pts F':0,\
                        'Pts A':0,\
                        'H Pts F':0,\
                        'H Pts A':0,\
                        'A Pts F':0,\
                        'A Pts A':0\
                       } 

A_T_RECORD_ELEMENTS = {'Wins':0,\
                      'Losses':0,\
                      'H Wins':0,\
                      'H Losses':0,\
                      'A Wins':0,\
                      'A Losses':0,\
                      'L10':[],\
                      'H L10':[],\
                      'A L10':[],\
                      'Streak':0,\
                      'H Streak':0,\
                      'A Streak':0,\
                     }

COUNT_STRINGS = {1:'st',2:'nd',3:'rd',4:'th',5:'th',6:'th',7:'th',8:'th',9:'th',0:'th'}

Y11_NEW_INFO_DICT = {'Alpha Teams':['QUE','HAR','RAY','CRO'],\
                     'Beta Teams':['KEN','BRE','WIL','LAT'],\
                     'Round Seq':('CRO','WIL','LAT','HAR','QUE','KEN','BRE','RAY')}
                     
HOME_SHOT_ADV = 3
HOME_FT_ADV = 2

YEAR_LETTERS = {1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'J',\
                11:'K',12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',\
                19:'S',20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'}
POS_TO_NAME_DICT = {'C1':'a','C2':'b','PF1':'c','PF2':'d','SF1':'e','SF2':'f',\
                    'SG1':'g','SG2':'h','PG1':'i','PG2':'j'}                
NAME_TO_POS_DICT = {'a':'C1','b':'C2','c':'PF1','d':'PF2','e':'SF1','f':'SF2',\
                    'g':'SG1','h':'SG2','i':'PG1','j':'PG2'}                
POS_TO_NUMBER_DICT = {'C1':1,'C2':2,'PF1':3,'PF2':4,'SF1':5,'SF2':6,'SG1':7,\
                      'SG2':8,'PG1':9,'PG2':10}
SIMPLE_POS_DICT = {'C1':'C','C2':'C','PF1':'PF','PF2':'PF','SF1':'SF',\
                   'SF2':'SF','SG1':'SG','SG2':'SG','PG1':'PG','PG2':'PG'}
TOT_DRAFTEES = 60
POS_PROB_DICT = {'C1':0.18,'C2':0.02,'PF1':0.16,'PF2':0.04,'SF1':0.15,\
                 'SF2':0.05,'SG1':0.12,'SG2':0.08,'PG1':0.12,'PG2':0.08}
                 
AGE_PROB_DICT = {18:0.1,19:0.2,20:0.4,21:0.2,22:0.1}

POS_DICTS_IN_DICT = {'C1':{},'C2':{},'PF1':{},'PF2':{},'SF1':{},'SF2':{},\
                     'SG1':{},'SG2':{},'PG1':{},'PG2':{}}
SIMP_POS_DICTS_IN_DICT = {'C':{},'PF':{},'SF':{},'SG':{},'PG':{}}
SIMP_POS_LISTS_IN_DICT = {'C':[],'PF':[],'SF':[],'SG':[],'PG':[]}

ATTS_RANGE_DICT = {'C1':{'InPro':(60,20),\
                         '2JPro':(10,20),\
                         '3PPro':(0,3),\
                         'InEff':(70,100,60,110,0.95),\
                         '2JEff':(40,80,20,95,0.95),\
                         '3PEff':(0,50,0,75,0.95),\
                         'OReb':(20,40,5,80,0.95),\
                         'DReb':(60,100,40,110,0.95),\
                         'BDom':(5,25,5,50,0.95),\
                         'PassR':(10,40,5,75,0.95),\
                         'PassE':(10,50,0,100,0.95),\
                         'InDef':(50,100,30,110,0.95),\
                         'PerDef':(10,30,5,75,0.95),\
                         'InFR':(40,80,20,100,0.95),\
                         'PerFR':(5,20,0,50,0.95),\
                         'FTEff':(50,75,25,95,0.95)\
                        },\
                   'C2':{'InPro':(30,40),\
                         '2JPro':(15,35),\
                         '3PPro':(10,30),\
                         'InEff':(60,90,45,100,0.95),\
                         '2JEff':(50,90,30,100,0.95),\
                         '3PEff':(60,95,40,105,0.95),\
                         'OReb':(10,30,5,50,0.95),\
                         'DReb':(45,90,25,105,0.95),\
                         'BDom':(5,25,5,50,0.95),\
                         'PassR':(10,40,5,75,0.95),\
                         'PassE':(10,50,0,100,0.95),\
                         'InDef':(30,90,20,100,0.95),\
                         'PerDef':(20,40,10,90,0.95),\
                         'InFR':(20,60,10,80,0.95),\
                         'PerFR':(10,30,5,75,0.95),\
                         'FTEff':(60,85,40,95,0.95)\
                        },\
                   'PF1':{'InPro':(50,30),\
                         '2JPro':(15,25),\
                         '3PPro':(0,3),\
                         'InEff':(65,95,55,105,0.95),\
                         '2JEff':(45,90,30,95,0.95),\
                         '3PEff':(0,50,0,75,0.95),\
                         'OReb':(15,35,5,70,0.95),\
                         'DReb':(50,95,35,105,0.95),\
                         'BDom':(5,25,5,50,0.95),\
                         'PassR':(10,40,5,75,0.95),\
                         'PassE':(10,50,0,80,0.95),\
                         'InDef':(40,90,20,100,0.95),\
                         'PerDef':(10,40,5,90,0.95),\
                         'InFR':(35,70,15,90,0.95),\
                         'PerFR':(10,30,0,60,0.95),\
                         'FTEff':(55,80,30,95,0.95)\
                        },\
                   'PF2':{'InPro':(20,45),\
                         '2JPro':(20,35),\
                         '3PPro':(15,30),\
                         'InEff':(55,90,40,100,0.95),\
                         '2JEff':(55,95,35,100,0.95),\
                         '3PEff':(60,90,40,100,0.95),\
                         'OReb':(10,25,5,45,0.95),\
                         'DReb':(40,80,20,100,0.95),\
                         'BDom':(5,25,5,50,0.95),\
                         'PassR':(10,40,5,75,0.95),\
                         'PassE':(10,50,0,80,0.95),\
                         'InDef':(20,80,10,90,0.95),\
                         'PerDef':(30,50,20,100,0.95),\
                         'InFR':(15,50,10,70,0.95),\
                         'PerFR':(15,40,5,85,0.95),\
                         'FTEff':(65,90,45,95,0.95)\
                        },\
                   'SF1':{'InPro':(30,35),\
                         '2JPro':(10,40),\
                         '3PPro':(15,20),\
                         'InEff':(60,95,45,105,0.95),\
                         '2JEff':(50,90,35,100,0.95),\
                         '3PEff':(50,90,35,100,0.95),\
                         'OReb':(15,25,5,60,0.95),\
                         'DReb':(45,85,30,100,0.95),\
                         'BDom':(10,35,5,65,0.95),\
                         'PassR':(20,50,5,80,0.95),\
                         'PassE':(20,60,10,80,0.95),\
                         'InDef':(30,75,15,95,0.95),\
                         'PerDef':(20,60,10,100,0.95),\
                         'InFR':(30,60,10,80,0.95),\
                         'PerFR':(20,40,5,80,0.95),\
                         'FTEff':(65,85,40,95,0.95)\
                        },\
                   'SF2':{'InPro':(15,30),\
                         '2JPro':(20,35),\
                         '3PPro':(25,30),\
                         'InEff':(45,85,35,95,0.95),\
                         '2JEff':(55,95,40,105,0.95),\
                         '3PEff':(60,95,45,105,0.95),\
                         'OReb':(10,20,5,45,0.95),\
                         'DReb':(35,70,20,90,0.95),\
                         'BDom':(10,35,5,65,0.95),\
                         'PassR':(20,50,5,80,0.95),\
                         'PassE':(20,60,10,80,0.95),\
                         'InDef':(10,60,5,85,0.95),\
                         'PerDef':(35,80,20,110,0.95),\
                         'InFR':(20,40,5,60,0.95),\
                         'PerFR':(30,60,10,90,0.95),\
                         'FTEff':(70,85,45,95,0.95)\
                        },\
                   'SG1':{'InPro':(20,30),\
                         '2JPro':(20,40),\
                         '3PPro':(15,25),\
                         'InEff':(60,90,45,100,0.95),\
                         '2JEff':(55,95,40,105,0.95),\
                         '3PEff':(50,95,40,105,0.95),\
                         'OReb':(10,20,5,45,0.95),\
                         'DReb':(30,65,20,85,0.95),\
                         'BDom':(20,50,10,75,0.95),\
                         'PassR':(30,60,10,85,0.95),\
                         'PassE':(30,70,10,90,0.95),\
                         'InDef':(10,55,0,80,0.95),\
                         'PerDef':(45,95,30,105,0.95),\
                         'InFR':(25,50,10,70,0.95),\
                         'PerFR':(25,50,10,80,0.95),\
                         'FTEff':(70,90,50,95,0.95)\
                        },\
                   'SG2':{'InPro':(10,30),\
                         '2JPro':(20,40),\
                         '3PPro':(25,30),\
                         'InEff':(45,85,30,95,0.95),\
                         '2JEff':(60,100,50,110,0.95),\
                         '3PEff':(60,100,50,110,0.95),\
                         'OReb':(5,15,0,40,0.95),\
                         'DReb':(25,50,15,70,0.95),\
                         'BDom':(20,50,10,75,0.95),\
                         'PassR':(30,60,10,85,0.95),\
                         'PassE':(30,70,10,90,0.95),\
                         'InDef':(5,35,0,60,0.95),\
                         'PerDef':(55,100,40,110,0.95),\
                         'InFR':(20,40,5,55,0.95),\
                         'PerFR':(30,60,15,90,0.95),\
                         'FTEff':(75,90,50,95,0.95)\
                        },\
                   'PG1':{'InPro':(20,25),\
                         '2JPro':(25,35),\
                         '3PPro':(20,20),\
                         'InEff':(55,90,40,100,0.95),\
                         '2JEff':(55,95,40,105,0.95),\
                         '3PEff':(50,95,40,105,0.95),\
                         'OReb':(5,15,0,35,0.95),\
                         'DReb':(20,45,10,65,0.95),\
                         'BDom':(60,100,40,110,0.95),\
                         'PassR':(55,85,40,95,0.95),\
                         'PassE':(40,90,30,100,0.95),\
                         'InDef':(10,40,5,65,0.95),\
                         'PerDef':(50,100,40,110,0.95),\
                         'InFR':(20,40,5,60,0.95),\
                         'PerFR':(25,50,10,80,0.95),\
                         'FTEff':(70,90,50,95,0.95)\
                        },\
                   'PG2':{'InPro':(10,25),\
                         '2JPro':(25,40),\
                         '3PPro':(25,30),\
                         'InEff':(40,85,30,95,0.95),\
                         '2JEff':(60,100,50,110,0.95),\
                         '3PEff':(65,100,50,110,0.95),\
                         'OReb':(5,10,0,30,0.95),\
                         'DReb':(15,35,5,55,0.95),\
                         'BDom':(60,100,40,110,0.95),\
                         'PassR':(55,85,40,95,0.95),\
                         'PassE':(40,90,30,100,0.95),\
                         'InDef':(5,25,0,50,0.95),\
                         'PerDef':(60,100,50,110,0.95),\
                         'InFR':(15,30,5,45,0.95),\
                         'PerFR':(25,50,15,90,0.95),\
                         'FTEff':(75,90,50,95,0.95)\
                        }\
                   }

ATTS_GRADE_SCALE = {'InPro':{5:'XL',10:'VL',20:'L',30:'ML',40:'M',50:'MH',\
                             60:'H',70:'VH',100:'XH'},\
                    '2JPro':{5:'XL',10:'VL',20:'L',30:'ML',40:'M',50:'MH',\
                             60:'H',70:'VH',100:'XH'},\
                    '3PPro':{5:'XL',10:'VL',20:'L',30:'ML',40:'M',50:'MH',\
                             60:'H',70:'VH',100:'XH'},\
                    'InEff':{50:'F',60:'E',70:'D',80:'C',90:'B',100:'A-',\
                             110:'A',1000:'A+'},\
                    '2JEff':{50:'F',60:'E',70:'D',80:'C',90:'B',100:'A-',\
                             110:'A',1000:'A+'},\
                    '3PEff':{50:'F',60:'E',70:'D',80:'C',90:'B',100:'A-',\
                             110:'A',1000:'A+'},\
                    'OReb':{5:'F',10:'E',20:'D',30:'C',40:'B',50:'A-',\
                            60:'A',1000:'A+'},\
                    'DReb':{20:'F',30:'E',45:'D',60:'C',75:'B',90:'A-',\
                            105:'A',1000:'A+'},\
                    'BDom':{5:'XL',10:'VL',20:'L',30:'ML',40:'M',60:'MH',\
                            80:'H',100:'VH',1000:'XH'},\
                    'PassR':{10:'XL',25:'VL',40:'L',50:'ML',60:'M',70:'MH',\
                             80:'H',90:'VH',100:'XH'},\
                    'PassE':{20:'F',30:'E',40:'D',50:'C',65:'B',80:'A-',\
                             95:'A',1000:'A+'},\
                    'InDef':{15:'F',30:'E',45:'D',60:'C',75:'B',90:'A-',\
                             105:'A',1000:'A+'},\
                    'PerDef':{15:'F',30:'E',45:'D',60:'C',75:'B',90:'A-',\
                              105:'A',1000:'A+'},\
                    'InFR':{10:'F',20:'E',35:'D',50:'C',65:'B',75:'A-',\
                            85:'A',1000:'A+'},\
                    'PerFR':{10:'F',20:'E',30:'D',40:'C',50:'B',60:'A-',\
                             70:'A',1000:'A+'},\
                    'FTEff':{50:'F',60:'E',70:'D',75:'C',80:'B',85:'A-',\
                             90:'A',100:'A+'}\
                   }

MIN_ROSTER_SIZE = 12
MAX_ROSTER_SIZE = 13    

MAX_PROB_CHANGE = {'C1':{'InPro':3,'2JPro':1.5,'3PPro':0.5,'BDom':2,'PassR':2},\
                   'C2':{'InPro':2,'2JPro':2,'3PPro':1.5,'BDom':2,'PassR':2},\
                   'PF1':{'InPro':3,'2JPro':1.5,'3PPro':0.5,'BDom':2,'PassR':2},\
                   'PF2':{'InPro':2,'2JPro':2,'3PPro':1.5,'BDom':2,'PassR':2},\
                   'SF1':{'InPro':2.5,'2JPro':2.5,'3PPro':1.5,'BDom':2.5,'PassR':2.5},\
                   'SF2':{'InPro':2,'2JPro':3,'3PPro':2.5,'BDom':2.5,'PassR':2.5},\
                   'SG1':{'InPro':2,'2JPro':3,'3PPro':2,'BDom':3,'PassR':3},\
                   'SG2':{'InPro':1.5,'2JPro':3,'3PPro':3,'BDom':3,'PassR':3},\
                   'PG1':{'InPro':2,'2JPro':3,'3PPro':2,'BDom':4,'PassR':4},\
                   'PG2':{'InPro':1.5,'2JPro':3,'3PPro':3,'BDom':4,'PassR':4}\
                  }
                  
MAX_REGRESS = {18:{'InEff':3,'2JEff':3,'3PEff':3,'OReb':2,'DReb':3,'PassE':3,\
                   'InDef':3,'PerDef':3,'InFR':3,'PerFR':2,'FTEff':3},\
               19:{'InEff':3,'2JEff':3,'3PEff':3,'OReb':2,'DReb':3,'PassE':3,\
                   'InDef':3,'PerDef':3,'InFR':3,'PerFR':2,'FTEff':3},\
               20:{'InEff':3,'2JEff':3,'3PEff':3,'OReb':2,'DReb':3,'PassE':3,\
                   'InDef':3,'PerDef':3,'InFR':3,'PerFR':2,'FTEff':3},\
               21:{'InEff':3,'2JEff':3,'3PEff':3,'OReb':2,'DReb':3,'PassE':3,\
                   'InDef':3,'PerDef':3,'InFR':3,'PerFR':2,'FTEff':3},\
               22:{'InEff':3,'2JEff':3,'3PEff':3,'OReb':2,'DReb':3,'PassE':3,\
                   'InDef':3,'PerDef':3,'InFR':3,'PerFR':2,'FTEff':3},\
               23:{'InEff':3,'2JEff':3,'3PEff':3,'OReb':2,'DReb':3,'PassE':3,\
                   'InDef':3,'PerDef':3,'InFR':3,'PerFR':2,'FTEff':3},\
               24:{'InEff':3,'2JEff':3,'3PEff':3,'OReb':2,'DReb':3,'PassE':3,\
                   'InDef':3,'PerDef':3,'InFR':3,'PerFR':2,'FTEff':3},\
               25:{'InEff':3,'2JEff':3,'3PEff':3,'OReb':2,'DReb':3,'PassE':3,\
                   'InDef':3,'PerDef':3,'InFR':3,'PerFR':2,'FTEff':3},\
               26:{'InEff':3,'2JEff':3,'3PEff':3,'OReb':2,'DReb':3,'PassE':3,\
                   'InDef':3,'PerDef':3,'InFR':3,'PerFR':2,'FTEff':3},\
               27:{'InEff':4,'2JEff':4,'3PEff':4,'OReb':2.5,'DReb':4,'PassE':3,\
                   'InDef':4,'PerDef':4,'InFR':4,'PerFR':2.5,'FTEff':3},\
               28:{'InEff':4,'2JEff':4,'3PEff':4,'OReb':2.5,'DReb':4,'PassE':3,\
                   'InDef':4,'PerDef':4,'InFR':4,'PerFR':2.5,'FTEff':3},\
               29:{'InEff':4,'2JEff':4,'3PEff':4,'OReb':2.5,'DReb':4,'PassE':3,\
                   'InDef':4,'PerDef':4,'InFR':4,'PerFR':2.5,'FTEff':3},\
               30:{'InEff':5,'2JEff':5,'3PEff':5,'OReb':3,'DReb':5,'PassE':3,\
                   'InDef':5,'PerDef':5,'InFR':5,'PerFR':3,'FTEff':3}\
             }
               
MAX_RATING = {'C1':{'InEff':120,'2JEff':90,'3PEff':80,'OReb':60,'DReb':120,\
                    'PassE':80,'InDef':120,'PerDef':40,'InFR':100,'PerFR':20,\
                    'FTEff':75},\
              'C2':{'InEff':100,'2JEff':100,'3PEff':100,'OReb':50,'DReb':100,\
                    'PassE':80,'InDef':110,'PerDef':60,'InFR':80,'PerFR':40,\
                    'FTEff':80},\
              'PF1':{'InEff':115,'2JEff':100,'3PEff':80,'OReb':50,'DReb':110,\
                     'PassE':80,'InDef':100,'PerDef':60,'InFR':90,'PerFR':30,\
                     'FTEff':80},\
              'PF2':{'InEff':95,'2JEff':110,'3PEff':100,'OReb':40,'DReb':90,\
                     'PassE':80,'InDef':90,'PerDef':80,'InFR':70,'PerFR':50,\
                     'FTEff':85},\
              'SF1':{'InEff':110,'2JEff':110,'3PEff':100,'OReb':40,'DReb':90,\
                     'PassE':90,'InDef':90,'PerDef':80,'InFR':80,'PerFR':60,\
                     'FTEff':85},\
              'SF2':{'InEff':90,'2JEff':120,'3PEff':110,'OReb':30,'DReb':75,\
                     'PassE':90,'InDef':70,'PerDef':100,'InFR':60,'PerFR':80,\
                     'FTEff':88},\
              'SG1':{'InEff':105,'2JEff':120,'3PEff':105,'OReb':30,'DReb':75,\
                     'PassE':100,'InDef':70,'PerDef':100,'InFR':70,'PerFR':60,\
                     'FTEff':90},\
              'SG2':{'InEff':85,'2JEff':120,'3PEff':115,'OReb':25,'DReb':60,\
                     'PassE':100,'InDef':50,'PerDef':120,'InFR':60,'PerFR':80,\
                     'FTEff':93},\
              'PG1':{'InEff':100,'2JEff':120,'3PEff':110,'OReb':20,'DReb':65,\
                     'PassE':120,'InDef':50,'PerDef':100,'InFR':60,'PerFR':60,\
                     'FTEff':90},\
              'PG2':{'InEff':80,'2JEff':120,'3PEff':120,'OReb':15,'DReb':50,\
                     'PassE':120,'InDef':30,'PerDef':120,'InFR':50,'PerFR':70,\
                     'FTEff':93}\
             }
             
POST_GAME_CHANGE_PROBS = {18:{'Max Improve Prob':0.08,'Min Improve Prob':0.05,\
                             'Regress Prob':0.03,'Injury Regress Prob':0.05},\
                          19:{'Max Improve Prob':0.07,'Min Improve Prob':0.045,\
                             'Regress Prob':0.03,'Injury Regress Prob':0.05},\
                          20:{'Max Improve Prob':0.06,'Min Improve Prob':0.045,\
                             'Regress Prob':0.03,'Injury Regress Prob':0.05},\
                          21:{'Max Improve Prob':0.055,'Min Improve Prob':0.04,\
                             'Regress Prob':0.03,'Injury Regress Prob':0.05},\
                          22:{'Max Improve Prob':0.05,'Min Improve Prob':0.04,\
                             'Regress Prob':0.03,'Injury Regress Prob':0.05},\
                          23:{'Max Improve Prob':0.045,'Min Improve Prob':0.035,\
                             'Regress Prob':0.03,'Injury Regress Prob':0.05},\
                          24:{'Max Improve Prob':0.04,'Min Improve Prob':0.035,\
                             'Regress Prob':0.03,'Injury Regress Prob':0.05},\
                          25:{'Max Improve Prob':0.035,'Min Improve Prob':0.03,\
                             'Regress Prob':0.03,'Injury Regress Prob':0.055},\
                          26:{'Max Improve Prob':0.03,'Min Improve Prob':0.03,\
                             'Regress Prob':0.03,'Injury Regress Prob':0.06},\
                          27:{'Max Improve Prob':0.03,'Min Improve Prob':0.03,\
                             'Regress Prob':0.03,'Injury Regress Prob':0.07},\
                          28:{'Max Improve Prob':0.03,'Min Improve Prob':0.03,\
                             'Regress Prob':0.03,'Injury Regress Prob':0.08},\
                          29:{'Max Improve Prob':0.03,'Min Improve Prob':0.03,\
                             'Regress Prob':0.03,'Injury Regress Prob':0.09},\
                          30:{'Max Improve Prob':0.03,'Min Improve Prob':0.03,\
                             'Regress Prob':0.03,'Injury Regress Prob':0.1}\
                         }

