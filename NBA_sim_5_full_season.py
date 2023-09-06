import pandas as pd
import random as rnd
from sklearn.preprocessing import StandardScaler
from sklearn import svm
import time
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

numsims=1000 #number of matchup simulations
lags=15      #number of games preceding the matchup to use as training data
gam=3      #gamma for the SVR linear model

tt=time.time()

factors={'AST':'assists', 'ATR':'assist to turnover ratio', 'AWP':'Away Winning Percentage','BAP':'Baskets Assisted percentage','DRB':'Defensive Rebounds','FBP':'fast break points','FGP':'field goal percentage','FTM':'free throws made','HWP':'Home Winning Percentage','LSP':'Leading Scorers Points','ORB':'Offensive Rebounds','PIP':'points in the paint','TO':'turnovers','TPP':'three point percentage','WP':'team winning percentage','FGM':'field goals made','FTP':'free throw percent','TPM':'three pointers made'}
#import data from SDQL site, add power rankings using dictionary
df=pd.read_excel('nba_sdql.xlsx',sheet_name='data2019')
dfkings=df[df['team'] == 'Kings']
real_outcome=dfkings[['game','W','L','H','A']]

#_____Fill out this before each simulation  ______________________    
metrics = pd.DataFrame(columns=['game','opp_name','kings_pts', 'opp_pts', 'total_pts','kings_win_pct'])
for index, row in df[df['team'] == 'Kings'].iterrows():
    print(f"game {row['game']}: Kings vs {row['oteam']}")
    team1='Kings'
    team2 =  row['oteam']
    df1=df[df.team==team1]
    df2=df[df.team==team2]
    gamenum = row['game']     #exclude games from after game gamenum
    lag=lags                  #exclude games from before game gamenum-lag
    #____________________________________________________
    df11=df1[(df1['game'] < gamenum) & (df1['game'] > gamenum - lag)]
    df22=df2[(df2['game'] < gamenum) & (df2['game'] > gamenum - lag)]
    #Create X and y dataframes 
    y_t1_pts=df1[['points']]
    y_t2_pts=df2[['points']]
    X1=df1.drop(['game','points','opoints','H','A','oH','oA','oteam','team','W','L','oW','oL','FTP','fouls','wins','oFTM','owins','FGP', 'TPP', 'LSP', 'ATR', 'FBP', 'oFGM', 'ofouls', 'oLSP', 'oTPM', 'DRB', 'oPIP', 'oAST', 'oFGP', 'oATR', 'oFTP', 'oTPP', 'tblocks', 'oFBP', 'ORB', 'oORB', 'BAP', 'oTO', 'oBAP', 'TO', 'oblocks'],axis=1)
    X2=df2.drop(['game','points','opoints','H','A','oH','oA','oteam','team','W','L','oW','oL','FTP','fouls','wins','oFTM','owins','FGP', 'TPP', 'LSP', 'ATR', 'FBP', 'oFGM', 'ofouls', 'oLSP', 'oTPM', 'DRB', 'oPIP', 'oAST', 'oFGP', 'oATR', 'oFTP', 'oTPP', 'tblocks', 'oFBP', 'ORB', 'oORB', 'BAP', 'oTO', 'oBAP', 'TO', 'oblocks'],axis=1)
    #Scale the input data
    scaler=StandardScaler().fit(X1)
    NormX1=scaler.transform(X1)
    scaler=StandardScaler().fit(X2)
    NormX2=scaler.transform(X2)
    #Normalize, Regression, 
    df1=pd.DataFrame(NormX1, columns=X1.columns)        #re adding column labels to normalized data
    df2=pd.DataFrame(NormX2, columns=X2.columns)
    mean1=X1.mean()       #distribution info for input data
    std1=X1.std()         #these functions spit out a vertical series
    mean2=X2.mean()
    std2=X2.std()
    mn1=mean1.to_frame()    #convert the series to dataframes
    st1=std1.to_frame()
    mn2=mean2.to_frame()
    st2=std2.to_frame()
    m1=mn1.T                #convert the vertical to horizontal to match the input matrices
    s1=st1.T
    m2=mn2.T
    s2=st2.T
    #Fit model (SVR)
