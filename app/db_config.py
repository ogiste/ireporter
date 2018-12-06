"""
Define the database URL to connect to using the psycopg2 connector to postgres
database.

Functions
---------
connection(url)
    Takes a db_url parameter that is used to establishes a connection
    with pyscopg2 that is used in all database
    operations create,select,drop and update.

connect():
    returns the connection object created with a particular db_url in the
    connection(url) function

create_tables():
    creates all tables using the connection established by the connnection
    method.

get_create_queries():
    returns the list of all table creation queries used in create_tables()

drop_tables():
    drops all tables created in the database

get_drop_queries():
    returns list of queries used in drop_tables
"""

import os
import psycopg2
from pprint import pprint
conn = None


def connection(db_name=None):
    """
    Function that creates a database connection using psycopg2 library to
    connect using a database uri

    Returns
    -------
        psycopg2 connection object
    """
    db_host = os.getenv("DB_HOST", default="localhost")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_port = os.getenv("DB_PORT", default=5432)
    if db_name is None:
        db_name = os.getenv("DB_NAME", default="ireporter")
    db_uri = "dbname={} host={} user={} password={} port={} ".\
        format(db_name, db_host, db_user, db_pass, db_port)
    if db_name is "ireporter_test":
        db_uri = "dbname={} host={} user={} password={}".\
            format(db_name, "localhost", 'test_user', 'test_ireporter')
    try:
        conn = psycopg2.connect(db_uri)
        conn.autocommit = True
        pprint("Database Connection established")
    except Exception:
        pprint("Cannot connect to database")
    return conn


def connect(db_name=None):
    """
    Function to return the established database connection

    Returns
    -------
        psycopg2 connection object
    """
    conn = connection(db_name)
    return conn


def create_tables():
    """
    Function to create all tables relevant to the database
    """
    conn = connect()
    cur = conn.cursor()
    queries = get_create_queries()
    for query in queries:
        cur.execute(query)
    conn.close()
    pprint("Tables created")


def get_create_queries():
    """
    Function that gets all queries defining the database tables to be created

    Returns
    -------
        list of all queries used in database table creation
    """
    create_user_table = """
    CREATE TABLE IF NOT EXISTS users(
    id serial PRIMARY KEY,
    fname VARCHAR(30) NOT NULL,
    lname VARCHAR(30) NOT NULL,
    othername VARCHAR(30) NOT NULL,
    email VARCHAR(60) NOT NULL,
    phone VARCHAR(12) NOT NULL,
    password VARCHAR(100) NOT NULL,
    isAdmin BOOLEAN NOT NULL DEFAULT false,
    createdOn DATE NOT NULL
    );
    """
    create_incident_table = """
    CREATE TABLE IF NOT EXISTS incidents(
    id serial PRIMARY KEY,
    createdBy INT NOT NULL,
    title VARCHAR(30) NOT NULL,
    type VARCHAR(12) NOT NULL,
    comment VARCHAR(100) NOT NULL,
    status VARCHAR(18) NOT NULL,
    location VARCHAR(40) NOT NULL,
    createdOn DATE NOT NULL,
    FOREIGN KEY (createdBy) REFERENCES users(id)
    );
    """

    return [create_user_table, create_incident_table]


def drop_tables():
    """
    Function that drops all created tables
    """
    conn = connect()
    cur = conn.cursor()
    queries = get_drop_queries()
    for query in queries:
        cur.execute(query)
    conn.close()
    pprint("Tables dropped")


def get_drop_queries():
    """
    Function that gets all queries defining the drop statements for db tables

    Returns
    -------
        list of all queries used in database table removal
    """
    drop_user_table = "DROP table if exists users CASCADE;"
    drop_incident_table = "DROP table if exists incidents CASCADE;"
    return [drop_user_table, drop_incident_table]


if __name__ == '__main__':
    connection()
    create_tables()
    drop_tables()
