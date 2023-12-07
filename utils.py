from key import get_key, get_default_params
import requests
import json
from headers import get_cookies, get_headers
import pandas as pd
import extract

def get_hash_key(id, name):
    return f"{id}_{name}"

def get_rows():
    return 100

def get_params(p = 1): 
    o = '0'
    rows = get_rows()
    if(p == 1): 
        o = '0'
    else:
        o = str((p - 1 ) * rows - 1)
    
    params = get_default_params()
    params['p'] = str(p)
    params['o'] =  o   
    params['rows'] =  str(rows)
    if(p == 1):
        del params['p']
    return params

def get_total_pages():
    response = make_request()
    totalCount = response['totalCount']
    rows = get_rows()
    if(totalCount % rows == 0):
        return int(totalCount / rows) 
    else:
        return int(totalCount / rows) + 1 

def make_request(key,pages):
    cookies = get_cookies()
    headers = get_headers()
    #key = get_key()
    file = open(key + ".txt","w+", encoding="utf-8")
    for i in range(1,pages):
        params = get_params(i)
        data = str(requests.get('https://www.myntra.com/' + key, cookies=cookies, headers=headers).text)
        file.write(data)
        #time.sleep(5)
        print("Waiting period ---------X------------X--------X--------> " + str(i))
    file.close()    
    
    print('Querying using key -> ', key, ' and  params -> ', params)
    print("------------------- Extraction Starts -------------------")
    extract.extract_large_file(key)
    
    
    file.close()
    response = json.loads("{}")
    return response



def get_products(p = 1):
    response = make_request(p)
    return response['products']