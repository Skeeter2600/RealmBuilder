from src.utils.db_utils import connect


def rebuild_special_image_linker():
    """
    This function will empty the special image linker table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS special_image_linker CASCADE;
        """
    create_sql = """
        CREATE TABLE special_image_linker(
            id              SERIAL PRIMARY KEY,
            special_id      INTEGER NOT NULL REFERENCES specials,
            image           bytea NOT NULL
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()
