from src.utils.db_utils import connect


def rebuild_npc_image_linker():
    """
    This function will empty the npc image linker table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS npc_image_linker CASCADE;
        """
    create_sql = """
        CREATE TABLE npc_image_linker(
            id              SERIAL PRIMARY KEY,
            npc_id          INTEGER NOT NULL REFERENCES npcs,
            image           bytea NOT NULL
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()
