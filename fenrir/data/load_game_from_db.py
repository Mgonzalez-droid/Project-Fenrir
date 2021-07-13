import fenrir.data.db_connection as db
from fenrir.common.global_game_state import GameState


def load_game_save_titles():
    save_list = []

    # connect to the database - close when finished
    conn = db.connect_to_db()
    curs = conn.cursor()

    for row in curs.execute("SELECT id, player_name, last_save FROM game_save"):
        save_list.append(row)

    conn.commit()
    conn.close()

    return save_list


def load_game_save_by_id(player_id: int):
    conn = db.connect_to_db()
    curs = conn.cursor()

    curs.execute(f"SELECT * FROM game_save WHERE id={player_id}")
    data = curs.fetchone()

    return GameState(data[0], data[1], data[2], data[3], data[4], data[5])

    conn.commit()
    conn.close()
