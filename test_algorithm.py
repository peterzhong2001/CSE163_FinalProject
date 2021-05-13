import pandas as pd


def objective_score(filepath):
    """
    This fucntion gives solutions to the first research question.
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

    return[dragon_score, elder_score, herald_score, baron_score]


def get_score(df_b, df_r, obj):
    """
    This is a helper function for objective_score.
    This fucntion takes two dataframe and name of the objective as parameters
    and calculate the total obkective score of that objective over all the
    games in the database.
    """
    score_b = df_b[obj + '_B'].sum() - df_b[obj + '_R'].sum()
    score_r = df_r[obj + '_R'].sum() - df_r[obj + '_B'].sum()
    score = score_b + score_r
    return score


def consistent_player(filepath):
    """
    This fucntion gives solutions to the second research question.
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

    # Removing players with less than 30 games and with high variacne
    df3 = players.copy()
    df3['Number_of_Games'] = 1
    df3 = df3.groupby('Player')[['Gold', 'Damage', 'Number_of_Games']].sum()
    df3['Variance'] = df_var['Variance']

    # Calculating overall most consistent player
    df4 = df3.copy()
    df4['Dmg_Per_Gold'] = df4['Damage'] / df4['Gold']
    df4 = df4.sort_values(by=['Dmg_Per_Gold'], ascending=False)

    result = df4.head(3).index.tolist()
    return result


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


def all_star(kda_file, region_file):
    """
    This fucntion gives solutions to the third research question.
    It takes two filepath (one containing player information, one containing
    region information) as parameters and calculates the best player in each
    position according to PT-score and plots the PT-score of players. It also
    plots the cumulative scores for the All-Star teams from each region.
    """
    # Loading and joining files
    df = pd.read_csv(kda_file, na_values='-').set_index('Player')
    df2 = pd.read_csv(region_file).set_index('Player').dropna()
    df = df.join(df2)
    df['KDA'] = df['KDA'].astype(float)
    df['Win rate'] = df['Win rate'].map(lambda x: x.rstrip('%')).astype(float)
    df['Win rate'] = df['Win rate'] / 100

    # Constructing dataframes of all-star teams
    A = get_regional_data(df, 'A')
    B = get_regional_data(df, 'B')
    C = get_regional_data(df, 'C')
    D = get_regional_data(df, 'D')
    E = get_regional_data(df, 'E')
    F = get_regional_data(df, 'F')

    # rank all the regions
    regions = A.append([B, C, D, E, F])
    result = rank_region(regions)
    return result


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
    result = total['Region'].tolist()
    return result
