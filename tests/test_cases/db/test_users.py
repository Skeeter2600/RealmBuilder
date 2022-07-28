import unittest

from src.components.users import *
from src.utils.table_manager import rebuild_tables
from tests.test_builders.test_build import load_data


class MyTestCase(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
