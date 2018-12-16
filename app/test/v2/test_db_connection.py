"""
Testcase for the database connection success
"""
import unittest
import os

from app.db_config import connect, create_tables, drop_tables,\
    get_create_queries, get_drop_queries


class TestIncidents(unittest.TestCase):
    """
    Class defining tests for verifying database connection
    """

    def setUp(self):
        """
        Method that is called to set the default connection and messages for
        for testing.
        """
        db_name = os.getenv("DB_NAME", default="tester")
        self.conn = connect(db_name)
        self.create_tables_message = "Tables created"
        self.drop_tables_message = "Tables dropped"

    def test_create_tables(self):
        """
        Method that is called to test the created tables
        """
        create_success = create_tables(self.conn)
        self.assertTrue(create_success)

    def test_drop_tables(self):
        """
        Method that is called to test the dropped tables
        """
        drop_success = drop_tables(self.conn)
        self.assertTrue(drop_success)

    def test_get_create_queries(self):
        """
        Method to test the get_create_queries method of the db config
        """
        self.assertIsInstance(get_create_queries(), list)

    def test_get_drop_queries(self):
        """
        Method to test the get_drop_queries method of the db config
        """
        self.assertIsInstance(get_drop_queries(), list)

    def tearDown(self):
        self.conn.close()
