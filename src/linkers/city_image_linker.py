from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect


def rebuild_city_image_linker():
    """
    This function will empty the city image linker table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS city_image_linker CASCADE;
        """
    create_sql = """
        CREATE TABLE city_image_linker(
            id              SERIAL PRIMARY KEY,
            city_id         INTEGER NOT NULL REFERENCES cities ON DELETE CASCADE,
            image           bytea NOT NULL
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def add_city_image_association(city_id, image, user_id, session_key):
    """
    This function will add an association between
    a city and an image to the linker table

    :param image: the image file
    :param city_id: the id of the city
    :param user_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()
        insert_request = """
            INSERT INTO city_image_linker(city_id, image) VALUES
            (%s, %s)
            """
        cur.execute(insert_request, (city_id, image))
        conn.commit()
        conn.close()
        return True
    return False


def remove_city_image_association(city_id, image, user_id, session_key):
    """
    This function will remove an association between
    a city and an image from the linker table

    :param image: the image file
    :param city_id: the id of the city
    :param user_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()
        delete_request = """
            DELETE FROM city_image_linker WHERE
            city_id = %s AND image = %s
            """
        cur.execute(delete_request, (city_id, image))
        conn.commit()
        conn.close()
        return True
    return False


def get_associated_city_images(city_id):
    """
    This function will get all of the images associated
    with an city

    :param city_id: the id of the city

    :return: a list of the image files
    """
    conn = connect()
    cur = conn.cursor()
    get_request = """
        SELECT image FROM city_image_linker
        WHERE city_id = %s
        """
    cur.execute(get_request, [city_id])
    outcome = cur.fetchall()
    conn.close()

    return outcome
