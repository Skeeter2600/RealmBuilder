from src.utils.db_utils import connect


def rebuild_comments_table():
    """
    This function will empty the comments table.
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS comments CASCADE;
        """
    create_sql = """
        CREATE TABLE comments(
            id                  SERIAL PRIMARY KEY,
            user_id             TEXT NOT NULL,
            comment             TEXT NOT NULL,
            time                TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            likes               INTEGER DEFAULT 0,
            dislikes            INTEGER DEFAULT 0,
            component_id        INTEGER NOT NULL,
            component_type      TEXT NOT NULL
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def get_component_comments(comp_id, comp_type):
    """
    This function will get the comments associated with
    a component and the reactions associated to them
    :return: list of comments and their reactions
        ([[comment, [reactions]], [comment, [reactions]]])
    """
    conn = connect()
    cur = conn.cursor()

    request = """
        SELECT * FROM comments
            INNER JOIN %s""" + 's' + """ AS %s
        WHERE %s.component_id = %s
        """

    cur.execute(request, (comp_type, comp_type, comp_type, comp_id))
    outcome = cur.fetchall()
    conn.close()

    return outcome


def get_user_comments(user_id, limit, page):
    """
    This function will get the comments made by a
    user with a page limit and selection

    :param user_id: the id of the user being checked
    :param limit: the amount of comments to return
        (if none, default 25)
    :param page: the offset of the comment page
    """

    conn = connect()
    cur = conn.cursor()

    if limit is None:
        limit = 25

    request = """
        SELECT * FROM comments
        WHERE user_id = %
        LIMIT %s OFFSET %s
        """
    cur.execute(request, (user_id, limit, (page - 1) * limit))
    outcome = cur.fetchall()

    conn.close()

    return outcome
