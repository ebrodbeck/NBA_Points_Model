# NBA_Points_Model
Using a dataset of common team statistics from the 2019 season, try to predict the results of each Sacramento Kings game as the season progresses.

## Stream of conciousness workflow
- queried data from killersports.com using SDQL - this this took place in 2021, and was picked up again in 2023
- Objective is to create a model to predict kings wins for the 2019 season based on key features that correlate with total points scored in a game
- Simulations will be run to predict the total points of the kings and their opponent.
- Feature engineering was done using data from the 2018 season, found that essentially field goals made, three pointers made, and free throws made were the most important (makes sense)
- Different regression models will be fit to these parameters and points
- Simulations are run with random gaussian samplings of the key features based on the mean and standard deviation of those features over the last X games
- loop the code to run the simulations for every game in the season from game X-72, where X is the number of games needed for the mean and std sample.
