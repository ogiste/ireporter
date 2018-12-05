"""
Testcase for the database connection success
"""
import unittest
import StringIO
import sys
import types

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
        self.conn = connect("ireporter_test")
        self.create_tables_message = "Tables created"
        self.drop_tables_message = "Tables dropped"

    def test_create_tables(self):
        """
        Method that is called to test the created tables
        """
        capturedOutput = StringIO.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput                   # and redirect stdout.
        create_tables()                               # Call unchanged function
        sys.stdout = sys.__stdout__                   # Reset redirect.
        print 'Captured', capturedOutput.getvalue()   # Now works as before.
        self.assertIn(self.create_tables_message, capturedOutput.getvalue())

    def test_drop_tables(self):
        """
        Method that is called to test the dropped tables
        """
        capturedOutput = StringIO.StringIO()          # Create StringIO object
        sys.stdout = capturedOutput                   # and redirect stdout.
        drop_tables()                               # Call unchanged function
        sys.stdout = sys.__stdout__                   # Reset redirect.
        print 'Captured ', capturedOutput.getvalue()   # Now works as before.
        self.assertIn(self.drop_tables_message, capturedOutput.getvalue())

    def test_get_create_queries(self):
        """
        Method to test the get_create_queries method of the db config
        """
        self.assertIsInstance(get_create_queries(), types.ListType)

    def test_get_drop_queries(self):
        """
        Method to test the get_drop_queries method of the db config
        """
        self.assertIsInstance(get_drop_queries(), types.ListType)

    def tearDown(self):
        self.conn.close()
