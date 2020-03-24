import datetime
import json
import time

import dateutil.parser
import requests

import config

API = config.API
URL = config.URL
HOST_ID = config.HOST_ID
HEADERS = config.HEADERS
RES_QUERY = config.RES_QUERY
REQ_STATUS = config.REQ_STATUS

print('What is the unit number?')
number = input()


def get_status(userinput):
    print(f'Searching for {userinput.upper()}...')
    PAYLOAD = {'value': userinput}
    response_post = requests.post(
        url=URL+RES_QUERY, headers=HEADERS, json=PAYLOAD)
    display_status(response_post.json(),userinput)


'''
    Grabs search string and POST a request to the server
'''


def display_status(response,userinput):
    print(userinput)
    '''
    Need to add logic ..json returns both DISPLAY and HOST it completes the search, if only has DISPLAY then should 
    print out this does not have a HOST
    '''
    for values in response['resource_query']:
        #if values['resource_type'] == 'display_unit' or values['resource_type'] == 'host':
        if values['resource_type'] == 'host':
            get_id(values['id'])
        else:
            print(f'{userinput} does not exist')

'''
   Grabs ID value of host
'''


def get_id(id):
    PLAYER_ID = str(id)
    params = dict(client_resource_id=PLAYER_ID,
                  domain_id=35270498)
    # Get Name
    PLAYER_QUERY = requests.get(
        URL+HOST_ID+'ids='+PLAYER_ID, headers=HEADERS)

    json_player = PLAYER_QUERY.json()
    # print(json_player)
    ID_BY_NAME = (json_player['host'][0]['name'])
    response_get = requests.get(
        URL + REQ_STATUS, headers=HEADERS, params=params)
    status(response_get.json(), ID_BY_NAME)


'''
Takes response from get_id and checks for monitor status == 1, if monitor_status == 0 it is Mia    
'''


def status(res, id):
    # print(res)
    status_of_tv = res['monitor_poll'][0]['monitor_status']
    mia_tv = res['monitor_poll'][0]['poll_last_utc']
    d = dateutil.parser.parse(mia_tv)
    mia = d.strftime('%m-%d-%Y')
    if status_of_tv == 1:
        print(f'{id} is currently online')
    else:
        print(f'{id} has been Missing in action since {mia}')


get_status(number)
