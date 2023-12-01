import os

import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
PGDATABASE = os.environ['PGDATABASE']
PGHOST = os.environ['PGHOST']
PGPORT = os.environ['PGPORT']
PGUSER = os.environ['PGUSER']
PGPASSWORD = os.environ['PGPASSWORD']

def db_conn():
    try:
        conn = psycopg2.connect(dbname=PGDATABASE, user=PGUSER, password=PGPASSWORD, host=PGHOST)
        return conn
    except Exception as e:
        print(f"Can't establish connection to database: {e}")


def take_data():
    conn = db_conn()
    if conn:
        with conn.cursor() as curs:
            curs.execute('SELECT * FROM sean')
            all_users = curs.fetchall()

    ID, SEAN_ID, LEN = all_users[0]
    return SEAN_ID, LEN

def change_sean(sean_id):
    conn = db_conn()
    if conn:
        with conn.cursor() as curs:
            curs.execute('UPDATE sean SET sean_id=%s WHERE id=%s', (sean_id, 0))
        conn.commit()

    return 'Success'

def change_len(len_rus):
    conn = db_conn()
    if conn:
        with conn.cursor() as curs:
            curs.execute('UPDATE sean SET len=%s WHERE id=%s', (len_rus, 0))
        conn.commit()

    return 'Success'
    