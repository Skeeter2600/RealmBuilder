import unittest

from src.components.users import login_user
from src.utils.table_manager import rebuild_tables
from tests.test_builders.test_build import load_data
from src.components.worlds import *


class MyTestCase(unittest.TestCase):

    def test_add_world(self):
        """
        This function will test the adding of a world
        """
        rebuild_tables()
        load_data()

        taylor_session_key = login_user('Taylor', 'TomathyPickles123')
        beck_session_key = login_user('Beck', 'RiamChesteroot26')

        # bad user session key combo
        outcome = add_world('Test World', 1, taylor_session_key)
        self.assertFalse(outcome[0], "should have been bad session key")

        outcome = add_world('Test World', 6, taylor_session_key)
        self.assertTrue(outcome[0], "should have been good to make")

        world_id = outcome[1]

        expected = {'valid': True,
                    'name': 'Test World',
                    'description': '',
                    'npcs': [],
                    'cities': [],
                    'specials': [],
                    'comments': [],
                    'user_list': [{'id': 6,
                                   'username': 'Taylor',
                                   'profile_picture': None}]
                    }

        # get info by user with bad session key
        outcome = get_world_details(world_id, 1, taylor_session_key)
        self.assertFalse(outcome['valid'], "should have not been a good session")

        # get info by user not in world
        outcome = get_world_details(world_id, 1, beck_session_key)
        self.assertFalse(outcome['valid'], "should have not been a good session")

        # get info by user with bad session key
        outcome = get_world_details(world_id, 6, taylor_session_key)
        self.assertEqual(expected, outcome, "should have gotten the right info")

    def test_delete_world(self):
        """
        This function will test the deleting of a world.
        This will be done by a user, admin, and owner
        """
        rebuild_tables()
        load_data()

        taylor_session_key = login_user('Taylor', 'TomathyPickles123')
        beck_session_key = login_user('Beck', 'RiamChesteroot26')

        outcome = delete_world(3, 6, taylor_session_key)
        self.assertFalse(outcome, "Should not be able to delete world")

        outcome = delete_world(3, 1, beck_session_key)
        self.assertTrue(outcome, "Should have been able to delete world")

        expected = {'valid': False,
                    'name': '',
                    'description': '',
                    'npcs': [],
                    'cities': [],
                    'specials': [],
                    'comments': [],
                    'user_list': []
                    }

        outcome = get_world_details(3, 1, beck_session_key)
        self.assertEqual(expected, outcome, "Shouldn't get info for non existent world")

    def test_edit_world(self):
        """
        This function will test the editing of a world.
        This will be done by a user and an admin/owner
        """
        rebuild_tables()
        load_data()

        taylor_session_key = login_user('Taylor', 'TomathyPickles123')
        beck_session_key = login_user('Beck', 'RiamChesteroot26')
        jacob_session_key = login_user('Jacob', 'MarkFellowsRulez')

        values = {'name': 'test',
                  'description': 'New description',
                  'public': False
                  }

        outcome = get_world_details(3, 8, jacob_session_key)
        self.assertTrue(outcome['valid'], "The world is not public, so he shouldn't see it")

        outcome = edit_world(3, 6, taylor_session_key, values)
        self.assertFalse(outcome, "Taylor should not be able to edit the world")

        outcome = edit_world(3, 1, beck_session_key, values)
        self.assertTrue(outcome, "Beck should be able to edit the world")

        outcome = get_world_details(3, 8, jacob_session_key)
        self.assertFalse(outcome['valid'], "The world is public now")

        outcome = get_world_details(3, 1, beck_session_key)
        self.assertTrue(outcome['valid'], "The world is public, so he should see it")
        self.assertEqual(values['name'], outcome['name'], "Didn't get the right details")
        self.assertEqual(values['description'], outcome['description'], "Didn't get the right details")

    def test_join_world(self):
        """
        This function will test joining a world.
        This is done privately and publicly
        """
        rebuild_tables()
        load_data()

        jacob_session_key = login_user('Jacob', 'MarkFellowsRulez')
        beck_session_key = login_user('Beck', 'RiamChesteroot26')

        # look at private world not in
        outcome = get_world_details(1, 8, jacob_session_key)
        self.assertFalse(outcome['valid'], "Shouldn't see a private world")

        # try to join private world publicly
        outcome = join_world_public(1, 8, jacob_session_key)
        self.assertFalse(outcome, "World is private, can't join publicly")

        # get member count before join
        member_count_before = len(get_world_details(3, 1, beck_session_key)['user_list'])

        # join the world publicly
        outcome = join_world_public(3, 8, jacob_session_key)
        self.assertTrue(outcome, "World is public, can join publicly")

        # get member count after join
        member_count_after = len(get_world_details(3, 1, beck_session_key)['user_list'])
        self.assertEqual(member_count_before+1, member_count_after, "didn't join properly")

        # try to join private world privately
        outcome = join_world_private(1, 8, 8, jacob_session_key)
        self.assertFalse(outcome, "isn't an admin or owner of the world")

        # get member count before join
        member_count_before = len(get_world_details(1, 1, beck_session_key)['user_list'])

        # have beck add jacob to the world
        outcome = join_world_private(1, 8, 1, beck_session_key)
        self.assertTrue(outcome, "is an admin or owner of the world")

        # get member count after join
        member_count_after = len(get_world_details(1, 1, beck_session_key)['user_list'])
        self.assertEqual(member_count_before + 1, member_count_after, "didn't join properly")

    def test_get_owner(self):
        """
        This function will test getting the owner of a world.
        """
        rebuild_tables()
        load_data()

        dralbrar = get_owner(1)
        saltmarsh = get_owner(2)
        saviors = get_owner(3)
        bad_world = get_owner(999)

        self.assertEqual(dralbrar, saviors, "have the same owner")

        self.assertEqual(saltmarsh['id'], 3, 'bad owner info')
        self.assertEqual(saltmarsh['name'], 'RyanC', 'bad owner info')
        self.assertEqual(saltmarsh['profile_pic'], None, 'bad owner info')

        self.assertEqual(bad_world['id'], '', 'bad owner info')
        self.assertEqual(bad_world['name'], '', 'bad owner info')
        self.assertEqual(bad_world['profile_pic'], '', 'bad owner info')

    def test_get_world_user_list(self):
        """
        This function will test getting the list of users
        in a world
        """
        rebuild_tables()
        load_data()

        ryan_c_session_key = login_user('RyanC', 'ThuaccTwumps')
        beck_session_key = login_user('Beck', 'RiamChesteroot26')
        jacob_session_key = login_user('Jacob', 'MarkFellowsRulez')

        # no permission for private world
        outcome = get_world_user_list(1, 8, jacob_session_key)
        self.assertEqual([], outcome, "shouldn't see any users in world that's private")

        # in private world
        outcome = get_world_user_list(5, 3, ryan_c_session_key)
        self.assertEqual(3, len(outcome), 'should have 3 users in Out of Touch')

        # from public world not in it
        outcome = get_world_user_list(3, 8, jacob_session_key)
        self.assertEqual(6, len(outcome), 'should have 6 users in Saviors Cradle')

        # from public world in it
        outcome = get_world_user_list(3, 1, beck_session_key)
        self.assertEqual(6, len(outcome), 'should have 6 users in Saviors Cradle')

    def test_world_search(self):
        """
        This function will test the searching of worlds that
        are in the system. This will be include searching for
        private ones by people in them and outside, as well as
        for public ones.
        """
        rebuild_tables()
        load_data()

        beck_session_key = login_user('Beck', 'RiamChesteroot26')
        taylor_session_key = login_user('Taylor', 'TomathyPickles123')

        beck_expected = [
            {'id': 1, 'name': 'Dralbrar'},
            {'id': 2, 'name': 'Saltmarsh'},
            {'id': 3, 'name': "Saviors' Cradle Sword Coast"},
            {'id': 4, 'name': "Three Lords Sword Coast"},
            {'id': 6, 'name': 'Real World'}
        ]

        taylor_expected = [
            {'id': 2, 'name': 'Saltmarsh'},
            {'id': 3, 'name': "Saviors' Cradle Sword Coast"},
            {'id': 4, 'name': "Three Lords Sword Coast"},
            {'id': 6, 'name': 'Real World'}
        ]

        outcome = search_world('a', None, 1, 1, beck_session_key)
        self.assertEqual(beck_expected, outcome, "didn't get the right worlds")

        outcome = search_world('a', None, 1, 6, taylor_session_key)
        self.assertEqual(taylor_expected, outcome, "didn't get the right worlds")

        beck_expected = [
            {'id': 3, 'name': "Saviors' Cradle Sword Coast"},
            {'id': 4, 'name': "Three Lords Sword Coast"}
        ]

        outcome = search_world('Sword Coast', None, 1, 1, beck_session_key)
        self.assertEqual(beck_expected, outcome, "didn't get the right worlds")


if __name__ == '__main__':
    unittest.main()
