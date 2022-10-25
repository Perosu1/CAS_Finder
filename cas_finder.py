#made by Peter Kenda in 2022

#importing stuff
import pandas as pd
import requests as requests
import json 
import time
import os
import sys

os.chdir(os.path.dirname(sys.argv[0]))

print(os.getcwd())

#importing the file
import_file_name = input('Enter the excel file with the chemical names *with the file extention*. It must be in the same folder as the python script. Example: BLANK:   ')

#dir_path = os.path.dirname(os.path.realpath(__file__))
#lines = os.path.join(dir_path, import_file_name)
#print(lines)

input = pd.read_excel(import_file_name, names = ['chems'])
input_data = input['chems'].tolist()

def casQuery(chemical):
    '''takes chemical as string, returns the name of the chemical and the CAS number from the commonchemistry.cas.org API.
     If more than one result is found or the API code is not 200 returns chemical for both name and 0000000 for CAS.'''
    
    response = requests.get(f'https://commonchemistry.cas.org/api/search?q={chemical}')
    
    #if the server cannot be reached or if it returns anything but a 200. MOVE out of function.
    if response.status_code != 200:
        print('API error')
        
    #checks if only one result was returned:
    elif response.json()['count'] == 1:
           
        result = response.json()['results'][0]
        name = result['name']
        cas = result['rn']
        return name, cas

    #if server returns multiple results
    else:
        response.json()['count'] != 1
        print(f'more than one result found for {chemical}, printing NA as cas number')
        name = 'error'
        cas = 'error'
        return name, cas

#finds and records the actual data
in_chems = []
names = []
cas_numbers = []

input_data = list(input_data)

i = 0

for chemical in input_data:
    i+=1
    print(i)
    name, cas = casQuery(chemical)
    print(chemical, name, cas)
    in_chems.append(chemical)
    names.append(name)
    cas_numbers.append(cas)
#    except:
#        print('can\'t find') IMPORTANT! I have to have some error handling to copy paste.

dict = {'input':in_chems, 'name':names, 'cas_number':cas_numbers}
df = pd.DataFrame(dict)

df.to_csv(f'{time.time()}_CAS_export.csv', index=False)