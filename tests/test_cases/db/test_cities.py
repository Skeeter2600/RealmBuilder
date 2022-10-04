import unittest
from datetime import datetime

from src.components.cities import *
from src.components.users import login_user
from src.utils.table_manager import rebuild_tables
from tests.test_builders.test_build import load_data


class MyTestCase(unittest.TestCase):

    def test_add_city(self):
        """
        This test will test if a city is being added correctly.
        This will be done by an owner and a standard user
        """
        rebuild_tables()
        load_data()

        ryan_r_info = login_user('RyanR', 'PabloWeegee69')
        ryan_c_info = login_user('RyanC', 'ThuaccTwumps')

        details = {'world_id': 2,
                   'name': 'Test',
                   'images': [],
                   'population': 123,
                   'song': 'test',
                   'trades': 'test',
                   'aesthetic': 'test',
                   'description': 'test',
                   'associated_npcs': [5],
                   'associated_specials': []}

        # testing making a new city
        outcome = add_city(ryan_r_info[1], ryan_r_info[0], details)
        self.assertFalse(outcome[0], "created city when is should not have")

        outcome = add_city(ryan_c_info[1], ryan_c_info[0], details)
        self.assertTrue(outcome[0], "did not create city properly")

        city_id = outcome[1]

        expected = {'name': 'Test',
                    'images': [],
                    'population': 123,
                    'song': 'test',
                    'trades': 'test',
                    'aesthetic': 'test',
                    'description': 'test',
                    'associated_npcs': [{'id': 5,
                                         'name': 'Riam Chesteroot'}],
                    'associated_specials': [],
                    'admin_content': {'edit_date': '',
                                      'revealed': False}}

        # testing getting the city
        outcome = get_city(ryan_r_info[1], ryan_r_info[0], city_id, False)
        self.assertEqual(outcome, {'name': '',
                                   'images': [],
                                   'population': 0,
                                   'song': '',
                                   'trades': '',
                                   'aesthetic': '',
                                   'description': '',
                                   'associated_npcs': [],
                                   'associated_specials': [],
                                   'admin_content': {}},
                         "should not be able to see any content as the city isn't revealed")

        outcome = get_city(ryan_c_info[1], ryan_c_info[0], city_id, True)
        # test each field is right for as an admin
        # (done this way due to timestamp in the creation changing each time)
        self.assertEqual(expected['name'], outcome['name'], "did not get the city properly")
        self.assertEqual(expected['images'], outcome['images'], "did not get the city properly")
        self.assertEqual(expected['population'], outcome['population'], "did not get the city properly")
        self.assertEqual(expected['song'], outcome['song'], "did not get the city properly")
        self.assertEqual(expected['trades'], outcome['trades'], "did not get the city properly")
        self.assertEqual(expected['aesthetic'], outcome['aesthetic'], "did not get the city properly")
        self.assertEqual(expected['description'], outcome['description'], "did not get the city properly")
        self.assertEqual(expected['associated_npcs'], outcome['associated_npcs'], "did not get the city properly")
        self.assertEqual(expected['associated_specials'],
                         outcome['associated_specials'], "did not get the city properly")
        self.assertEqual(expected['admin_content']['revealed'],
                         outcome['admin_content']['revealed'], "did not get the city properly")

        outcome = get_city(ryan_c_info[1], ryan_c_info[0], city_id, False)
        # test each field is right for as an admin
        # (done this way due to timestamp in the creation changing each time)
        self.assertEqual('', outcome['name'], "City has not been revealed, so should not be visible")

    def test_copy_city(self):
        """
        This function will test copying a city to
        a new world
        """
        rebuild_tables()
        load_data()

        ryan_r_info = login_user('RyanR', 'PabloWeegee69')
        ryan_c_info = login_user('RyanC', 'ThuaccTwumps')

        success_expected = {'name': 'Jamestown',
                            'images': [],
                            'population': 28712,
                            'song': 'https://www.youtube.com/watch?v=5KiAWfu7cu8',
                            'trades': 'Furniture',
                            'aesthetic': 'Small City Vibes',
                            'description': 'Jamestown is a city in southern Chautauqua County, New York, United States. ' + \
                                           'The population was 28,712 at the 2020 census. Situated between Lake Erie to the north and the ' + \
                                           'Allegheny National Forest to the south, Jamestown is the largest population center in the county. ' + \
                                           'Nearby Chautauqua Lake is a freshwater resource used by fishermen, boaters, and naturalists.',
                            'associated_npcs': [],
                            'associated_specials': [],
                            'admin_content': {
                                'revealed': True,
                                'edit_date': ''
                                }
                            }

        outcome = copy_city(ryan_r_info[1], ryan_r_info[0], 4, 2)[0]
        self.assertFalse(outcome, "Should not have been successful")

        outcome = copy_city(ryan_c_info[1], ryan_c_info[0], 4, 2)
        self.assertTrue(outcome[0], "Should have been successful")

        outcome = get_city(ryan_c_info[1], ryan_c_info[0], 4, True)
        self.assertEqual(success_expected['name'], outcome['name'], "did not get the city properly")
        self.assertEqual(success_expected['images'], outcome['images'], "did not get the city properly")
        self.assertEqual(success_expected['population'], outcome['population'], "did not get the city properly")
        self.assertEqual(success_expected['song'], outcome['song'], "did not get the city properly")
        self.assertEqual(success_expected['trades'], outcome['trades'], "did not get the city properly")
        self.assertEqual(success_expected['aesthetic'], outcome['aesthetic'], "did not get the city properly")
        self.assertEqual(success_expected['description'], outcome['description'], "did not get the city properly")
        self.assertEqual(success_expected['associated_npcs'], outcome['associated_npcs'], "did not get the city properly")
        self.assertEqual(success_expected['associated_specials'],
                         outcome['associated_specials'], "did not get the city properly")
        self.assertEqual(success_expected['admin_content']['revealed'],
                         outcome['admin_content']['revealed'], "did not get the city properly")

    def test_delete_city(self):
        """
        This function will test the deleting of a city.
        This will be done as a user and as an owner
        """
        rebuild_tables()
        load_data()

        ryan_c_info = login_user('RyanC', 'ThuaccTwumps')
        beck_info = login_user('Beck', 'RiamChesteroot26')

        outcome = delete_city(ryan_c_info[1], ryan_c_info[0], 1, 3)
        self.assertFalse(outcome, "Should not be able to delete city")
        outcome = delete_city(beck_info[1], beck_info[0], 1, 3)
        self.assertTrue(outcome, "Should be able to delete city")

        check_city_exists = get_city(beck_info[1], beck_info[0], 1, True)
        self.assertEqual('', check_city_exists['name'], "city shouldn't exists any more")

    def test_edit_city(self):
        """
        This function will test the editing of a city.
        This is done by a user and an admin/owner
        """
        rebuild_tables()
        load_data()

        # login an admin for Three Lords Sword Coast (Ryan C) and an admin for Real World (Ryan R)
        ryan_r_info = login_user('RyanR', 'PabloWeegee69')
        ryan_c_info = login_user('RyanC', 'ThuaccTwumps')

        # values to update Jamestown with
        edit_values = {'name': 'Jamestown 2.0',
                       'population': 67890,
                       'song': 'test',
                       'trades': 'test',
                       'aesthetic': 'test',
                       'description': 'test',
                       'revealed': True}

        outcome = edit_city(ryan_c_info[1], ryan_c_info[0], 4, 6, edit_values)
        self.assertEqual(outcome['name'], '', "should not have edited any info")
        outcome = edit_city(ryan_r_info[1], ryan_r_info[0], 4, 6, edit_values)
        self.assertEqual(edit_values['name'], outcome['name'], "did not get the city properly")
        self.assertEqual(edit_values['population'], outcome['population'], "did not get the city properly")
        self.assertEqual(edit_values['song'], outcome['song'], "did not get the city properly")
        self.assertEqual(edit_values['trades'], outcome['trades'], "did not get the city properly")
        self.assertEqual(edit_values['aesthetic'], outcome['aesthetic'], "did not get the city properly")
        self.assertEqual(edit_values['description'], outcome['description'], "did not get the city properly")

        # get the info to make sure
        outcome = get_city(ryan_c_info[1], ryan_c_info[0], 4, False)
        self.assertEqual(edit_values['name'], outcome['name'], "did not get the city properly")
        self.assertEqual(edit_values['population'], outcome['population'], "did not get the city properly")
        self.assertEqual(edit_values['song'], outcome['song'], "did not get the city properly")
        self.assertEqual(edit_values['trades'], outcome['trades'], "did not get the city properly")
        self.assertEqual(edit_values['aesthetic'], outcome['aesthetic'], "did not get the city properly")
        self.assertEqual(edit_values['description'], outcome['description'], "did not get the city properly")

    def test_get_city(self):
        """
        This test will test the getting of a city
        as an admin and as a user
        """
        rebuild_tables()
        load_data()

        # login an admin for Greenest (Ryan C) and an admin for Jamestown (Ryan R)
        ryan_r_info = login_user('RyanR', 'PabloWeegee69')
        ryan_c_info = login_user('RyanC', 'ThuaccTwumps')

        # should get Jamestown for both
        outcome = get_city(ryan_r_info[1], ryan_r_info[0], 4, True)
        self.assertEqual("Jamestown", outcome['name'], "not the right city name")
        outcome = get_city(ryan_c_info[1], ryan_c_info[0], 4, False)
        self.assertEqual("Jamestown", outcome['name'], "not the right city name")

        # should get Greenest for both
        outcome = get_city(ryan_c_info[1], ryan_c_info[0], 2, True)
        self.assertEqual("Greenest", outcome['name'], "not the right city name")
        outcome = get_city(ryan_r_info[1], ryan_r_info[0], 2, False)
        self.assertEqual('', outcome['name'], "shouldn't get anything (not revealed)")

    def test_get_cities(self):
        """
        This test will test searching, both as an admin
        and as a normal user
        """
        rebuild_tables()
        load_data()

        beck_info = login_user('Beck', 'RiamChesteroot26')
        charles_info = login_user('Charles', 'CalvionNeedsAA')

        # searching in Savior's Cradle for all cities as admin, should be 3
        outcome = get_cities(beck_info[1], beck_info[0], 3, None, 1)
        self.assertEqual(3, outcome.__len__(), "not the right number of cities")

        # searching in Savior's Cradle for all cities as normal user, should be 2
        outcome = get_cities(charles_info[1], charles_info[0], 3, None, 1)
        self.assertEqual(2, outcome.__len__(), "not the right number of cities")

    def test_search_cities(self):
        """
        This test will simulate searching for cities
        both as a user and as an admin
        """
        rebuild_tables()
        load_data()

        beck_info = login_user('Beck', 'RiamChesteroot26')
        charles_info = login_user('Charles', 'CalvionNeedsAA')

        # searching for cities with the string 'Meridia' as an admin, expecting 2 results
        outcome = search_for_city('Meridia', 3, None, 1, beck_info[1], beck_info[0])
        self.assertEqual([{'id': 1, 'name': 'New Meridia', 'population': 10392, 'reveal_status': False},
                          {'id': 5, 'name': 'Meridia', 'population': 1392, 'reveal_status': True}],
                         outcome, "not the right cities")

        # searching for cities with the string 'Meridia' as a user, expecting 1 result
        outcome = search_for_city('Meridia', 3, None, 1, charles_info[1], charles_info[0])
        self.assertEqual([{'id': 5, 'name': 'Meridia', 'population': 1392}], outcome, "not the right cities")

        outcome = search_for_city('e', 3, None, 1, beck_info[1], beck_info[0])
        self.assertEqual(len(outcome), 3, "not the right number of cities")

        outcome = search_for_city('e', 3, None, 1, charles_info[1], charles_info[0])
        self.assertEqual(len(outcome), 2, "not the right number of cities")

    def test_get_npcs_in_city(self):
        """
        This test will simulate loading the npcs
        in a city as an admin and a user
        """
        rebuild_tables()
        load_data()

        beck_info = login_user('Beck', 'RiamChesteroot26')
        charles_info = login_user('Charles', 'CalvionNeedsAA')

        # loading the npcs in Meridia as an admin, expecting 3 results
        outcome = get_npcs_by_city(beck_info[1], beck_info[0], 5)
        self.assertEqual(3, outcome.__len__(), "didn't get all of the NPCs in Meridia")

        # loading the npcs in Meridia as a user, expecting 2 result
        outcome = get_npcs_by_city(charles_info[1], charles_info[0], 5)
        self.assertEqual(2, outcome.__len__(), "didn't get all of the NPCs in Meridia")

        # loading the npcs in Charlote as an admin, expecting 1 result
        outcome = get_npcs_by_city(beck_info[1], beck_info[0], 3)
        self.assertEqual(1, outcome.__len__(), "didn't get all of the NPCs in Charlote")

        # loading the npcs in Charlote as an admin, expecting 0 results
        outcome = get_npcs_by_city(charles_info[1], charles_info[0], 3)
        self.assertEqual(0, outcome.__len__(), "Shouldn't have gotten any NPCs in Charlote")

    def test_get_specials_in_city(self):
        """
        This test will simulate loading the specials
        in a city as an admin and a user
        """
        rebuild_tables()
        load_data()

        beck_info = login_user('Beck', 'RiamChesteroot26')
        charles_info = login_user('Charles', 'CalvionNeedsAA')

        # loading the specials in Meridia as an admin, expecting 1 result
        outcome = get_specials_by_city(beck_info[1], beck_info[0], 5)
        self.assertEqual(1, outcome.__len__(), "didn't get all of the specials in Meridia")

        # loading the specials in Meridia as a user, expecting 0 results
        outcome = get_specials_by_city(charles_info[1], charles_info[0], 5)
        self.assertEqual(0, outcome.__len__(), "got too many specials in Meridia")


if __name__ == '__main__':
    unittest.main()
