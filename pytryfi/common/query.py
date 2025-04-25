from pytryfi.const import *
from pytryfi.exceptions import *
from typing import Literal
import json
import logging
import requests

LOGGER = logging.getLogger(__name__)

def getUserDetail(session: requests.Session):
    qString = QUERY_CURRENT_USER + FRAGMENT_USER_DETAILS
    response = query(session, qString)
    LOGGER.debug(f"getUserDetails: {response}")
    return response['data']['currentUser']

def getHouseHolds(session: requests.Session):
    qString = QUERY_CURRENT_USER_FULL_DETAIL + FRAGMENT_USER_DETAILS \
        + FRAGMENT_USER_FULL_DETAILS + FRAGMENT_PET_PROFILE + FRAGEMENT_BASE_PET_PROFILE \
        + FRAGMENT_BASE_DETAILS + FRAGMENT_POSITION_COORDINATES + FRAGMENT_BREED_DETAILS \
        + FRAGMENT_PHOTO_DETAILS + FRAGMENT_DEVICE_DETAILS + FRAGMENT_LED_DETAILS + FRAGMENT_OPERATIONAL_DETAILS \
        + FRAGMENT_CONNECTION_STATE_DETAILS
    response = query(session, qString)
    LOGGER.debug(f"getHouseHolds: {response}")
    return response['data']['currentUser']['userHouseholds']

# Simplified version of the above, but only gets details about the bases
def getBaseList(session: requests.Session):
    qString = QUERY_GET_BASES + FRAGMENT_BASE_DETAILS + FRAGMENT_POSITION_COORDINATES
    response = query(session, qString)
    LOGGER.debug(f"getBaseList: {response}")
    return response['data']['currentUser']['userHouseholds']

def getCurrentPetLocation(session: requests.Session, petId: str):
    qString = QUERY_PET_CURRENT_LOCATION.replace(VAR_PET_ID, petId) + FRAGMENT_ONGOING_ACTIVITY_DETAILS \
        + FRAGMENT_LOCATION_POINT \
        + FRAGMENT_PLACE_DETAILS + FRAGMENT_POSITION_COORDINATES
    response = query(session, qString)
    LOGGER.debug(f"getCurrentPetLocation: {response}")
    return response['data']['pet']['ongoingActivity']

def getPetAllInfo(session: requests.Session, petId: str):
    qString = QUERY_PET_ACTIVE_DETAILS.replace(VAR_PET_ID, petId) + FRAGMENT_ACTIVITY_SUMMARY_DETAILS + FRAGMENT_ONGOING_ACTIVITY_DETAILS + FRAGMENT_OPERATIONAL_DETAILS + FRAGMENT_CONNECTION_STATE_DETAILS + FRAGMENT_LED_DETAILS \
        + FRAGMENT_REST_SUMMARY_DETAILS + FRAGMENT_POSITION_COORDINATES + FRAGMENT_LOCATION_POINT + FRAGMENT_USER_DETAILS + FRAGMENT_PLACE_DETAILS
    response = query(session, qString)
    LOGGER.debug(f"getPetAllInfo: {response}")
    return response['data']['pet']

def getCurrentPetStats(session: requests.Session, petId: str):
    qString = QUERY_PET_ACTIVITY.replace(VAR_PET_ID, petId) + FRAGMENT_ACTIVITY_SUMMARY_DETAILS
    response = query(session, qString)
    LOGGER.debug(f"getCurrentPetStats: {response}")
    return response['data']['pet']

def getCurrentPetRestStats(session: requests.Session, petId: str):
    qString = QUERY_PET_REST.replace(VAR_PET_ID, petId) + FRAGMENT_REST_SUMMARY_DETAILS
    response = query(session, qString)
    LOGGER.debug(f"getCurrentPetStats: {response}")
    return response['data']['pet']

def getDevicedetails(session: requests.Session, petId: str):
    qString = QUERY_PET_DEVICE_DETAILS.replace(VAR_PET_ID, petId) + FRAGMENT_PET_PROFILE + FRAGEMENT_BASE_PET_PROFILE + \
        FRAGMENT_DEVICE_DETAILS + FRAGMENT_LED_DETAILS + FRAGMENT_OPERATIONAL_DETAILS + FRAGMENT_CONNECTION_STATE_DETAILS + \
        FRAGMENT_USER_DETAILS + FRAGMENT_BREED_DETAILS + FRAGMENT_PHOTO_DETAILS
    response = query(session, qString)
    LOGGER.debug(f"getDevicedetails: {response}")
    return response['data']['pet']

def setLedColor(session: requests.Session, deviceId: str, ledColorCode):
    qString = MUTATION_SET_LED_COLOR + FRAGMENT_DEVICE_DETAILS + FRAGMENT_OPERATIONAL_DETAILS + FRAGMENT_CONNECTION_STATE_DETAILS + FRAGMENT_USER_DETAILS + FRAGMENT_LED_DETAILS
    qVariables = '{"moduleId":"'+deviceId+'","ledColorCode":'+str(ledColorCode)+'}'
    response = mutation(session, qString, qVariables)
    LOGGER.debug(f"setLedColor: {response}")
    return response['data']

def turnOnOffLed(session: requests.Session, moduleId, ledEnabled: bool):
    qString = MUTATION_DEVICE_OPS + FRAGMENT_DEVICE_DETAILS + FRAGMENT_OPERATIONAL_DETAILS + FRAGMENT_CONNECTION_STATE_DETAILS + FRAGMENT_USER_DETAILS + FRAGMENT_LED_DETAILS
    qVariables = '{"input": {"moduleId":"'+moduleId+'","ledEnabled":'+str(ledEnabled).lower()+'}}'
    response = mutation(session, qString, qVariables)
    LOGGER.debug(f"turnOnOffLed: {response}")
    return response['data']

def setLostDogMode(session: requests.Session, moduleId, action: bool):
    if action:
        mode = PET_MODE_LOST
    else:
        mode = PET_MODE_NORMAL
    qString = MUTATION_DEVICE_OPS + FRAGMENT_DEVICE_DETAILS + FRAGMENT_OPERATIONAL_DETAILS + FRAGMENT_CONNECTION_STATE_DETAILS + FRAGMENT_USER_DETAILS + FRAGMENT_LED_DETAILS
    qVariables = '{"input": {"moduleId":"'+moduleId+'","mode":"'+mode+'"}}'
    response = mutation(session, qString, qVariables)
    LOGGER.debug(f"setLostDogMode: {response}")
    return response['data']

def getGraphqlURL():
    return API_HOST_URL_BASE + API_GRAPHQL

def mutation(session: requests.Session, qString, qVariables):
    url = getGraphqlURL()
    
    params = {"query": qString, "variables": json.loads(qVariables)}
    return execute(url, session, params=params, method='POST').json()

def query(session: requests.Session, qString):
    url = getGraphqlURL()
    params={'query': qString}
    resp = execute(url, session, params=params)
    if not resp.ok:
        LOGGER.warning(f"non-okay response: {resp.json()}")
        resp.raise_for_status()
    return resp.json()

def execute(url : str, session : requests.Session, method: Literal['GET', 'POST'] = 'GET', params=None, cookies=None):
    if method == 'GET':
        return session.get(url, params=params)
    elif method == 'POST':
        return session.post(url, json=params)
    else:
        raise TryFiError(f"Method Passed was invalid: {method}. Only GET and POST are supported")
