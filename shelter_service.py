from flask import Flask
import mysql.connector
import json

app = Flask(__name__)

@app.route('/')
def landing_page():
    return 'Welcome to Animal Shelter Server'


@app.route('/shelters')
def get_shelters():
    try:
        conn = mysql.connector.connect(user='root', password='cs3200db2019',
                                       host='localhost',
                                       database='animal_shelter')
        cursor = conn.cursor()
        select_all_shelters_q = ("""select * from shelter;""")
        cursor = conn.cursor()
        cursor.execute(select_all_shelters_q)
        rows = cursor.fetchall()
        print(rows)
        all_data = dict()
        shelters = []
        all_data["shelters"] = shelters
        for (id, name, address, city, state, postcode, email, phone) in rows:
            data = dict()
            data["id"] = id
            data["name"] = name
            shelters.append(data)

        response = json.dumps(all_data)
        return response
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.debug = True
    app.run()

