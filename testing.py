"""
Peter Zhong & Tony Song
CSE 163 Final Project
This file implements all the testing functions for
algorithm.py.
"""

import pandas as pd
from test_algorithm import objective_score
from test_algorithm import consistent_player
from test_algorithm import all_star


def process_file(filename):
    """
    Takes a filename as parameter and returns a csv file containing
    the first 10 rows of that file.
    """
    df = pd.read_csv(filename).head(10)
    df.to_csv('Test_' + filename)


def test_objective_score():
    """
    prints 'Objective Score Passed' if the objective_score method
    result matches the correct result. prints 'Error in Objective Score'
    otherwise.
    """
    result = objective_score('Test_Matches_Objectives.csv')
    if result == [0.3, 0.3, 0.0, 0.6]:
        print('Objective Score Passed')
    else:
        print('Error in Objective Score')
        print(result)


def test_consistent_player():
    """
    prints 'Consistent Player Passed' if the consistent_player method
    result matches the correct result. prints 'Error in Consistent
    Player' otherwise.
    """
    result = consistent_player('Test_Players_Gold_And_Damage.csv')
    if result == ['GimGoon', 'Perkz', 'Doinb']:
        print('Consistent Player Passed')
    else:
        print('Error in Consistent Player')
        print(result)


def test_all_star():
    """
    prints 'All Star Passed' if the all_star method result
    matches the correct result. prints 'Error in All Star'
    otherwise.
    """
    result = all_star('Test_Players_KDA_And_Winrate.csv',
                      'Test_Players_Region.csv')
    if result == ['A', 'B', 'C', 'D', 'E', 'F']:
        print('All Star Passed')
    else:
        print('Error in All Star')
        print(result)


def main():
    process_file('Matches_Objectives.csv')
    process_file('Players_Gold_And_Damage.csv')

    test_objective_score()
    test_consistent_player()
    test_all_star()


if __name__ == '__main__':
    main()
