from src.utils.db_utils import connect
from src.utils.table_manager import rebuild_tables


def load_data():
    conn = connect()
    cur = conn.cursor()
    rebuild_tables()

    # passwords & session key for users
    # Beck:    RiamChesteroot26
    # RyanR:   PabloWeegee69
    # RyanC:   ThuaccTwumps
    # Charles: CalvionNeedsAA
    # Nolan:   TinkerTillYaMakeIt
    # Taylor:  TomathyPickles123
    # Josh:    ShadowWatcher58
    # Jacob:   MarkFellowsRulez

    add_users = """
        INSERT INTO users(username, password, email) VALUES 
            ('Beck', '6bdb83aeccb26b1f038953bc2b140f4ef1aadd4313413f3496b2f6fac84f0696f5dff73d3dd7a23663262c874757242449f6abbdb6190352c16eb383943846e9',
                'skeeter26@gmail.com'),
            ('RyanR', '4648a2fe2a26ae6b199d72cab221ed85640ede7bd107579e6a1956ce95aaafd61e5867f8c3d4ad9ba465e145e66c030db88e41a1555239161570d799e39ad5e1', 
                'carpet_s@yahoo.com'),
            ('RyanC', 'c9f0792a65687739f20b95d00e1fd948a7426be26d581027b8ea6102e0209a8687c225b4c3634da8274a8f81589acff6161d5e8ac5fdec0f4742f4005a8b920f',
                'KabumJr@gmail.com'),
            ('Charles', '0057e1db257e769b47aa441679714abc8e49c303168e0352fb42ddfd334caa7c046178133463ecf2dfbf4ccab159464c6a6a1d89f6791b92e0a488eafd487150',
                'Chazam@yahoo.com'),
            ('Nolan', '07e611ce413b6ba6593c43ee55505abffd8aa6565b9946c12498369428b1c91c13b079f648f4bc5f5507d4ac1b27b670d6032d0d720bdbcae59f9fc377f7f298',
                'pugalicious@gmail.com'),
            ('Taylor', 'e2ccce9bc27ac9f86b7d610f88b7138906b5c2f1ed66be4e76ef1f67698080610fae6ed5b06c3911f3a3c769860808ed0264be1e96eb7c3ef2d59d615107095b',
                'biggwatt@gmail.com'),
            ('Josh', 'a3a47eb80147656bc1842d1c124880f73ee8fc029304853cc84591c41f2d585f1be0e551404b2d68e40ac9cc6cc795d93a08b89f69bdc5b7b54e57738c51ed6d', 
                'JoshyBigMac@aol.com'),
            ('Jacob', 'b696bed74199f2d07ec58a7c12bdb6c58f680200eadb06ab687e94c1b762f5e7056bd0a62e869e399bd003d930905d84e38cddf7f900e2db7433883e9aee501a', 
                'gumbo2600@gmail.com')
        """

    cur.execute(add_users)
    conn.commit()

    add_worlds = """
        INSERT INTO worlds(name, owner_id) VALUES
            ('Dralbrar', 1),
            ('Saltmarsh', 3),
            ('Saviors'' Cradle Sword Coast', 1),
            ('Three Lords Sword Coast', 3),
            ('Out of Touch', 5),
            ('Real World', 2)
        """
    cur.execute(add_worlds)
    conn.commit()

    #    cities and their ids, worlds, and reveal status

    # New Meridia     | 1 | Saviors' Cradle Sword Coast | False
    # Greenest        | 2 | Three Lords Sword Coast     | False
    # Charlote        | 3 | Dralbrar                    | False
    # Jamestown       | 4 | Real World                  | True
    # Meridia         | 5 | Saviors' Cradle Sword Coast | True
    # Saltmarsh       | 6 | Saltmarsh                   | True
    # Greenest        | 7 | Saviors' Cradle Sword Coast | True
    # Washington D.C. | 8 | Real World                  | True

    add_citys_unrevealed = """
        INSERT INTO citys(name, population, song, trades, aesthetic, description, world_id) VALUES
            ('New Meridia', 10392, 'https://www.youtube.com/watch?v=ojEyUU2M6z4', 'Farming, Storefronts',
                'Small town vibes',
                    'New Meridia is a medium sized town in which many people flock for various reasons. Too many
                     to put here.',
                3),
            ('Greenest', 123, 'https://www.youtube.com/watch?v=EiyuZ7CTsbY', 'Storefronts',
                'Super small village vibes',
                    'Greenest is a small village in which many people flock for various reasons. Too many
                     to put here.',
                4),
            ('Charlote', 112, 'https://www.youtube.com/watch?v=Y_tPE3o5NWk', 'Fishing and Farming',
                'historic sector of an older city, with ivy covering the walls of most of the buildings 
                    and running along the ground',
                'Charlote is a small, seaside fishing village. The area around it is mostly farmland due 
                    to the richness of the soil provided by the nearby ocean. Small streams run alongside the 
                    roads in and out of the town and go for about a mile before they run out due to irrigation 
                    ditches taking it to the fields.',
                1)
        """
    cur.execute(add_citys_unrevealed)
    conn.commit()

    add_citys_revealed = """
        INSERT INTO citys(name, population, song, trades, aesthetic, description, world_id, 
            revealed, revealed_date) VALUES
            ('Jamestown', 28712, 'https://www.youtube.com/watch?v=5KiAWfu7cu8', 'Furniture',
                'Small City Vibes', 
                    'Jamestown is a city in southern Chautauqua County, New York, United States. 
                    The population was 28,712 at the 2020 census. Situated between Lake Erie to the north and the 
                    Allegheny National Forest to the south, Jamestown is the largest population center in the county. 
                    Nearby Chautauqua Lake is a freshwater resource used by fishermen, boaters, and naturalists.',
                6, 't', '1886-04-19 01:23:45'),
            ('Meridia', 1392, 'https://www.youtube.com/watch?v=ojEyUU2M6z4', 'Farming, Storefronts',
                'Small town vibes',
                    'Meridia is a small town in which many people flock for various reasons. Too many
                     to put here.',
                3, 't', '2018-07-12 14:32:17'),
            ('Saltmarsh', 5091, 'https://www.youtube.com/watch?v=eCMO-LpKsU8', 'Sailing, Trading',
                'English fishing town of the 14th Century', 
                    'Saltmarsh is a small, respectable fishing town in the Viscounty of Salinmoor, in the southernmost 
                    part of Keoland, noted for adventuring although it is normally a sleepy little town.',
                2, 't', '2019-08-19 20:19:00'),
            ('Greenest', 456, 'https://www.youtube.com/watch?v=EiyuZ7CTsbY', 'Storefronts',
                    'Small village vibes',
                        'Greenest is a small village in which many people flock for various reasons. Too many
                         to put here.',
                    3, 't', '2019-12-11 19:22:33'),
            ('Washington D.C.', 689545, 'https://www.youtube.com/watch?v=vPKp29Luryc', 'Politics, Museums, Stores',
                    '', 
                        'Washington, D.C., formally the District of Columbia, also known as just Washington or simply 
                        D.C., is the capital city and federal district of the United States. It is located on the east 
                        bank of the Potomac River, which forms its southwestern and southern border with the U.S. state 
                        of Virginia, and it shares a land border with the U.S. state of Maryland on its remaining sides. 
                        The city was named for George Washington, a Founding Father and the first president of the 
                        United States, and the federaldistrict is named after Columbia, a female personification of the 
                        nation. As the seat of the U.S. federal government and several international organizations, the 
                        city is an important world political capital. It is one of the most visited cities in the U.S., 
                        seeing over 20 million visitors in 2016.',
                    6, 't', '1790-07-16 12:00:00')
        """
    cur.execute(add_citys_revealed)
    conn.commit()

    #    npcs and their ids, worlds, location, hidden description status, and reveal status

    # Margarette Chesteroot | 1 | Dralbrar                    | Charlote        | False | False
    # Soni Paustel          | 2 | Out of Touch                | Null            | False | False
    # Prometheus            | 3 | Three Lords Sword Coast     | Null            | False | False
    # Prometheus            | 4 | Saviors' Cradle Sword Coast | Meridia         | False | False
    # Riam Chesteroot       | 5 | Saltmarsh                   | Saltmarsh       | False | True
    # Prometheus            | 6 | Out of Touch                | Null            | False | True
    # Oliver Quinn          | 7 | Saviors' Cradle Sword Coast | Meridia         | True  | True
    # Richard Nixon         | 8 | Real World                  | Washington D.C. | True  | True
    # Evelyn                | 9 | Saviors' Cradle Sword Coast | Null            | True  | False

    add_npcs_non_hidden_unrevealed = """
        INSERT INTO npcs(name, age, occupation, description, world_id) VALUES
            ('Margarette Chesteroot', 67, 'Caretaker of the Vine',
                'Margarete Chesteroot has the title of “Caretaker of the Vine,” something given to the eldest individual
                    in Charlote. Her main duty is to look after The Vine and make sure of its well being.',
                1
            ),
            ('Soni Paustel', 22, 'Detective',
                'Soni is an ace detective who boasts a sharp wit and high level of intelligence. His aptitude for 
                    solving cases has him named "The Second Advent of the Detective Prince". Despite his popularity, 
                    Soni is actually quite lonely and yearns for attention and validation. He was abandoned by his 
                    father amd lost his mother to suicide (which he later claims were the result of him being a 
                    "cursed child") and never had any genuine friends.',
                6
            ),
            ('Prometheus', 970, 'Artificer',
                'Prometheus is a medium robotesk being with a knack for tinkering. Despite his intelligence, he has no 
                    knowledge of clothes and its reasons.',
                4
            ),
            ('Prometheus', 1000, 'Tinkerer',
                'Prometheus is a medium robotesk being with a knack for tinkering. Despite his intelligence, he has no 
                    knowledge of clothes and its reasons. He will awkwardly talk about the players clothes with a little
                    bit of knowledge, but ultimately trail off.',
                3
            )
        """
    cur.execute(add_npcs_non_hidden_unrevealed)
    conn.commit()

    add_npcs_non_hidden_revealed = """
        INSERT INTO npcs(name, age, occupation, description, world_id, revealed, revealed_date) VALUES
            ('Riam Chesteroot', 27, 'Captain',
                'Riam Chesteroot is a 5’8” tall human weighing in at around 130 lbs. He has long, messy, black hair, 
                    which is often pushed down and over his left ear. He has a slim face with a small nose and prominent
                    chin line, as well as two different colored eyes, his left being blue and his right being green. 
                    Riam often wears darker colored clothes, not out of edginess, but due to not caring about how he 
                    looks and it often being easier to maintain due to spots being harder to see. When standing around, 
                    he is often shuffling his deck of cards, a memento from home and what he uses for his spellbook. 
                    The 3 of spades is missing from this deck. He usually will stay away from the center of action, 
                    watching and waiting for a perfect time to make a move. Chesteroot just wants to be able to call a 
                    group of people his “family.” His history of distrust with those who were his family stunt his 
                    ability to keep others from getting close.',
                2, 't', '2020-01-29 13:18:32'),
            ('Prometheus', 9999999, 'Scholar',
                'Prometheus is a medium robotesk being with a knack for tinkering. Despite his intelligence, he has no 
                    knowledge of clothes and its reasons. He has been adopted over the past countless years
                    to become the arch scholar of the area and knows more about what might be going on that anyone esle',
                6, 't', '2021-03-04 12:14:52')
        """
    cur.execute(add_npcs_non_hidden_revealed)
    conn.commit()

    add_npcs_hidden_revealed = """
        INSERT INTO npcs(name, age, occupation, description, hidden_description, world_id, 
            revealed, revealed_date) VALUES
            ('Oliver Quinn', 39, 'Trader', 
                'Oliver Quinn is a man standing 5''11" with dirty blonde hair. He is married
                to Susie Quinn and had a son, Robby, who was tragically lost to travelling adventurers', 
                'Oliver made a deal with Kyneas in order to get his son back and prevent the adventurers from ever
                killing his son. He went back in time to prevent them from ever becoming adventurers, but was killed
                due to them denying his reality and doing things how they wanted to.', 
                3, 't', '2020-05-12 17:18:22'),
            ('Richard Nixon', 109, 'President of the United States',
                'Richard Milhous Nixon was the 37th president of the United States, serving from 1969 to 1974. He was 
                a member of the Republican Party who previously served as a representative and senator from California 
                and was the 36th vice president from 1953 to 1961', 
                'Was responsible for the Watergate Scandal', 
                6, 't', '1972-06-17 12:54:21')
        """
    cur.execute(add_npcs_hidden_revealed)
    conn.commit()

    add_npcs_hidden_unrevealed = """
        INSERT INTO npcs(name, age, occupation, description, hidden_description, world_id) VALUES
            ('Evelyn', 28, 'Adventurer', 'Evelyn was a half elf warlock who''s allegiance was to an unknown being ', 
                'His allegiance was alter revealed to be to Kyneas, and fought against the party, during which he lost
                his life', 3)
        """
    cur.execute(add_npcs_hidden_unrevealed)
    conn.commit()

    #    npcs and their ids, worlds, location, hidden description status, and reveal status

    # Margarette Chesteroot | 1 | Dralbrar                    | Charlote             | False | False
    # Soni Paustel          | 2 | Out of Touch                | Null                 | False | False
    # Prometheus            | 3 | Three Lords Sword Coast     | Greenest(2)          | False | False
    # Prometheus            | 4 | Saviors' Cradle Sword Coast | Meridia, Greenest(7) | False | False
    # Riam Chesteroot       | 5 | Saltmarsh                   | Saltmarsh            | False | True
    # Prometheus            | 6 | Out of Touch                | Null                 | False | True
    # Oliver Quinn          | 7 | Saviors' Cradle Sword Coast | Meridia              | True  | True
    # Richard Nixon         | 8 | Real World                  | Washington D.C.      | True  | True
    # Evelyn                | 9 | Saviors' Cradle Sword Coast | Null                 | True  | False

    link_npcs_and_cities = """
        INSERT INTO city_npc_linker(city_id, npc_id) VALUES
            (3, 1),
            (2, 3),
            (5, 4),
            (7, 4),
            (6, 5),
            (5, 7),
            (8, 8)
        """
    cur.execute(link_npcs_and_cities)
    conn.commit()

    #    cities and their ids, worlds, associated city(s), associated user(s), hidden status, and reveal status

    # Jamestown Key to the City | 1 | Real World                  | Jamestown(4)    | NULL                       | False | True
    # Soul Phylactery           | 2 | Out of Touch                | NULL            | NULL                       | False | True
    # The Vines                 | 3 | Dralbrar                    | Charlote        | Margarette Chesteroot(1)   | False | False
    # Ring of Gander            | 4 | Saviors' Cradle Sword Coast | Meridia(5)      | NULL                       | True  | False
    # The Golden Candle         | 5 | Saviors' Cradle Sword Coast | NULL            | Oliver Quinn(7), Evelyn(9) | True  | False

    add_specials_non_hidden_revealed = """
        INSERT INTO specials(name, description, world_id, revealed, revealed_date) VALUES
            ('Jamestown Key to the City', 'A city to the city of Jamestown, NY', 6, 't', '1934-12-20 16:15:00'),
            ('Soul Phylactery', 'A large crystal with the souls of countless tortured individuals trapped within',
                5, 't', '2021-06-19 15:12:22')
        """
    cur.execute(add_specials_non_hidden_revealed)
    conn.commit()

    add_specials_non_hidden_non_revealed = """
        INSERT INTO specials(name, description, world_id) VALUES
            ('The Vines', 'The vines of the town come from a small bush in the village center. These vines have been 
                there for hundreds of years and seem to keep the buildings in good condition, preventing them from 
                needing maintenance. The only building that the roots seem to avoid is the town hall, going around its 
                base and moving out past it. The roots follow the irrigated ditches along the road and to the fields 
                and seem to turn the water from the ocean into pure water and add natural fertilizers to it, allowing 
                the crops to grow larger and stronger than normal. These roots were a gift to the town by Atandia for 
                their constant tranquility and provide those who consume the plants aided by its fertilizers with health, 
                and keeping them looking young. They still age however, but there is no physical evidence of it.',
            1)
        """
    cur.execute(add_specials_non_hidden_non_revealed)
    conn.commit()

    add_specials_hidden = """
        INSERT INTO specials(name, description, hidden_description, world_id) VALUES
            ('Ring of Gander', 'A ring to improve the user''s charisma with those of the same sex', 'Is actually the
                Ring of Gender. In addition to the other effect, it also binds with the wearer transforming them into the
                opposite sex over the course of the next 2 weeks. The effect remains on those of the wearer''s initial gender',
                3),
            ('The Golden Candle', 'Hidden in the depth of the Carcer Caverns lies the Golden Candle, worshiped
                by the countless kobolds that lie within', 'The candle is the prison for the demon Kyneas and will release
                him if ever extinguished. The kobolds protected it from ever happening, they never worshiped it.', 3)
        """
    cur.execute(add_specials_hidden)
    conn.commit()

    link_specials_and_npcs = """
        INSERT INTO npc_special_linker(npc_id, special_id) VALUES
            (1, 3),
            (7, 5),
            (9, 5)
        """
    cur.execute(link_specials_and_npcs)
    conn.commit()

    link_specials_and_cities = """
        INSERT INTO city_special_linker(city_id, special_id) VALUES
            (4, 1),
            (3, 3),
            (5, 4)
        """
    cur.execute(link_specials_and_cities)
    conn.commit()

    add_comments = """
        INSERT INTO comments(user_id, comment, time, likes, dislikes, component_id, component_type) VALUES
            (1, 'hey, dats me!', '2022-01-29 13:17:32', 1, 0, 1, 'npcs'),
            (3, 'That is my world', '2022-07-07 04:01:00', 2, 0, 3, 'worlds'),
            (3, 'That is my world', '2022-07-07 04:02:00', 1, 1, 2, 'worlds'),
            (4, 'Didn''t see that coming', '2020-05-12 17:18:22', 5, 0, 1, 'npcs'),
            (5, 'hey, dats me!', '2022-01-29 13:17:32', 2, 0, 4, 'npcs'),
            (5, 'hey, dats me again!', '2022-01-29 13:18:32', 1, 1, 5, 'npcs'),
            (5, 'hey, dats me again again!', '2022-01-29 13:19:32', 0, 0, 6, 'npcs'),
            (2, 'I live there...', '2019-05-05 11:11:11', 6, 0, 6, 'cities')
        """
    cur.execute(add_comments)
    conn.commit()

    conn.close()
