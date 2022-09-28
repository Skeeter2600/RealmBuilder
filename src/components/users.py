import hashlib
import secrets

from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect


def rebuild_users_table():
    """
    This function will empty the users table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS users CASCADE;
        """
    create_sql = """
        CREATE TABLE users(
            id              SERIAL PRIMARY KEY,
            username        TEXT NOT NULL,
            password        TEXT NOT NULL,
            profile_pic     bytea DEFAULT NULL,
            public          BOOLEAN DEFAULT FALSE,
            bio             TEXT,
            email           TEXT NOT NULL,
            session_key     TEXT
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def create_user(username, password, email):
    """
    This function will create a new user
    :param username: The new user's username
    :param password: The new user's password
    :param email: the new user's email
    :return: a message based on the status
    """
    conn = connect()
    cur = conn.cursor()

    username_check = """
        SELECT COUNT(*) FROM users
        WHERE username = %s
        """
    cur.execute(username_check, [username])
    outcome = cur.fetchall()

    if outcome[0][0] > 0:
        conn.close()
        return "A user with that username already exists"

    encrypted = hashlib.sha512(password.encode()).hexdigest()

    add_user = """
        INSERT INTO users(username, password, email) VALUES
        (%s, %s, %s)
        RETURNING id
        """
    cur.execute(add_user, (username, encrypted, email))
    outcome = cur.fetchall()

    if outcome == ():
        conn.close()
        return "An error occurred, try again"

    conn.commit()
    conn.close()
    return "Success!"


def delete_user(user_id, session_key):
    """
    This function will delete a user and for each
    world they own, will try to move ownership to an
    admin
    :param user_id: the id of the user deleting
    :param session_key: the user's session key
    :return: True if successful, False if failure
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        worlds_check = """
            SELECT id FROM worlds
            WHERE owner_id = %s
            """

        cur.execute(worlds_check, [user_id])
        worlds = cur.fetchall()
        if worlds != ():
            for world in worlds:
                admin_check = """
                    SELECT user_id FROM admins
                    WHERE world_id = %s
                    """
                cur.execute(admin_check, [world])
                users = cur.fetchall()
                if len(users) > 0:
                    update_world = """
                        UPDATE worlds SET
                        owner_id = %s
                        WHERE id = %s
                        """
                    cur.execute(update_world, (user_id, world))
                    delete_admin_link = """
                        DELETE FROM admins
                        WHERE user_id = %s AND world_id = %s
                        """
                    cur.execute(delete_admin_link, (user_id, world))

            delete_user = """
                DELETE FROM users
                WHERE id = %s
                RETURNING id
                """
            cur.execute(delete_user, [user_id])
            outcome = cur.fetchall()
            conn.commit()
            conn.close()

            if outcome != ():
                return True

    return False


def edit_account(user_id, session_key, details):
    """
    This function will edit a user's information
    given they are the user requesting it

    :param user_id: the user's id
    :param session_key: the user's session key
    :param details: the information to change

    :format details: { username: new username,
                       profile_pic: new profile picture,
                       public: True or False,
                       bio: new bio
                     }

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        edit_query = """
            UPDATE users SET
            username = %s, profile_pic = %s, public = %s, bio = %s
            WHERE id = %s
            RETURNING id
            """

        cur.execute(edit_query, (details['username'], details['profile_pic'], details['public'], details['bio'], user_id))
        outcome = cur.fetchall()

        if outcome != ():
            conn.commit()
            conn.close()

            return True

        conn.close()
    return False


def get_user_public(user_id):
    """
    This function will get public the info on a user
    :param user_id: the user's id
    :return: the user's info in json format

    :format return: { username: user's username,
                      profile_pic: user's profile picture,
                      bio: the user's bio,
                      worlds: [{id: world id,
                                name: world name} (note: only public ones)]
                    }
    """
    info = {'username': '',
            'profile_pic': '',
            'bio': '',
            'worlds': []}
    conn = connect()
    cur = conn.cursor()

    info_query = """
        SELECT username, profile_pic, bio FROM users 
        WHERE id = %s
        """
    cur.execute(info_query, [user_id])
    values = cur.fetchall()
    if len(values) > 0:
        values = values[0]
        info['username'] = values[0]
        info['profile_pic'] = values[1]
        info['bio'] = values[2]

        worlds_selection = """
            SELECT world_id, name FROM world_user_linker
            INNER JOIN worlds ON world_user_linker.world_id = worlds.id
            WHERE user_id = %s
            """
        cur.execute(worlds_selection, [user_id])
        worlds = cur.fetchall()

        for world in worlds:
            info['worlds'].append({'id': world[0],
                                   'name': world[1]})

    conn.close()
    return info


def login_user(username, password):
    """
    This will log a user in and get them the session
    key for their current session
    :param username: the user's username
    :param password: the user's password
    :return: the session key of successful, error string if not
    """
    conn = connect()
    cur = conn.cursor()

    encrypted = hashlib.sha512(password.encode()).hexdigest()

    request = """
        SELECT session_key FROM users
        WHERE users.username = %s and users.password = %s
        """
    cur.execute(request, (username, encrypted))
    outcome = cur.fetchall()

    if not outcome:
        conn.close()
        return "Bad username or password"

    if outcome[0] == (None,):
        session_key = secrets.token_hex(16)
        session_key_request = """
            UPDATE users
            SET session_key = %s
            WHERE users.username = %s and users.password = %s
            """
        cur.execute(session_key_request, (session_key, username, encrypted))

        conn.commit()
        conn.close()
        return session_key


def logout_user(user_id, session_key):
    """
    This function will log a user out and wipe
    their session key from the database

    :param user_id: the user's id
    :param session_key: the user's current session_key

    :return: "signed out" if signed out, "bad request" otherwise
    """
    valid = check_session_key(user_id, session_key)

    if valid:
        conn = connect()
        cur = conn.cursor()
        request = """
            UPDATE users
            SET session_key = ''
            WHERE users.id = %s
            """
        cur.execute(request, [user_id])

        conn.commit()
        conn.close()

        return "signed out"
    return "bad request"


def search_user(param, limit, page, user_id, session_key):
    """
    This function will search for users that have the
    searched string in them

    :param param: the string to search for
    :param limit: the number of results to show
    :param page: the selection of users to show
    :param user_id: the id of the user requesting
    :param session_key: the session key of the user requesting

    :return: the list of users and their elements that
        meet the search requirements in json format

    :format return: [{ id: user_id
                       username: user's username}]
    """
    user_list = []
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        if limit is None:
            limit = 25

        param = '%' + param + '%'

        request = """
            SELECT id, username FROM users
            WHERE username ILIKE %s AND
                users.public = 't' AND users.id != %s
             LIMIT %s OFFSET %s
                    """
        cur.execute(request, (param, limit, user_id, (page - 1) * limit))
        users_raw = cur.fetchall()
        for user in users_raw:
            user_list.append({'id': user[0],
                             'username': user[1]})

        conn.close()

    return user_list
