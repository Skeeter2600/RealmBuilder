from src.components.comments import get_component_comments
from src.components.likes_dislikes import get_likes_dislike
from src.linkers.world_user_linker import get_new_elements
from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect
from src.utils.permissions import check_editable, check_viewable


def rebuild_worlds_table():
    """
    This function will empty the worlds table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS worlds CASCADE;
        """
    create_sql = """
        CREATE TABLE worlds(
            id              SERIAL PRIMARY KEY,
            name            TEXT NOT NULL,
            description     TEXT DEFAULT '',
            owner_id        INTEGER NOT NULL REFERENCES users ON DELETE CASCADE,
            public          BOOLEAN NOT NULL DEFAULT 'f'
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def add_world(name, owner_id, session_key):
    """
    This function will add a world to the database
    :param name: The name of the world
    :param owner_id: the id of the user who made the world
    :param session_key: the supposed session key of the user

    :return: { result: bool,
               world_id: int (-1 if failed)
              }
    """
    if check_session_key(owner_id, session_key):
        conn = connect()
        cur = conn.cursor()

        request = """
                    INSERT INTO worlds(name, owner_id) VALUES
                    (%s, %s)
                    RETURNING id
                    """
        cur.execute(request, (name, owner_id))
        outcome = cur.fetchall()
        if outcome != ():
            insert_request = """
                INSERT INTO world_user_linker(world_id, user_id) VALUES
                (%s, %s)
                RETURNING id
                """
            cur.execute(insert_request, (outcome[0][0], owner_id))

            conn.commit()
            conn.close()
            return {'result': True, 'world_id': outcome[0][0]}
    return {'result': False, 'world_id': -1}


def delete_world(world_id, owner_id, session_key):
    """
    This function will delete a world and all of
    the components associated with it
    :param world_id: the id of the world to delete
    :param owner_id: the id of the owner of the world
    :param session_key: the supposed session key of the user

    :return: True if successful, False if not
    """

    if check_session_key(owner_id, session_key):
        if get_owner(world_id)['id'] == owner_id:
            conn = connect()
            cur = conn.cursor()

            delete_request = """
                DELETE FROM worlds
                WHERE id = %s
                RETURNING id
                """
            cur.execute(delete_request, [world_id])
            outcome = cur.fetchall()

            conn.commit()
            conn.close()

            # if the delete was successful
            if len(outcome) > 0:
                return {'result': True}
    return {'result': False}


def edit_world(world_id, user_id, session_key, elements):
    """
    This function will edit the elements of a world
    :param world_id: the id of the world
    :param user_id: the id of the user requesting the edit
    :param session_key: the session key of the user
    :param elements: the elements being changed in json

    :format elements:
            { name: the world name,
              description: the world description,
              public: True or False
            }

    :return: True if edited, False if not
    """
    if check_editable(world_id, user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        update_request = """
            UPDATE worlds
            SET name = %s, description = %s, public = %s
            WHERE id = %s
            """
        cur.execute(update_request, (elements['name'], elements['description'], elements['public'], world_id))
        conn.commit()

        conn.close()
        return {'result': True}
    return {'result': False}


def join_world_public(world_id, user_id, session_key):
    """
    This function will allow a user to join a world

    :param world_id: the id of the world
    :param user_id: the id of the user
    :param session_key: the session_key of the user

    :return: True if successful, False if not
    """
    conn = connect()
    cur = conn.cursor()

    if check_session_key(user_id, session_key):
        world_check_query = """
            SELECT EXISTS(
                SELECT 1 FROM worlds
                WHERE id = %s  AND public = 't'
            )
            """
        cur.execute(world_check_query, [world_id])
        outcome = cur.fetchall()

        if outcome[0][0]:
            add_query = """
                INSERT INTO world_user_linker(world_id, user_id) VALUES 
                (%s, %s)
                returning id
                """
            cur.execute(add_query, (world_id, user_id))
            outcome = cur.fetchall()
            if outcome != ():
                conn.commit()
                conn.close()
                return {'result': True}
    return {'result': False}


def join_world_private(world_id, user_id, admin_id, session_key):
    """
    This function will allow a user to join a world

    :param world_id: the id of the world
    :param user_id: the id of the user
    :param admin_id: the id of the admin
    :param session_key: the session_key of the user

    :return: True if successful, False if not
    """
    conn = connect()
    cur = conn.cursor()

    if check_session_key(admin_id, session_key):
        if check_editable(world_id, admin_id, session_key):
            world_check_query = """
                SELECT EXISTS(
                    SELECT 1 FROM worlds
                    WHERE id = %s
                )
                """
            cur.execute(world_check_query, [world_id])
            outcome = cur.fetchall()

            if outcome[0][0]:
                add_query = """
                    INSERT INTO world_user_linker(world_id, user_id) VALUES 
                    (%s, %s)
                    returning id
                    """
                cur.execute(add_query, (world_id, user_id))
                outcome = cur.fetchall()
                if outcome != ():
                    conn.commit()
                    conn.close()
                    return {'result': True}
    return {'result': False}


def get_owner(world_id):
    """
    This will get the info on the owner of the world

    :param world_id: the id of the world being checked

    :return: the info on the owner
    :format return:
            {  id:   user id,
               name: user's name,
               profile_pic: user's profile picture
            }
    """
    conn = connect()
    cur = conn.cursor()
    owner_request = """
                SELECT users.id, users.username, users.profile_pic FROM worlds
                    INNER JOIN users ON worlds.owner_id = users.id
                WHERE worlds.id = %s
                """
    cur.execute(owner_request, [world_id])
    outcome = cur.fetchall()
    conn.close()

    if outcome:
        return {
            "id": outcome[0][0],
            "name": outcome[0][1],
            "profile_pic": outcome[0][2]}
    return {
            "id": '',
            "name": '',
            "profile_pic": ''}


def get_world_admin_list(world_id, user_id, session_key):
    """
    This function will get a list of all users who
    are admins of a world
    :param world_id: the id of the world being checked
    :param user_id: the id of the user requesting the edit
    :param session_key: the session key of the user

    :return: a list of the admins in a world

    :format return:
            [{  id:   user id,
                name: user's name,
                profile_picture: user's profile picture
            }]
    """
    if check_session_key(user_id, session_key):
        if check_viewable(world_id, user_id)['viewable']:
            conn = connect()
            cur = conn.cursor()

            user_list = []

            # add the admins to the list
            admin_request = """
                    SELECT users.id, users.username, users.profile_pic FROM admins
                        INNER JOIN users ON admins.user_id = users.id
                    WHERE world_id = %s
                    """
            cur.execute(admin_request, [world_id])
            outcome = cur.fetchall()
            for admin in outcome:
                user_list.append(admin)

            conn.close()
            return user_list
    return []


def get_world_user_list(world_id, user_id, session_key):
    """
    This function will get a list of all users who
    are a part of a world
    :param world_id: the id of the world being checked
    :param user_id: the id of the user requesting the edit
    :param session_key: the session key of the user

    :return: a list of the users in a world

    :format return:
            [{  id:   user id,
                name: user's name,
                profile_picture: user's profile picture
            }]
    """
    if check_session_key(user_id, session_key):
        if check_viewable(world_id, user_id)['viewable']:
            conn = connect()
            cur = conn.cursor()

            user_list = []

            # add the members to the list
            member_request = """
                SELECT users.id, users.username, users.profile_pic FROM world_user_linker
                    INNER JOIN users ON world_user_linker.user_id = users.id
                WHERE world_id = %s
                """
            cur.execute(member_request, [world_id])
            outcome = cur.fetchall()
            for user in outcome:
                user_list.append({'id': user[0],
                                  'username': user[1],
                                  'profile_picture': user[2]})

            conn.close()
            return user_list
    return []


def get_world_details(world_id, user_id, session_key):
    """
    This function will get the information about a world
    based on if they are an owner, admin, or if they are
    able to access it
    :param world_id: the id of the world being accessed
    :param user_id: the id of the user requesting it
    :param session_key: the session key of the user requesting
        the information
    :return: The information in json format if good
             {valid: False} if not good

    :format return:
            { valid: able to view details,
              like_dislike_info: {
                  likes: int of likes,
                  dislikes: int of dislikes
                  user_like: is user liked it (True or False),
                  user_dislike: is user disliked it (True or False)
              }
              name: world name,
              description: world description,
              npcs:     [{ id: npc id,
                           name: npc name}],
              cities:   [{ id: city id,
                           name: city name}],
              specials: [{ id: special id,
                           name: special name}],
              comments:     [{ user: { user_id: user's id,
                                       user_name: user's name,
                                       profile_picture: user's profile picture},
                              comment: the comment,
                              time: the time stamp of the comment
                              likes: int of likes,
                              dislikes: int of dislikes
                            }]
              user_list:    [{ id: user id,
                               username: user's name,
                               profile_picture: user's profile picture}]
            }
    """
    access_check = check_viewable(world_id, user_id)['viewable']
    if access_check:
        if check_session_key(user_id, session_key) or access_check["public"]:
            conn = connect()
            cur = conn.cursor()
            world_info = {
                'valid': True,
                'like_dislike_info': get_likes_dislike(user_id, world_id, 'worlds'),
                'name': '',
                'description': '',
                'npcs': [],
                'cities': [],
                'specials': [],
                'comments': [],
                'user_list': []
            }
            world_info_request = """
                SELECT name, description FROM worlds
                WHERE id = %s
                """
            cur.execute(world_info_request, [world_id])
            outcome = cur.fetchall()

            conn.close()

            if outcome:

                world_info['name'] = outcome[0][0]
                world_info['description'] = outcome[0][1]

                new_info = get_new_elements(world_id, user_id, session_key)
                world_info['npcs'] = new_info['npcs']
                world_info['cities'] = new_info['cities']
                world_info['specials'] = new_info['specials']

                world_info['comments'] = get_component_comments(user_id, world_id, 'worlds')
                world_info['user_list'] = get_world_user_list(world_id, user_id, session_key)

                return world_info

    return {'valid': False,
            'like_dislike_info':
                {'likes': 0,
                 'dislikes': 0,
                 'user_like': False,
                 'user_dislike': False
                 },
            'name': '',
            'description': '',
            'npcs': [],
            'cities': [],
            'specials': [],
            'comments': [],
            'user_list': []
            }


def search_world(param, limit, page, user_id, session_key):
    """
    This function will search for worlds that have the
    searched string in them

    :param param: the string to search for
    :param limit: the number of results to show
    :param page: the selection of worlds to show
    :param user_id: the id of the world requesting
    :param session_key: the session key of the world requesting

    :return: the list of worlds and their elements that
        meet the search requirements in json format

    :format return: [{ id: world_id
                       name: world's name}]
    """
    world_list = []
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        if limit is None:
            limit = 25

        param = '%' + param + '%'

        request = """
            SELECT DISTINCT ON (worlds.id) worlds.id, worlds.name FROM world_user_linker
                INNER JOIN worlds on worlds.id = world_user_linker.world_id
            WHERE name ILIKE %s AND
                (worlds.public = 't' OR world_user_linker.user_id = %s)
            LIMIT %s OFFSET %s
                    """
        cur.execute(request, (param, user_id, limit, (page - 1) * limit))
        worlds_raw = cur.fetchall()
        for world in worlds_raw:
            world_list.append({'id': world[0],
                               'name': world[1]})

        conn.close()

    return world_list
