import psycopg2
import contextlib

from app.errors import QueryError


@contextlib.contextmanager
def cursor():
    conn = psycopg2.connect("dbname=fast user=username password=password host=db")
    cur = conn.cursor()

    yield cur

    conn.commit()
    cur.close()
    conn.close()


def get_user(email):
    with cursor() as cur:
        sql = """SELECT "text" FROM "user" WHERE "email" = %s;"""
        cur.execute(sql, (email,))
        try:
            return cur.fetchone()[0]
        except TypeError:
            raise QueryError('Entry does not exist.')


def create_user(email_value, text_value):
    with cursor() as cur:
        sql = """INSERT INTO "user" VALUES(%s, %s) ON CONFLICT (email) DO UPDATE SET text = EXCLUDED.text RETURNING email;"""
        try:
            cur.execute(sql, (email_value, text_value,))
            return cur.fetchone()[0]
        except psycopg2.errors.UniqueViolation:
            raise QueryError('Duplicate entry.')


def delete_user(email):
    with cursor() as cur:
        sql = """DELETE FROM "user" WHERE "email" = (%s) RETURNING email;"""

        cur.execute(sql, (email,))
        try:
            return cur.fetchone()[0]
        except TypeError:
            raise QueryError('Entry does not exist.')


def get_all_users(limit, offset):
    with cursor() as cur:
        sql = """SELECT * FROM "user" ORDER BY email limit %s offset %s;"""
        cur.execute(sql, (limit, offset,))
        return cur.fetchall()

