from src.components.comments import get_component_comments
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
            description     TEXT,
            owner_id        INTEGER NOT NULL REFERENCES users,
            public          BOOLEAN NOT NULL DEFAULT 'f'
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def add_world(name, owner_id):
    """
    This function will add a world to the database
    :param name: The name of the world
    :param owner_id: the id of the user who made the world

    :return: the id of the new world if successful, False if not
    """
    conn = connect()
    cur = conn.cursor()

    request = """
                INSERT INTO worlds(name, owner_id) VALUES
                (%s, %s)
                RETURNING id
                """
    cur.execute(request, (name, owner_id))
    outcome = cur.fetchall()
    conn.commit()
    conn.close()
    if outcome != ():
        return outcome[0][0]
    return False


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
            return True
    return False


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
        return True
    return False


def join_world(world_id, user_id, session_key):
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
                WHERE id = %s
            )
            """
        cur.execute(world_check_query)
        outcome = cur.fetchall()

        if outcome:
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
                return True
    return False


def get_owner(world_id):
    """
    This will get the info on the owner of the world

    :param world_id: the id of the world being checked

    :return: the info on the owner
    :format return:
            {  id:   user id,
               name: user's name,
               profile_picture: user's profile picture
            }
    """
    conn = connect()
    cur = conn.cursor()
    owner_request = """
                SELECT users.id, users.name, users.profile_pic FROM worlds
                    INNER JOIN users ON users.id = worlds.owner_id = users.id
                WHERE worlds.id = %s
                """
    cur.execute(owner_request, [world_id])
    outcome = cur.fetchall()
    conn.close()

    info = {
        "id": outcome[0][0],
        "name": outcome[0][1],
        "profile_picture": outcome[0][2]
    }

    return info


def get_world_user_list(world_id):
    """
    This function will get a list of all users who
    are a part of a world
    :param world_id: the id of the world being checked

    :return: a list of the users in a world

    :format return:
            [{  id:   user id,
                name: user's name,
                profile_picture: user's profile picture
            }]
    """
    conn = connect()
    cur = conn.cursor()

    user_list = []

    # add the owner to the list
    owner_request = """
            SELECT users.id, users.name, users.profile_pic FROM worlds
                INNER JOIN users ON users.id = worlds.owner_id = users.id
            WHERE worlds.id = %s
            """
    cur.execute(owner_request, [world_id])
    outcome = cur.fetchall()
    user_list.append(outcome[0])

    # add the admins to the list
    admin_request = """
            SELECT users.id, users.name, users.profile_pic FROM admins
                INNER JOIN users ON users.id = admins.user_id = users.id
            WHERE world_id = %s
            """
    cur.execute(admin_request, [world_id])
    outcome = cur.fetchall()
    for admin in outcome:
        user_list.append(admin)

    # add the members to the list
    member_request = """
        SELECT users.id, users.name, users.profile_pic FROM world_user_linker
            INNER JOIN users ON users.id = world_user_linker.user_id = users.id
        WHERE world_id = %s
        """
    cur.execute(member_request, [world_id])
    outcome = cur.fetchall()
    for user in outcome:
        user_list.append(user)

    conn.close()
    return user_list


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
              name: world name,
              description: world description,
              new_npcs:     [{ id: npc id,
                               name: npc name}],
              new_cities:   [{ id: city id,
                               name: city name}],
              new_specials: [{ id: special id,
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
                               name: user's name,
                               profile_picture: user's profile picture}]
            }
    """
    if check_session_key(user_id, session_key):
        if check_viewable(world_id, user_id):
            conn = connect()
            cur = conn.cursor()
            world_info = {
                'valid': True,
                'name': '',
                'description': '',
                'new_npcs': [],
                'new_cities': [],
                'new_specials': [],
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

            world_info['name'] = outcome[0][0]
            world_info['description'] = outcome[0][1]

            new_info = get_new_elements(world_id, user_id, session_key)
            world_info['new_npcs'] = new_info['npcs']
            world_info['new_cities'] = new_info['cities']
            world_info['new_specials'] = new_info['specials']

            world_info['comments'] = get_component_comments(world_id, 'worlds')
            world_info['user_list'] = get_world_user_list(world_id)

            return world_info

    else:
        return {'valid': False,
                'name': '',
                'description': '',
                'new_npcs': [],
                'new_cities': [],
                'new_specials': [],
                'comments': [],
                'user_list': []
                }
