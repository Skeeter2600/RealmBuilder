from src.linkers.npc_npc_linker import get_associated_npcs
from src.linkers.npc_special_linker import get_specials_by_npc
from src.linkers.city_npc_linker import get_cities_by_npc
from src.linkers.npc_image_linker import get_associated_npc_images
from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect
from src.utils.permissions import check_editable


def rebuild_npcs_table():
    """
    This function will empty the npcs table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS npcs CASCADE;
        """
    create_sql = """
        CREATE TABLE npcs(
            id                  SERIAL PRIMARY KEY,
            name                TEXT NOT NULL,
            age                 INTEGER,
            occupation          TEXT,
            description         TEXT NOT NULL,
            hidden_description  TEXT DEFAULT NULL,
            revealed            BOOLEAN NOT NULL DEFAULT 'f',
            edit_date           TIMESTAMP DEFAULT NULL,
            world_id            INTEGER NOT NULL REFERENCES worlds ON DELETE CASCADE
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def add_npc(user_id, session_key, details):
    """
    This function will add a new npc to the world,
    given the user is an owner or admin

    :param user_id: the id of the user adding
    :param session_key: the user's session key
    :param details: the info on the new npc

    :format details:{ world_id: world npc is in,
                      name: npc name,
                      images: [images associated with npc],
                      age: npc's age,
                      occupation: npc's occupation
                      description: city description,
                      hidden_description: the npc hidden description ('' if not used)
                      associated_cities: [id: city id],
                      associated_npcs: [id: npc id],
                      associated_specials: [id: special id],
                      }

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        if details['hidden_description'] == '':
            add_request = """
                        INSERT INTO npcs(NAME, AGE, OCCUPATION, DESCRIPTION, hidden_description, WORLD_ID) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING id
                        """
            cur.execute(add_request, (details['name'], details['age'], details['occupation'], details['description'],
                                      details['hidden_description'], details['world_id']))
        else:
            add_request = """
                INSERT INTO npcs(NAME, AGE, OCCUPATION, DESCRIPTION, WORLD_ID) 
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """
            cur.execute(add_request, (details['name'], details['age'], details['occupation'],
                                      details['description'], details['world_id']))

        npc_id = conn.fetchall()

        if npc_id != ():
            npc_id = npc_id[0][0]

            # compile image list to add to npc image linker
            image_add_request = """
                INSERT INTO npc_image_linker(npc_id, image) VALUES
                """
            add_values = ''
            for image in details['images']:
                add_values = add_values + '(' + npc_id + ', ' + image + '), '

            add_values = add_values + 'returning id'
            image_add_request = image_add_request + add_values

            cur.execute(image_add_request)
            outcome = cur.fetchall()
            if outcome == ():
                return False

            # compile the city list to add to the linker
            city_add_request = """
                INSERT INTO city_npc_linker(city_id, npc_id) VALUES
                """
            add_values = ''
            for city in details['associated_cities']:
                add_values = add_values + '(' + city + ', ' + npc_id + '), '

            add_values = add_values + 'returning id'
            city_add_request = city_add_request + add_values

            cur.execute(city_add_request)
            outcome = cur.fetchall()
            if outcome == ():
                return False

            # compile the npc list to add to the npc_npc_linker
            npc_add_request = """
                        INSERT INTO npc_npc_linker(npc_1_id, npc_2_id) VALUES
                        """
            add_values = ''
            for other_npc in details['associated_npcs']:
                add_values = add_values + '(' + other_npc + ', ' + npc_id + '), '

            add_values = add_values + 'returning id'
            npc_add_request = npc_add_request + add_values

            cur.execute(npc_add_request)
            outcome = cur.fetchall()
            if outcome == ():
                return False

            # compile the special list to add to the linker
            special_add_request = """
                INSERT INTO npc_special_linker(npc_id, special_id) VALUES
                """
            add_values = ''
            for special in details['associated_specials']:
                add_values = add_values + '(' + npc_id + ', ' + special + '), '

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


def delete_npc(user_id, session_key, npc_id, world_id):
    """
    This function will delete a npc from the world

    :param user_id: the id of the user requesting
    :param session_key: the session key of the user requesting
    :param npc_id: id of the npc
    :param world_id: id that the world is in

    :return: True if deleted, False if not
    """
    if check_session_key(user_id, session_key):
        if check_editable(world_id, user_id, session_key):
            conn = connect()
            cur = conn.cursor()

            delete_request = """
                DELETE FROM npcs
                WHERE id = %s
                returning id
            """
            cur.execute(delete_request, [npc_id])
            outcome = cur.fetchall()
            conn.commit()
            conn.close()

            if outcome != ():
                return True
    return False


