import json
import requests
import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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


cur.execute('CREATE TABLE IF NOT EXISTS STATE (name TEXT, population INTEGER)')

cur.execute('CREATE TABLE IF NOT EXISTS COUNTY (name TEXT, population INTEGER)')

cur.execute('CREATE TABLE IF NOT EXISTS EMPLOYMENT (year INTEGER, month TEXT, employment INTEGER)')

cur.execute('CREATE TABLE IF NOT EXISTS UNEMPLOYED (year INTEGER, month TEXT, unemployed INTEGER)')


state_data = get_state_data()
state_cache = state_data['data']

def insert_states(start_pos, end_pos):
    for ind in range(start_pos, end_pos):
        if (ind <= 52):
            row = state_cache[ind]
            _name = row['State']
            _population = row['Population']
            cur.execute('INSERT INTO STATE (name, population) VALUES (?, ?)',(_name, _population))
            conn.commit()
        else:
            continue
    start_pos = end_pos
    end_pos += 13
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
    end_pos += 13
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
    end_pos += 13
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
    end_pos += 13
    return start_pos, end_pos

def call():
    start_pos = 0
    end_pos = 13
    for i in range(4):
        insert_states(start_pos,end_pos)
        start_pos+= 13
        end_pos+= 13
    for i in range(5):
        insert_employment(start_pos, end_pos)
        insert_unemployed(start_pos, end_pos)
        start_pos+= 13
        end_pos+= 13
    for i in range(10):
        insert_counties(start_pos, end_pos)
        start_pos += 13
        end_pos += 13
#call()

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
    average_pop_county = int((population_sum_county/260))

    employment_sum = 0
    cur.execute('SELECT employment FROM EMPLOYMENT')
    for row in cur:
        employment_sum += int(row[0])
    average_employment = int((employment_sum/130))

    unemployment_sum = 0
    cur.execute('SELECT unemployed FROM UNEMPLOYED')
    for row in cur:
        unemployment_sum += int(row[0])
    average_unemployment = int((unemployment_sum/130))


    full_path = os.path.join(os.path.dirname(__file__), filename)
    file_obj = open(full_path, 'w')
    file_obj.write('These are the calculations we did using our API data.'+'\n')
    file_obj.write('We found the populations of all the states in america from our State data table and took that total and divided it by 52. This is the average population of all 52 states in America: ')
    file_obj.write(str(average_pop) + '\n')
    file_obj.write('We found the populations from the Counties data table and totaled it, then divided it by 260. This is the average population of 260 counties in America: ')
    file_obj.write(str(average_pop_county)+'\n')
    file_obj.write('We found the number of empoloyed Americans each month from our Employment data table, then averaged this. This is the average number of people who are reported as "employed" each month: ')
    file_obj.write(str(average_employment) + '\n')
    file_obj.write('We found the number of unemployed Americans each month from our Unemployment data table, then found the average.This is the average number of people who are reported as "unemployed" each month: ')
    file_obj.write(str(average_unemployment))

    # insert calculations
    file_obj.close()

def get_state_dict():
    try:
        conn = sqlite3.connect('final.sqlite')
    except:
        print("Error")
    state_dict = {}
    cur = conn.cursor()
    cur.execute("SELECT name, population FROM STATE ")
    rows = cur.fetchall()
    for row in rows:
        if row[0] not in state_dict:
            state_dict[row[0]] = row[1]
        else:
            pass
    conn.commit()
    return state_dict


def visualize_state(state_dict):
    tup_list = []
    for item in state_dict.keys():
        tup_list.append(tuple([item,state_dict[item]]))
    sorted_tup_list = sorted(tup_list, key = lambda x: x[0])
    state_list = []
    vals_list = []
    for item in sorted_tup_list:
        state_list.append(item[0])
        vals_list.append(item[1])
    plt.bar(state_list, vals_list, color = (0.1, 0.2, 0.3, 0.4), edgecolor = 'magenta')
    plt.xlabel('State', fontsize=10)
    plt.ylabel('Population', fontsize=10)
    plt.title('State Populations in the United States')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    return sorted_tup_list


def job():
    try:
        conn = sqlite3.connect('final.sqlite')
    except:
        print("Error")

    dictionary_of_employ = {}
    cur.execute('SELECT employment, month FROM EMPLOYMENT WHERE year = 2013')
    for row in cur:
        employment = row[0]
        month = row[1]
        if month not in dictionary_of_employ.keys():
            dictionary_of_employ[month] = employment
    dictionary_of_unemploy = {}

    cur.execute('SELECT unemployed, month FROM UNEMPLOYED WHERE year = 2013')
    for row in cur:
        unemployed = row[0]
        month = row[1]
        if month not in dictionary_of_unemploy.keys():
            dictionary_of_unemploy[month] = unemployed
    dictionary_of_emp_unemp = {}
    cur.execute('SELECT Employment.employment, Unemployed.unemployed, Unemployed.month FROM Employment LEFT JOIN Unemployed on Employment.month = Unemployed.month WHERE Employment.year = 2013')
    for row in cur:
        employment = row[0]
        unemployed = row[1]
        month = row[2]
        if month not in dictionary_of_emp_unemp.keys():
            dictionary_of_emp_unemp[month] = (employment, unemployed)
    job_tup_list = []
    for item in dictionary_of_emp_unemp.keys():
        job_tup_list.append(tuple([item,dictionary_of_emp_unemp[item]]))
    conn.commit()
    emp_list = []
    unemp_list = []
    month_list = []
    for item in job_tup_list:
        emp_list.append(item[1][0])
        unemp_list.append(item[1][1])
        month_list.append(item[0])
    fig, ax = plt.subplots()
    N = 12
    width = 0.35
    ind = np.arange(N)
    p1 = ax.bar(ind, emp_list, width, color='blue')
    p2 = ax.bar(ind + width, unemp_list, width, color='yellow')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(month_list)
    ax.legend((p1[0], p2[0]), ('Employed', 'Unemployed'))
    ax.autoscale_view()
    ax.set(xlabel='Month', ylabel='Number of Americans',
           title='Number of Americans Employed and Unemployed in 2013')
    fig.savefig("job.png")
    plt.show()

def commit():
    conn.commit()

def main():
    calc(cur,conn,'calc.txt')
    visualize_state(get_state_dict())
    job()
    commit()

if __name__ == "__main__":
    main()



