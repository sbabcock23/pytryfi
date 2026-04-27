from operator import le
from pytryfi.const import *
from pytryfi.exceptions import *
import json
import requests
import logging

# from sentry_sdk import capture_exception

LOGGER = logging.getLogger(__name__)


def getUserDetail():
    # try:
    qString = QUERY_CURRENT_USER + FRAGMENT_USER_DETAILS
    return qString


# except Exception as e:
#     LOGGER.error(f"Error performing query: {e}")
#     ## capture_exception(e)


def getPetList():
    # try:
    qString = (
        QUERY_CURRENT_USER_FULL_DETAIL
        + FRAGMENT_USER_DETAILS
        + FRAGMENT_USER_FULL_DETAILS
        + FRAGMENT_PET_PROFILE
        + FRAGEMENT_BASE_PET_PROFILE
        + FRAGMENT_BASE_DETAILS
        + FRAGMENT_POSITION_COORDINATES
        + FRAGMENT_BREED_DETAILS
        + FRAGMENT_PHOTO_DETAILS
        + FRAGMENT_DEVICE_DETAILS
        + FRAGMENT_LED_DETAILS
        + FRAGMENT_OPERATIONAL_DETAILS
        + FRAGMENT_CONNECTION_STATE_DETAILS
    )

    return qString


# except Exception as e:
#     LOGGER.error(f"Error performing query: {e}")
## capture_exception(e)


def getBaseList():
    # try:
    qString = (
        QUERY_CURRENT_USER_FULL_DETAIL
        + FRAGMENT_USER_DETAILS
        + FRAGMENT_USER_FULL_DETAILS
        + FRAGMENT_PET_PROFILE
        + FRAGEMENT_BASE_PET_PROFILE
        + FRAGMENT_BASE_DETAILS
        + FRAGMENT_POSITION_COORDINATES
        + FRAGMENT_BREED_DETAILS
        + FRAGMENT_PHOTO_DETAILS
        + FRAGMENT_DEVICE_DETAILS
        + FRAGMENT_LED_DETAILS
        + FRAGMENT_OPERATIONAL_DETAILS
        + FRAGMENT_CONNECTION_STATE_DETAILS
    )

    return qString


# except Exception as e:
#     LOGGER.error(f"Error performing query: {e}")
# capture_exception(e)


def getCurrentPetLocation(petId):
    # try:
    qString = (
        QUERY_PET_CURRENT_LOCATION.replace(VAR_PET_ID, petId)
        + FRAGMENT_ONGOING_ACTIVITY_DETAILS
        + FRAGMENT_UNCERTAINTY_DETAILS
        + FRAGMENT_CIRCLE_DETAILS
        + FRAGMENT_LOCATION_POINT
        + FRAGMENT_PLACE_DETAILS
        + FRAGMENT_USER_DETAILS
        + FRAGMENT_POSITION_COORDINATES
    )

    # LOGGER.debug(f"getCurrentPetLocation: {response}")
    return qString  # response['data']['pet']['ongoingActivity']


# except Exception as e:
#     LOGGER.error(f"Error performing query: {e}")
#     ## capture_exception(e)


def getCurrentPetStats(petId):
    # try:
    qString = (
        QUERY_PET_ACTIVITY.replace(VAR_PET_ID, petId)
        + FRAGMENT_ACTIVITY_SUMMARY_DETAILS
    )

    # LOGGER.debug(f"getCurrentPetStats: {response}")
    return qString


# except Exception as e:
#     LOGGER.error(f"Error performing query: {e}")
# # capture_exception(e)


def getCurrentPetRestStats(petId):
    # try:
    qString = QUERY_PET_REST.replace(VAR_PET_ID, petId) + FRAGMENT_REST_SUMMARY_DETAILS

    return qString  # response['data']['pet']


# except Exception as e:
#     LOGGER.error(f"Error performing query: {e}")
# capture_exception(e)


def getDevicedetails(petId):
    # try:
    qString = (
        QUERY_PET_DEVICE_DETAILS.replace(VAR_PET_ID, petId)
        + FRAGMENT_PET_PROFILE
        + FRAGEMENT_BASE_PET_PROFILE
        + FRAGMENT_DEVICE_DETAILS
        + FRAGMENT_LED_DETAILS
        + FRAGMENT_OPERATIONAL_DETAILS
        + FRAGMENT_CONNECTION_STATE_DETAILS
        + FRAGMENT_USER_DETAILS
        + FRAGMENT_BREED_DETAILS
        + FRAGMENT_PHOTO_DETAILS
    )

    return qString  # response['data']['pet']


