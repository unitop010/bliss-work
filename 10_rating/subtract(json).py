import json
from json_diff import diff

with open('item_url - all.json', 'r') as f1:
    data1 = json.load(f1)

with open('item_url.json', 'r') as f2:
    data2 = json.load(f2)

differences = diff(data1, data2)
print(differences)