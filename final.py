import json
import requests
import sqlite3
import http.client


def get_state_data():
    request_url = 'https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    limits = 20
    data = requests.get(request_url, headers = headers)
    dict_list = json.loads(data.text) # decoding JSON file
    return(dict_list)

def get_county_data():
    request_url_county = 'https://datausa.io/api/data?drilldowns=County&measures=Population'
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    county_data = requests.get(request_url_county, headers=headers)
    county_dict = json.loads(county_data.text)
    return(county_dict)

def get_job_data():
    request_url_2 = 'https://jobs.github.com/positions.json?description={}&page={}'

conn = sqlite3.connect('final.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS STATE')
cur.execute('CREATE TABLE STATE(name TEXT, population INTEGER)')
cur.execute('DROP TABLE IF EXISTS COUNTY')
cur.execute('CREATE TABLE COUNTY(name TEXT, population INTEGER)')
cur.execute('DROP TABLE IF EXISTS Jobs')
cur.execute('CREATE TABLE Jobs(name TEXT, owner TEXT, species TEXT, age INTEGER, dob TIMESTAMP)')


state_data = get_state_data()
def insert_states(state_data):
    for state in state_data['data']:
        #print(state)
        _name = state['State']
        _population = state['Population']
        cur.execute('INSERT INTO STATE (name, population) VALUES (?, ?)',
                    (_name, _population))
        conn.commit()

county_data = get_county_data()
def insert_counties(county_data):
    for county in county_data['data']:
        #print(county)
        _name = county['County']
        _population = county['Population']
        cur.execute('INSERT INTO COUNTY (name, population) VALUES (?, ?)',
                    (_name, _population))
        conn.commit()

def commit():
    conn.commit()

def main():
    # CO2 emission in the US in 2014 (tons per capita)
   # print(get_state_data())
   # print(get_job_data())
    insert_states(state_data)
    insert_counties(county_data)
    commit()
    #value1 = population_year()
    #print(value1)

if __name__ == "__main__":
    main()



