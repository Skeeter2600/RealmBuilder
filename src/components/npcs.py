from src.linkers.npc_npc_linker import get_associated_npcs
from src.utils.db_tools import check_session_key
from src.utils.db_utils import connect


def rebuild_npcs_table():
    """
    This function will empty the npcs table
    """
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE if EXISTS npcs CASCADE;
        """
    create_sql = """
        CREATE TABLE npcs(
            id                  SERIAL PRIMARY KEY,
            name                TEXT NOT NULL,
            age                 INTEGER,
            occupation          TEXT,
            description         TEXT NOT NULL,
            hidden_description  TEXT DEFAULT NULL,
            revealed            BOOLEAN NOT NULL DEFAULT 'f',
            edit_date           TIMESTAMP DEFAULT NULL,
            world_id            INTEGER NOT NULL REFERENCES worlds ON DELETE CASCADE
        )
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()


def get_npc_info(npc_id, user_id, session_key, admin):
    """
    This function will get the information associated
    with an NPC based on the user's permissions
    :param npc_id: the id of the npc being checked
    :param user_id: the id of the user checking
    :param session_key: the user's session key
    :param admin: if the user is an admin

    :return: the npc info in a json format

    :format return: { name: npc name,
                      images: [images associated with npc]
                      age: npc age,
                      occupation: npc occupation,
                      description: npc description,
                      associated_npcs: [{id: npc id,
                                         name: npc name}]
                      associated_specials: [{id: special id,
                                             name: special name}],
                      associated_cities: [{id: city id,
                                           name: city name}],
                      admin_content: {
                            hidden_description: npc hidden description,
                            revealed: T or F,
                            edit_date: last time updated
                      } (empty if not admin)
    """
    npc_info = {'name': '',
                'images': [],
                'age': '',
                'occupation': "",
                'description': "",
                'associated_npcs': [],
                'associated_specials': [],
                'associated_cities': [],
                'admin_content': {}}

    if check_session_key(user_id, session_key):
        conn = connect()
        cur = conn.cursor()

        all_info_query = """
            SELECT name, age, occupation, description FROM npcs
            WHERE id = %s
            """
        cur.execute(all_info_query, [npc_id])
        all_outcome = cur.fetchall()[0]
        npc_info['name'] = all_outcome[0]

        # TODO get_images

        npc_info['age'] = all_outcome[1]
        npc_info['occupation'] = all_outcome[2]
        npc_info['description'] = all_outcome[3]

        npc_info['associated_npcs'] = get_associated_npcs(npc_id)

        # TODO get_associated_specials & get_associated_cities

        if admin:
            admin_content = {'hidden_description': '',
                             'revealed': None,
                             'edit_date': ''
                             }
            admin_query = """
                SELECT hidden_description, revealed, edit_date FROM npcs
                WHERE id = %s
                """
            cur.execute(admin_query, [npc_id])
            admin_outcome = cur.fetchall[0]

            admin_content['hidden_description'] = admin_outcome[0]
            admin_content['revealed'] = admin_outcome[1]
            admin_content['edit_date'] = admin_outcome[2]

            npc_info['admin_content'] = admin_content

        conn.close()

    return npc_info
