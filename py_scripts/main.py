from api_function import *
from champions import *
from db import *

# initalize SQL
db = create_connection('sql db/legends_never_die.db')
create_tables(db)

# Getting info for me - the summoner
summoner_info = get_current_summoner()
summoner_name = summoner_info['gameName']
puuid = summoner_info['puuid']

# Getting my match history
match_history = get_match_history_summoner(puuid)
game_id_list = []

for i in range(20):
    game_id = match_history['games']['games'][i]['gameId']
    game_id_list.append(game_id)

for game_id in game_id_list:
    game_history = get_game_history(game_id)

    participants = game_history['participantIdentities']
    participant_list = []
    for participant in participants:
        participantId = participant['participantId']
        gameName = participant['player']['gameName']
        participant_dict = {participantId: gameName}
        participant_list.append(participant_dict)

    games = game_history['participants']
    for game in games:
        participantId_game = game['participantId']
        participant_game = participant_list[participantId_game - 1][participantId_game]
        champion_id = game['championId']
        try:
            champion_name = next((sub for sub in champ_list if sub['id'] == str(champion_id)), None)['champ']
        except TypeError:
            champion_name = "unknown"
        win = game['stats']['win']

        # Take all of the data and insert into database
        insert_data_game(db, game_id, participant_game, champion_name, win)

select_game_data(db)

close_connection(db)
