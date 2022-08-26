from src.utils.db_utils import connect


def rebuild_cities_table():
    """
    This function will empty the cities table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS cities CASCADE;
        """
    create_sql = """
        CREATE TABLE cities(
            id              SERIAL PRIMARY KEY,
            name            TEXT NOT NULL,
            population      INTEGER NOT NULL,
            song            TEXT,
            trades          TEXT,
            aesthetic       TEXT,
            description     TEXT NOT NULL,
            revealed        BOOLEAN NOT NULL DEFAULT 'f',
            edit_date       TIMESTAMP DEFAULT NULL,
            world_id        INTEGER NOT NULL REFERENCES worlds ON DELETE CASCADE
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def get_city(user_id, session_key, city_id, admin):
    """
    This function will get the parameters for a city
    based on admin status, given the user is logged in

    :param user_id: the id of the user logging in
    :param session_key: the session key the user has
    :param city_id: the id of the city
    :param admin: if the user is an admin or not

    :return: the information about the city
    """
    conn = connect()
    cur = conn.cursor()

    session_key_receive = """
        SELECT session_key FROM users
        WHERE users.id = %s
        """

    cur.execute(session_key_receive, [user_id])

    outcome = cur.fetchall()

    if not outcome:
        conn.close()
        return "Bad session_key"

    if session_key == outcome[0][0]:

        if admin:
            request = """
            SELECT * FROM cities
            WHERE cities.id = %s
            """
            cur.execute(request, [city_id])

        else:
            request = """
                SELECT * FROM cities
                WHERE cities.id = %s AND cities.revealed = 't'
            """
            cur.execute(request, [city_id])

        outcome = cur.fetchall()
        conn.close()

        return outcome


def get_cities(world, admin, limit, page):
    """
    This function will get all the cities in a world
    within a limit

    :param world: the id of the world being accessed
    :param limit: the number of cities to return
        if None, defaults to 25
    :param admin: if the user looking is an admin
    :param page: determines the cities to show

    :return: a list of cities (name, population, and
        revealed status if admin)
    """
    conn = connect()
    cur = conn.cursor()

    if limit is None:
        limit = 25

    if admin:
        request = """
        SELECT name, population, revealed FROM cities
        WHERE cities.world_id = %s
        LIMIT %s OFFSET %s
        """
        cur.execute(request, (world, limit, (page - 1) * limit))

    else:
        request = """
            SELECT name, population FROM cities
            WHERE cities.world_id = %s AND cities.revealed = 't'
            LIMIT %s OFFSET %s
        """
        cur.execute(request, (world, limit, (page - 1) * limit))

    outcome = cur.fetchall()
    conn.close()

    return outcome


def search_for_city(param, world, admin, limit, page):
    """
    This function will search for cities that contain the
    searched string within them.

    :param param: the string to search for
    :param world: the world to search in
    :param admin: if the system should show unrevealed elements
    :param limit: the number of results to show
    :param page: the selection of elements to show

    :return: the list of cities and their elements that
        meet the search requirements
    """

    conn = connect()
    cur = conn.cursor()

    if limit is None:
        limit = 25

    parts = param.split(" ")
    content_search = parts[0]

    if len(parts) > 1:
        for part in parts:
            content_search = content_search + " & "
            content_search = content_search + part

    if admin:
        request = """
        SELECT name, population, revealed FROM cities
        WHERE to_tsvector('english', name) @@ to_tsquery('english', %s) AND
            cities.world_id = %s
        LIMIT %s OFFSET %s
        """
        cur.execute(request, (content_search, world, limit, (page - 1) * limit))

    else:
        request = """
            SELECT name, population FROM cities
            WHERE to_tsvector('english', name) @@ to_tsquery('english', %s) AND 
                cities.world_id = %s AND cities.revealed = 't'
            LIMIT %s OFFSET %s
        """
        cur.execute(request, (content_search, world, limit, (page - 1) * limit))

    outcome = cur.fetchall()
    conn.close()

    return outcome


def get_npcs_in_city(city_id, admin):
    """
    This function will return the basic information for
    NPCs in a city
    :param city_id: the id of the city to be looked at
    :param admin: if it should show hidden npcs

    :return: the list of viewable NPCs

    :format return: [{ id: npc id,
                       name: npc name,
                       revealed: reveal status (if admin)}]
    """
    conn = connect()
    cur = conn.cursor()

    npc_list = []

    if admin:
        request = """
            SELECT npc.id, name, revealed FROM city_npc_linker
                INNER JOIN npcs AS npc ON city_npc_linker.npc_id = npc.id
            WHERE city_npc_linker.city_id = %s
            """
        cur.execute(request, [city_id])
        outcome = cur.fetchall()

        for special in outcome:
            npc_list.append(
                {'id': special[0],
                 'name': special[1],
                 'revealed': special[2]
                 })

    else:
        request = """
            SELECT npc.id, name FROM city_npc_linker
                INNER JOIN npcs AS npc ON city_npc_linker.npc_id = npc.id
            WHERE city_npc_linker.city_id = %s AND npc.revealed = 't'
            """
        cur.execute(request, [city_id])
        outcome = cur.fetchall()

        for special in outcome:
            npc_list.append(
                {'id': special[0],
                 'name': special[1]
                 })

    conn.close()
    return npc_list


def get_specials_in_city(city_id, admin):
    """
    This function will return the basic information for
    specials in a city
    :param city_id: the id of the city to be looked at
    :param admin: if it should show hidden npcs

    :return: the list of viewable specials

    :format return: [{ id: special id,
                       name: special name,
                       revealed: reveal status (if admin)}]
    """
    conn = connect()
    cur = conn.cursor()

    special_list = []

    if admin:
        request = """
            SELECT special.id, name, revealed FROM city_special_linker
                INNER JOIN specials AS special ON city_special_linker.special_id = special.id
            WHERE city_special_linker.city_id = %s
            """
        cur.execute(request, [city_id])
        outcome = cur.fetchall()

        for special in outcome:
            special_list.append(
                {'id': special[0],
                 'name': special[1],
                 'revealed': special[2]
                 })

    else:
        request = """
            SELECT special.id, name FROM city_special_linker
                INNER JOIN specials AS special ON city_special_linker.special_id = special.id
            WHERE city_special_linker.city_id = %s AND special.revealed = 't'
            """
        cur.execute(request, [city_id])
        outcome = cur.fetchall()

        for special in outcome:
            special_list.append(
                {'id': special[0],
                 'name': special[1]
                 })

    conn.close()
    return special_list
