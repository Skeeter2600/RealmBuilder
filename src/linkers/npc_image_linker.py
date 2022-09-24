from src.utils.db_tools import check_session_key
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
            npc_id          INTEGER NOT NULL REFERENCES npcs ON DELETE CASCADE,
            image           bytea NOT NULL
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()
    
    
def add_npc_image_association(npc_id, image, user_id, session_key):
    """
    This function will add an association between
    a npc and an image to the linker table

    :param image: the image file
    :param npc_id: the id of the npc
    :param user_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()
        insert_request = """
            INSERT INTO npc_image_linker(npc_id, image) VALUES
            (%s, %s)
            """
        cur.execute(insert_request, (npc_id, image))
        outcome = cur.fetchall()

        conn.commit()
        conn.close()

        if outcome != ():
            return True
    return False


def remove_npc_image_association(npc_id, image, user_id, session_key):
    """
    This function will remove an association between
    a npc and an image from the linker table

    :param image: the image file
    :param npc_id: the id of the npc
    :param user_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()
        delete_request = """
            DELETE FROM npc_image_linker WHERE
            npc_id = %s AND image = %s
            """
        cur.execute(delete_request, (npc_id, image))
        conn.commit()
        conn.close()
        return True
    return False


def get_associated_npc_images(npc_id):
    """
    This function will get all of the images associated
    with an npc

    :param npc_id: the id of the npc

    :return: a list of the image files
    """
    conn = connect()
    cur = conn.cursor()
    get_request = """
        SELECT image FROM npc_image_linker
        WHERE npc_id = %s
        """
    cur.execute(get_request, [npc_id])
    outcome = cur.fetchall()
    conn.close()

    return outcome