#    reg1=svm.SVR(kernel='linear',gamma=gam)
#    reg1.fit(df1,y_t1_pts.values.ravel())
#    reg2=svm.SVR(kernel='linear',gamma=gam)
#    reg2.fit(df2,y_t2_pts.values.ravel())
    #fit model (ELastic Net)
    alpha = 0.5  # L1 regularization parameter
    l1_ratio = 0.5  # L1 ratio parameter (0.5 means equal L1 and L2 regularization)
    reg1 = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
    reg2 = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
    reg1.fit(df1,y_t1_pts.values.ravel())
    reg2.fit(df2,y_t2_pts.values.ravel())
    #functions for calculating point totals for a matchup
    def gamesim(): # this gives the winner of a single simulation
        data1=[[rnd.gauss(m1.AST.item(),s1.AST.item()),rnd.gauss(m1.FTM.item(),s1.FTM.item()),rnd.gauss(m1.PIP.item(),s1.PIP.item()),rnd.gauss(m1.FGM.item(),s1.FGM.item()),rnd.gauss(m1.TPM.item(),s1.TPM.item()),rnd.gauss(m1.oDRB.item(),s1.oDRB.item())]]
        data2=[[rnd.gauss(m2.AST.item(),s2.AST.item()),rnd.gauss(m2.FTM.item(),s2.FTM.item()),rnd.gauss(m2.PIP.item(),s2.PIP.item()),rnd.gauss(m2.FGM.item(),s2.FGM.item()),rnd.gauss(m2.TPM.item(),s2.TPM.item()),rnd.gauss(m2.oDRB.item(),s2.oDRB.item())]]
        Ndata1=scaler.transform(data1)
        Ndata2=scaler.transform(data2)
        Data1=pd.DataFrame(Ndata1,columns=df1.columns)  
        Data2=pd.DataFrame(Ndata2,columns=df2.columns)                   
        t1score=reg1.predict(Data1)
        t2score=reg2.predict(Data2)
        if ((t1score))>((t2score)):
            return 1
        elif ((t1score))<((t2score)):
            return -1
        else: return 0 
    def gamesimou(): # this gives the total points of the simulations - use for over/under
        data1=[[rnd.gauss(m1.AST.item(),s1.AST.item()),rnd.gauss(m1.FTM.item(),s1.FTM.item()),rnd.gauss(m1.PIP.item(),s1.PIP.item()),rnd.gauss(m1.FGM.item(),s1.FGM.item()),rnd.gauss(m1.TPM.item(),s1.TPM.item()),rnd.gauss(m1.oDRB.item(),s1.oDRB.item())]]
        data2=[[rnd.gauss(m2.AST.item(),s2.AST.item()),rnd.gauss(m2.FTM.item(),s2.FTM.item()),rnd.gauss(m2.PIP.item(),s2.PIP.item()),rnd.gauss(m2.FGM.item(),s2.FGM.item()),rnd.gauss(m2.TPM.item(),s2.TPM.item()),rnd.gauss(m2.oDRB.item(),s2.oDRB.item())]]
        Ndata1=scaler.transform(data1)
        Ndata2=scaler.transform(data2)
        Data1=pd.DataFrame(Ndata1,columns=df1.columns)  
        Data2=pd.DataFrame(Ndata2,columns=df2.columns)                   
        t1score=reg1.predict(Data1)
        t2score=reg2.predict(Data2)
        OU=t1score+t2score
        return OU
    def gamesimt1(): #gives score for team 1 for visualization
        data1=[[rnd.gauss(m1.AST.item(),s1.AST.item()),rnd.gauss(m1.FTM.item(),s1.FTM.item()),rnd.gauss(m1.PIP.item(),s1.PIP.item()),rnd.gauss(m1.FGM.item(),s1.FGM.item()),rnd.gauss(m1.TPM.item(),s1.TPM.item()),rnd.gauss(m1.oDRB.item(),s1.oDRB.item())]]
        Ndata1=scaler.transform(data1)
        Data1=pd.DataFrame(Ndata1,columns=df1.columns)  
        t1score=reg1.predict(Data1)
        return t1score 
    def gamesimt2(): #gives score for team 2 for visualization
        data2=[[rnd.gauss(m2.AST.item(),s2.AST.item()),rnd.gauss(m2.FTM.item(),s2.FTM.item()),rnd.gauss(m2.PIP.item(),s2.PIP.item()),rnd.gauss(m2.FGM.item(),s2.FGM.item()),rnd.gauss(m2.TPM.item(),s2.TPM.item()),rnd.gauss(m2.oDRB.item(),s2.oDRB.item())]]
        Ndata2=scaler.transform(data2)
        Data2=pd.DataFrame(Ndata2,columns=df2.columns)                   
        t2score=reg2.predict(Data2)
        return t2score
    def gamesSim(ns): #runs the simulation (ns) times
        gamesout=[]
        O_U=[]
        score1=[]
        score2=[]
        t1win=0
        t2win=0
        tie=0
        for i in range(ns):
            gm=gamesim()
            ov=gamesimou()
            sc1=gamesimt1()
            sc2=gamesimt2()
            gamesout.append(gm)
            O_U.append(ov)
            score1.append(sc1)
            score2.append(sc2)
            if gm==1:
                t1win +=1
            elif gm==-1:
                t2win +=1
            else: tie +=1
        t1_win_pct=(100*t1win/(t1win+t2win+tie))
        oudf=pd.DataFrame(O_U,columns=['OUs'])
        t1df=pd.DataFrame(score1,columns=['t1'])
        t2df=pd.DataFrame(score2,columns=['t2'])
        ouav=oudf.mean()
        t1av=t1df.mean()
        t2av=t2df.mean()
        ouav_val=ouav[0]
        t1av_val=t1av[0]
        t2av_val=t2av[0]        
        series_data=pd.Series([row['game'], team2, t1av_val, t2av_val, ouav_val, t1_win_pct],index=metrics.columns)
        return series_data

    result=gamesSim(numsims)  # Run simulations
    metrics = metrics.append(result, ignore_index=True)

