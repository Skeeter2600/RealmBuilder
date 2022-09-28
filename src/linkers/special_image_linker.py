from src.utils.db_tools import check_session_key
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
            special_id      INTEGER NOT NULL REFERENCES specials ON DELETE CASCADE,
            image           bytea NOT NULL
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()
    
    
def add_special_image_association(special_id, image, user_id, session_key):
    """
    This function will add an association between
    a special and an image to the linker table

    :param image: the image file
    :param special_id: the id of the special
    :param user_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()
        insert_request = """
            INSERT INTO special_image_linker(special_id, image) VALUES
            (%s, %s)
            RETURNING id
            """
        cur.execute(insert_request, (special_id, image))
        outcome = cur.fetchall()

        conn.commit()
        conn.close()

        if outcome != ():
            return True
    return False


def remove_special_image_association(special_id, image, user_id, session_key):
    """
    This function will remove an association between
    a special and an image from the linker table

    :param image: the image file
    :param special_id: the id of the special
    :param user_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()
        delete_request = """
            DELETE FROM special_image_linker WHERE
            special_id = %s AND image = %s
            """
        cur.execute(delete_request, (special_id, image))
        conn.commit()
        conn.close()
        return True
    return False


def get_associated_special_images(special_id):
    """
    This function will get all of the images associated
    with an special

    :param special_id: the id of the special

    :return: a list of the image files
    """
    conn = connect()
    cur = conn.cursor()
    get_request = """
        SELECT image FROM special_image_linker
        WHERE special_id = %s
        """
    cur.execute(get_request, [special_id])
    outcome = cur.fetchall()
    conn.close()

    return outcome
