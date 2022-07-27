from src.components.citys import rebuild_citys_table
from src.components.comments import rebuild_comments_table
from src.components.npcs import rebuild_npcs_table
from src.components.specials import rebuild_specials_table
from src.components.users import rebuild_users_table
from src.components.worlds import rebuild_worlds_table


def rebuild_tables():
    rebuild_users_table()
    rebuild_worlds_table()
    rebuild_specials_table()
    rebuild_npcs_table()
    rebuild_citys_table()
    rebuild_comments_table()
