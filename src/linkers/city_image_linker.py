import os
import shutil

from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect
from src.utils.permissions import check_editable


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
            image           TEXT NOT NULL
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

        world_id_check = """
            SELECT world_id FROM cities
            WHERE id = %s
            """
        cur.execute(world_id_check, [city_id])
        world_id = cur.fetchall()[0][0]

        if check_editable(world_id, user_id, session_key):
            insert_request = """
                INSERT INTO city_image_linker(city_id, %s) VALUES
                (%s, %s)
                RETURNING id
                """
            cur.execute(insert_request, ('temp', city_id, image))
            outcome = cur.fetchall()
            conn.commit()

            if outcome != ():
                image_link_id = outcome[0][0]
                update_request = """
                    UPDATE city_image_linker SET
                    image = %s
                    WHERE id = %s
                    """
                cur.execute(update_request, (os.getcwd() + '/images/city/' + image_link_id, image_link_id))
                outcome = cur.fetchall()
                conn.commit()

                if outcome != ():
                    shutil.copy(image, os.getcwd() + '/images/city/' + outcome[0][0])
                    conn.close()
                    return True

        conn.close()
    return False


def remove_city_image_association(city_id, image_id, user_id, session_key):
    """
    This function will remove an association between
    a city and an image from the linker table

    :param image_id: the image file
    :param city_id: the id of the city
    :param user_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        world_id_check = """
                    SELECT world_id FROM cities
                    WHERE id = %s
                    """
        cur.execute(world_id_check, [city_id])
        world_id = cur.fetchall()[0][0]

        if check_editable(world_id, user_id, session_key):
            delete_request = """
                DELETE FROM city_image_linker WHERE
                city_id = %s AND id = %s
                """
            cur.execute(delete_request, (city_id, image_id))
            conn.commit()
            conn.close()
            return True

        conn.close()
    return False


def get_associated_city_images(city_id):
    """
    This function will get all the images associated
    with a city

    :param city_id: the id of the city

    :return: a list of the image addresses
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
