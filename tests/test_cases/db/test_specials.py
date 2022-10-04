import unittest

from src.components.users import login_user
from src.components.specials import *
from src.utils.table_manager import rebuild_tables
from tests.test_builders.test_build import load_data


class MyTestCase(unittest.TestCase):

    def test_add_city(self):
        """
        This test will test if a special is being added correctly.
        This will be done by an owner and a standard user
        """
        rebuild_tables()
        load_data()

        ryan_r_info = login_user('RyanR', 'PabloWeegee69')
        ryan_c_info = login_user('RyanC', 'ThuaccTwumps')

        details = {'world_id': 2,
                   'name': 'Test',
                   'images': [],
                   'description': 'test',
                   'hidden_description': '',
                   'associated_npcs': [{'id': 5}],
                   'associated_cities': []}
        outcome = add_special(ryan_r_info[1], ryan_r_info[0], details)
        self.assertFalse(outcome[0], "created specal when is should not have")

        outcome = add_special(ryan_c_info[1], ryan_c_info[0], details)
        self.assertTrue(outcome[0], "did not create special properly")

        special_id = outcome[1]

        expected = {'name': 'Test',
                    'images': [],
                    'description': 'test',
                    'associated_npcs': [{'id': 5,
                                         'name': 'Riam Chesteroot'}],
                    'associated_specials': [],
                    'admin_content': {'edit_date': '',
                                      'hidden_description': '',
                                      'revealed': False}}

        outcome = get_special_info(ryan_c_info[1], ryan_c_info[0], special_id, True)
        self.assertEqual(expected['name'], outcome['name'], "did not get the special properly")
        self.assertEqual(expected['images'], outcome['images'], "did not get the special properly")
        self.assertEqual(expected['description'], outcome['description'], "did not get the special properly")
        self.assertEqual(expected['associated_npcs'], outcome['associated_npcs'], "did not get the special properly")
        self.assertEqual(expected['admin_content']['revealed'],
                         outcome['admin_content']['revealed'], "did not get the special properly")

        outcome = get_special_info(ryan_r_info[1], ryan_r_info[0], special_id, False)
        # test each field is right for as an admin
        # (done this way due to timestamp in the creation changing each time)
        self.assertEqual('', outcome['name'], "Special has not been revealed, so should not be visible")

    def test_copy_special(self):
        rebuild_tables()
        load_data()

        ryan_r_info = login_user('RyanR', 'PabloWeegee69')
        ryan_c_info = login_user('RyanC', 'ThuaccTwumps')

        expected = {'name': 'Jamestown Key to the City',
                    'images': [],
                    'description': 'A key to the city of Jamestown, NY',
                    'associated_npcs': [],
                    'associated_specials': [],
                    'admin_content': {'edit_date': '',
                                      'hidden_description': '',
                                      'revealed': False}}

        outcome = copy_special(ryan_r_info[1], ryan_r_info[0], 1, 2)[0]
        self.assertFalse(outcome, "Should not have been successful")

        outcome = copy_special(ryan_c_info[1], ryan_c_info[0], 1, 2)
        self.assertTrue(outcome[0], "Should have been successful")

        outcome = get_special_info(ryan_c_info[1], ryan_c_info[0], outcome[1], True)
        self.assertEqual(expected['name'], outcome['name'], "did not get the special properly")
        self.assertEqual(expected['images'], outcome['images'], "did not get the special properly")
        self.assertEqual(expected['description'], outcome['description'], "did not get the special properly")
        self.assertEqual(expected['associated_npcs'], outcome['associated_npcs'], "did not get the special properly")
        self.assertEqual(expected['admin_content']['revealed'],
                         outcome['admin_content']['revealed'], "did not get the special properly")

    def test_delete_special(self):
        """
        This function will test the deleting of a special
        This will be done as a user and as an admin/owner
        """
        rebuild_tables()
        load_data()

        ryan_c_info = login_user('RyanC', 'ThuaccTwumps')
        beck_info = login_user('Beck', 'RiamChesteroot26')

        outcome = delete_special(ryan_c_info[1], ryan_c_info[0], 4, 3)
        self.assertFalse(outcome, "Should not be able to delete special")
        outcome = delete_special(beck_info[1], beck_info[0], 4, 3)
        self.assertTrue(outcome, "Should be able to delete special")

        check_city_exists = get_special_info(beck_info[1], beck_info[0], 4, True)
        self.assertEqual('', check_city_exists['name'], "special shouldn't exists any more")

    def test_edit_special(self):
        """
        This function will test the editing of a special.
        This is done by a user and an admin/owner.
        """
        rebuild_tables()
        load_data()

        # login an admin for Three Lords Sword Coast (Ryan C) and an admin for Real World (Ryan R)
        ryan_r_info = login_user('RyanR', 'PabloWeegee69')
        ryan_c_info = login_user('RyanC', 'ThuaccTwumps')

        edit_values = {'name': 'Key to Jamestown',
                       'description': 'test',
                       'hidden_description': '',
                       'revealed': True}

        outcome = edit_special(ryan_c_info[1], ryan_c_info[0], 1, 6, edit_values)
        self.assertEqual(outcome['name'], '', "should not have edited any info")

        outcome = edit_special(ryan_r_info[1], ryan_r_info[0], 1, 6, edit_values)
        self.assertEqual(edit_values['name'], outcome['name'], "did not get the city properly")
        self.assertEqual(edit_values['description'], outcome['description'], "did not get the city properly")

        outcome = get_special_info(ryan_c_info[1], ryan_c_info[0], 1, False)
        self.assertEqual(edit_values['name'], outcome['name'], "did not get the city properly")
        self.assertEqual(edit_values['description'], outcome['description'], "did not get the city properly")

    def test_reveal_hidden_special(self):
        """
        This function will test the revealing of a
        hidden description on a special
        """
        rebuild_tables()
        load_data()

        ryan_r_info = login_user('RyanR', 'PabloWeegee69')
        beck_info = login_user('Beck', 'RiamChesteroot26')

        expected_values = {'name': 'The Golden Candle',
                           'description': 'Hidden in the depth of the Carcer Caverns lies the Golden Candle, worshiped by the countless kobolds that lie within' + \
                                          '\n\nREVEAL\n\nThe candle is the prison for the demon Kyneas and will release him if ever extinguished. The kobolds protected it from ever happening, they never worshiped it.'
                           }
        outcome = reveal_hidden_special(ryan_r_info[1], ryan_r_info[0], 3, 5)
        self.assertEqual({}, outcome, 'should not have been able to reveal content')

        outcome = reveal_hidden_special(beck_info[1], beck_info[0], 3, 5)
        self.assertEqual(expected_values['name'], outcome['name'], 'should have been able to reveal content')
        self.assertEqual(expected_values['description'], outcome['description'],
                         'should have been able to reveal content')

        user_check = get_special_info(beck_info[1], beck_info[0], 5, True)
        self.assertEqual(expected_values['description'], user_check['description'],
                         'should have been able to reveal content')

    def test_special_search(self):
        """
        This function will test the searching of specials
        as a user and as an admin/owner
        """
        rebuild_tables()
        load_data()

        beck_info = login_user('Beck', 'RiamChesteroot26')
        taylor_info = login_user('Taylor', 'TomathyPickles123')

        beck_e_expected = [{'id': 4,
                            'name': 'Ring of Gander',
                            'reveal_status': False},
                           {'id': 5,
                            'name': 'The Golden Candle',
                            'reveal_status': False}]

        taylor_e_expected = []

        outcome = search_for_special('e', 3, None, 1, beck_info[1], beck_info[0])
        self.assertEqual(outcome, beck_e_expected, "Didn't get the right specials")

        outcome = search_for_special('e', 3, None, 1, taylor_info[1], taylor_info[0])
        self.assertEqual(outcome, taylor_e_expected, "Didn't get the right specials")

        edit_special(beck_info[1], beck_info[0], 4, 3, {'name': 'Ring of Gander',
                                                 'description': '',
                                                 'hidden_description': '',
                                                 'revealed': True})
        taylor_e_expected = [{'id': 4,
                              'name': 'Ring of Gander'}]

        outcome = search_for_special('e', 3, None, 1, taylor_info[1], taylor_info[0])
        self.assertEqual(outcome, taylor_e_expected, "Didn't get the right specials")


if __name__ == '__main__':
    unittest.main()
