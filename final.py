import json
import requests
import sqlite3
import os

def get_state_data():
    request_url = 'https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
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
state_cache = state_data['data']

def insert_states(start_pos, end_pos):
    for ind in range(start_pos, end_pos):
        if ind <= 52:
            row = state_cache[ind]
            _name = row['State']
            _population = row['Population']
            cur.execute('INSERT INTO STATE (name, population) VALUES (?, ?)',(_name, _population))
            conn.commit()
        else: 
            continue
    start_pos = end_pos
    end_pos += 20
    return start_pos, end_pos

county_data = get_county_data()
county_cache = county_data['data']

def insert_counties(start_pos,end_pos):
    for ind in range(start_pos, end_pos):
        row = county_cache[ind]
        _name = row['County']
        _population = row['Population']
        cur.execute('INSERT INTO COUNTY (name, population) VALUES (?, ?)',(_name, _population))
        conn.commit()
    start_pos = end_pos
    end_pos += 20
    return start_pos, end_pos


employ_data = get_employ_data()
employ_cache = employ_data['Results']['series'][0]['data']

def insert_employment(start_pos, end_pos):
    for ind in range(start_pos, end_pos):
        row = employ_cache[ind]
        _year = row['year']
        _employment = row['value']
        _month = row['periodName']
        cur.execute('INSERT INTO EMPLOYMENT (year, month, employment) VALUES (?, ?,?)', (_year, _month, _employment))
        conn.commit()
    start_pos = end_pos
    end_pos += 20
    return start_pos, end_pos


unemployed_data = get_unemployed_data()
unemployed_cache = unemployed_data['Results']['series'][0]['data']

def insert_unemployed(start_pos, end_pos):
    for ind in range(start_pos, end_pos):
        row = unemployed_cache[ind]
        _year = row['year']
        _unemployed = row['value']
        _month = row['periodName']
        cur.execute('INSERT INTO UNEMPLOYED (year, month, unemployed) VALUES (?, ?,?)', (_year, _month, _unemployed))
        conn.commit()
    start_pos = end_pos
    end_pos += 20
    return start_pos, end_pos



def call():
    start_pos = 0
    end_pos = 20
    for i in range(2):
        insert_states(start_pos,end_pos)
        insert_employment(start_pos, end_pos)
        insert_unemployed(start_pos, end_pos)
        start_pos+= 20
        end_pos+= 20
    for i in range(5):
        insert_counties(start_pos, end_pos)
        start_pos += 20
        end_pos += 20
call()

def calc(cur, conn,filename):
    population_sum = 0
    cur.execute('SELECT population FROM STATE')
    for row in cur:
        population_sum = population_sum + int(row[0])
    average_pop = int((population_sum / 52))
    population_sum_county = 0
    cur.execute('SELECT population FROM COUNTY')
    for row in cur: 
        population_sum_county+= int(row[0])
    average_pop_county = int((population_sum_county/100))
    full_path = os.path.join(os.path.dirname(__file__), filename)
    file_obj = open(full_path, 'w')
    file_obj.write('These are the calculations did using our API data.'+'\n')
    file_obj.write('This is the average population of all 52 states in America: ') #not really its 40 for now.
    file_obj.write(str(average_pop) + '\n')
    file_obj.write('This is the average population of 100 counties in America: ')
    file_obj.write(str(average_pop_county))

        # insert calculations
    file_obj.close()


def visualize():
    pass


def commit():
    conn.commit()

def main():
    # CO2 emission in the US in 2014 (tons per capita)
    calc(cur,conn,'calc.txt')
    #insert_states(state_data)
    #insert_counties(county_data)
    #insert_employment(employ_data)
   # insert_unemployed(unemployed_data)
    commit()


if __name__ == "__main__":
    main()



