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

