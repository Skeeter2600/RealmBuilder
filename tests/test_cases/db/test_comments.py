import unittest

from src.components.comments import *
from src.components.users import login_user
from src.utils.table_manager import rebuild_tables
from tests.test_builders.test_build import load_data


class MyTestCase(unittest.TestCase):

    def test_add_comment(self):
        """
        This function will test adding a comment to a component
        """
        rebuild_tables()
        load_data()

        ryan_r_session_key = login_user('RyanR', 'PabloWeegee69')

        outcome = add_comment(2, ryan_r_session_key, 1, 1, 'npc', "testing")
        self.assertTrue(outcome[0], "Comment should have been able to be made")

        outcome = get_comment(outcome[1])
        self.assertEqual(outcome['comment'], "testing", "Got the wrong comment info")

    def test_delete_comment(self):
        """
        This function will test the deleting of a comment
        both by the user, a random one, and an admin/owner
        """
        rebuild_tables()
        load_data()

        ryan_r_session_key = login_user('RyanR', 'PabloWeegee69')
        ryan_c_session_key = login_user('RyanC', 'ThuaccTwumps')
        beck_session_key = login_user('Beck', 'RiamChesteroot26')

        outcome = add_comment(2, ryan_r_session_key, 1, 1, 'npcs', "testing")
        self.assertTrue(outcome[0], "Comment should have been able to be made")

        comment_id = outcome[1]

        outcome = get_comment(comment_id)
        self.assertEqual(outcome['comment'], "testing", "Got the wrong comment info")

        outcome = delete_comment(3, ryan_c_session_key, comment_id)
        self.assertFalse(outcome, "Should not have been able to delete someone else's comment unless admin")

        outcome = delete_comment(2, ryan_r_session_key, comment_id)
        self.assertFalse(outcome, "Should have been able to delete their own comment")

        outcome = add_comment(2, ryan_r_session_key, 1, 1, 'npcs', "testing")
        self.assertTrue(outcome[0], "Comment should have been able to be made")

        comment_id = outcome[1]

        outcome = delete_comment(1, beck_session_key, comment_id)
        self.assertFalse(outcome, "Should have been able to delete since they are the owner")

    def test_get_component_comments(self):
        """
        This function will test the getting of the comments
        on a component
        """
        rebuild_tables()
        load_data()

        ryan_r_session_key = login_user('RyanR', 'PabloWeegee69')

        outcome = add_comment(2, ryan_r_session_key, 2, 5, 'npcs', "testing")
        self.assertTrue(outcome[0], "Comment should have been able to be made")

        outcome = get_component_comments(5, 'npcs')
        self.assertEqual(2, len(outcome), "should have gotten 2 comments")

    def test_get_user_comments(self):
        """
        This function will test the getting of the comments
        made by a user
        """
        rebuild_tables()
        load_data()

        outcome = get_user_comments(3, None, 1)
        self.assertEqual(2, len(outcome), "should have gotten 2 comments made by RyanC")

        outcome = get_user_comments(5, None, 1)
        self.assertEqual(3, len(outcome), "should have gotten 3 comments made by Nolan")


if __name__ == '__main__':
    unittest.main()
