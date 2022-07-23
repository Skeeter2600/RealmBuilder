from src.utils.db_utils import connect
from src.utils.table_manager import rebuild_tables


def load_data():
    conn = connect()
    cur = conn.cursor()
    rebuild_tables()

    # passwords & ids for users
    # Beck:    RiamChesteroot26, 1
    # RyanR:   PabloWeegee69, 2
    # RyanC:   ThuaccTwumps, 3
    # Charles: CalvionNeedsAA, 4
    # Nolan:   TinkerTillYaMakeIt, 5
    # Taylor:  TomathyPickles123, 6
    # Josh:    ShadowWatcher58, 7
    # Jacob:   MarkFellowsRulez, 8

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

    add_citys = """
        INSERT INTO citys(name, population, song, trades, aesthetic, description, world_id) VALUES
            ('Jamestown', 28712, 'https://www.youtube.com/watch?v=5KiAWfu7cu8', 'Furniture',
                'Small City Vibes', 
                    'Jamestown is a city in southern Chautauqua County, New York, United States. 
                    The population was 28,712 at the 2020 census. Situated between Lake Erie to the north and the 
                    Allegheny National Forest to the south, Jamestown is the largest population center in the county. 
                    Nearby Chautauqua Lake is a freshwater resource used by fishermen, boaters, and naturalists.',
                6),
            ('Meridia', 1392, 'https://www.youtube.com/watch?v=ojEyUU2M6z4', 'Farming, Storefronts',
                'Small town vibes',
                    'Meridia is a small town in which many people flock for various reasons. Too many
                     to put here.',
                3),
            ('Greenest', 123, 'https://www.youtube.com/watch?v=EiyuZ7CTsbY', 'Storefronts',
                'Super small village vibes',
                    'Greenest is a small village in which many people flock for various reasons. Too many
                     to put here.',
                4),
            ('Greenest', 456, 'https://www.youtube.com/watch?v=EiyuZ7CTsbY', 'Storefronts',
                'Small village vibes',
                    'Greenest is a small village in which many people flock for various reasons. Too many
                     to put here.',
                3),
            ('Charlote', 112, 'https://www.youtube.com/watch?v=Y_tPE3o5NWk', 'Fishing and Farming',
                'historic sector of an older city, with ivy covering the walls of most of the buildings 
                    and running along the ground',
                'Charlote is a small, seaside fishing village. The area around it is mostly farmland due 
                    to the richness of the soil provided by the nearby ocean. Small streams run alongside the 
                    roads in and out of the town and go for about a mile before they run out due to irrigation 
                    ditches taking it to the fields.',
                1)
        """
    cur.execute(add_citys)
    conn.commit()

    add_npcs_non_hidden = """
        INSERT INTO npcs(name, age, occupation, description, world_id) VALUES
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
                2),
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
            ),
            ('Prometheus', 9999999, 'Scholar',
                'Prometheus is a medium robotesk being with a knack for tinkering. Despite his intelligence, he has no 
                    knowledge of clothes and its reasons. He has been adopted over the past countless years
                    to become the arch scholar of the area and knows more about what might be going on that anyone esle',
                6
            )
        """
    cur.execute(add_npcs_non_hidden)
    conn.commit()

    add_npcs_hidden = """
        INSERT INTO npcs(name, age, occupation, description, hidden_description, world_id) VALUES
        """

    conn.close()
