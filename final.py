import json
import requests
import sqlite3


#jooble
host = 'jooble.org/api'
key = '59eb2b82-b173-4925-aff7-36c1b17fff46'



#data usa
api = 'https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest'

def get_usa_data():

    request_url = 'https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest'

    r = requests.get(request_url)
    data = r.text
    dict_list = json.loads(data) # decoding JSON file

    return(dict_list)

def population_year():

    data1 = get_usa_data()
    return data1[1][0]['value']

# MAKE JSON FILE W DATA
# file1 = "USA.json"
# file2 = "JOBS.json"
#
#
# conn = sqlite3.connect('final.sqlite')
# cur = conn.cursor()
#
# cur.execute('DROP TABLE IF EXISTS USA')
# cur.execute('CREATE TABLE USA(name TEXT, owner TEXT, species TEXT, age INTEGER, dob TIMESTAMP)')
# cur.execute('DROP TABLE IF EXISTS Jobs')
# cur.execute('CREATE TABLE Jobs(name TEXT, owner TEXT, species TEXT, age INTEGER, dob TIMESTAMP)')
#
#
#
# usa_file = open('USA.json','r')
# contents1 = usa_file.read()
# usa_file.close()
#
# usa_data = json.loads(contents1)
# print("num pets: " + str(len(usa_data)))
#
#
# for state in usa_data:
#     print(state)
#     _name = state['name']
#     _owner = state['owner']
#     _species = state['species']
#     _age = state['age']
#     _dob = state['dob']
#     cur.execute('INSERT INTO USA (name, owner, species, age, dob) VALUES (?, ?, ?, ?, ?)',
#                  (_name, _owner, _species, _age, _dob))
#
# conn.commit()


def main():
    # CO2 emission in the US in 2014 (tons per capita)
    print("testing")
    value1 = population_year()
    print(value1)

if __name__ == "__main__":
    main()



