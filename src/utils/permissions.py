from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect


def check_viewable(world_id, user_id):
    """
    This function will see if a user can view the
        information for a world
    :param world_id: the id of the world being checked
    :param user_id: the id of the user checking

    :return: True if viewable, False if not
    """
    conn = connect()
    cur = conn.cursor()

    world_info_request = """
        SELECT owner_id, public FROM worlds
        WHERE id = %s
        """
    values = cur.execute(world_info_request, [world_id])
    owner_id = values[0][0]
    public = values[0][1]
    # if user not the owner or the world is private
    if owner_id != user_id or not public:

        user_request = """
                    SELECT EXISTS(
                            SELECT 1 FROM world_user_linker
                            WHERE user_id = %s AND world_id = %s
                        )
                    """
        cur.execute(user_request, (user_id, world_id))
        # if user is not in the list of users
        if not cur.fetchall():
            admin_request = """
                            SELECT EXISTS(
                                SELECT 1 FROM admins
                                WHERE user_id = %s AND world_id = %s
                            )
                            """
            cur.execute(admin_request, (user_id, world_id))
            outcome = cur.fetchall()
            conn.close()
            # if user is an admin
            return outcome
        conn.close()
        return True
    # user is owner
    conn.close()
    return True


def check_editable(world_id, user_id, session_key):
    """
    This function will check if a user can edit a world
        i.e. they are an admin or owner
    :param world_id: the id of the world being checked
    :param user_id: the id of the user being checked
    :param session_key: the session key of the user being checked

    :return: true if editable, false if not
    """
    conn = connect()
    cur = conn.cursor()
    if check_session_key(user_id, session_key):
        owner_request = """
            SELECT EXISTS(
                SELECT 1 FROM worlds
                WHERE owner_id = %s AND id = %s
            )
            """
        cur.execute(owner_request, (user_id, world_id))
        # if user not the owner
        if not cur.fetchall():
            admin_request = """
                SELECT EXISTS(
                    SELECT 1 FROM admins
                    WHERE user_id = %s AND world_id = %s
                )
                """
            cur.execute(admin_request, (user_id, world_id))
            # if user is admin
            outcome = cur.fetchall()
            conn.close()
            return outcome
        # user is owner
        conn.close()
        return True

    conn.close()
    return False
