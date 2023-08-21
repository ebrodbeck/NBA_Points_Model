# NBA_Points_Model (In progress)
Using a dataset of common team statistics from the 2019 season, try to predict the results of each Sacramento Kings game as the season progresses.

## Stream of conciousness workflow
- queried data from killersports.com using SDQL - this this took place in 2021, and was picked up again in 2023
- Objective is to create a model to predict kings wins for the 2019 season based on key features that correlate with total points scored in a game
- Simulations will be run to predict the total points of the kings and their opponent.
- Feature engineering was done using data from the 2018 season, found that essentially field goals made, three pointers made, and free throws made were the most important (makes sense)
- Different regression models will be fit to these parameters and points
- Simulations are run with random gaussian samplings of the key features based on the mean and standard deviation of those features over the last X games
- loop the code to run the simulations for every game in the season from game X-72, where X is the number of games needed for the mean and std sample. (working plan to do this by August 31 2023)

### Features
| Parameter | Description |
|:------------|:--------------:|
| GAME |  game number, integer 1-72  |
| TEAM |  team name  |
| POINTS |  points scored in the game  |
| AST |  assists  |
| ATR |  assist to turnover ratio  |
| BAP |  Baskets Assisted percentage  |
| DRB |  defensive rebounds  |
| FBP |  fast break points  |
| FGP |  field goal percentage  |
| FTM |  free throws made  |
| LSP |  leading scorer points  |
| ORB |  offensive rebounds  |
| PIP |  points in the paint  |
| TO |  turnovers  |
| TPP |  three point percentage  |
| FGM |  field goals made  |
| FTP |  free throw percentage  |
| TPM |  three pointers made  |
| TBLOCKS |  team blocks  |
| *NOTE |  *all features have corresponding oFEATURE denoting "opponent" feature |

### Correlation Heatmap for Available Features
![](https://github.com/ebrodbeck/NBA_Points_Model/blob/main/Correlation%20Heatmap.png)
### Ranked Correlations of Features with "Points Scored"
![](https://github.com/ebrodbeck/NBA_Points_Model/blob/main/Correlation%20with%20Points%20-%20All%20NBA%20Data.png)
### Top Features Correlated with "Points Scored"
![](https://github.com/ebrodbeck/NBA_Points_Model/blob/main/Significant%20Features%20to%20Points%20Scored.png)
### Feature Importance of SVM Model - Trained on 10 games leading to 2019 Kings vs Heat, Game 51
![](https://github.com/ebrodbeck/NBA_Points_Model/blob/main/Feature%20importance%20-%20arbitraty%20team%202%20vs%20Kings.png)
### Distribution of Total Points Scored from 1000 Simulations
![](https://github.com/ebrodbeck/NBA_Points_Model/blob/main/Arbitrary%20Game%20-%20Total%20Points%20Distribution.png)
### Distributions of Points Scored by Each Team - 1000 Simulations
![](https://github.com/ebrodbeck/NBA_Points_Model/blob/main/Arbitrary%20Game%20-%20Team%20Points%20Distribution.png)
