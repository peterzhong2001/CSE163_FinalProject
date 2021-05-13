"""
Peter Zhong & Tony Song
CSE 163 Final Project
This file implements all the functions used to conduct calculations,
process data and plot graphs that are related to our initial research
questions.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def objective_score(filepath):
    """
    This function gives solutions to the first research question.
    It takes a filepath as parameter and calculates and plots the
    objective scores of each of the four neutral objectives in
    League of Legends.
    """
    # Load in file
    df = pd.read_csv(filepath)
    num_matches = len(df.index)
    df_b = df[df['Win_B'] == 1]
    df_r = df[df['Win_R'] == 1]

    # Calculate objective scores
    dragon_score = get_score(df_b, df_r, 'Dragon') / num_matches
    elder_score = get_score(df_b, df_r, 'Elder_Dragon') / num_matches
    herald_score = get_score(df_b, df_r, 'Herald') / num_matches
    baron_score = get_score(df_b, df_r, 'Baron') / num_matches

    # Plotting the objective scores
    objs = ('Dragon', 'Elder Dragon', 'Herald', 'Baron')
    scores = [dragon_score, elder_score, herald_score, baron_score]
    position = np.arange(len(scores))
    figure, ax = plt.subplots()
    ax.bar(position, scores)
    ax.set_xticks(position)
    ax.set_xticklabels(objs)
    ax.set_ylabel('Objective Score')
    ax.set_title('Objective Score of All Four Neutral Objectives in LOL')
    plt.savefig('objective_score.jpg')


def get_score(df_b, df_r, obj):
    """
    This is a helper function for objective_score.
    This function takes two dataframe and name of the objective as parameters
    and calculate the total obkective score of that objective over all the
    games in the database.
    """
    score_b = df_b[obj + '_B'].sum() - df_b[obj + '_R'].sum()
    score_r = df_r[obj + '_R'].sum() - df_r[obj + '_B'].sum()
    score = score_b + score_r
    return score


def consistent_player(filepath):
    """
    This function gives solutions to the second research question.
    It takes a filepath as parameter and calculates and plots the
    damage per gold ratio for the top 10 most consistent players.
    It also plots the performance over time plot for the three most
    consistent players.
    """
    # Reading in the data
    df = pd.read_csv(filepath)
    top_laners = group_by_position(df, 'Top')
    junglers = group_by_position(df, 'Jun')
    mid_laners = group_by_position(df, 'Mid')
    adcs = group_by_position(df, 'ADC')
    supports = group_by_position(df, 'Sup')
    players = top_laners.append([junglers, mid_laners, adcs, supports])

    # Calculating variance for each player
    df2 = players.copy()
    df2['Dmg_Per_Gold'] = df2['Damage'] / df2['Gold']
    variance = df2.groupby('Player')['Dmg_Per_Gold'].var()
    df_var = pd.DataFrame({'Player': variance.index,
                          'Variance': variance.values})
    df_var = df_var.set_index('Player')

    # Plotting out all the variances to determine a good threshold
    position = np.arange(len(df_var.index))
    figure, ax = plt.subplots()
    ax.bar(position, df_var['Variance'])
    ax.set_ylabel('Damage Per Gold Variance')
    ax.set_title('Damage Per Gold Variance Plot for All Players')
    plt.savefig('All_player_variances.jpg')

    # Removing players with less than 30 games and with high variacne
    df3 = players.copy()
    df3['Number_of_Games'] = 1
    df3 = df3.groupby('Player')[['Gold', 'Damage', 'Number_of_Games']].sum()
    df3['Variance'] = df_var['Variance']
    filter1 = (df3['Number_of_Games'] >= 30) & (df3['Variance'] <= 0.2)
    filter2 = df3['Number_of_Games'] >= 60

    # Calculating overall most consistent player
    df4 = df3.copy()
    df4 = df4[filter1]
    df4['Dmg_Per_Gold'] = df4['Damage'] / df4['Gold']
    df4 = df4.sort_values(by=['Dmg_Per_Gold'], ascending=False).head(10)

    # Calculating most consistent veteran player (60+ games)
    df5 = df3.copy()
    df5 = df5[filter2]
    df5['Dmg_Per_Gold'] = df5['Damage'] / df5['Gold']
    df5 = df5.sort_values(by=['Dmg_Per_Gold'], ascending=False).head(10)

    # Plotting everything
    plot_player_data(df4, 'Overall', 'Dmg_Per_Gold', 'blue')
    plot_player_data(df4, 'Overall', 'Number_of_Games', 'green')
    plot_player_data(df4, 'Overall', 'Variance', 'red')
    plot_player_data(df5, 'Veteran', 'Dmg_Per_Gold', 'blue')
    plot_player_data(df5, 'Veteran', 'Number_of_Games', 'green')
    plot_player_data(df5, 'Veteran', 'Variance', 'red')
    plot_player_performance(df2, 'Bang')
    plot_player_performance(df2, 'PraY')
    plot_player_performance(df2, 'Uzi')


def group_by_position(df, position):
    """
    This is a helper function for consistent_player.
    This function takes a dataframe and a LOL position as parameters
    and group all the players within that position. It returns a new
    dataframe with columns named Player, Gold and Damage.
    """
    df1 = df[[position + '_B', position + '_B_Gold', position + '_B_Damage']]
    df1 = df1.rename(columns={position + '_B': 'Player',
                     position + '_B_Gold': 'Gold',
                     position + '_B_Damage': 'Damage'})
    df2 = df[[position + '_R', position + '_R_Gold', position + '_R_Damage']]
    df2 = df2.rename(columns={position + '_R': 'Player',
                     position + '_R_Gold': 'Gold',
                     position + '_R_Damage': 'Damage'})
    df = df1.append(df2).dropna()
    return df


def plot_player_data(df, type, datatype, color):
    """
    This is a helper function for consistent_player.
    This fucntion takes a dataframe, an analysis type, a data name
    and a color as parameter, and plot the corresponding data on a
    bar chart with the passed color. It saves the graph and names it
    according to the type of the analysis and name of data plotted.
    """
    position = np.arange(len(df.index))
    fig, ax = plt.subplots()
    ax.bar(position, df[datatype], align='center', color=color)
    ax.set_xticks(position)
    ax.set_xticklabels(df.index)
    plt.xticks(rotation=45)
    if datatype == 'Dmg_Per_Gold':
        datatype = 'Damage Per Gold'
    elif datatype == 'Number_of_Games':
        datatype = 'Number of Games'
    ax.set_ylabel(datatype)
    ax.set_title(type + ' Top 10 Most Consistent Players - ' + datatype)
    plt.savefig(type + '_' + datatype + '.jpg')


def plot_player_performance(df, player):
    """
    This is a helper function for consistent_player.
    This function takes a dataframe and the name of a player as parameters
    and plots the change of that player's damage per gold over all the
    games that that player have played.
    """
    games = df.copy()
    games = games[games['Player'] == player]
    position = np.arange(len(games.index))
    fig, ax = plt.subplots()
    ax.plot(position, games['Dmg_Per_Gold'])
    ax.set_ylabel('Damage Per Gold')
    ax.set_xlabel('Number of Games')
    ax.set_title(player + "'s Performance Over Time")
    plt.savefig(player + '_Performance.jpg')


def all_star(kda_file, region_file):
    """
    This function gives solutions to the third research question.
    It takes two filepath (one containing player information, one containing
    region information) as parameters and calculates the best player in each
    position according to PT-score and plots the PT-score of players. It also
    plots the cumulative scores for the All-Star teams from each region.
    """
    # Loading and joining files
    df = pd.read_csv(kda_file, na_values='-').set_index('Player')
    df2 = pd.read_csv(region_file, keep_default_na=False).set_index('Player')
    df = df.join(df2).dropna()
    df['KDA'] = df['KDA'].astype(float)
    df['Win rate'] = df['Win rate'].map(lambda x: x.rstrip('%')).astype(float)
    df['Win rate'] = df['Win rate'] / 100

    # Constructing dataframes of all-star teams
    cn = get_regional_data(df, 'CN')
    tw = get_regional_data(df, 'TW')
    na = get_regional_data(df, 'NA')
    euw = get_regional_data(df, 'EUW')
    kr = get_regional_data(df, 'KR')
    vn = get_regional_data(df, 'VN')

    # Plotting all the regions
    plot_region(cn, 'China', 'red')
    plot_region(tw, 'Taiwan', 'purple')
    plot_region(na, 'North America', 'blue')
    plot_region(euw, 'Europe West', 'green')
    plot_region(kr, 'Korea', 'black')
    plot_region(vn, 'Vietnam', 'yellow')

    # rank all the regions
    regions = cn.append([tw, na, euw, kr, vn])
    rank_region(regions)


def get_regional_data(df, region):
    """
    This is a helper function for all_star.
    It takes a dataframe and the string representing a region as parameters
    and returns a new dataframe containing the 5 best player from each region
    determined by calculating the PT-rating of each player.
    """
    df2 = df.copy()
    df2 = df2[df2['Region'] == region]
    df2['Games'] = df2.groupby('Player')['Games'].sum()
    df2 = df2[df2['Games'] >= 15]
    df2['KDA'] = df2.groupby('Player')['KDA'].mean()
    df2['Win rate'] = df2.groupby('Player')['Win rate'].mean()
    df2 = df2.drop_duplicates()
    df2['PT-score'] = df2['KDA'] + df2['Win rate']
    best_team = df2.groupby('Position')['PT-score'].idxmax()
    mask = df2.index.isin(best_team.values)
    df2 = df2[mask]
    return df2


def plot_region(df, region, color):
    """
    This is a helper function for all_star.
    It takes a dataframe, the string representing a region and a color as
    parameters and plots the performance of the 5 players on that regional
    All-Star team.
    """
    position = np.arange(5)
    fig, ax = plt.subplots()
    ax.bar(position, df['PT-score'], align='center', color=color)
    ax.set_xticks(position)
    ax.set_xticklabels(df.index)
    ax.set_ylabel('PT-score')
    ax.set_title(region + ' Regional All Star Player Ratings')
    ax.set_ylim((0, 10))
    plt.savefig(region + '_all_star.jpg')


def rank_region(regions):
    """
    This is a helper function for all_star.
    It takes a list of dataframes representing different regions. It
    sorts them according to their cumulative PT-score and plots the
    cumulative PT-score of each team.
    """
    rank = regions.groupby('Region')['PT-score'].sum()
    total = pd.DataFrame({'Region': rank.index,
                         'Cumulative Rating': rank.values})
    total = total.sort_values(by='Cumulative Rating', ascending=False)
    position = np.arange(len(total.index))
    fig, ax = plt.subplots()
    ax.bar(position, total['Cumulative Rating'], align='center')
    ax.set_xticks(position)
    ax.set_xticklabels(total['Region'])
    ax.set_ylabel('Cumulative Rating')
    ax.set_title('All-Star Team Cumulative Ratings')
    plt.savefig('best_all_star.jpg')


def main():
    objective_score('Matches_Objectives.csv')
    consistent_player('Players_Gold_And_Damage.csv')
    all_star('Players_KDA_And_Winrate.csv', 'Players_Region.csv')


if __name__ == '__main__':
    main()
