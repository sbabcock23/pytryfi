from pytryfi.const import *
from pytryfi.exceptions import *
import requests

def getUserDetail(sessionId):
    qString = QUERY_CURRENT_USER + FRAGMENT_USER_DETAILS
    response = query(sessionId, qString)
    return response['data']['currentUser']

def getPetList(sessionId):
    qString = QUERY_CURRENT_USER_FULL_DETAIL + FRAGMENT_USER_DETAILS \
        + FRAGMENT_USER_FULL_DETAILS + FRAGMENT_PET_PROFILE + FRAGEMENT_BASE_PET_PROFILE \
        + FRAGMENT_BASE_DETAILS + FRAGMENT_POSITION_COORDINATES + FRAGMENT_BREED_DETAILS \
        + FRAGMENT_PHOTO_DETAILS + FRAGMENT_DEVICE_DETAILS + FRAGMENT_LED_DETAILS + FRAGMENT_OPERATIONAL_DETAILS \
        + FRAGMENT_CONNECTION_STATE_DETAILS
    response = query(sessionId, qString)
    return response['data']['currentUser']['userHouseholds'][0]['household']['pets']

def getBaseList(sessionId):
    qString = QUERY_CURRENT_USER_FULL_DETAIL + FRAGMENT_USER_DETAILS \
        + FRAGMENT_USER_FULL_DETAILS + FRAGMENT_PET_PROFILE + FRAGEMENT_BASE_PET_PROFILE \
        + FRAGMENT_BASE_DETAILS + FRAGMENT_POSITION_COORDINATES + FRAGMENT_BREED_DETAILS \
        + FRAGMENT_PHOTO_DETAILS + FRAGMENT_DEVICE_DETAILS + FRAGMENT_LED_DETAILS + FRAGMENT_OPERATIONAL_DETAILS \
        + FRAGMENT_CONNECTION_STATE_DETAILS
    response = query(sessionId, qString)
    return response['data']['currentUser']['userHouseholds'][0]['household']['bases']

def getCurrentPetLocation(sessionId, petId):
    qString = QUERY_PET_CURRENT_LOCATION.replace(VAR_PET_ID, petId) + FRAGMENT_ONGOING_ACTIVITY_DETAILS \
        + FRAGMENT_UNCERTAINTY_DETAILS + FRAGMENT_CIRCLE_DETAILS + FRAGMENT_LOCATION_POINT \
        + FRAGMENT_PLACE_DETAILS + FRAGMENT_USER_DETAILS + FRAGMENT_POSITION_COORDINATES
    response = query(sessionId, qString)
    return response['data']['pet']['ongoingActivity']

def getCurrentPetStats(sessionId, petId):
    qString = QUERY_PET_ACTIVITY.replace(VAR_PET_ID, petId) + FRAGMENT_ACTIVITY_SUMMARY_DETAILS
    response = query(sessionId, qString)
    return response['data']['pet']

def getDevicedetails(sessionId, petId):
    qString = QUERY_PET_DEVICE_DETAILS.replace(VAR_PET_ID, petId) + FRAGMENT_PET_PROFILE + FRAGEMENT_BASE_PET_PROFILE + FRAGMENT_DEVICE_DETAILS + FRAGMENT_LED_DETAILS + FRAGMENT_OPERATIONAL_DETAILS + FRAGMENT_CONNECTION_STATE_DETAILS + FRAGMENT_USER_DETAILS + FRAGMENT_BREED_DETAILS + FRAGMENT_PHOTO_DETAILS
    response = query(sessionId, qString)
    return response['data']['pet']

def setLedColor(sessionId, deviceId, ledColorCode):
    qString = MUTATION_SET_LED_COLOR + FRAGMENT_DEVICE_DETAILS + FRAGMENT_OPERATIONAL_DETAILS + FRAGMENT_CONNECTION_STATE_DETAILS + FRAGMENT_USER_DETAILS + FRAGMENT_LED_DETAILS
    qVariables = '{"moduleId":"'+deviceId+'","ledColorCode":'+str(ledColorCode)+'}'
    response = mutation(sessionId, qString, qVariables)
    return response['data']

def turnOnOffLed(sessionId, moduleId, mode, ledEnabled):
    qString = MUTATION_ENABLE_LED + FRAGMENT_DEVICE_DETAILS + FRAGMENT_OPERATIONAL_DETAILS + FRAGMENT_CONNECTION_STATE_DETAILS + FRAGMENT_USER_DETAILS + FRAGMENT_LED_DETAILS
    qVariables = '{"input": {"moduleId":"'+moduleId+'","mode":"'+mode+'","ledEnabled":'+str(ledEnabled).lower()+'}}'
    response = mutation(sessionId, qString, qVariables)
    return response['data']

def getGraphqlURL():
    return API_HOST_URL_BASE + API_GRAPHQL

def mutation(sessionId, qString, qVariables):
    jsonObject = None
    url = getGraphqlURL()
    params = {"query": qString, "variables": qVariables}
    jsonObject = execute(url, sessionId, params=params, method='POST').json()
    return jsonObject

def query(sessionId, qString):
    jsonObject = None
    url = getGraphqlURL()
    params={'query': qString}
    jsonObject = execute(url, sessionId, params=params).json()
    return jsonObject

def execute(url, sessionId, method='GET', params=None, cookies=None):
    response = None
    try:
        if method == 'GET':
            response = sessionId.get(url, params=params)
        elif method == 'POST':
            response = sessionId.post(url, data=params)
        else:
            raise TryFiError(f"Method Passed was invalid: {method}")
    except requests.RequestException as e:
        raise requests.RequestException(e)
    return response
    