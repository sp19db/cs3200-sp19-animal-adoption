from flask import render_template, request
import mysql.connector
import json
from webapp import app

DEVELOPMENT = False

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


def animal_filter_where_clause(type_name, breed_name, size, gender, age):
    criteria = ""
    filters = [("type_name", type_name),
               ("breed_name", breed_name),
               ("size", size),
               ("gender", gender),
               ("age", age)]
    for filter_name, filter_value in filters:
        if filter_value is not None:
            criteria += filter_name + " = " + "\'" + filter_value + "\'" + " and "
    if criteria != "":
        criteria = "\nwhere " + criteria[:-4]
    return criteria


@app.route('/')
def landing_page():
    return render_template("index.html")


@app.route('/shelters')
def get_shelters():
    try:
        conn = connect_to_db()
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


@app.route('/breeds')
def get_breeds():
    try:
        type_name = request.args.get('type', default=None, type=str)

        select_breeds_by_type = """select breed_name
        from animal
        join breed using (breed_id)
        join animal_type using (type_id)
        where type_name = {}
        group by breed_name;""".format("\'" + type_name + "\'")
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(select_breeds_by_type)
        rows = cursor.fetchall()
        breeds = []
        for breed_name in rows:
            breeds.append(breed_name)
        cursor.close()
        conn.close()
        return json.dumps(breeds)
    except mysql.connector.Error as e:
        print(e)


@app.route('/animal')
def get_animal():
    try:
        animal_id = request.args.get('id', default=None, type=str)
        animal_data_points = ["animal_id", "animal_name", "animal_image",
                              "breed_name", "type_name", "gender",
                              "age", "bio", "color", "size", "shelter_name",
                              "city", "state", "postcode",
                              "email_address", "phone_number"]
        select = "select "
        for column in animal_data_points:
            select += column + ", "
        select = select[:-2] + "\n"
        select_animal_by_id = select \
                              + "from animal\n" \
                              + "join shelter using (shelter_id)\n" \
                              + "join breed using (breed_id)\n" \
                              + "join animal_type using (type_id)\n" \
                              + "join image using (animal_id)" \
                              + "where animal_id = {};".format(animal_id)
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(select_animal_by_id)
        row = cursor.fetchone()
        animal_data = {}
        for index in range(len(animal_data_points)):
            animal_data[animal_data_points[index]] = row[index]
        return json.dumps(animal_data)
    except mysql.connector.Error as e:
        print(e)


@app.route('/animals')
def get_all_animals():
    try:
        type_name = request.args.get('type', default=None, type=str)
        breed_name = request.args.get('breed', default=None, type=str)
        size = request.args.get('size', default=None, type=str)
        gender = request.args.get('gender', default=None, type=str)
        age = request.args.get('age', default=None, type=str)
        select_animals_by_filter = ("""select animal_id, animal_name, gender, age, size, animal_image 
        from animal
        join breed using (breed_id)
        join animal_type using (type_id)
        join image using (animal_id) """)
        select_animals_by_filter += animal_filter_where_clause(type_name, breed_name, size, gender, age)
        select_animals_by_filter += "\norder by animal_name limit 50;"
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(select_animals_by_filter)
        rows = cursor.fetchall()
        animals = []
        for (id, name, gender, age, size, img_url) in rows:
            animal = dict()
            animal['id'] = id
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


@app.route('/map')
def get_map():
    try:
        type_name = request.args.get('type', default=None, type=str)
        breed_name = request.args.get('breed', default=None, type=str)
        size = request.args.get('size', default=None, type=str)
        gender = request.args.get('gender', default=None, type=str)
        age = request.args.get('age', default=None, type=str)
        lat = request.args.get('lat', default=None, type=str)
        lng = request.args.get('lng', default=None, type=str)
        radius = request.args.get('radius', default=None, type=str)

        select_animals_by_filter = "SELECT DISTINCT shelter_id " \
                                   "from animal join breed using (breed_id) " \
                                   "join animal_type using (type_id)"
        select_animals_by_filter += animal_filter_where_clause(type_name, breed_name, size, gender, age)
        select_all_shelters_q = "SELECT id, lat, lng, name, address, " \
                                "( 3959 * acos( cos( radians({}) )" \
                                " * cos( radians( lat ) ) * cos( radians( lng )" \
                                " - radians({}) ) + sin( radians({}) )" \
                                " * sin( radians( lat ) ) ) ) AS distance " \
                                "FROM markers " \
                                    .format(lat, lng, lat) \
                                + 'join(' + select_animals_by_filter + ')temp on(id = shelter_id) ' \
                                                                       "HAVING distance < {} " \
                                                                       "ORDER BY distance LIMIT 0 , 20;".format(radius)
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(select_all_shelters_q)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        xml = '<?xml version="1.0"?>\n<markers>'
        for (id, lat, lng, name, address, distance) in rows:
            string = ''
            string = string + '<marker id=' + '''"''' + str(id) + '''" ''' + 'name=' + '''"''' + str(name) \
                     + '''" ''' + 'address=' + '''"''' + str(address) + '''" ''''lat=' + '''"''' + str(lat) \
                     + '''" ''' + 'lng=' + '''"''' + str(lng) \
                     + '''" ''' + "distance=" + '''"''' + str(distance) + '''"''' + '/>'
            xml = xml + '\n' + string
        xml = xml + '\n' + '</markers>'
        xml_wrapper = {"location": xml}
        return json.dumps(xml_wrapper)
    except mysql.connector.Error as e:
        print(e)
