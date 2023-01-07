from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect


def rebuild_likes_dislikes_table():
    """
    This function will empty the likes_dislikes_table table.
    Like is represented by a true value for the like_dislike
    Dislike is represented by a false value for the like_dislike
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS likes_dislikes CASCADE;
        """
    create_sql = """
        CREATE TABLE likes_dislikes(
            id                  SERIAL PRIMARY KEY,
            user_id             INTEGER NOT NULL,
            like_dislike        BOOLEAN NOT NULL,
            time                TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            component_id        INTEGER NOT NULL,
            component_type      TEXT NOT NULL
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def add_like_dislike(user_id, session_key, like_dislike, component_id, component_type):
    """
    This function will add a new like or dislike to the table.

    :param user_id: the id of the user liking or disliking
    :param session_key: the user's session key
    :param like_dislike: if it is a like or dislike
                         (True for like, False for dislike)
    :param component_id: the id of the component being liked
    :param component_type: the type of component being liked
    """

    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        request = """
            INSERT INTO likes_dislikes(user_id, like_dislike, component_id, component_type) VALUES
            (%s, %s, %s, %s)
            returning id
            """
        cur.execute(request, (user_id, like_dislike, component_id, component_type))
        outcome = cur.fetchall()
        if outcome != ():
            conn.commit()
            conn.close()
            return [True, outcome[0][0]]
    return [False, -1]


def remove_like_dislike(user_id, session_key, component_id, component_type):
    """
    This function will remove a new like or dislike to the table.

    :param user_id: the id of the user liking or disliking
    :param session_key: the user's session key
    :param component_id: the id of the component being liked
    :param component_type: the type of component being liked
    """

    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        request = """
            SELECT id FROM likes_dislikes
            WHERE user = %s AND component_id = %s AND component_type = %s
            """
        cur.execute(request, (user_id, component_id, component_type))
        outcome = cur.fetchall()
        if outcome != ():
            delete_request = """
                DELETE FROM likes_dislikes
                WHERE id = %s
                returning id
            """
            cur.execute(delete_request, [outcome[0][0]])
            conn.commit()
            conn.close()

            if outcome != ():
                return True
    return False
