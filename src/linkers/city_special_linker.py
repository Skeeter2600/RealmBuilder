from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect


def rebuild_city_special_linker():
    """
    This function will empty the city special linker table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS city_special_linker CASCADE;
        """
    create_sql = """
        CREATE TABLE city_special_linker(
            id              SERIAL PRIMARY KEY,
            city_id         INTEGER NOT NULL REFERENCES cities ON DELETE CASCADE,
            special_id      INTEGER NOT NULL REFERENCES specials ON DELETE CASCADE
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def add_city_special_association(city_id, special_id, user_id, session_key):
    """
    This function will add an association between
    a city and an special to the linker table

    :param special_id: the id of the special
    :param city_id: the id of the city
    :param user_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()
        insert_request = """
            INSERT INTO city_special_linker(city_id, special_id) VALUES
            (%s, %s)
            RETURNING id
            """
        cur.execute(insert_request, (city_id, special_id))
        outcome = cur.fetchall()

        conn.commit()
        conn.close()

        if outcome != ():
            return True
    return False


def remove_city_special_association(city_id, special_id, user_id, session_key):
    """
    This function will remove an association between
    a city and a special from the linker table

    :param special_id: the id of the special
    :param city_id: the id of the city
    :param user_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()
        delete_request = """
            DELETE FROM city_special_linker WHERE
            city_id = %s AND special_id = %s
            RETURNING id
            """
        cur.execute(delete_request, (city_id, special_id))
        outcome = cur.fetchall()
        if outcome != ():
            conn.commit()
            conn.close()
            return True
    return False


def get_cities_by_special(special_id):
    """
    This function will get all cities an NPC
    is associated with
    :param special_id: the id of the special being checked

    :return: a list of the cities

    :format return: [{id: city id,
                      name: city name}]
    """
    conn = connect()
    cur = conn.cursor()

    npc2_query = """
            SELECT cities.id, name FROM city_special_linker
                INNER JOIN cities ON city_special_linker.city_id = cities.id
            WHERE city_id = %s
            """
    cur.execute(npc2_query, [special_id])
    outcome = cur.fetchall()
    conn.close()

    return outcome


def get_specials_by_city(city_id):
    """
    This function will get all of the NPCs associated
    with a city
    :param city_id: the id of the city being checked

    :return: a list of specials

    :format return: [{id: specials id,
                      name: specials name}]
    """
    conn = connect()
    cur = conn.cursor()

    npc2_query = """
                SELECT specials.id, name FROM city_special_linker
                    INNER JOIN specials ON city_special_linker.city_id = specials.id
                WHERE special_id = %s
                """
    cur.execute(npc2_query, [city_id])
    outcome = cur.fetchall()
    conn.close()

    return outcome
