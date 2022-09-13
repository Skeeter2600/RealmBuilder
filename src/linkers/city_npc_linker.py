from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect


def rebuild_city_npc_linker():
    """
    This function will empty the city npc linker table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS city_npc_linker CASCADE;
        """
    create_sql = """
        CREATE TABLE city_npc_linker(
            id              SERIAL PRIMARY KEY,
            city_id         INTEGER NOT NULL REFERENCES cities ON DELETE CASCADE,
            npc_id          INTEGER NOT NULL REFERENCES npcs ON DELETE CASCADE
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def add_city_npc_association(city_id, npc_id, user_id, session_key):
    """
    This function will add an association between
    a city and an npc to the linker table

    :param npc_id: the id of the npc
    :param city_id: the id of the city
    :param user_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()
        insert_request = """
            INSERT INTO city_npc_linker(city_id, npc_id) VALUES
            (%s, %s)
            """
        cur.execute(insert_request, (city_id, npc_id))
        conn.commit()
        conn.close()
        return True
    return False


def remove_city_npc_association(city_id, npc_id, user_id, session_key):
    """
    This function will remove an association between
    a city and an npc to the linker table

    :param npc_id: the id of the npc
    :param city_id: the id of the city
    :param user_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()
        delete_request = """
            DELETE FROM city_npc_linker WHERE
            city_id = %s AND npc_id = %s
            """
        cur.execute(delete_request, (city_id, npc_id))
        conn.commit()
        conn.close()
        return True
    return False


def get_cities_by_npc(npc_id):
    """
    This function will get all cities an NPC
    is associated with
    :param npc_id: the id of the npc being checked

    :return: a list of the cities

    :format return: [{id: city id,
                      name: city name}]
    """
    conn = connect()
    cur = conn.cursor()

    npc2_query = """
            SELECT cities.id, name FROM city_npc_linker
                INNER JOIN cities ON city_npc_linker.city_id = cities.id
            WHERE city_id = %s
            """
    cur.execute(npc2_query, [npc_id])
    outcome = cur.fetchall()
    conn.close()

    return outcome


def get_npcs_by_city(city_id):
    """
    This function will get all of the NPCs associated
    with a city
    :param city_id: the id of the city being checked

    :return: a list of npcs

    :format return: [{id: npc id,
                      name: npc name}]
    """
    conn = connect()
    cur = conn.cursor()

    npc2_query = """
            SELECT npcs.id, name FROM city_npc_linker
                INNER JOIN npcs ON city_npc_linker.city_id = npcs.id
            WHERE npc_id = %s
            """
    cur.execute(npc2_query, [city_id])
    outcome = cur.fetchall()
    conn.close()

    return outcome
