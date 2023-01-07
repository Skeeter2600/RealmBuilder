from src.components.cities import rebuild_cities_table
from src.components.comments import rebuild_comments_table
from src.components.npcs import rebuild_npcs_table
from src.components.specials import rebuild_specials_table
from src.components.users import rebuild_users_table
from src.components.worlds import rebuild_worlds_table
from src.linkers.admins import rebuild_admins_table
from src.linkers.city_image_linker import rebuild_city_image_linker
from src.linkers.city_npc_linker import rebuild_city_npc_linker
from src.linkers.city_special_linker import rebuild_city_special_linker
from src.linkers.npc_image_linker import rebuild_npc_image_linker
from src.linkers.npc_special_linker import rebuild_npc_special_linker
from src.linkers.special_image_linker import rebuild_special_image_linker
from src.linkers.world_user_linker import rebuild_world_user_linker
from src.linkers.npc_npc_linker import rebuild_npc_npc_linker
from src.components.likes_dislikes import rebuild_likes_dislikes_table


def rebuild_tables():
    rebuild_users_table()
    rebuild_worlds_table()
    rebuild_specials_table()
    rebuild_npcs_table()
    rebuild_npc_npc_linker()
    rebuild_cities_table()
    rebuild_comments_table()
    rebuild_admins_table()
    rebuild_city_image_linker()
    rebuild_city_npc_linker()
    rebuild_city_special_linker()
    rebuild_npc_image_linker()
    rebuild_npc_special_linker()
    rebuild_special_image_linker()
    rebuild_world_user_linker()
    rebuild_likes_dislikes_table()
