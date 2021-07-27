import fenrir.data.db_connection as db
from datetime import datetime


def save_game(state_obj):
    conn = db.connect_to_db()
    curs = conn.cursor()

    date = datetime.now()
    formatted_date = date.strftime("%b %d, %Y %I:%M %p")
    formatted_player_party = ':'.join(state_obj.player_party)

    # if state object has id then update values in db
    if state_obj.player_id:
        statement = f"""UPDATE game_save SET
                                player_name='{state_obj.player_name}',
                                last_save='{formatted_date}',
                                player_level={state_obj.player_level},
                                x_location={state_obj.game_state_location_x},
                                y_location={state_obj.game_state_location_y},
                                player_party='{formatted_player_party}',
                                current_map='{state_obj.game_state_current_map}',
                                boss_victory='{state_obj.final_victory}'
                        WHERE id = {state_obj.player_id}"""
    else:
        # if state obj has no id then it is a new save and db will create id
        statement = f"""INSERT INTO game_save (player_name, last_save, player_level, x_location,
                                                y_location, player_party, current_map, boss_victory) 
                        VALUES ('{state_obj.player_name}',
                                '{formatted_date}',
                                 {state_obj.player_level},
                                 {state_obj.game_state_location_x},
                                 {state_obj.game_state_location_y},
                                 '{formatted_player_party}',
                                 '{state_obj.game_state_current_map}',
                                 '{state_obj.final_victory}')
                                 """

    curs.execute(statement)

    conn.commit()
    conn.close()
