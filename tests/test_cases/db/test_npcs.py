import unittest
from datetime import datetime

from src.components.npcs import *
from src.components.users import login_user
from src.utils.table_manager import rebuild_tables
from tests.test_builders.test_build import load_data


class MyTestCase(unittest.TestCase):

    def test_add_npc(self):
        """
        This function will test the adding of a
        new npc, both as a user and an owner
        """
        rebuild_tables()
        load_data()

        ryan_r_session_key = login_user('RyanR', 'PabloWeegee69')
        ryan_c_session_key = login_user('RyanC', 'ThuaccTwumps')

        details = {'world_id': 2,
                   'name': 'Paul Blart',
                   'images': [],
                   'age': 42,
                   'occupation': 'Mall Cop',
                   'description': 'Fat, but determined',
                   'hidden_description': '',
                   'associated_cities': [{'id': 6}],
                   'associated_npcs': [{'id': 5}],
                   'associated_specials': []
                   }

        outcome = add_npc(2, ryan_r_session_key, details)[0]
        self.assertFalse(outcome, "Should not have been able to add npc")

        outcome = add_npc(3, ryan_c_session_key, details)
        self.assertTrue(outcome[0], "Should have been able to add npc")

        npc_id = outcome[1]
        expected = {'world_id': 2,
                    'name': 'Paul Blart',
                    'images': [],
                    'age': 42,
                    'occupation': 'Mall Cop',
                    'description': 'Fat, but determined',
                    'associated_cities': [{'id': 6, 'name': 'Saltmarsh'}],
                    'associated_npcs': [{'id': 5, 'name': 'Riam Chesteroot'}],
                    'associated_specials': [],
                    'admin_content': {'hidden_description': '',
                                      'revealed': False}
                    }
        outcome = get_npc_info(npc_id, 3, ryan_c_session_key, True)
        self.assertEqual(expected['name'], outcome['name'], "did not get the npc properly")
        self.assertEqual(expected['images'], outcome['images'], "did not get the npc properly")
        self.assertEqual(expected['age'], outcome['age'], "did not get the npc properly")
        self.assertEqual(expected['occupation'], outcome['occupation'], "did not get the npc properly")
        self.assertEqual(expected['description'], outcome['description'], "did not get the npc properly")
        self.assertEqual(expected['admin_content']['hidden_description'],
                         outcome['admin_content']['hidden_description'], "did not get the npc properly")
        self.assertEqual(expected['associated_npcs'], outcome['associated_npcs'], "did not get the npc properly")
        self.assertEqual(expected['associated_cities'], outcome['associated_cities'], "did not get the npc properly")
        self.assertEqual(expected['associated_specials'],
                         outcome['associated_specials'], "did not get the npc properly")
        self.assertEqual(expected['admin_content']['revealed'],
                         outcome['admin_content']['revealed'], "did not get the npc properly")

    def test_copy_npc(self):
        """
        This function will test the copying of an
        NPC, both as an admin and a user
        """
        rebuild_tables()
        load_data()

        ryan_r_session_key = login_user('RyanR', 'PabloWeegee69')
        ryan_c_session_key = login_user('RyanC', 'ThuaccTwumps')

        success_expected = {'name': 'Thuacc',
                            'age': 26,
                            'images': [],
                            'occupation': 'Adventurer',
                            'description': "Thuacc is a half orc paladin with a need for adventure. He is short tempered and straight to the point. What ever way will get to the goal is the right way and any one who stands in the way is only another obstacle in the way of success.",
                            'associated_npcs': [],
                            'associated_specials': [],
                            'associated_cities': [],
                            'admin_content': {'hidden_description': None,
                                              'revealed': False,
                                              'edit_date': ''
                                              }}

        outcome = copy_npc(2, ryan_r_session_key, 7, 2)[0]
        self.assertFalse(outcome, "Should not have been successful")

        outcome = copy_npc(3, ryan_c_session_key, 7, 2)
        self.assertTrue(outcome[0], "Should have been successful")

        outcome = get_npc_info(outcome[1], 3, ryan_c_session_key, True)
        self.assertEqual(success_expected['name'], outcome['name'], "did not get the npc properly")
        self.assertEqual(success_expected['images'], outcome['images'], "did not get the npc properly")
        self.assertEqual(success_expected['age'], outcome['age'], "did not get the npc properly")
        self.assertEqual(success_expected['occupation'], outcome['occupation'], "did not get the npc properly")
        self.assertEqual(success_expected['description'], outcome['description'], "did not get the npc properly")
        self.assertEqual(success_expected['admin_content']['hidden_description'],
                         outcome['admin_content']['hidden_description'], "did not get the npc properly")
        self.assertEqual(success_expected['associated_npcs'], outcome['associated_npcs'],
                         "did not get the npc properly")
        self.assertEqual(success_expected['associated_cities'], outcome['associated_cities'],
                         "did not get the npc properly")
        self.assertEqual(success_expected['associated_specials'],
                         outcome['associated_specials'], "did not get the npc properly")
        self.assertEqual(success_expected['admin_content']['revealed'],
                         outcome['admin_content']['revealed'], "did not get the npc properly")

    def test_delete_npc(self):
        """
        This function test deleting an npc from a world,
        both as a user and an admin/owner
        """
        rebuild_tables()
        load_data()

        ryan_r_session_key = login_user('RyanR', 'PabloWeegee69')
        ryan_c_session_key = login_user('RyanC', 'ThuaccTwumps')

        outcome = delete_npc(3, ryan_c_session_key, 9, 6)
        self.assertFalse(outcome, "Ryan C should not have been able to delete Richard Nixon")

        outcome = delete_npc(2, ryan_r_session_key, 9, 6)
        self.assertTrue(outcome, "Ryan R should have been able to delete Richard Nixon")

        expected = {'name': '',
                    'images': [],
                    'age': '',
                    'occupation': "",
                    'description': "",
                    'associated_npcs': [],
                    'associated_specials': [],
                    'associated_cities': [],
                    'admin_content': {}}

        info = get_npc_info(9, 2, ryan_r_session_key, True)
        self.assertEqual(info, expected, "Should not have gotten info for an npc that doesn't exist")

    def test_edit_npc(self):
        """
        This function will test the editing of an npc,
        both as a user and as an admin/owner
        """
        rebuild_tables()
        load_data()

        ryan_r_session_key = login_user('RyanR', 'PabloWeegee69')
        ryan_c_session_key = login_user('RyanC', 'ThuaccTwumps')

        details = {'name': 'Nixonator',
                   'age': 123456,
                   'occupation': 'Pro Tester',
                   'description': 'The best around',
                   'revealed': True
                   }

        outcome = edit_npc(3, ryan_c_session_key, 9, 6, details)
        self.assertFalse(outcome, "Ryan C should not be able to edit Richard Nixon in The Real World")

        outcome = edit_npc(2, ryan_r_session_key, 9, 6, details)
        self.assertTrue(outcome, "Ryan R should be able to edit Richard Nixon in The Real World")

        outcome = get_npc_info(9, 2, ryan_r_session_key, True)
        self.assertEqual(details['name'], outcome['name'], "did not get the npc properly")
        self.assertEqual(details['age'], outcome['age'], "did not get the npc properly")
        self.assertEqual(details['occupation'], outcome['occupation'], "did not get the npc properly")
        self.assertEqual(details['description'], outcome['description'], "did not get the npc properly")
        self.assertTrue(outcome['admin_content']['revealed'], "did not get the npc properly")

    def test_reveal_hidden_npc(self):
        """
        This function will test the revealing of the
        hidden description of an npc as a user and an admin/owner
        """
        rebuild_tables()
        load_data()

        ryan_r_session_key = login_user('RyanR', 'PabloWeegee69')
        beck_session_key = login_user('Beck', 'RiamChesteroot26')

        expected_values = {'name': 'Thuacc',
                           'age': 26,
                           'occupation': 'Adventurer',
                           'description': 'Thuacc is a half orc paladin with a need for adventure. He is short tempered and straight to the point. What ever way will get to the goal is the right way and any one who stands in the way is only another obstacle in the way of success.' + \
                                          '\n\nREVEAL\n\nThuacc was born with the name Bonc and had a brother named Thuacc. In a battle for their home town, Bonc took advantage of the situation and killed his brother, taking his name and leaving town.',
                           }
        outcome = reveal_hidden_npc(2, ryan_r_session_key, 3, 7)
        self.assertEqual({}, outcome, 'should not have been able to reveal content')

        outcome = reveal_hidden_npc(1, beck_session_key, 3, 7)
        self.assertEqual(expected_values['name'], outcome['name'], 'should have been able to reveal content')
        self.assertEqual(expected_values['age'], outcome['age'], 'should have been able to reveal content')
        self.assertEqual(expected_values['occupation'], outcome['occupation'],
                         'should have been able to reveal content')
        self.assertEqual(expected_values['description'], outcome['description'],
                         'should have been able to reveal content')

        user_check = get_npc_info(7, 2, ryan_r_session_key, False)
        self.assertEqual(expected_values['description'], user_check['description'],
                         'should have been able to reveal content')

    def test_npc_search(self):
        """
        This function will test the npc search function,
        both as a user and as an admin/owner
        """
        rebuild_tables()
        load_data()

        beck_session_key = login_user('Beck', 'RiamChesteroot26')
        taylor_session_key = login_user('Taylor', 'TomathyPickles123')

        beck_e_expected = [{'id': 4,
                            'occupation': 'Tinkerer',
                            'name': 'Prometheus',
                            'reveal_status': False},
                           {'id': 8,
                            'occupation': 'Trader',
                            'name': 'Oliver Quinn',
                            'reveal_status': True},
                           {'id': 10,
                            'occupation': 'Adventurer',
                            'name': 'Evelyn',
                            'reveal_status': False}]

        taylor_e_expected = [{'id': 8,
                              'occupation': 'Trader',
                              'name': 'Oliver Quinn'}]

        outcome = search_for_npc('e', 3, None, 1, 1, beck_session_key)
        self.assertEqual(outcome, beck_e_expected, "Didn't get the right NPCs")

        outcome = search_for_npc('e', 3, None, 1, 6, taylor_session_key)
        self.assertEqual(outcome, taylor_e_expected, "Didn't get the right NPCs")

        edit_npc(1, beck_session_key, 4, 3, {'name': 'Prometheus',
                                             'age': 1000,
                                             'occupation': 'Tinkerer',
                                             'description': 'Prometheus is a medium robotesk being with a knack for tinkering. Despite his intelligence, he has no knowledge of clothes and its reasons. He will awkwardly talk about the players clothes with a little bit of knowledge, but ultimately trail off.',
                                             'revealed': True
                                             })

        taylor_e_expected = [{'id': 8,
                              'occupation': 'Trader',
                              'name': 'Oliver Quinn'},
                             {'id': 4,
                              'occupation': 'Tinkerer',
                              'name': 'Prometheus'}]

        outcome = search_for_npc('e', 3, None, 1, 6, taylor_session_key)
        self.assertEqual(outcome, taylor_e_expected, "Didn't get the right NPCs")


if __name__ == '__main__':
    unittest.main()
