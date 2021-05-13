from bs4 import BeautifulSoup
import requests
import csv

region_data = []
players_data = []


def all_tournaments():
    tournaments = []
    tournament_type = ['World%20Championship%20201',
                       'Mid-Season%20Invitational%20201']
    for i in range(9, 5, -1):
        tournaments.append(tournament_type[0] + str(i))
        tournaments.append(tournament_type[1] + str(i))
    for tournament in tournaments:
        players_stats(tournament)
        players_region(tournament)


def players_stats(tournament):
    url = "https://gol.gg/players/list/season-ALL/split-ALL/tournament-" + (
           tournament) + "/position-ALL/week-ALL/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', class_='table_list playerslist ' + (
                      'tablesaw trhover'))
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        if td:
            row = [i.text for i in td]
            players_data.append(row[0:5])


def players_region(tournament):
    url = "https://gol.gg/teams/list/season-ALL/split-ALL/region-ALL/" + (
          "tournament-" + tournament + "/week-ALL/")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', class_='table_list playerslist ' + (
                      'tablesaw trhover'))
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        if td:
            new_link = td[0].find('a').get('href')
            region = td[2].text
            players_name(new_link, region)


def players_name(link, region):
    url = 'https://gol.gg/teams' + '%20'.join(link[1:].split())
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', class_='table_list footable ' + (
                      'toggle-square-filled'))
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        if (len(td) > 2):
            temp = [td[1].text.strip(), region]
            region_data.append(temp)


def store_data(filename, data, header):
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)


def main():
    region_header = ['Player', 'Region']
    players_header = ['Player', 'Position', 'Games', 'Win rate', 'KDA']
    all_tournaments()
    store_data('Players_Region.csv', region_data, region_header)
    store_data('Players_KDA_And_Winrate.csv', players_data, players_header)


if __name__ == '__main__':
    main()
