from pytryfi.const import *
from pytryfi.exceptions import *
import json
import logging
import requests
from typing import Literal

LOGGER = logging.getLogger(__name__)

def getUserDetail(sessionId):
    qString = QUERY_CURRENT_USER + FRAGMENT_USER_DETAILS
    response = query(sessionId, qString)
    LOGGER.debug(f"getUserDetails: {response}")
    return response['data']['currentUser']

def getPetList(sessionId):
    qString = QUERY_CURRENT_USER_FULL_DETAIL + FRAGMENT_USER_DETAILS \
        + FRAGMENT_USER_FULL_DETAILS + FRAGMENT_PET_PROFILE + FRAGEMENT_BASE_PET_PROFILE \
        + FRAGMENT_BASE_DETAILS + FRAGMENT_POSITION_COORDINATES + FRAGMENT_BREED_DETAILS \
        + FRAGMENT_PHOTO_DETAILS + FRAGMENT_DEVICE_DETAILS + FRAGMENT_LED_DETAILS + FRAGMENT_OPERATIONAL_DETAILS \
        + FRAGMENT_CONNECTION_STATE_DETAILS
    response = query(sessionId, qString)
    LOGGER.debug(f"getPetList: {response}")
    return response['data']['currentUser']['userHouseholds']

def getBaseList(sessionId):
    qString = QUERY_CURRENT_USER_FULL_DETAIL + FRAGMENT_USER_DETAILS \
        + FRAGMENT_USER_FULL_DETAILS + FRAGMENT_PET_PROFILE + FRAGEMENT_BASE_PET_PROFILE \
        + FRAGMENT_BASE_DETAILS + FRAGMENT_POSITION_COORDINATES + FRAGMENT_BREED_DETAILS \
        + FRAGMENT_PHOTO_DETAILS + FRAGMENT_DEVICE_DETAILS + FRAGMENT_LED_DETAILS + FRAGMENT_OPERATIONAL_DETAILS \
        + FRAGMENT_CONNECTION_STATE_DETAILS
    response = query(sessionId, qString)
    LOGGER.debug(f"getBaseList: {response}")
    return response['data']['currentUser']['userHouseholds']

def getCurrentPetLocation(sessionId, petId):
    qString = QUERY_PET_CURRENT_LOCATION.replace(VAR_PET_ID, petId) + FRAGMENT_ONGOING_ACTIVITY_DETAILS \
        + FRAGMENT_UNCERTAINTY_DETAILS + FRAGMENT_CIRCLE_DETAILS + FRAGMENT_LOCATION_POINT \
        + FRAGMENT_PLACE_DETAILS + FRAGMENT_USER_DETAILS + FRAGMENT_POSITION_COORDINATES
    response = query(sessionId, qString)
    LOGGER.debug(f"getCurrentPetLocation: {response}")
    return response['data']['pet']['ongoingActivity']

def getCurrentPetStats(sessionId, petId):
    qString = QUERY_PET_ACTIVITY.replace(VAR_PET_ID, petId) + FRAGMENT_ACTIVITY_SUMMARY_DETAILS
    response = query(sessionId, qString)
    LOGGER.debug(f"getCurrentPetStats: {response}")
    return response['data']['pet']

def getCurrentPetRestStats(sessionId, petId):
    qString = QUERY_PET_REST.replace(VAR_PET_ID, petId) + FRAGMENT_REST_SUMMARY_DETAILS
    response = query(sessionId, qString)
    LOGGER.debug(f"getCurrentPetStats: {response}")
    return response['data']['pet']

def getDevicedetails(sessionId, petId):
    qString = QUERY_PET_DEVICE_DETAILS.replace(VAR_PET_ID, petId) + FRAGMENT_PET_PROFILE + FRAGEMENT_BASE_PET_PROFILE + FRAGMENT_DEVICE_DETAILS + FRAGMENT_LED_DETAILS + FRAGMENT_OPERATIONAL_DETAILS + FRAGMENT_CONNECTION_STATE_DETAILS + FRAGMENT_USER_DETAILS + FRAGMENT_BREED_DETAILS + FRAGMENT_PHOTO_DETAILS
    response = query(sessionId, qString)
    LOGGER.debug(f"getDevicedetails: {response}")
    return response['data']['pet']

def setLedColor(sessionId, deviceId, ledColorCode):
    qString = MUTATION_SET_LED_COLOR + FRAGMENT_DEVICE_DETAILS + FRAGMENT_OPERATIONAL_DETAILS + FRAGMENT_CONNECTION_STATE_DETAILS + FRAGMENT_USER_DETAILS + FRAGMENT_LED_DETAILS
    qVariables = '{"moduleId":"'+deviceId+'","ledColorCode":'+str(ledColorCode)+'}'
    response = mutation(sessionId, qString, qVariables)
    LOGGER.debug(f"setLedColor: {response}")
    return response['data']

def turnOnOffLed(sessionId, moduleId, ledEnabled):
    qString = MUTATION_DEVICE_OPS + FRAGMENT_DEVICE_DETAILS + FRAGMENT_OPERATIONAL_DETAILS + FRAGMENT_CONNECTION_STATE_DETAILS + FRAGMENT_USER_DETAILS + FRAGMENT_LED_DETAILS
    qVariables = '{"input": {"moduleId":"'+moduleId+'","ledEnabled":'+str(ledEnabled).lower()+'}}'
    response = mutation(sessionId, qString, qVariables)
    LOGGER.debug(f"turnOnOffLed: {response}")
    return response['data']

def setLostDogMode(sessionId, moduleId, action):
    if action:
        mode = PET_MODE_LOST
    else:
        mode = PET_MODE_NORMAL
    qString = MUTATION_DEVICE_OPS + FRAGMENT_DEVICE_DETAILS + FRAGMENT_OPERATIONAL_DETAILS + FRAGMENT_CONNECTION_STATE_DETAILS + FRAGMENT_USER_DETAILS + FRAGMENT_LED_DETAILS
    qVariables = '{"input": {"moduleId":"'+moduleId+'","mode":"'+mode+'"}}'
    response = mutation(sessionId, qString, qVariables)
    LOGGER.debug(f"setLostDogMode: {response}")
    return response['data']

def getGraphqlURL():
    return API_HOST_URL_BASE + API_GRAPHQL

def mutation(sessionId, qString, qVariables):
    jsonObject = None
    url = getGraphqlURL()
    
    params = {"query": qString, "variables": json.loads(qVariables)}
    jsonObject = execute(url, sessionId, params=params, method='POST').json()
    return jsonObject

def query(sessionId : requests.Session, qString):
    jsonObject = None
    url = getGraphqlURL()
    params={'query': qString}
    jsonObject = execute(url, sessionId, params=params).json()
    return jsonObject

def execute(url : str, sessionId : requests.Session, method: Literal['GET', 'POST'] = 'GET', params=None, cookies=None):
    response = None
    if method == 'GET':
        response = sessionId.get(url, params=params)
    elif method == 'POST':
        response = sessionId.post(url, json=params)
    else:
        raise TryFiError(f"Method Passed was invalid: {method}. Only GET and POST are supported")
    return response
