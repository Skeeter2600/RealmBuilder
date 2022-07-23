from src.utils.db_utils import connect


def rebuild_world_user_linker_table():
    """
    This function will empty the world user linker table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS world_user_linker CASCADE;
        """
    create_sql = """
        CREATE TABLE world_user_linker(
            id              SERIAL PRIMARY KEY,
            world_id        INTEGER NOT NULL REFERENCES worlds,
            user_id         INTEGER NOT NULL REFERENCES users
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()

