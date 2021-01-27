README

```virtualenv venv```

```. venv/bin/activate```

```pip install --editable .```

```nba```


```
(venv) Chases-MacBook-Pro chasemarshall1$ nba
Usage: nba [OPTIONS] COMMAND [ARGS]...

  A command line application

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  fbplayers
  fbteams
```

## fbplayers Output Example
```
Players: 478
                          Name         Roster status   IS  GP    pts  fg3m    reb   ast   stl   blk    fga    fgm   ftm    fta    min    TO  ft_per  fg_per  Total_zscore
Total Rank                                                                                                                                                               
1                 Nikola Jokic  ja dunno big up urrr       16  25.75  1.12  12.06  9.62  1.88  0.50  17.50   9.81  5.00   6.00  35.70  4.06   0.833   0.561        13.556
2           Karl-Anthony Towns    Like and Subscribe  INJ   4  22.00  1.50  12.50  4.25  0.50  2.75  15.75   7.25  6.00   6.25  32.93  2.50   0.960   0.460        13.514
3                 Kevin Durant       The White Mamba  INJ  13  31.23  2.92   7.23  5.77  0.77  1.38  19.46  10.46  7.38   8.54  36.27  3.69   0.864   0.538        13.127
4                 Kyrie Irving    Winnings Overrated       10  29.30  3.60   4.60  5.80  1.20  0.70  21.00  11.00  3.70   3.90  34.64  2.30   0.949   0.524        12.833
5                  Joel Embiid               Tropics       14  27.71  1.21  11.50  2.71  1.36  1.36  15.86   8.79  8.93  10.71  31.58  3.14   0.834   0.554        12.530
6                Kawhi Leonard            Chef Curry       15  25.93  2.07   5.40  5.73  2.00  0.67  18.87   9.53  4.80   5.33  34.50  1.80   0.901   0.505        12.358
7               Damian Lillard  Chuck it for buckets       14  28.14  3.71   4.71  6.71  1.00  0.29  19.29   8.50  7.43   7.86  36.18  3.07   0.945   0.441        11.126
8                 Bradley Beal               Tropics       11  31.73  2.18   5.00  4.73  1.27  0.64  22.36  11.00  7.55   8.64  33.14  3.00   0.874   0.492        10.249
9                  CJ McCollum       Load Management       13  26.69  4.85   3.92  5.00  1.31  0.31  20.00   9.46  2.92   3.46  33.84  1.00   0.844   0.473        10.139
10                Myles Turner       The White Mamba       14  14.00  1.57   6.79  1.07  1.50  4.21  10.21   5.14  2.14   2.79  32.73  1.64   0.767   0.503        10.089
11                 Bam Adebayo              Yao Ming       13  20.31  0.08   8.92  5.46  0.85  0.92  11.85   7.31  5.62   6.54  32.16  3.31   0.859   0.617         9.776
12                Clint Capela    Winnings Overrated       13  14.15  0.00  14.54  1.08  0.77  2.31  10.54   6.00  2.15   3.92  29.48  1.23   0.548   0.569         9.710
13               Stephen Curry            Chef Curry       16  27.94  4.19   5.56  6.19  1.12  0.12  20.12   9.12  5.50   5.94  33.89  3.38   0.926   0.453         9.627
14               Anthony Davis    Winnings Overrated       15  22.13  1.00   8.80  3.53  1.33  1.87  16.13   8.67  3.80   5.20  32.42  1.67   0.731   0.538         9.107
15                 Rudy Gobert    Like and Subscribe       16  12.12  0.00  13.62  1.44  0.44  2.69   8.00   4.88  2.38   4.94  29.92  1.56   0.482   0.610         8.951
```

