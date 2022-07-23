from src.utils.db_utils import connect


def rebuild_worlds_table():
    """
    This function will empty the users table
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
            owner_id        INTEGER NOT NULL REFERENCES users
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()
