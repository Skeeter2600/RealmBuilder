from src.utils.db_utils import connect


def rebuild_citys_table():
    """
    This function will empty the citys table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS citys CASCADE;
        """
    create_sql = """
        CREATE TABLE citys(
            id              SERIAL PRIMARY KEY,
            name            TEXT NOT NULL,
            population      INTEGER NOT NULL,
            song            TEXT,
            trades          TEXT,
            aesthetic       TEXT,
            description     TEXT NOT NULL,
            revealed        BOOLEAN NOT NULL DEFAULT 'f',
            revealed_date   TIMESTAMP DEFAULT NULL,
            world_id        INTEGER NOT NULL REFERENCES worlds
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()

