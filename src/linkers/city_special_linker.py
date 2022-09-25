from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect
from src.utils.permissions import check_editable


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


def get_cities_by_special(user_id, session_key, special_id):
    """
    This function will get all cities a special
    is associated with
    :param user_id: the id of the user requesting
    :param session_key: the user's session key
    :param special_id: the id of the special being checked

    :return: a list of the cities

    :format return: [{id: city id,
                      name: city name}]
    """
    outcome = []
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        world_id_check = """
            SELECT world_id FROM specials
            WHERE id = %s
            """
        cur.execute(world_id_check, [special_id])
        world_id = cur.fetchall()[0][0]

        if check_editable(world_id, user_id, session_key):
            city_query = """
                SELECT cities.id, name FROM city_special_linker
                    INNER JOIN cities ON city_special_linker.city_id = cities.id
                WHERE special_id = %s
                """
        else:
            city_query = """
                SELECT cities.id, name FROM city_special_linker
                    INNER JOIN cities ON city_special_linker.city_id = cities.id
                WHERE special_id = %s AND cities.revealed = 't'
                """
        cur.execute(city_query, [special_id])
        outcome = cur.fetchall()
        conn.close()

    return outcome


def get_specials_by_city(user_id, session_key, city_id):
    """
    This function will get all the specials associated
    with a city
    :param user_id: the id of the user requesting
    :param session_key: the user's session key
    :param city_id: the id of the city being checked

    :return: a list of specials

    :format return: [{id: specials id,
                      name: specials name}]
    """
    outcome = []
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        world_id_check = """
            SELECT world_id FROM cities
            WHERE id = %s
            """
        cur.execute(world_id_check, [city_id])
        world_id = cur.fetchall()[0][0]

        if check_editable(world_id, user_id, session_key):
            specials_query = """
                SELECT specials.id, name FROM city_special_linker
                    INNER JOIN specials ON city_special_linker.city_id = specials.id
                WHERE city_id = %s
                """
        else:
            specials_query = """
                SELECT specials.id, name FROM city_special_linker
                    INNER JOIN specials ON city_special_linker.city_id = specials.id
                WHERE city_id = %s AND specials.revealed = 't'
                """
        cur.execute(specials_query, [city_id])
        outcome = cur.fetchall()
        conn.close()

    return outcome