## fbteams Output Example
```
                          FGM/A    FG%    FTM/A    FT%  3PM   PTS   REB  AST  STL  BLK   TO  FG% Rank  FT% Rank  3PM Rank  PTS Rank  REB Rank  AST Rank  STL Rank  BLK Rank  TO Rank  Top 6 Rank  Total Rank
name                                                                                                                                                                                                        
Load Management       1286/2651  0.485  633/822  0.770  343  3548  1273  793  165  158  455      8.98      5.98      8.80     10.00      7.10      8.64      4.00      7.88     1.00       51.40       62.38
The White Mamba       1228/2587  0.475  571/744  0.767  341  3368  1313  822  191  129  411      7.28      5.76      8.70      8.60      7.67      9.33      5.81      5.42     3.69       47.39       62.26
Chef Curry            1205/2499  0.482  606/743  0.816  334  3350  1063  611  183  120  367      8.47      9.34      8.36      8.46      4.09      4.31      5.26      4.65     6.39       46.28       59.33
Chuck it for buckets  1246/2751  0.453  573/726  0.789  368  3433  1188  850  190  113  434      3.55      7.37     10.00      9.11      5.88     10.00      5.74      4.06     2.29       48.10       58.00
Winnings Overrated    1202/2488  0.483  464/628  0.739  299  3167  1170  645  180  161  365      8.64      3.71      6.68      7.04      5.62      5.12      5.05      8.13     6.51       42.62       56.50
Like and Subscribe     961/2045  0.470  492/701  0.702  211  2625  1476  661  251  183  397      6.43      1.00      2.44      2.82     10.00      5.50     10.00     10.00     4.55       46.48       52.74
Jameson's Team         895/1961  0.456  404/492  0.821  355  2549   925  652  169  119  308      4.06      9.71      9.37      2.23      2.12      5.29      4.28      4.57    10.00       43.22       51.63
Yao Ming              1064/2165  0.491  466/585  0.797  298  2892   976  629  167   77  379     10.00      7.95      6.63      4.90      2.85      4.74      4.14      1.00     5.65       39.87       47.86
ja dunno big up urrr   903/1847  0.489  404/498  0.811  181  2391   860  631  122   95  313      9.66      8.98      1.00      1.00      1.19      4.79      1.00      2.53     9.69       36.84       39.84
Dame Time              936/2136  0.438  462/560  0.825  279  2613   847  472  140  104  315      1.00     10.00      5.72      2.73      1.00      1.00      2.26      3.29     9.57       33.57       36.57
```

## playerindex Output Example
```
(venv) Chases-MacBook-Pro:fantasybball chasemarshall1$ nba playerindex
Use -n to specify a partial first name
Eg: '-n Le' would return 'Lebron James'
(venv) Chases-MacBook-Pro:fantasybball chasemarshall1$ nba playerindex -n Le
Reading: player_stats_index.json
Reading: owner_index.json
Players: 479
           Name    Roster status   IS Eligible positions  GP    pts  fg3m   reb   ast   stl   blk    fga   fgm  ftm   fta    min    TO
0  LeBron James  Load Management  GTD       [PG, SG, SF]  18  25.17  2.72  7.89  7.39  0.94  0.44  18.56  9.22  4.0  5.61  32.67  3.67
```

## games Output Example
```
(venv) Chases-MacBook-Pro:fantasybball chasemarshall1$ nba games
Use -n to specify a partial first name
Eg: '-n Le' would return 'Lebron James'
(venv) Chases-MacBook-Pro:fantasybball chasemarshall1$ nba games -n Lillard
Reading: player_stats_index.json
Reading: owner_index.json
                      name  fg_pct  ft_pct  fg3m  pts  reb  ast  stl  blk  to
date                                                                         
2021-01-25  Damian Lillard    36.4    87.5     3   26    6   10    0    0   3
2021-01-24  Damian Lillard    64.7   100.0     6   39    5    8    1    0   3
2021-01-18  Damian Lillard    43.5   100.0     3   35    3    6    1    1   5
2021-01-16  Damian Lillard    43.5   100.0     4   36    7    7    1    0   3
2021-01-14  Damian Lillard    43.8   100.0     2   22    6    4    1    0   5
2021-01-13  Damian Lillard    47.8   100.0     6   40    1   13    3    0   0
2021-01-11  Damian Lillard    50.0   100.0     3   23    7    5    0    1   8
2021-01-09  Damian Lillard    31.2   100.0     1   17    4    6    1    0   0
2021-01-07  Damian Lillard    61.9    85.7     7   39    7    7    3    0   1
2021-01-05  Damian Lillard    35.3    81.8     3   24    5    9    0    0   0
2021-01-03  Damian Lillard    41.7    85.7     6   32    4    4    0    0   5
2021-01-01  Damian Lillard    52.4   100.0     6   34    4    8    1    0   1
2020-12-30  Damian Lillard    21.4    93.3     0   20    5    4    1    0   4
2020-12-28  Damian Lillard    62.5   100.0     5   31    4    5    0    1   5
2020-12-26  Damian Lillard    39.3   100.0     5   32    5    9    1    0   5
2020-12-23  Damian Lillard    33.3     0.0     1    9    4    7    1    1   1
```

# Some useful docs

- [Click startup guide](https://readthedocs.org/projects/pocoo-click/downloads/pdf/latest/)
- [More Click docs](https://click.palletsprojects.com/en/7.x/)
- Ball dont lie Api Example: `https://www.balldontlie.io/api/v1/stats?seasons[]=2020&player_ids[]=115`
- [Ball dont lie homepage](https://www.balldontlie.io/#stats)
- [Yahoo API docs](https://yahoo-fantasy-api.readthedocs.io/en/latest/yahoo_fantasy_api.html#the-game-class)
- [Fantasy Basketball Rankings](https://hashtagbasketball.com/fantasy-basketball-rankings?fbclid=IwAR1rv-ahMnvfuuQb7Y366svoOu3Cco4kB-VJCd8fMTma6-Mey9CgrPtJfX8)