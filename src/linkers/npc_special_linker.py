from src.utils.db_utils import connect


def rebuild_npc_special_linker_table():
    """
    This function will empty the npc special linker table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS npc_special_linker CASCADE;
        """
    create_sql = """
        CREATE TABLE npc_special_linker(
            id              SERIAL PRIMARY KEY,
            npc_id         INTEGER NOT NULL REFERENCES npcs,
            special_id     INTEGER NOT NULL REFERENCES specials
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()
