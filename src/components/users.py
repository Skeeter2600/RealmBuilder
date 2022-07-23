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
            session_key     TEXT,
            email           TEXT NOT NULL
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()
