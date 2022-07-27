from src.utils.db_utils import connect


def rebuild_specials_table():
    """
    This function will empty the specials table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS specials CASCADE;
        """
    create_sql = """
        CREATE TABLE specials(
            id                  SERIAL PRIMARY KEY,
            name                TEXT NOT NULL,
            description         TEXT NOT NULL,
            hidden_description  TEXT DEFAULT NULL,
            revealed            BOOLEAN NOT NULL DEFAULT 'f',
            revealed_date       TIMESTAMP,
            world_id            INTEGER NOT NULL REFERENCES worlds
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()

