'''
Implements all the procedures to scrap necessary data for the
1st and 2nd research question from several online webpages.
'''
from bs4 import BeautifulSoup
import requests
import csv

objective_data = []
players_data = []


def get_players_header():
    '''
    Automaticly generate the proper headers for table we are using in the
    2nd research question without typing manually
    '''
    header = []
    players_pos = ['Top', 'Jun', 'Mid', 'ADC', 'Sup']
    players_side = ['_B', '_R']
    players_stats = ['_Gold', '_Danmage']
    players = []
    for i in players_side:
        players_one_side = [j+i for j in players_pos]
        players.extend(players_one_side)
    header.extend(players)
    for i in players_stats:
        players_one_side_stats = [j+i for j in players]
        header.extend(players_one_side_stats)
    return header


def all_tournaments():
    '''
    Getting the data for both the 1st and 2nd research questions from each
    year's World Championhip and Mid Season Invitation tournaments.
    '''
    tournaments = []
    tournament_type = ['World%20Championship%20201',
                       'Mid-Season%20Invitational%20201']
    for i in range(9, 5, -1):
        tournaments.append(tournament_type[0] + str(i))
        tournaments.append(tournament_type[1] + str(i))
    for tournament in tournaments:
        single_tournament(tournament)


def single_tournament(tournament):
    '''
    Take a tournament as parameter to get the webpage of a single tournament
    and try to go to either a bo1 or bo5 game webpage to get detailed data
    for research questions.
    '''
    url = "https://gol.gg/tournament/tournament-stats/" + tournament + '/'
    choose_objective_data = int(tournament[-1]) >= 8
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all(
        'table', class_='table_list footable toggle-square-filled')[1]
    for new_link_raw in table.find_all('a'):
        new_link = new_link_raw.get('href')
        if 'summary' in new_link:
            bo5(new_link, choose_objective_data)
        else:
            bo1_players_stats(new_link)
            if choose_objective_data:
                bo1_objective(new_link)


def bo5(link, choose_objective_data):
    '''
    Take a link and a boolean choose_objective_data which decides whether
    go to that webpage about 1st research questions's data as parameters and
    try to go to each game's webpage in that bo5 game to get detailed data
    for research questions.
    '''
    url = 'https://gol.gg' + link[2:]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    nav_link = soup.find_all('a', class_='nav-link')
    matches = nav_link[9:len(nav_link) - 1]
    for new_link in matches:
        bo1_players_stats(new_link.get('href'))
        if choose_objective_data:
            bo1_objective(new_link.get('href'))


def bo1_objective(link):
    '''
    Take a link as parameter to get the webpage about single match(bo1)'s
    summary and scrap red side's and blue side's natural objectives they got
    in that match as the data for the 1st research question
    '''
    url = 'https://gol.gg' + link[2:]
    page = requests.get(url)
    row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    soup = BeautifulSoup(page.content, 'html.parser')
    blue = soup.find_all('span', class_='blue_action')
    red = soup.find_all('span', class_='red_action')
    for i in blue:
        s = i.find('img').attrs['alt']
        if s == 'Nashor':
            row[3] += 1
        elif s == 'Rift Herald':
            row[0] += 1
        elif s == 'Elder Drake':
            row[2] += 1
        elif s.find('Drake') > -1:
            row[1] += 1
    for i in red:
        s = i.find('img').attrs['alt']
        if s == 'Nashor':
            row[7] += 1
        elif s == 'Rift Herald':
            row[4] += 1
        elif s == 'Elder Drake':
            row[6] += 1
        elif s.find('Drake') > -1:
            row[5] += 1
    if 'WIN' in soup.find('div', class_="col-12 blue-line-header").text:
        row[8] = 1
    else:
        row[9] = 1
    objective_data.append(row)


def bo1_players_stats(link):
    '''
    Take a link as parameter to get the webpage about single match(bo1)'s
    stats and scrap all player names, golds and total damage to champion from
    that match as data for the 2nd research question
    '''
    url = 'https://gol.gg' + link[2:-5] + 'fullstats/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', class_='completestats tablesaw')
    table_rows = table.find_all('tr')
    row = []
    for tr in table_rows:
        td = tr.find_all('td')
        if td:
            col_name = td[0].text.strip()
            if col_name == 'Player' or col_name == 'Golds' or (
               col_name == 'Total damage to Champion'):
                row_part = [i.text.strip() for i in td[1:]]
                row.extend(row_part)
    players_data.append(row)


def store_data(filename, data, header):
    '''
    Take filename, data and header as parameters and store all the information
    into the csv file with the given filename.
    '''
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)


def main():
    players_header = get_players_header()
    objective_header = ['Herald_B', 'Dragon_B', 'Elder_Dragon_B', 'Baron_B',
                        'Herald_R', 'Dragon_R', 'Elder_Dragon_R', 'Baron_R',
                        'Win_B', 'Win_R']
    all_tournaments()
    store_data('Matches_Objectives.csv', objective_data, objective_header)
    store_data('Players_Gold_And_Damage.csv', players_data, players_header)


if __name__ == '__main__':
    main()
