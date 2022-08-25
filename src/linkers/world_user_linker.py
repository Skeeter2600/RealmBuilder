from src.utils.db_utils import connect

"""
NOTES FROM A TIRED BECK:

The logic behind checking for new elements is as follows:
    1) When a user opens a world, the last_checked is looked at.
    2) IF the difference between the current time and last_checked is greater
            than 15 minutes:
        2a) new_check = last_checked
        2b) last_checked = current_time
    3) when looking for the new elements, compare to the new_check
            * ie get elements that have a newer edit_date than new_check
"""


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
                last_checked    TIMESTAMP DEFAULT CURRENT_DATE,
                new_check       TIMESTAMP DEFAULT CURRENT_DATE
            )
            """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()
