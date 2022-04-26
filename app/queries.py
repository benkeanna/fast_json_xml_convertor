"""Queries module."""
import contextlib

import psycopg2

from app.errors import QueryError


@contextlib.contextmanager
def cursor():
    """Returns cursor to DB. Handles connection closing."""
    conn = psycopg2.connect("dbname=fast user=username password=password host=db")
    cur = conn.cursor()

    yield cur

    conn.commit()
    cur.close()
    conn.close()


def get_user(email):
    """Returns text value according to given email. Raises QueryError when user does not exist."""
    with cursor() as cur:
        sql = """SELECT "text" FROM "user" WHERE "email" = %s;"""
        cur.execute(sql, (email,))
        try:
            return cur.fetchone()[0]
        except TypeError as error:
            raise QueryError('Entry does not exist.') from error


def create_user(email_value, text_value):
    """Returns email value of created user. Raises QueryError when user already exists exist."""
    with cursor() as cur:
        sql = """INSERT INTO "user" VALUES(%s, %s)
                 ON CONFLICT (email) DO UPDATE SET text = EXCLUDED.text RETURNING email;"""
        try:
            cur.execute(sql, (email_value, text_value,))
            return cur.fetchone()[0]
        except psycopg2.errors.UniqueViolation as error:
            raise QueryError('Duplicate entry.') from error


def delete_user(email):
    """Returns email value of deleted user. Raises QueryError when user does not exist in."""
    with cursor() as cur:
        sql = """DELETE FROM "user" WHERE "email" = (%s) RETURNING email;"""

        cur.execute(sql, (email,))
        try:
            return cur.fetchone()[0]
        except TypeError as error:
            raise QueryError('Entry does not exist.') from error


def get_all_users(limit, offset):
    """Returns all users wth given limit and offset. Raises QueryError when user does not exist."""
    with cursor() as cur:
        sql = """SELECT * FROM "user" ORDER BY email limit %s offset %s;"""
        cur.execute(sql, (limit, offset,))
        return cur.fetchall()
