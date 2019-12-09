import json
import requests
import sqlite3
import http.client


def get_usa_data():

    request_url = 'https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    limits = 20
    data = requests.get(request_url, headers = headers)
    dict_list = json.loads(data.text) # decoding JSON file
    return(dict_list)

def get_job_data():
    print('Testing job api ')
    host = 'jooble.org'
    key = '59eb2b82-b173-4925-aff7-36c1b17fff46'
    connection = http.client.HTTPConnection(host)
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    body = '{ "keywords": "it", "location": "Bern"}'
    connection.request('POST','/api/' + key, body, headers)
    response = connection.getresponse()
    print(response.status, response.reason)
    print(response.read())

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
    print(get_usa_data())
    print(get_job_data())
    #value1 = population_year()
    #print(value1)

if __name__ == "__main__":
    main()



