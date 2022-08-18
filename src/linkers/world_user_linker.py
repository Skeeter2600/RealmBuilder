from src.utils.db_utils import connect


def rebuild_world_user_linker():
    """
    This function will empty the world user linker
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
            DROP TABLE if EXISTS world_user_linker CASCADE;
            """
    create_sql = """
            CREATE TABLE world_user_linker(
                id              SERIAL PRIMARY KEY,
                world_id        INTEGER NOT NULL REFERENCES worlds ON DELETE CASCADE,
                user_id         INTEGER NOT NULL REFERENCES users ON DELETE CASCADE,
                last_checked    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()