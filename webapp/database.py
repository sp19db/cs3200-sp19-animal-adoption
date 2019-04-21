import mysql.connector

DEVELOPMENT = True

if DEVELOPMENT:
    db_user = 'root'
    db_password = 'cs3200db2019'
    db_host = 'localhost'
    db_name = 'animal_shelter'
else:
    db_user = 'bf5bd74fa96389'
    db_password = 'eefffcd0'
    db_host = 'us-cdbr-iron-east-02.cleardb.net'
    db_name = 'heroku_cafd19139116b9e'


def connect_to_db():
    conn = mysql.connector.connect(user=db_user, password=db_password,
                                   host=db_host,
                                   database=db_name)
    return conn


def execute_query(query):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except mysql.connector.Error as e:
        print(e)
