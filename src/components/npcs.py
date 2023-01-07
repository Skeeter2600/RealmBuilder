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
            edit_date           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
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

    :return: [created boolean, npc id (-1 if failed)]
    """
    if check_session_key(user_id, session_key):
        if check_editable(details['world_id'], user_id, session_key):
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

            npc_id = cur.fetchall()

            if npc_id != ():
                npc_id = npc_id[0][0]

                if len(details['images']) > 0:
                    # compile image list to add to npc image linker
                    image_add_request = """
                        INSERT INTO npc_image_linker(npc_id, image) VALUES
                        """
                    add_values = ''
                    length = len(details['images'])
                    i = 0
                    while i < length-1:
                        add_values = add_values + '(' + str(npc_id) + ', ' + str(details['images'][i]) + '), '
                        i += 1
                    add_values = add_values + '(' + str(npc_id) + ', ' + str(details['images'][i]) + ') '

                    add_values = add_values + 'returning id'
                    image_add_request = image_add_request + add_values

                    cur.execute(image_add_request)
                    outcome = cur.fetchall()
                    if outcome == ():
                        return False

                # compile the city list to add to the linker
                if len(details['associated_cities']) > 0:
                    city_add_request = """
                        INSERT INTO city_npc_linker(city_id, npc_id) VALUES
                        """
                    add_values = ''
                    length = len(details['associated_cities'])
                    i = 0
                    while i < length-1:
                        add_values = add_values + '(' + str(details['associated_cities'][i]['id']) + ', ' + str(npc_id) + '), '
                        i += 1

                    add_values = add_values + '(' + str(details['associated_cities'][i]['id']) + ', ' + str(npc_id) + ') '
                    add_values = add_values + 'returning id'
                    city_add_request = city_add_request + add_values

                    cur.execute(city_add_request)
                    outcome = cur.fetchall()
                    if outcome == ():
                        return False

                # compile the npc list to add to the npc_npc_linker
                if len(details['associated_npcs']) > 0:
                    npc_add_request = """
                                INSERT INTO npc_npc_linker(npc_1_id, npc_2_id) VALUES
                                """
                    add_values = ''
                    length = len(details['associated_npcs'])
                    i = 0
                    while i < length-1:
                        add_values = add_values + '(' + str(details['associated_npcs'][i]['id']) + ', ' + str(npc_id) + '), '
                        i += 1

                    add_values = add_values + '(' + str(details['associated_npcs'][i]['id']) + ', ' + str(npc_id) + ') '

                    add_values = add_values + 'returning id'
                    npc_add_request = npc_add_request + add_values

                    cur.execute(npc_add_request)
                    outcome = cur.fetchall()
                    if outcome == ():
                        return False

                # compile the special list to add to the linker
                if len(details['associated_specials']) > 0:
                    special_add_request = """
                        INSERT INTO npc_special_linker(npc_id, special_id) VALUES
                        """
                    add_values = ''
                    length = len(details['associated_specials'])
                    i = 0
                    while i < length-1:
                        add_values = add_values + '(' + str(npc_id) + ', ' + str(details['associated_specials'][i]['id']) + '), '

                    add_values = add_values + '(' + str(npc_id) + ', ' + str(details['associated_specials'][i]['id']) + ') '
                    add_values = add_values + 'returning id'
                    special_add_request = special_add_request + add_values

                    cur.execute(special_add_request)
                    outcome = cur.fetchall()
                    if outcome == ():
                        return False

                conn.commit()
                conn.close()
                return [True, npc_id]
    return [False, -1]


def copy_npc(user_id, session_key, npc_id, world_id):
    """
    This function will make a copy of the specified npc
    in the world of the user's choice, given they have permission
    to create new elements

    :param user_id: the id of the user requesting
    :param session_key: the session key of the user
    :param npc_id: the id of the special
    :param world_id: the id of the world

    :return: [created boolean, npc id (-1 if failed)]
    """
    if check_editable(world_id, user_id, session_key):
        conn = connect()
        cur = conn.cursor()
        duplicate_request = """
            INSERT INTO npcs(name, age, occupation, description, world_id)
            SELECT name, age, occupation, description, world_id FROM npcs
            WHERE id = %s
            RETURNING id
            """
        cur.execute(duplicate_request, [npc_id])
        new_id = cur.fetchall()[0][0]

        change_world = """
            UPDATE npcs SET
            world_id = %s
            WHERE id = %s
            RETURNING id
            """
        cur.execute(change_world, (world_id, new_id))

        outcome = cur.fetchall()
        conn.commit()
        conn.close()
        if outcome != ():
            return [True, new_id]
    return [False, -1]


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


def get_npc_info(user_id, session_key, npc_id, admin):
    """
    This function will get the information associated
    with an NPC based on the user's permissions
    :param npc_id: the id of the npc being checked
    :param user_id: the id of the user checking
    :param session_key: the user's session key
    :param admin: if the user is an admin

    :return: the npc info in a json format

    :format return: { name: npc name,
                      images: [images associated with npc],
                      likes: npc likes,
                      dislikes: npc dislikes,
                      user_like: is user liked it (True or False),
                      user_dislike: is user disliked it (True or False),
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
                'likes': 0,
                'dislikes': 0,
                'user_like': False,
                'user_dislike': False,
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

        if not admin:
            all_info_query = all_info_query + " AND revealed = 't'"

        cur.execute(all_info_query, [npc_id])
        all_outcome = cur.fetchall()
        if len(all_outcome) > 0:
            all_outcome = all_outcome[0]
            npc_info['name'] = all_outcome[0]

            npc_info['images'] = get_associated_npc_images(npc_id)

            npc_info['age'] = all_outcome[1]
            npc_info['occupation'] = all_outcome[2]
            npc_info['description'] = all_outcome[3]

            npc_info['associated_npcs'] = get_associated_npcs(user_id, session_key, npc_id)
            npc_info['associated_specials'] = get_specials_by_npc(user_id, session_key, npc_id)
            npc_info['associated_cities'] = get_cities_by_npc(user_id, session_key, npc_id)

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
                admin_outcome = cur.fetchall()[0]

                admin_content['hidden_description'] = admin_outcome[0]
                admin_content['revealed'] = admin_outcome[1]
                admin_content['edit_date'] = admin_outcome[2]

                npc_info['admin_content'] = admin_content

            likes_dislike_query = """
                    SELECT COUNT(*) AS total,
                    sum(case when like_dislike = 'T' then 1 else 0 end) AS likes,
                    sum(case when like_dislike = 'F' then 1 else 0 end) AS dislikes,
                    sum(case when like_dislike = 'T' AND user_id = %s then 1 else 0 end) AS user_like,
                    sum(case when like_dislike = 'F' AND user_id = %s then 1 else 0 end) AS user_dislike
                    FROM likes_dislikes
                    WHERE component_id = %s AND component_type = 'npcs'
                """

            cur.execute(likes_dislike_query, [user_id, user_id, npc_id])
            like_dislike_outcome = cur.fetchall()

            if len(like_dislike_outcome) > 0 and (like_dislike_outcome[0][0] != 0):
                like_dislike_outcome = like_dislike_outcome[0]

                npc_info['likes'] = like_dislike_outcome[1]
                npc_info['dislikes'] = like_dislike_outcome[2]
                npc_info['user_like'] = (like_dislike_outcome[3] > 0)
                npc_info['user_dislike'] = (like_dislike_outcome[4] > 0)

        conn.close()

    return npc_info


def reveal_hidden_npc(user_id, session_key, world_id, npc_id):
    """
    This function will reveal the hidden description by amending
    it to the description, given the user requesting has edit permission

    :param user_id: id of the user requesting
    :param session_key: the user's session key
    :param world_id: the id of the world the special is in
    :param npc_id: the id of the npc to be revealed

    :return: The npc's info if good, {} if bad
    """
    if check_editable(world_id, user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        reveal_query = """
        UPDATE npcs SET
        description = concat(description, '\n\nREVEAL\n\n', hidden_description),
        hidden_description = ''
        WHERE id = %s
        returning id
        """
        cur.execute(reveal_query, [npc_id])
        outcome = cur.fetchall()
        conn.commit()
        conn.close()
        if outcome != ():
            return get_npc_info(user_id, session_key, npc_id, True)

    return {}


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

    :format return: [{ id: npc's id,
                       name: npc name,
                       reveal_status: revealed(if admin)}]
    """
    npc_list = []
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        if limit is None:
            limit = 25

        param = '%' + param + '%'

        if check_editable(world, user_id, session_key):
            request = """
                SELECT id, name, occupation, revealed FROM npcs
                WHERE name ILIKE %s AND
                    npcs.world_id = %s
                LIMIT %s OFFSET %s
            """
            cur.execute(request, (param, world, limit, (page - 1) * limit))
            npcs_raw = cur.fetchall()
            for npc in npcs_raw:
                npc_list.append({'id': npc[0],
                                 'name': npc[1],
                                 'occupation': npc[2],
                                 'reveal_status': npc[3]})

        else:
            request = """
                SELECT id, name, occupation FROM npcs
                WHERE name ILIKE %s AND
                    npcs.world_id = %s AND npcs.revealed = 't'
                LIMIT %s OFFSET %s
            """
            cur.execute(request, (param, world, limit, (page - 1) * limit))
            npcs_raw = cur.fetchall()
            for npc in npcs_raw:
                npc_list.append({'id': npc[0],
                                 'name': npc[1],
                                 'occupation': npc[2]})

        conn.close()

    return npc_list
