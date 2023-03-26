import mysql.connector
import pymysql
import psycopg2
import utils.config as config

# used to create database

class MysqlConn4DB:
    def __init__(self, host, user, password, port) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.password
        )
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


class MysqlConn:
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.db = db

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, db=self.db, charset="utf8")
        self.cursor = self.conn.cursor()
        return self.cursor


    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


class PostgresqlConn:
    """pg connection"""

    def __init__(self, host, port, user, password, db, options=None):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.db = db
        self.options = options
    def __enter__(self):
        self.conn = psycopg2.connect(database=self.db, user=self.user,
                                     password=self.password, host=self.host, port=self.port, options=self.options)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

