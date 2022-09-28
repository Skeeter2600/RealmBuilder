from datetime import datetime, timedelta

from src.utils.db_tools import check_session_key
from src.utils.permissions import check_viewable
from src.utils.db_utils import connect

"""
NOTES FROM A TIRED BECK:

The logic behind checking for new elements is as follows:
    1) When a user opens a world, the last_checked is looked at.
    2) If the difference between the current time and last_checked is greater
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


def add_world_user_association(world_id, user_id, requester_id, session_key):
    """
    This function will add an association between
    a world and a user to the linker table

    :param world_id: the id of the city
    :param user_id: the id of the user being linked
    :param requester_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(requester_id, session_key):
        conn = connect()
        cur = conn.cursor()
        insert_request = """
            INSERT INTO world_user_linker(world_id, user_id) VALUES
            (%s, %s)
            RETURNING id
            """
        cur.execute(insert_request, (world_id, user_id))
        outcome = cur.fetchall()

        conn.commit()
        conn.close()

        if outcome != ():
            return True
    return False


def delete_world_user_association(world_id, user_id, requester_id, session_key):
    """
    This function will add an association between
    a world and a user to the linker table

    :param world_id: the id of the city
    :param user_id: the id of the user being linked
    :param requester_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(requester_id, session_key):
        conn = connect()
        cur = conn.cursor()
        delete_request = """
            DELETE FROM world_user_linker WHERE
            world_id = %s AND user_id = %s
            """
        cur.execute(delete_request, (world_id, user_id))
        conn.commit()
        conn.close()
        return True
    return False


def get_new_elements(world_id, user_id, session_key):
    """
    This function will get a list of each type of new
    elements for a user in a world
    :param user_id: the id of the user being checked
    :param world_id: the id of the world being checked
    :param session_key: the session key of the user checking

    :return: a dictionary with a list of each element in each slot

    :format return:
            { npcs:     [{ id: npc id,
                           name: npc name}],
              cities:   [{ id: city id,
                           name: city name}],
              specials: [{ id: special id,
                           name: special name}]
            }
    """
    if check_session_key(user_id, session_key):
        if check_viewable(world_id, user_id):
            conn = connect()
            cur = conn.cursor()

            time_requests = """
                SELECT last_checked, new_check, id FROM world_user_linker
                WHERE world_id = %s AND user_id = %s
                """

            cur.execute(time_requests, (world_id, user_id))
            outcome = cur.fetchall()
            if outcome:
                outcome = outcome[0]
                last_checked = outcome[0]
                new_check = outcome[1]

                # update times if last checked is older than 15 min
                if last_checked > datetime.now() - timedelta(minutes=15):
                    new_check = last_checked
                    last_checked = datetime.now()
            else:
                new_check = datetime.now()
                last_checked = datetime.now()

            elements = {'npcs': [],
                        'cities': [],
                        'specials': []}

            npc_query = """
                SELECT id, name FROM npcs
                WHERE edit_date > %s AND world_id = %s
                """
            cur.execute(npc_query, (last_checked, world_id))
            elements['npcs'] = cur.fetchall()

            cities_query = """
                SELECT id, name FROM cities
                WHERE edit_date > %s AND world_id = %s
                """
            cur.execute(cities_query, (last_checked, world_id))
            elements['cities'] = cur.fetchall()

            specials_query = """
                SELECT id, name FROM npcs
                WHERE edit_date > %s AND world_id = %s
                """
            cur.execute(specials_query, (last_checked, world_id))
            elements['specials'] = cur.fetchall()

            update_query = """
                UPDATE world_user_linker
                SET last_checked = %s, new_check = %s
                WHERE world_id = %s AND user_id = %s
                """
            cur.execute(update_query, (last_checked.strftime('%Y-%m-%d %H:%M:%S'),
                                       new_check.strftime('%Y-%m-%d %H:%M:%S'), world_id, user_id))
            conn.commit()
            conn.close()

            return elements
