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
            component_id        INTEGER NOT NULL,
            component_type      TEXT NOT NULL
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()
