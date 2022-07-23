from src.utils.db_utils import connect


def rebuild_admins_table():
    """
    This function will empty the admins table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS admins CASCADE;
        """
    create_sql = """
        CREATE TABLE admins(
            id              SERIAL PRIMARY KEY,
            world_id        INTEGER NOT NULL REFERENCES worlds,
            user_id         INTEGER NOT NULL REFERENCES users
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()

