from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect


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
        conn = connect()
        cur = conn.cursor()
        insert_request = """
            INSERT INTO npc_special_linker(npc_id, special_id) VALUES
            (%s, %s)
            """
        cur.execute(insert_request, (npc_id, special_id))
        conn.commit()
        conn.close()
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


def get_specials_by_npc(npc_id):
    """
    This function will get all specials an NPC
    is associated with
    :param npc_id: the id of the npc being checked

    :return: a list of the specials

    :format return: [{id: special id,
                      name: special name}]
    """
    conn = connect()
    cur = conn.cursor()

    npc2_query = """
            SELECT specials.id, name FROM npc_special_linker
                INNER JOIN specials ON npc_special_linker.special_id = specials.id
            WHERE special_id = %s
            """
    cur.execute(npc2_query, [npc_id])
    outcome = cur.fetchall()
    conn.close()

    return outcome


def get_npcs_by_special(special_id):
    """
    This function will get all of the NPCs associated
    with a special
    :param special_id: the id of the special being checked

    :return: a list of npcs

    :format return: [{id: npc id,
                      name: npc name}]
    """
    conn = connect()
    cur = conn.cursor()

    npc2_query = """
            SELECT npcs.id, name FROM npc_special_linker
                INNER JOIN npcs ON npc_special_linker.npc_id = npcs.id
            WHERE npc_id = %s
            """
    cur.execute(npc2_query, [special_id])
    outcome = cur.fetchall()
    conn.close()

    return outcome
