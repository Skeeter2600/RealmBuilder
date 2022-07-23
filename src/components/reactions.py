from src.utils.db_utils import connect


def rebuild_reactions_table():
    """
    This function will empty the reactions table.
    Type will be an emoji of some sort.
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS reactions CASCADE;
        """
    create_sql = """
        CREATE TABLE reactions(
            id                  SERIAL PRIMARY KEY,
            user_id             TEXT NOT NULL,
            type                TEXT NOT NULL,
            component_id        INTEGER NOT NULL,
            component_type      TEXT NOT NULL
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()