elapsed=time.time()-tt

#model metrics after predicting all games
actual_v_pred=metrics.merge(real_outcome[['game','W','L','H','A']],on='game')
actual_v_pred['pred_W'] = actual_v_pred['kings_win_pct'] >= 50
actual_v_pred_confident = actual_v_pred[(actual_v_pred['kings_win_pct'] <= 30) | (actual_v_pred['kings_win_pct'] >= 70)]

confusion_matrix_kings = confusion_matrix(actual_v_pred['W'], actual_v_pred['pred_W'])
M_accuracy = accuracy_score(actual_v_pred['W'], actual_v_pred['pred_W'])
M_precision = precision_score(actual_v_pred['W'], actual_v_pred['pred_W'])
M_recall = recall_score(actual_v_pred['W'], actual_v_pred['pred_W'])
M_f1 = f1_score(actual_v_pred['W'], actual_v_pred['pred_W'])

metrics_series = pd.Series({'M_accuracy': M_accuracy,
                            'M_precision': M_precision,
                            'M_recall': M_recall,
                            'M_f1': M_f1})

M_accuracy_c = accuracy_score(actual_v_pred_confident['W'], actual_v_pred_confident['pred_W'])
M_precision_c = precision_score(actual_v_pred_confident['W'], actual_v_pred_confident['pred_W'])
M_recall_c = recall_score(actual_v_pred_confident['W'], actual_v_pred_confident['pred_W'])
M_f1_c = f1_score(actual_v_pred_confident['W'], actual_v_pred_confident['pred_W'])


metrics_series_c = pd.Series({'M_accuracy': M_accuracy_c,
                            'M_precision': M_precision_c,
                            'M_recall': M_recall_c,
                            'M_f1': M_f1_c})

print('normal model', metrics_series)
print('confident games model', metrics_series_c)