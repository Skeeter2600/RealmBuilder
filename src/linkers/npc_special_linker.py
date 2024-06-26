from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect
from src.utils.permissions import check_editable, check_viewable


def rebuild_npc_special_linker():
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
            npc_id         INTEGER NOT NULL REFERENCES npcs ON DELETE CASCADE,
            special_id     INTEGER NOT NULL REFERENCES specials ON DELETE CASCADE
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def check_same_world(npc_id, special_id):
    """
    This function will check if two elements are in
    the same world, which would allow a link

    :param npc_id: the id of the npc
    :param special_id: the id of the special

    :return: -1 if no link, the world id if they do
    """
    conn = connect()
    cur = conn.cursor()

    world_id_check = """
                    SELECT world_id FROM specials
                    WHERE id = %s
                """
    cur.execute(world_id_check, [special_id])
    special_world_id = cur.fetchall()[0][0]

    world_id_check = """
               SELECT world_id FROM npcs
               WHERE id = %s
            """
    cur.execute(world_id_check, [npc_id])
    npc_world_id = cur.fetchall()[0][0]
    conn.close()

    if npc_world_id == special_world_id:
        return npc_world_id

    return -1


def add_npc_special_association(npc_id, special_id, user_id, session_key):
    """
    This function will add an association between
    a npc and an special to the linker table

    :param special_id: the id of the special
    :param npc_id: the id of the npc
    :param user_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        world_id = check_same_world(npc_id, special_id)

        if world_id > 0:
            if check_editable(world_id, user_id, session_key):
                conn = connect()
                cur = conn.cursor()
                insert_request = """
                    INSERT INTO npc_special_linker(npc_id, special_id) VALUES
                    (%s, %s)
                    RETURNING id
                    """
                cur.execute(insert_request, (npc_id, special_id))
                outcome = cur.fetchall()

                conn.commit()
                conn.close()

                if outcome != ():
                    return True
    return False


def remove_npc_special_association(npc_id, special_id, user_id, session_key):
    """
    This function will remove an association between
    a npc and a special from the linker table

    :param special_id: the id of the special
    :param npc_id: the id of the npc
    :param user_id: the id of the user requesting this
    :param session_key: the user's session key

    :return: True if successful, False if not
    """
    if check_session_key(user_id, session_key):
        world_id = check_same_world(npc_id, special_id)

        if world_id > 0:
            if check_editable(world_id, user_id, session_key):
                conn = connect()
                cur = conn.cursor()

                delete_request = """
                    DELETE FROM npc_special_linker WHERE
                    npc_id = %s AND special_id = %s
                    """
                cur.execute(delete_request, (npc_id, special_id))
                conn.commit()
                conn.close()
                return True
    return False


def get_specials_by_npc(user_id, session_key, npc_id):
    """
    This function will get all specials an NPC
    is associated with
    :param user_id: the is of the user requesting
    :param session_key: the user's session key
    :param npc_id: the id of the npc being checked

    :return: a list of the specials

    :format return: [{id: special id,
                      name: special name}]
    """
    outcome = []
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        world_id_check = """
                SELECT world_id FROM npcs
                WHERE id = %s
                """
        cur.execute(world_id_check, [npc_id])
        world_id = cur.fetchall()[0][0]

        if check_editable(world_id, user_id, session_key):
            special_query = """
                    SELECT specials.id, name FROM npc_special_linker
                        INNER JOIN specials ON npc_special_linker.special_id = specials.id
                    WHERE npc_id = %s
                    """
            cur.execute(special_query, [npc_id])
        else:
            if check_viewable(world_id, user_id)['viewable']:
                special_query = """
                    SELECT specials.id, name FROM npc_special_linker
                        INNER JOIN specials ON npc_special_linker.special_id = specials.id
                    WHERE npc_id = %s AND specials.revealed = 't'
                    """
                cur.execute(special_query, [npc_id])

        for npc in cur.fetchall():
            outcome.append({'id': npc[0],
                            'name': npc[1]})
        conn.close()

    return outcome


def get_npcs_by_special(user_id, session_key, special_id):
    """
    This function will get all of the NPCs associated
    with a special
    :param user_id: the is of the user requesting
    :param session_key: the user's session key
    :param special_id: the id of the special being checked

    :return: a list of npcs

    :format return: [{id: npc id,
                      name: npc name}]
    """
    outcome = []
    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        world_id_check = """
            SELECT world_id FROM specials
            WHERE id = %s
            """
        cur.execute(world_id_check, [special_id])
        world_id = cur.fetchall()[0][0]

        if check_editable(world_id, user_id, session_key):
            npc_query = """
                SELECT npcs.id, name FROM npc_special_linker
                    INNER JOIN npcs ON npc_special_linker.npc_id = npcs.id
                WHERE special_id = %s
                """
            cur.execute(npc_query, [special_id])
        else:
            if check_viewable(world_id, user_id)['viewable']:
                npc_query = """
                    SELECT npcs.id, name FROM npc_special_linker
                        INNER JOIN npcs ON npc_special_linker.npc_id = npcs.id
                    WHERE special_id = %s AND npcs.revealed = 't'
                    """
                cur.execute(npc_query, [special_id])

        for npc in cur.fetchall():
            outcome.append(({'id': npc[0],
                             'name': npc[1]}))
        conn.close()

    return outcome
