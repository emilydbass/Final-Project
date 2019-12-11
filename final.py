import json
import requests
import sqlite3

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

def get_employ_data():
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": ['LNS12000000'], "startyear": "2009", "endyear": "2019"})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    employment_data = json.loads(p.text)
    return(employment_data)

def get_unemployed_data():
    headers = {'Content-type': 'application/json'}
    data2 = json.dumps({"seriesid": ['LNS13000000'], "startyear": "2009", "endyear": "2019"})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data2, headers=headers)
    unemployed_data = json.loads(p.text)
    return(unemployed_data)


conn = sqlite3.connect('final.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS STATE')
cur.execute('CREATE TABLE STATE(name TEXT, population INTEGER)')
cur.execute('DROP TABLE IF EXISTS COUNTY')
cur.execute('CREATE TABLE COUNTY(name TEXT, population INTEGER)')
cur.execute('DROP TABLE IF EXISTS EMPLOYMENT')
cur.execute('CREATE TABLE EMPLOYMENT(year INTEGER, month TEXT, employment INTEGER)')
cur.execute('DROP TABLE IF EXISTS UNEMPLOYED')
cur.execute('CREATE TABLE UNEMPLOYED(year INTEGER, month TEXT, unemployed INTEGER)')


state_data = get_state_data()
def insert_states(state_data):
    for state in state_data['data']:
        _name = state['State']
        _population = state['Population']
        cur.execute('INSERT INTO STATE (name, population) VALUES (?, ?)',
                    (_name, _population))
        conn.commit()

county_data = get_county_data()
def insert_counties(county_data):
    for county in county_data['data']:
        _name = county['County']
        _population = county['Population']
        cur.execute('INSERT INTO COUNTY (name, population) VALUES (?, ?)',
                    (_name, _population))
        conn.commit()

employ_data = get_employ_data()
def insert_employment(employ_data):
    for item in employ_data['Results']['series'][0]['data']:
        _year = item['year']
        _employment = item['value']
        _month = item['periodName']
        cur.execute('INSERT INTO EMPLOYMENT (year, month, employment) VALUES (?, ?,?)',
                    (_year, _month, _employment))
        conn.commit()


unemployed_data = get_unemployed_data()
def insert_unemployed(unemployed_data):
    for item in unemployed_data['Results']['series'][0]['data']:
        _year = item['year']
        _unemployed = item['value']
        _month = item['periodName']
        cur.execute('INSERT INTO UNEMPLOYED (year, month, unemployed) VALUES (?, ?,?)',
                    (_year, _month, _unemployed))
        conn.commit()

def commit():
    conn.commit()

def main():
    # CO2 emission in the US in 2014 (tons per capita)
    insert_states(state_data)
    insert_counties(county_data)
    insert_employment(employ_data)
    insert_unemployed(unemployed_data)
    commit()


if __name__ == "__main__":
    main()



