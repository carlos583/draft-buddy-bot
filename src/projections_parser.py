import csv_reader
import json_dumper
from functools import reduce
from math import sqrt


player_db_fields = ['name', 'team', 'pos']
# other_stats = ['rank', 'gp', 'mpg', 'fgma', 'ftma']
counting_stats = ['pts', 'reb', 'ast', 'stl', 'blk', 'm3s', 'fg', 'ft', 'to']


def generate_player_info(row, player_id):
    player_info = { key : val for key, val in row.items() if key in player_db_fields }
    player_info['id'] = player_id
    return player_info

def generate_player_stat(row, player_id):
    player_stat = { key : val for key, val in row.items() if key != 'total' }
    player_stat['id'] = player_id
    return player_stat

def get_sums_of_counting_stats(players_stats):
    return reduce(lambda x, y: 
        { key : float(val) + float(y[key]) for key, val in x.items() if key in counting_stats}, players_stats)

def calculate_zscores(pergame_stats):
    num_players = len(pergame_stats)

    # Get the mean for every category
    sums = get_sums_of_counting_stats(pergame_stats)
    means = { cat: catsum / num_players for cat, catsum in sums.items() }

    # Get squared deviations before getting variances
    squared_diffs = [ { cat : (float(val) - means[cat]) ** 2 if cat in counting_stats else val 
        for cat, val in player.items() } for player in pergame_stats ]
    sums_of_squares = get_sums_of_counting_stats(squared_diffs)
    variances = { cat: catsum / (num_players - 1) for cat, catsum in sums_of_squares.items() }

    # Get standard deviations
    std_devs = { cat : sqrt(variance) for cat, variance in variances.items() }
    
    # Return zscores
    return [ { cat : (float(val) - means[cat]) / std_devs[cat] if cat in counting_stats else val 
        for cat, val in player.items() } for player in pergame_stats ]


def parse():
    filename = '../data/raw/projections_pergame.csv'
    rows = csv_reader.read(filename)
    
    player_db = []
    proj_pergame = []
    player_id = 100
    
    for row in rows:
        player_db.append(generate_player_info(row, player_id))
        proj_pergame.append(generate_player_stat(row, player_id))
        player_id = player_id + 1

    proj_zscores = calculate_zscores(proj_pergame)

    json_dumper.dump(player_db, '../data/processed/1_player_db.json')
    json_dumper.dump(proj_pergame, '../data/processed/2_proj_pergame.json')
    json_dumper.dump(proj_zscores, '../data/processed/3_proj_zscores.json')


if __name__ == '__main__':
  parse()