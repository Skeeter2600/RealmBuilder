from src.utils.db_utils import connect


def rebuild_city_special_linker():
    """
    This function will empty the city special linker table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS city_special_linker CASCADE;
        """
    create_sql = """
        CREATE TABLE city_special_linker(
            id              SERIAL PRIMARY KEY,
            city_id         INTEGER NOT NULL REFERENCES citys ON DELETE CASCADE,
            special_id      INTEGER NOT NULL REFERENCES specials ON DELETE CASCADE
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()
