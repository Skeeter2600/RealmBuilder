from src.components.worlds import get_owner
from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect


def rebuild_admins_table():
    """
    This function will empty the admins table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS admins CASCADE;
        """
    create_sql = """
        CREATE TABLE admins(
            id              SERIAL PRIMARY KEY,
            world_id        INTEGER NOT NULL REFERENCES worlds ON DELETE CASCADE,
            user_id         INTEGER NOT NULL REFERENCES users
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def add_world_user_association(world_id, user_id, requester_id, session_key):
    """
    This function will add an association between
    a world and a user to the linker table

    :param world_id: the id of the city
    :param user_id: the id of the user being linked
    :param requester_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(requester_id, session_key) & get_owner(world_id)["id"] == requester_id:
        conn = connect()
        cur = conn.cursor()
        insert_request = """
            INSERT INTO admins(world_id, user_id) VALUES
            (%s, %s)
            RETURNING id
            """
        cur.execute(insert_request, (world_id, user_id))
        outcome = cur.fetchall()
        conn.commit()
        conn.close()

        if outcome != ():
            return True
    return False


def delete_world_user_association(world_id, user_id, requester_id, session_key):
    """
    This function will add an association between
    a world and a user to the linker table

    :param world_id: the id of the city
    :param user_id: the id of the user being linked
    :param requester_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(requester_id, session_key):
        conn = connect()
        cur = conn.cursor()
        delete_request = """
            DELETE FROM world_user_linker WHERE
            world_id = %s AND user_id = %s
            """
        cur.execute(delete_request, (world_id, user_id))
        conn.commit()
        conn.close()
        return True
    return False
