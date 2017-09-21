import csv_reader
import json_dumper

def parse():
    filename = '../data/raw/lastseason_pergame.csv'
    rows = csv_reader.read(filename)


if __name__ == '__main__':
  parse()