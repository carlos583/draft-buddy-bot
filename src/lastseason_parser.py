import constants
import csv_reader
import json_helper

not_in_newcomer_stats = ['rank', 'puntv', 'leagv', 'puntplus', 'gp', 'mpg', 'fga', 'fta']

def find(player, player_lookup):
    for player_info in player_lookup:
        if player_info['name'] == player['name'] and not player_info['found']:
            player_info['found'] = True
            return player_info
    return None


def generate_newcomers_stats(player_lookup):
    null_stats = { stat : 0.0 for stat in constants.COUNTING_STATS + not_in_newcomer_stats }
    newcomers = [ player for player in player_lookup if not player['found'] ]
    for newcomer in newcomers:
        newcomer.update(null_stats)
        del newcomer['found']

    return newcomers


def generate_player_lookup(player_db):
    player_lookup = player_db['players']
    for player in player_lookup:
        player.update({ 'found' : False })
    return player_lookup


def generate_lastseason_data(rows, player_db):
    last_pergame = []
    last_zscores = []
    player_lookup = generate_player_lookup(player_db)

    for row in rows:
        player_info = find(row, player_lookup)
        if player_info:
            player_info.update(row)
            last_pergame.append(
                { cat : catvalue for cat, catvalue in player_info.items() 
                if not cat.startswith('z') })
            last_zscores.append(
                { cat if not cat.startswith('z') else cat[1:] : catvalue for cat, catvalue in player_info.items() 
                if cat not in constants.COUNTING_STATS })

    newcomers = generate_newcomers_stats(player_lookup)
    last_pergame.extend(newcomers)
    last_zscores.extend(newcomers)
    
    return last_pergame, last_zscores


def parse():
    filename = '../data/raw/lastseason_pergame.csv'
    rows = csv_reader.read(filename)
    player_db = json_helper.load('../data/processed/1_player_db.json')

    last_pergame, last_zscores = generate_lastseason_data(rows, player_db)

    json_helper.dump({ 'count' : len(last_pergame), 'players' : last_pergame}, '../data/processed/4_last_pergame.json')
    json_helper.dump({ 'count' : len(last_zscores), 'players' : last_zscores}, '../data/processed/5_last_zscores.json')


if __name__ == '__main__':
  parse()