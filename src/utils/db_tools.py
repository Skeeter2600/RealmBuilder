from src.utils.db_utils import connect


def check_session_key(user_id, session_key):
    """
    This function will check if the user's session
    key is valid

    :param user_id: the id of the user
    :param session_key: the session key they are checking

    :return: true if valid, false if not
    """
    if not session_key or session_key == "":
        return False

    conn = connect()
    cur = conn.cursor()

    request = """
        SELECT session_key FROM users
        WHERE users.id = %s
        """
    cur.execute(request, [user_id])
    outcome = cur.fetchall()[0][0]
    return outcome == session_key

