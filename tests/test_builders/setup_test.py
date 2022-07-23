import unittest
from src.utils.db_utils import connect
from src.utils.table_manager import rebuild_tables
from tests.test_builders.test_build import load_data


class TestPostgreSQL(unittest.TestCase):

    def test_can_connect(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT VERSION()')
        self.assertTrue(cur.fetchone()[0].startswith('PostgreSQL'))
        conn.close()

    def test_reset_tables(self):
        """
        This will wipe all tables
        DO NOT USE IN PRODUCTION EVER
        """
        conn = connect()
        cur = conn.cursor()
        rebuild_tables()
        cur.execute('SELECT * FROM users')
        self.assertEqual([], cur.fetchall(), "no rows in example_table")
        conn.close()

    def test_rebuild_tables(self):
        """
        This will wipe all tables
        DO NOT USE IN PRODUCTION EVER
        """
        conn = connect()
        cur = conn.cursor()
        rebuild_tables()
        load_data()
        cur.execute('SELECT COUNT(username) FROM users')
        self.assertEqual(8, cur.fetchall()[0][0], "no rows in example_table")
        conn.close()


if __name__ == '__main__':
    unittest.main()
