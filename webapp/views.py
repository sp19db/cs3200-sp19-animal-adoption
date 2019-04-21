from flask import render_template, request
import json
from webapp import app
from webapp import database as db


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
    select_all_shelters_q = ("""select * from shelter;""")
    rows = db.execute_query(select_all_shelters_q)
    shelters = []
    for (id, name, address, city, state, postcode, email, phone) in rows:
        data = dict()
        data["id"] = id
        data["name"] = name
        data["address"] = address + ", " + city + ", " + state + ". " + postcode
        shelters.append(data)
    return json.dumps(shelters)


@app.route('/breeds')
def get_breeds():
    type_name = request.args.get('type', default=None, type=str)
    select_breeds_by_type = """select breed_name
    from animal
    join breed using (breed_id)
    join animal_type using (type_id)
    where type_name = {}
    group by breed_name;""".format("\'" + type_name + "\'")
    rows = db.execute_query(select_breeds_by_type)
    breeds = []
    for breed_name in rows:
        breeds.append(breed_name)
    return json.dumps(breeds)


@app.route('/animal')
def get_animal():
    animal_id = request.args.get('id', default=None, type=str)
    animal_data_points = ["animal_id", "animal_name", "animal_image",
                          "breed_name", "type_name", "gender",
                          "age", "bio", "color", "size", "shelter_name",
                          "city", "state", "postcode",
                          "email_address", "phone_number", "lat", "lng"]
    select = "select "
    for column in animal_data_points:
        select += column + ", "
    select = select[:-2] + "\n"
    select_animal_by_id = select \
                          + "from animal\n" \
                          + "join shelter using (shelter_id)\n" \
                          + "join breed using (breed_id)\n" \
                          + "join animal_type using (type_id)\n" \
                          + "join image using (animal_id)\n" \
                          + "left join markers on (shelter_name = name)\n" \
                          + "where animal_id = {};".format(animal_id)
    print(select_animal_by_id)
    row = db.execute_query(select_animal_by_id)[0]
    animal_data = {}
    for index in range(len(animal_data_points)):
        animal_data[animal_data_points[index]] = row[index]
    return json.dumps(animal_data)


@app.route('/animals')
def get_all_animals():
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
    rows = db.execute_query(select_animals_by_filter)
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
    return json.dumps(animals)


@app.route('/map')
def get_map():
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
                            + "HAVING distance < {} ORDER BY distance LIMIT 0 , 20;".format(radius)
    rows = db.execute_query(select_all_shelters_q)
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
