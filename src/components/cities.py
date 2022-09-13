from src.components.worlds import check_editable
from src.linkers.city_image_linker import get_associated_city_images
from src.linkers.city_npc_linker import get_npcs_by_city
from src.linkers.city_special_linker import get_specials_by_city
from src.utils.db_tools import check_session_key
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

    :return: the city info in a json format

    :format return: { name: city name,
                      images: [images associated with npc],
                      population: city population,
                      song: city song,
                      trades: city trades,
                      aesthetic: city aesthetic
                      description: city description,
                      associated_npcs: [{id: npc id,
                                         name: npc name}]
                      associated_specials: [{id: special id,
                                             name: special name}],
                      admin_content: {
                            revealed: T or F,
                            edit_date: last time updated
                      } (empty if not admin)
    """
    city_info = {'name': '',
                 'images': [],
                 'population': 0,
                 'song': '',
                 'trades': '',
                 'aesthetic': '',
                 'description': '',
                 'associated_npcs': [],
                 'associated_specials': [],
                 'admin_content': {}}

    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        all_info_query = """
            SELECT name, population, song, trades, aesthetic, description FROM cities
            WHERE id = %s
            """
        cur.execute(all_info_query, [city_id])
        all_outcome = cur.fetchall()[0]
        city_info['name'] = all_outcome[0]

        city_info['images'] = get_associated_city_images(city_id)

        city_info['population'] = all_outcome[1]
        city_info['song'] = all_outcome[2]
        city_info['trades'] = all_outcome[3]
        city_info['aesthetic'] = all_outcome[4]
        city_info['description'] = all_outcome[5]

        city_info['associated_npcs'] = get_npcs_by_city(city_id)
        city_info['associated_specials'] = get_specials_by_city(city_id)

        if admin:
            admin_content = {'revealed': None,
                             'edit_date': ''
                             }
            admin_query = """
                SELECT revealed, edit_date FROM cities
                WHERE id = %s
                """
            cur.execute(admin_query, [city_id])
            admin_outcome = cur.fetchall[0]

            admin_content['revealed'] = admin_outcome[0]
            admin_content['edit_date'] = admin_outcome[1]

            city_info['admin_content'] = admin_content

        conn.close()

    return city_info


def get_cities(user_id, session_key, world, limit, page):
    """
    This function will get all the cities in a world
    within a limit

    :param user_id: the id of the user requesting
    :param session_key: the session key of the user
    :param world: the id of the world being accessed
    :param limit: the number of cities to return
        if None, defaults to 25
    :param page: determines the cities to show

    :return: a list of cities (name, population, and
        revealed status if admin) each in json format

    :format return: [{ name: city name,
                       population: city population,
                       reveal_status: revealed(if admin)}]
    """

    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()
        if limit is None:
            limit = 25

        city_list = []

        if check_editable(world, user_id, session_key):
            request = """
            SELECT name, population, revealed FROM cities
            WHERE cities.world_id = %s
            LIMIT %s OFFSET %s
            """
            cur.execute(request, (world, limit, (page - 1) * limit))
            cities_raw = cur.fetchall()
            city_info = {'name': '',
                         'population': 0,
                         'reveal_status': False}
            for city in cities_raw:
                city_info['name'] = city[0]
                city_info['population'] = city[1]
                city_info['reveal_status'] = city[2]
                city_list.append(city_info)

        else:
            request = """
                SELECT name, population FROM cities
                WHERE cities.world_id = %s AND cities.revealed = 't'
                LIMIT %s OFFSET %s
            """
            cur.execute(request, (world, limit, (page - 1) * limit))
            cities_raw = cur.fetchall()
            city_info = {'name': '',
                         'population': 0}
            for city in cities_raw:
                city_info['name'] = city[0]
                city_info['population'] = city[1]
                city_list.append(city_info)

        conn.close()
        return city_list
    return []


def search_for_city(param, world, limit, page, user_id, session_key):
    """
    This function will search for cities that contain the
    searched string within them.

    :param param: the string to search for
    :param world: the world to search in
    :param limit: the number of results to show
    :param page: the selection of elements to show
    :param user_id: the id of the user requesting
    :param session_key: the session key of the user requesting

    :return: the list of cities and their elements that
        meet the search requirements in json format

    :format return: [{ name: city name,
                       population: city population,
                       reveal_status: revealed(if admin)}]
    """

    if check_session_key(user_id, session_key):

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

        city_list = []

        if check_editable(world, user_id, session_key):
            request = """
            SELECT name, population, revealed FROM cities
            WHERE to_tsvector('english', name) @@ to_tsquery('english', %s) AND
                cities.world_id = %s
            LIMIT %s OFFSET %s
            """
            cur.execute(request, (content_search, world, limit, (page - 1) * limit))
            cities_raw = cur.fetchall()
            city_info = {'name': '',
                         'population': 0,
                         'reveal_status': False}
            for city in cities_raw:
                city_info['name'] = city[0]
                city_info['population'] = city[1]
                city_info['reveal_status'] = city[2]
                city_list.append(city_info)

        else:
            request = """
                SELECT name, population FROM cities
                WHERE to_tsvector('english', name) @@ to_tsquery('english', %s) AND 
                    cities.world_id = %s AND cities.revealed = 't'
                LIMIT %s OFFSET %s
            """
            cur.execute(request, (content_search, world, limit, (page - 1) * limit))
            cities_raw = cur.fetchall()
            city_info = {'name': '',
                         'population': 0}
            for city in cities_raw:
                city_info['name'] = city[0]
                city_info['population'] = city[1]
                city_list.append(city_info)

        outcome = cur.fetchall()
        conn.close()

        return outcome
    return []
