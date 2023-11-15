import json

f = open('other data/champions.json', encoding="utf8")

data = json.load(f)

champ_list = []

for champ in data['data']:
    id = data['data'][champ]['key']
    champ_dict = {'id': id, 'champ': champ}
    champ_list.append(champ_dict)
