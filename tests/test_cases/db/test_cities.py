import unittest

from src.components.cities import *
from src.components.users import login_user
from src.utils.table_manager import rebuild_tables
from tests.test_builders.test_build import load_data


class MyTestCase(unittest.TestCase):

    def test_get_city(self):
        """
        This test will test the getting of a city
        as an admin and as a user
        """
        rebuild_tables()
        load_data()

        # login an admin for Greenest (Ryan C) and an admin for Jamestown (Ryan R)
        ryan_r_session_key = login_user('RyanR', 'PabloWeegee69')
        ryan_c_session_key = login_user('RyanC', 'ThuaccTwumps')

        # should get Jamestown for both
        outcome = get_city(2, ryan_r_session_key, 4, True)
        self.assertEqual("Jamestown", outcome[0][1], "not the right city name")
        outcome = get_city(3, ryan_c_session_key, 4, False)
        self.assertEqual("Jamestown", outcome[0][1], "not the right city name")

        # should get Greenest for both
        outcome = get_city(3, ryan_c_session_key, 2, True)
        self.assertEqual("Greenest", outcome[0][1], "not the right city name")
        outcome = get_city(2, ryan_r_session_key, 2, False)
        self.assertEqual([], outcome, "shouldn't get anything (not revealed)")

    def test_get_cities(self):
        """
        This test will test searching, both as an admin
        and as a normal user
        """
        rebuild_tables()
        load_data()

        beck_session_key = login_user('Beck', 'RiamChesteroot26')
        charles_session_key = login_user('Charles', 'CalvionNeedsAA')

        # searching in Savior's Cradle for all cities as admin, should be 3
        outcome = get_cities(1, beck_session_key, 3, None, 1)
        self.assertEqual(3, outcome.__len__(), "not the right number of cities")

        # searching in Savior's Cradle for all cities as normal user, should be 2
        outcome = get_cities(1, charles_session_key, 3, None, 1)
        self.assertEqual(2, outcome.__len__(), "not the right number of cities")

    def test_search_cities(self):
        """
        This test will simulate searching for cities
        both as a user and as an admin
        """
        rebuild_tables()
        load_data()

        beck_session_key = login_user('Beck', 'RiamChesteroot26')
        charles_session_key = login_user('Charles', 'CalvionNeedsAA')

        # searching for cities with the string 'Meridia' as an admin, expecting 2 results
        outcome = search_for_city('Meridia', 3, None, 1, 1, beck_session_key)
        self.assertEqual([{'name': 'New Meridia', 'population': 10392, 'reveal_status': False},
                          {'name': 'Meridia', 'population': 1392, 'reveal_status': True}],
                         outcome, "not the right cities")

        # searching for cities with the string 'Meridia' as a user, expecting 1 result
        outcome = search_for_city('Meridia', 3, None, 1, 4, charles_session_key)
        self.assertEqual([{'name': 'Meridia', 'population': 1392}], outcome, "not the right cities")

        outcome = search_for_city('e', 3, None, 1, 1, beck_session_key)
        self.assertEqual(len(outcome), 3, "not the right number of cities")

        outcome = search_for_city('e', 3, None, 1, 4, charles_session_key)
        self.assertEqual(len(outcome), 2, "not the right number of cities")

    def test_get_npcs_in_city(self):
        """
        This test will simulate loading the npcs
        in a city as an admin and a user
        """
        rebuild_tables()
        load_data()

        # loading the npcs in Meridia as an admin, expecting 2 results
        outcome = get
        self.assertEqual(2, outcome.__len__(), "didn't get all of the NPCs in Meridia")

        # loading the npcs in Meridia as a user, expecting 1 result
        outcome = get_npcs_in_city(5, False)
        self.assertEqual(1, outcome.__len__(), "didn't get all of the NPCs in Meridia")

        # loading the npcs in Charlote as an admin, expecting 1 result
        outcome = get_npcs_in_city(3, True)
        self.assertEqual(1, outcome.__len__(), "didn't get all of the NPCs in Charlote")

        # loading the npcs in Charlote as an admin, expecting 0 results
        outcome = get_npcs_in_city(3, False)
        self.assertEqual(0, outcome.__len__(), "Shouldn't have gotten any NPCs in Charlote")


if __name__ == '__main__':
    unittest.main()
