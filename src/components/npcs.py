from src.utils.db_utils import connect


def rebuild_npcs_table():
    """
    This function will empty the npcs table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS npcs CASCADE;
        """
    create_sql = """
        CREATE TABLE npcs(
            id                  SERIAL PRIMARY KEY,
            name                TEXT NOT NULL,
            age                 INTEGER,
            occupation          TEXT,
            description         TEXT NOT NULL,
            hidden_description  TEXT,
            revealed            BOOLEAN NOT NULL DEFAULT 'f',
            revealed_date       TIMESTAMP,
            world_id            INTEGER NOT NULL REFERENCES worlds
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()

