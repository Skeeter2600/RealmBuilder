from src.utils.permissions import check_editable
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
            edit_date       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            world_id        INTEGER NOT NULL REFERENCES worlds ON DELETE CASCADE
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def add_city(user_id, session_key, details):
    """
    This function will add a new city to the world,
    given the user is an owner or admin

    :param user_id: the id of the user adding
    :param session_key: the user's session key
    :param details: the info on the new city

    :format details:{ world_id: world city is in,
                      name: city name,
                      images: [images associated with npc],
                      population: city population,
                      song: city song,
                      trades: city trades,
                      aesthetic: city aesthetic
                      description: city description,
                      associated_npcs: [id: npc id],
                      associated_specials: [id: special id],
                      }

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        add_request = """
            INSERT INTO cities(NAME, POPULATION, SONG, TRADES, AESTHETIC, DESCRIPTION, WORLD_ID) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """
        cur.execute(add_request, (details['name'], details['population'], details['song'], details['trades'],
                                  details['aesthetic'], details['description'], details['world_id']))
        city_id = conn.fetchall()

        if city_id != ():
            city_id = city_id[0][0]

            # compile image list to add to city image linker
            image_add_request = """
                INSERT INTO city_image_linker(city_id, image) VALUES
                """
            add_values = ''
            for image in details['images']:
                add_values = add_values + '(' + city_id + ', ' + image + '), '

            add_values = add_values + 'returning id'
            image_add_request = image_add_request + add_values

            cur.execute(image_add_request)
            outcome = cur.fetchall()
            if outcome == ():
                return False

            # compile the npc list to add to the linker
            npc_add_request = """
                INSERT INTO city_npc_linker(city_id, npc_id) VALUES
                """
            add_values = ''
            for npc in details['associated_npcs']:
                add_values = add_values + '(' + city_id + ', ' + npc + '), '

            add_values = add_values + 'returning id'
            npc_add_request = npc_add_request + add_values

            cur.execute(npc_add_request)
            outcome = cur.fetchall()
            if outcome == ():
                return False

            # compile the special list to add to the linker
            special_add_request = """
                INSERT INTO city_special_linker(city_id, special_id) VALUES
                """
            add_values = ''
            for special in details['associated_specials']:
                add_values = add_values + '(' + city_id + ', ' + special + '), '

            add_values = add_values + 'returning id'
            special_add_request = special_add_request + add_values

            cur.execute(special_add_request)
            outcome = cur.fetchall()
            if outcome == ():
                return False

            conn.commit()
            conn.close()
            return True
    return False


def delete_city(user_id, session_key, city_id, world_id):
    """
    This function will delete a city from the world

    :param user_id: the id of the user requesting
    :param session_key: the session key of the user requesting
    :param city_id: id of the city
    :param world_id: id that the world is in

    :return: True if deleted, False if not
    """
    if check_session_key(user_id, session_key):
        if check_editable(world_id, user_id, session_key):
            conn = connect()
            cur = conn.cursor()

            delete_request = """
                DELETE FROM cities
                WHERE id = %s
                returning id
            """
            cur.execute(delete_request, [city_id])
            outcome = cur.fetchall()
            conn.commit()
            conn.close()

            if outcome != ():
                return True
    return False


def edit_city(user_id, session_key, city_id, world_id, details):
    """
    This function will modify the elements of a city
    in a world, give te user can edit it

    :param user_id: the id of the user editing
    :param session_key: the session_key of the user editing
    :param city_id: the id of the city being edited
    :param world_id: the id of the world the city is in
    :param details: the new info for the city

    :format details: { name: city name,
                       population: city population,
                       song: city song,
                       trades: city trades,
                       aesthetic: city aesthetic
                       description: city description,
                       revealed: T or F,
                     }

    :return: the updated city info, {} if failure
    """
    if check_session_key(user_id, session_key):
        if check_editable(world_id, user_id, session_key):
            conn = connect()
            cur = conn.cursor()

            edit_request = """
                UPDATE cities SET
                name = %s, population = %s, song = %s, trades = %s,
                aesthetic = %s, description = %s, revealed = %s, edit_date = now()
                WHERE id = %s
                RETURNING id
                """
            cur.execute(edit_request, (details['name'], details['population'], details['song'], details['trades'],
                                       details['aesthetic'], details['description'], details['revealed'], city_id))
            outcome = cur.fetchall()

            if outcome == ():
                conn.close()
                return {}
            conn.commit()
            conn.close()

            return get_city(user_id, session_key, city_id, True)

    return {}


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
                    }
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
    city_list = []
    if check_session_key(user_id, session_key):

        conn = connect()
        cur = conn.cursor()

        if limit is None:
            limit = 25

        param = '%' + param + '%'

        if check_editable(world, user_id, session_key):
            request = """
            SELECT name, population, revealed FROM cities
            WHERE name ILIKE %s AND
                cities.world_id = %s
            LIMIT %s OFFSET %s
            """
            cur.execute(request, (param, world, limit, (page - 1) * limit))
            cities_raw = cur.fetchall()
            for city in cities_raw:
                city_list.append({'name': city[0],
                                  'population': city[1],
                                  'reveal_status': city[2]})
        else:
            request = """
                SELECT name, population FROM cities
                WHERE name ILIKE %s AND cities.world_id = %s AND cities.revealed = 't'
                LIMIT %s OFFSET %s
            """
            cur.execute(request, (param, world, limit, (page - 1) * limit))
            cities_raw = cur.fetchall()
            for city in cities_raw:
                city_list.append({'name': city[0],
                                  'population': city[1]})
        conn.close()

    return city_list
