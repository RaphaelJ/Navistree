#!/usr/bin/python
#-*- coding: Utf-8 -*-

import psycopg2, navistree

DBNAME = 'navistree'

USER = 'navistree'
PASSWORD = 'YqD8K6hYr'

class Connection():
    def __init__(self):
        self.conn = psycopg2.connect(database=DBNAME,
            user=USER, password=PASSWORD)

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        return self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return isinstance(value, TypeError)
