import csv
import json

def csv_to_json(csv_file, json_file):
    data = []

    with open(csv_file, encoding = 'utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)

    with open(json_file, 'w', encoding = 'utf-8') as json_file:
        json.dump(data, json_file, indent = 4)

csv_to_json('../data/sneakers_output_with_collab_and_brand.csv', 'data/sneaker_collab_brand.json')
