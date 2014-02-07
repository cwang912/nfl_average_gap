nfl_average_gap
===============

Looking at point differential in NFL games. Takes in free NFL play by play data, i.e. 2012_nfl_pbp_data_reg.csv, and outputs the actual point differential and a metric that determines that sums for each game the average point differential over the course of the game. This reduces the spread, as the game begins tied, so it rewards scoring early and maintaining a lead, and does not penalize for choking in end-of-game situations. This is perhaps why the metric, for 2012, has a poorer linear fit that the total point differential, not weighted by time.
