import unittest
from src.worlds import *
from src.db_utils import connect


class TestChat(unittest.TestCase):

    def rebuild_tables(self):
        """Build the tables"""
        conn = connect()
        cur = conn.cursor()
        build_worlds()
        cur.execute('SELECT * FROM example_table')
        self.assertEqual([], cur.fetchall(), "no rows in example_table")
        conn.close()

    def test_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        self.rebuild_tables()
        self.rebuild_tables()
        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM example_table')
        self.assertEqual([], cur.fetchall(), "no rows in example_table")
        conn.close()
