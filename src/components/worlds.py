from src.components.users import check_session_key
from src.utils.db_utils import connect


def rebuild_worlds_table():
    """
    This function will empty the worlds table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS worlds CASCADE;
        """
    create_sql = """
        CREATE TABLE worlds(
            id              SERIAL PRIMARY KEY,
            name            TEXT NOT NULL,
            description     TEXT,
            owner_id        INTEGER NOT NULL REFERENCES users,
            public          BOOLEAN NOT NULL DEFAULT 'f'
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def add_world(name, description, owner_id):
    """
    This function will add a world to the database
    :param name: The name of the world
    :param description: The world's description
    :param owner_id: the id of the user who made the world
    """
    conn = connect()
    cur = conn.cursor()

    if description != '':

        request = """
            INSERT INTO worlds(name, descripton, owner_id) VALUE
            (%s, %s, %s)
            """
        cur.execute(request, (name, description, owner_id))

    else:
        request = """
                    INSERT INTO worlds(name, owner_id) VALUE
                    (%s, %s)
                    """
        cur.execute(request, (name, owner_id))

    conn.commit()
    conn.close()


def delete_world(world_id, owner_id, session_key):
    """
    This function will delete a world and all of
    the components associated with it
    :param world_id: the id of the world to delete
    :param owner_id: the id of the owner of the world
    :param session_key: the supposed session key of the user
    """

    if check_session_key(owner_id, session_key):
        conn = connect()
        cur = conn.cursor()

        delete_request = """
            DELETE FROM worlds
            WHERE world_id = %
            """
        cur.execute(delete_request, [world_id])

        conn.commit()
        conn.close()


def get_world_details(world_id):
    """
    This function will get the description of the
    selected world
    :param world_id: the id of the wanted world
    """
    conn = connect()
    cur = conn.cursor()

    request = """
        SELECT name, description, username FROM worlds
            INNER JOIN users ON worlds.owner_id = users.id
        WHERE worlds.id = %s
        """

    cur.execute(request, [world_id])
    outcome = cur.fetchall()
    conn.close()

    return outcome

