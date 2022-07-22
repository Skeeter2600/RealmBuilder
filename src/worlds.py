from src.db_utils import connect


def build_worlds():
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE IF EXISTS example_table
    """
    add_sql = """
            CREATE TABLE example_table(
            example_col VARCHAR(40))
            """
    cur.execute(drop_sql)
    cur.execute(add_sql)
    conn.commit()
    conn.close()
