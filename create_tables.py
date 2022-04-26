import psycopg2


def create_tables():
    """ create tables in the PostgreSQL database"""
    command = """
        CREATE TABLE "user" (
            email VARCHAR(255) PRIMARY KEY,
            text VARCHAR(255) NULL
        )
        """
    conn = None
    try:
        conn = psycopg2.connect("dbname=fast user=username password=password host=localhost port=54320")
        cur = conn.cursor()

        cur.execute(command)

        cur.close()

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