# except Exception as e:
#     LOGGER.error(f"Error performing query: {e}")
# capture_exception(e)


def set_led_color(device_id: str, led_color_code: str):
    print(device_id, led_color_code)

    # Combine all fragments and mutation into one string
    q_string = (
        MUTATION_SET_LED_COLOR
        + FRAGMENT_DEVICE_DETAILS
        + FRAGMENT_OPERATIONAL_DETAILS
        + FRAGMENT_CONNECTION_STATE_DETAILS
        + FRAGMENT_USER_DETAILS
        + FRAGMENT_LED_DETAILS
    )

    # Correctly format the variables using an f-string for proper string interpolation
    q_variables = json.dumps({
        "input": {
            "moduleId": device_id,
            "ledColorCode": led_color_code  # This can be a hex code like "#FFFFFF"
        }
    })

    # Call the mutation function with the query and variables
    response = mutation(q_string, q_variables)
    return response


# except Exception as e:
#     LOGGER.error(f"Error performing query: {e}")
# # capture_exception(e)


def turn_on_off_led(module_id: str, led_enable: bool):
    # Combine all fragments and mutation into one string
    q_string = (
        MUTATION_DEVICE_OPS
        + FRAGMENT_DEVICE_DETAILS
        + FRAGMENT_OPERATIONAL_DETAILS
        + FRAGMENT_CONNECTION_STATE_DETAILS
        + FRAGMENT_USER_DETAILS
        + FRAGMENT_LED_DETAILS
    )

    # Format variables properly for a GraphQL request
    q_variables = json.dumps({"input": {"moduleId": module_id, "ledEnabled": led_enable}})

    # Call the mutation function with the query and variables
    response = mutation(q_string, q_variables)
    return response


def setLostDogMode(moduleId, action):
    # try:
    if action:
        mode = PET_MODE_LOST
    else:
        mode = PET_MODE_NORMAL
    qString = (
        MUTATION_DEVICE_OPS
        + FRAGMENT_DEVICE_DETAILS
        + FRAGMENT_OPERATIONAL_DETAILS
        + FRAGMENT_CONNECTION_STATE_DETAILS
        + FRAGMENT_USER_DETAILS
        + FRAGMENT_LED_DETAILS
    )
    qVariables = '{"input": {"moduleId":"' + moduleId + '","mode":"' + mode + '"} }'
    response = mutation(qString, qVariables)
    return response


# except Exception as e:
#     LOGGER.error(f"Error performing query: {e}")
# capture_exception(e)


def mutation(qString, qVariables):
    # try:
    print(qVariables)
    params = {"query": qString, "variables": json.loads(qVariables)}
    # jsonObject = execute(url, , params=params, method='POST').json()
    return params


# except Exception as e:
#     LOGGER.error(f"Error performing query: {e}")
# # capture_exception(e)

# def query(, qString):
#     try:
#         jsonObject = None
#         url = getGraphqlURL()
#         params={'query': qString}
#         jsonObject = execute(url, , params=params).json()
#         return qStringjsonObject
#     except Exception as e:
#         LOGGER.error(f"Error performing query:  {e}")
#        # capture_exception(e)

# def execute(url, : requests.Session, method='GET', params=None, cookies=None):
#     LOGGER.debug(f"url:{url} \n params:{params} \n sid:{.__str__()}")
#     try:
#         if method == 'GET':
#             response = .get(url, params=params)
#         elif method == 'POST':
#             response = .post(url, json=params)
#         else:
#             raise TryFiError(f"Method Passed was invalid: {method}")
#     except requests.RequestException as e:
#        # capture_exception(e)
#         raise requests.RequestException(e)
#     except Exception as e:
#            # capture_exception(e)
#            LOGGER.debug(e)
#     return qStringresponse


def main():
    queries = [
        getUserDetail(),
        getPetList(),
        getBaseList(),
        getCurrentPetLocation("12"),
        getCurrentPetStats("12"),
        getCurrentPetRestStats("12"),
        getDevicedetails("12"),
        set_led_color("1i1i1l1d1", "#FFFFFF"),
        turn_on_off_led("1i1i1l1d1", True),
        setLostDogMode("1i1i1l1d1", PET_MODE_LOST),
    ]
    # print(queries)
    for i in queries:
        print(f"\n\n\n {i} \n\n\n")


main()
