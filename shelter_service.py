from flask import Flask, render_template, request
from flask_cors import CORS
import mysql.connector
import json

app = Flask(__name__)
CORS(app)


@app.route('/')
def landing_page():
    return render_template("animal_searches.html")
    # return render_template("index.html")


@app.route('/shelters')
def get_shelters():
    try:
        conn = mysql.connector.connect(user='root', password='cs3200db2019',
                                       host='localhost',
                                       database='animal_shelter')
        select_all_shelters_q = ("""select * from shelter;""")
        cursor = conn.cursor()
        cursor.execute(select_all_shelters_q)
        rows = cursor.fetchall()
        shelters = []
        for (id, name, address, city, state, postcode, email, phone) in rows:
            data = dict()
            data["id"] = id
            data["name"] = name
            data["address"] = address + ", " + city + ", " + state + ". " + postcode
            shelters.append(data)
        cursor.close()
        conn.close()
        return json.dumps(shelters)
    except mysql.connector.Error as e:
        print(e)


@app.route('/animals')
def get_animals():
    try:
        type_name = request.args.get('type', default=None, type=str)
        breed_name = request.args.get('breed', default=None, type=str)
        size = request.args.get('size', default=None, type=str)
        gender = request.args.get('gender', default=None, type=str)
        age = request.args.get('age', default=None, type=str)

        select_animals_by_filter = ("""select animal_name, gender, age, size, animal_image 
        from animal
        join breed using (breed_id)
        join animal_type using (type_id)
        join image using (animal_id) """)

        filters = [("type_name", type_name),
                   ("breed_name", breed_name),
                   ("size", size),
                   ("gender", gender),
                   ("age", age)]

        criteria = ""
        for filter_name, filter_value in filters:
            if filter_value is not None:
                criteria += filter_name + " = " + "\'" + filter_value + "\'" + " and "

        if criteria != "":
            select_animals_by_filter += "\nwhere " + criteria[:-4]

        select_animals_by_filter += "\norder by animal_name limit 50;"

        print(select_animals_by_filter)
        conn = mysql.connector.connect(user='root', password='cs3200db2019',
                                       host='localhost',
                                       database='animal_shelter')
        cursor = conn.cursor()
        cursor.execute(select_animals_by_filter)
        rows = cursor.fetchall()
        animals = []
        for (name, gender, age, size, img_url) in rows:
            animal = dict()
            animal['name'] = name
            animal['gender'] = gender
            animal['age'] = age
            animal['size'] = size
            animal['img_url'] = img_url
            animals.append(animal)
        cursor.close()
        conn.close()
        return json.dumps(animals)
    except mysql.connector.Error as e:
        print(e)


@app.route('/animals-page')
def get_animals_page():
    return render_template("animals.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