def edit_npc(user_id, session_key, npc_id, world_id, details):
    """
    This function will modify the elements of a npc
    in a world, give te user can edit it

    :param user_id: the id of the user editing
    :param session_key: the session_key of the user editing
    :param npc_id: the id of the npc being edited
    :param world_id: the id of the world the city is in
    :param details: the new info for the city

    :format details: { name: npc name,
                       age: npc's age
                       occupation: the npc's occupation
                       description: npc description,
                       revealed: T or F
                     }

    :return: the updated npc info, {} if failure
    """
    if check_session_key(user_id, session_key):
        if check_editable(world_id, user_id, session_key):
            conn = connect()
            cur = conn.cursor()

            edit_request = """
                UPDATE npcs SET
                name = %s, age = %s, occupation = %s, description = %s, revealed = %s, edit_date = now()
                WHERE id = %s
                RETURNING id
                """
            cur.execute(edit_request, (details['name'], details['age'], details['occupation'], details['description'],
                                       details['revealed'], npc_id))
            outcome = cur.fetchall()

            if outcome == ():
                conn.close()
                return {}

            conn.commit()
            conn.close()

            return get_npc_info(user_id, session_key, npc_id, True)

    return {}


def get_npc_info(npc_id, user_id, session_key, admin):
    """
    This function will get the information associated
    with an NPC based on the user's permissions
    :param npc_id: the id of the npc being checked
    :param user_id: the id of the user checking
    :param session_key: the user's session key
    :param admin: if the user is an admin

    :return: the npc info in a json format

    :format return: { name: npc name,
                      images: [images associated with npc]
                      age: npc age,
                      occupation: npc occupation,
                      description: npc description,
                      associated_npcs: [{id: npc id,
                                         name: npc name}]
                      associated_specials: [{id: special id,
                                             name: special name}],
                      associated_cities: [{id: city id,
                                           name: city name}],
                      admin_content: {
                            hidden_description: npc hidden description,
                            revealed: T or F,
                            edit_date: last time updated
                      } (empty if not admin)
    """
    npc_info = {'name': '',
                'images': [],
                'age': '',
                'occupation': "",
                'description': "",
                'associated_npcs': [],
                'associated_specials': [],
                'associated_cities': [],
                'admin_content': {}}

    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        all_info_query = """
            SELECT name, age, occupation, description FROM npcs
            WHERE id = %s
            """
        cur.execute(all_info_query, [npc_id])
        all_outcome = cur.fetchall()[0]
        npc_info['name'] = all_outcome[0]

        npc_info['images'] = get_associated_npc_images(npc_id)

        npc_info['age'] = all_outcome[1]
        npc_info['occupation'] = all_outcome[2]
        npc_info['description'] = all_outcome[3]

        npc_info['associated_npcs'] = get_associated_npcs(npc_id)
        npc_info['associated_specials'] = get_specials_by_npc(npc_id)
        npc_info['associated_cities'] = get_cities_by_npc(npc_id)

        if admin:
            admin_content = {'hidden_description': '',
                             'revealed': None,
                             'edit_date': ''
                             }
            admin_query = """
                SELECT hidden_description, revealed, edit_date FROM npcs
                WHERE id = %s
                """
            cur.execute(admin_query, [npc_id])
            admin_outcome = cur.fetchall[0]

            admin_content['hidden_description'] = admin_outcome[0]
            admin_content['revealed'] = admin_outcome[1]
            admin_content['edit_date'] = admin_outcome[2]

            npc_info['admin_content'] = admin_content

        conn.close()

    return npc_info


def search_for_npc(param, world, limit, page, user_id, session_key):
    """
    This function will search for npcs that contain the
    searched string within them.

    :param param: the string to search for
    :param world: the world to search in
    :param limit: the number of results to show
    :param page: the selection of elements to show
    :param user_id: the id of the user requesting
    :param session_key: the session key of the user requesting

    :return: the list of npcs and their elements that
        meet the search requirements in json format

    :format return: [{ name: npc name,
                       reveal_status: revealed(if admin)}]
    """
    npc_list = []
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

        if check_editable(world, user_id, session_key):
            request = """
            SELECT name, occupation, revealed FROM npcs
            WHERE to_tsvector('english', name) @@ to_tsquery('english', %s) AND
                npcs.world_id = %s
            LIMIT %s OFFSET %s
            """
            cur.execute(request, (content_search, world, limit, (page - 1) * limit))
            npcs_raw = cur.fetchall()
            npc_info = {'name': '',
                        'occupation': '',
                        'reveal_status': False}
            for npc in npcs_raw:
                npc_info['name'] = npc[0]
                npc_info['occupation'] = npc[1]
                npc_info['reveal_status'] = npc[2]
                npc_list.append(npc_info)

        else:
            request = """
                SELECT name, occupation FROM npcs
                WHERE to_tsvector('english', name) @@ to_tsquery('english', %s) AND 
                    npcs.world_id = %s AND npcs.revealed = 't'
                LIMIT %s OFFSET %s
            """
            cur.execute(request, (content_search, world, limit, (page - 1) * limit))
            npcs_raw = cur.fetchall()
            npc_info = {'name': '',
                        'occupation': 0}
            for npc in npcs_raw:
                npc_info['name'] = npc[0]
                npc_info['occupation'] = npc[1]
                npc_list.append(npc_info)

        conn.close()

    return npc_list
