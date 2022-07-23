from src.utils.db_utils import connect


def rebuild_city_npc_linker_table():
    """
    This function will empty the city npc linker table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS city_npc_linker CASCADE;
        """
    create_sql = """
        CREATE TABLE city_npc_linker(
            id              SERIAL PRIMARY KEY,
            city_id         INTEGER NOT NULL REFERENCES cities,
            npc_id          INTEGER NOT NULL REFERENCES npcs
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()
