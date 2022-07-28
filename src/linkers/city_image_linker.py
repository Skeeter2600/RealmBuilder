from src.utils.db_utils import connect


def rebuild_city_image_linker():
    """
    This function will empty the city image linker table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS city_image_linker CASCADE;
        """
    create_sql = """
        CREATE TABLE city_image_linker(
            id              SERIAL PRIMARY KEY,
            city_id         INTEGER NOT NULL REFERENCES citys,
            image           bytea NOT NULL
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()
