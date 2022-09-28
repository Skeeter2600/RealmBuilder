import json
import unittest

from src.components.users import *
from src.utils.table_manager import rebuild_tables
from tests.test_builders.test_build import load_data


class MyTestCase(unittest.TestCase):

    def test_create_account(self):
        """
        This function will test the creation of a
        new account.
        """
        rebuild_tables()
        load_data()

        print("\n Making a new account where another individual had the same username:\n"
              "    username: Beck\n"
              "    password: password\n"
              "    email: test1@test.com\n")
        result = create_user('Beck', 'password', 'test1@test.com')
        print("logging in returned: '" + result + "' (should be 'A user with that username already exists')\n\n")
        self.assertEqual(result, "A user with that username already exists",
                         "shouldn't work with user with the same username")

        print("\n Making a new account where another individual had a different username:\n"
              "    username: Beck Jr\n"
              "    password: password\n"
              "    email: test1@test.com\n")
        result = create_user('Beck Jr', 'password', 'test1@test.com')
        print("logging in returned: '" + result + "' (should be 'Success!')\n\n")
        self.assertEqual(result, "Success!", "should work as it is unique")

    def test_delete_user(self):
        """
        This function will test the deleting of a user
        """
        rebuild_tables()
        load_data()

        print("\n Deleting the user Beck by Ryan R:\n")

        ryan_session_key = login_user('RyanR', 'PabloWeegee69')

        outcome = delete_user(1, ryan_session_key)
        print("Delete request returned: " + str(outcome) + ". (should be False)")
        self.assertFalse(outcome, "Ryan shouldn't be able to delete Beck")

        print("\n Deleting the user RyanR by Ryan R:\n")
        outcome = delete_user(2, ryan_session_key)
        print("Delete request returned: " + str(outcome) + ". (should be True)")
        self.assertTrue(outcome, "Ryan should be able to delete himself")

        print("checking if RyanR exists:\n")
        outcome = get_user_public(2)
        check_values = {'username': '',
                        'profile_pic': '',
                        'bio': '',
                        'worlds': []}
        print("Get Request returned: " + json.dumps(outcome) + ". (should be " + json.dumps(check_values) + ')')
        self.assertEqual(outcome, check_values, "Somehow got values for a deleted user")

    def test_edit_user(self):
        """
        This function will test the editing of a user
        """
        rebuild_tables()
        load_data()

        ryan_session_key = login_user('RyanR', 'PabloWeegee69')

        details = {'username': 'Ryan2',
                   'profile_pic': None,
                   'public': True,
                   'bio': 'Testing'}

        outcome = edit_account(1, ryan_session_key, details)
        self.assertFalse(outcome, "Ryan shouldn't be able to edit Beck")

        outcome = edit_account(2, ryan_session_key, details)
        self.assertTrue(outcome, "Ryan should be able to edit himself")

        check_values = {'username': 'Ryan2',
                        'profile_pic': None,
                        'bio': 'Testing',
                        'worlds': 'not testing this'}

        outcome = get_user_public(2)
        self.assertEqual(check_values['username'], outcome['username'], 'Should have gotten Ryan2 as the username')
        self.assertEqual(check_values['profile_pic'], outcome['profile_pic'], 'Should have gotten None as the profile pic')
        self.assertEqual(check_values['bio'], outcome['bio'], "Should have gotten 'Testing' as the bio")

    def test_get_user_public(self):
        """
        This will test the getting of a user's public info
        """
        rebuild_tables()
        load_data()

        print("Getting a nonexistent user: id = 999")
        outcome = get_user_public(999)
        check_values = {'username': '',
                        'profile_pic': '',
                        'bio': '',
                        'worlds': []}
        print("Get request returned: " + json.dumps(outcome) + ". (should be " + json.dumps(check_values) + ")")
        self.assertEqual(outcome, check_values, "Should not have gotten info for nonexistent person")

        print("Getting a user Jacob: id = 8")
        outcome = get_user_public(8)
        check_values = {'username': 'Jacob',
                        'profile_pic': None,
                        'bio': 'Bruh.',
                        'worlds': [{'id': 6, 'name': 'Real World'}]}
        print("Get request returned: " + json.dumps(outcome) + ". (should be " + json.dumps(check_values) + ")")
        self.assertEqual(outcome, check_values, "Should have gotten info for Jacob")

    def test_login(self):
        """
        This test will ensure that logins are working
        properly, and we can get info
        """
        rebuild_tables()
        load_data()

        # logging in existing user with bad credentials
        print("\nLogging in an existing user with bad password:\n"
              "    username: Beck\n"
              "    password: RiamChesteroot1\n")
        result = login_user('Beck', 'RiamChesteroot1')

        print("logging in returned: " + result + " (should be 'Bad username or password')\n\n")
        self.assertEqual(result, "Bad username or password", "Shouldn't have been the right password")

        # logging in user that doesn't exist
        print("Logging in an existing user with information:\n"
              "    username: billyBob67\n"
              "    password: password123456\n")

        result = login_user('billyBob67', 'password123456')

        print("logging in returned: " + result + " (should be 'Bad username or password')\n\n")
        self.assertEqual(result, "Bad username or password", "Shouldn't have been the right password")

        # logging in existing user with good credentials
        print("\nLogging in an existing user with bad password:\n"
              "    username: Beck\n"
              "    password: RiamChesteroot26\n")
        new_key = login_user('Beck', 'RiamChesteroot26')

        print("logging in returned: " + new_key + " (should be session key)\n\n")
        self.assertNotEqual(new_key, "Bad username or password", "Should have been the right password")

        # try with bad session key
        print("\nChecking a bad session key:\n"
              "    user id: 1 (Beck)\n"
              "    bad key: test\n"
              "    good session key:" + new_key + "\n")
        result = check_session_key(1, 'test')

        print("check returned: " + str(result) + " (should be False)\n\n")
        self.assertFalse(result, "shouldn't have been the proper session key")

        # try with good new session key
        print("\nChecking a good session key:\n"
              "    user id: 1 (Beck)\n"
              "    session key:" + new_key + "\n")
        result = check_session_key(1, new_key)

        print("check returned: " + str(result) + " (should be True)\n\n")
        self.assertTrue(result, "should have been the proper session key")

    def test_logout(self):
        """
        This test will make sure that the logout
        function is working properly
        """
        rebuild_tables()
        load_data()

        # log in two users
        taylor_key = login_user('Taylor', 'TomathyPickles123')
        josh_key = login_user('Josh', 'ShadowWatcher58')
        self.assertNotEqual(taylor_key, "Bad username or password", "Should have been the right password")
        self.assertNotEqual(josh_key, "Bad username or password", "Should have been the right password")
        print("\nLogging in two users:\n"
              "    user 1: \n"
              "        Username:    Taylor\n"
              "        ID:          6\n"
              "        Password:    TomathyPickles123\n"
              "        Session Key: " + taylor_key + "\n"
              "    user 2: \n"
              "        Username:    Josh\n"
              "        ID:          7\n"
              "        Password:    ShadowWatcher58\n"
              "        Session Key: " + josh_key + "\n\n")

        print("\nValidating both sessions:")
        taylor_result = check_session_key(6, taylor_key)
        josh_result = check_session_key(7, josh_key)

        print("    check returned: \n"
              "        Taylor Results: " + str(taylor_result) + " (should be True)\n"
              "        Josh Results:   " + str(josh_result) + " (should be True)\n\n")
        self.assertTrue(taylor_result, "should have been the proper session key for Taylor")
        self.assertTrue(josh_key, "should have been the proper session key for Josh")

        print("\nTrying to log Taylor out with bad session key:")
        taylor_result = logout_user(6, 'test')

        print("     check returned: " + taylor_result + " (should be 'bad request')\n\n")
        self.assertEqual(taylor_result, "bad request", "shouldn't have been the proper session key")

        print("\nTrying to log Josh out with bad session key:")
        josh_result = logout_user(7, 'test')

        print("     check returned: " + josh_result + " (should be 'bad request')\n\n")
        self.assertEqual(josh_result, "bad request", "shouldn't have been the proper session key")

        print("\nTrying to log Josh out with Taylor's key:")
        josh_result = logout_user(7, taylor_key)

        print("    check returned: " + josh_result + " (should be 'bad request')\n\n")
        self.assertEqual(josh_result, "bad request", "shouldn't have been the proper session key")

        print("\nTrying to log Taylor out with Josh's key:")
        taylor_result = logout_user(6, josh_key)

        print("    check returned: " + taylor_result + " (should be 'bad request')\n\n")
        self.assertEqual(taylor_result, "bad request", "shouldn't have been the proper session key")

        print("\nTrying to log Taylor out with Taylor's key:")
        taylor_result = logout_user(6, taylor_key)

        print("    check returned: " + taylor_result + " (should be 'signed out')\n\n")
        self.assertEqual(taylor_result, "signed out", "should have been the proper session key")

        print("\nTrying to log Josh out with Josh's key:")
        josh_result = logout_user(7, josh_key)

        print("    check returned: " + josh_result + " (should be 'signed out')\n\n")
        self.assertEqual(josh_result, "signed out", "should have been the proper session key")

        print("\nTrying old session keys:")
        taylor_result = check_session_key(6, taylor_key)
        josh_result = check_session_key(7, josh_key)

        print("    check returned: \n"
              "        Taylor Results: " + str(taylor_result) + " (should be False)\n"
              "        Josh Results:   " + str(josh_result) + " (should be False)\n\n")
        self.assertFalse(taylor_result, "should not have been the proper session key for Taylor")
        self.assertFalse(josh_result, "should not have been the proper session key for Josh")

        print("\nTrying blank (logged out users have no session key):")
        taylor_result = check_session_key(6, taylor_key)
        josh_result = check_session_key(7, josh_key)

        print("    check returned: \n"
              "        Taylor Results: " + str(taylor_result) + " (should be False)\n"
              "        Josh Results:   " + str(josh_result) + " (should be False)\n\n")
        self.assertFalse(taylor_result, "should not have been the proper session key for Taylor")
        self.assertFalse(josh_result, "should not have been the proper session key for Josh")

    def test_search_users(self):
        """
        This function will test the searching
        for users
        """
        rebuild_tables()
        load_data()

        # log in two users
        taylor_key = login_user('Taylor', 'TomathyPickles123')
        josh_key = login_user('Josh', 'ShadowWatcher58')

        outcome = search_user('o', None, 1, 7, josh_key)
        self.assertEqual(3, len(outcome), "Should have gotten the other 3 users with o in their usernames")

        outcome = search_user('o', None, 1, 6, taylor_key)
        self.assertEqual(3, len(outcome), "Should have gotten the 3 users with o in their usernames and are public")


if __name__ == '__main__':
    unittest.main()
