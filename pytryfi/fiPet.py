import logging
from pytryfi.fiDevice import FiDevice
from pytryfi.common import query
from pytryfi.exceptions import *
from pytryfi.const import PET_ACTIVITY_ONGOINGWALK
import datetime
from sentry_sdk import capture_exception

LOGGER = logging.getLogger(__name__)

class FiPet(object):
    def __init__(self, petId):
        self._petId = petId

    def setPetDetailsJSON(self, petJSON):
        try:
            self._name = petJSON['name']
        except:
            LOGGER.warning(f"Unknown Pet Name")
            self._name = "Unknown Pet Name"
        try:
            self._homeCityState = petJSON['homeCityState']
        except:
            LOGGER.warning(f"Unknown City")
            self._homeCityState = "FakeCity"
        try:
            self._yearOfBirth = int(petJSON['yearOfBirth'])
        except:
            LOGGER.warning(f"Unknown Year of Birth")
            self._yearOfBirth = 1900
        try:
            self._monthOfBirth = int(petJSON['monthOfBirth'])
        except:
            LOGGER.warning(f"Unknown Month of Birth")
            self._monthOfBirth = 1
        try:
            self._dayOfBirth = int(petJSON['dayOfBirth'])
        except:
            LOGGER.warning(f"Unknown day of birth")
            self._dayOfBirth = 1
        try:
            self._gender = petJSON['gender']
        except:
            LOGGER.warning(f"Unknown Gender")
            self._gender = "Male"
        try:
            #weight is in kg
            self._weight = float(petJSON['weight'])
        except:
            LOGGER.warning(f"Unknown Weight")
            self._weight = float(1.00)
        try:
            self._breed = petJSON['breed']['name']
        except:
            LOGGER.warning(f"Unknown Breed of Dog")
            self._breed = "Dog"
            #track last updated
        self._lastUpdated = datetime.datetime.now()
        try:
            self._photoLink = petJSON['photos']['first']['image']['fullSize']
        except Exception as e:
            #capture_exception(e)
            LOGGER.warning(f"Cannot find photo of your pet. Defaulting to empty string.")
            self._photoLink = ""
        try:
            self._device = FiDevice(petJSON['device']['id'])
            self._device.setDeviceDetailsJSON(petJSON['device'])
        except Exception as e:
            capture_exception(e)

    def __str__(self):
        return f"Last Updated - {self.lastUpdated} - Pet ID: {self.petId} Name: {self.name} Is Lost: {self.isLost} From: {self.homeCityState} ActivityType: {self.activityType} Located: {self.currLatitude},{self.currLongitude} Last Updated: {self.currStartTime}\n \
            using Device/Collar: {self._device}"
    
    # set the Pet's current location details
    def setCurrentLocation(self, activityJSON):
        activityType = activityJSON['__typename']
        self._activityType = activityType
        self._areaName = activityJSON['areaName']
        try:
            if activityType == PET_ACTIVITY_ONGOINGWALK:
                positionSize = len(activityJSON['positions'])
                self._currLongitude = float(activityJSON['positions'][positionSize-1]['position']['longitude'])
                self._currLatitude = float(activityJSON['positions'][positionSize-1]['position']['latitude'])
                self._currStartTime = datetime.datetime.fromisoformat(activityJSON['start'].replace('Z', '+00:00'))            
            else:
                self._currLongitude = float(activityJSON['position']['longitude'])
                self._currLatitude = float(activityJSON['position']['latitude'])
                self._currStartTime = datetime.datetime.fromisoformat(activityJSON['start'].replace('Z', '+00:00'))
            try:
                self._currPlaceName = activityJSON['place']['name']
                self._currPlaceAddress = activityJSON['place']['address']
            except Exception as e:
                #capture_exception(e)
                LOGGER.warning("Could not set place, defaulting to Unknown")
                self._currPlaceName = "UNKNOWN"
                self._currPlaceAddress = "UNKNOWN"
            self._lastUpdated = datetime.datetime.now()
        except TryFiError as e:
            capture_exception(e)
            LOGGER.error(f"Unable to set values Current Location for Pet {self.name}.\nException: {e}\nwhile parsing {activityJSON}")
            raise TryFiError("Unable to set Pet Location Details")
        except Exception as e:
            capture_exception(e)

    # set the Pet's current steps, goals and distance details for daily, weekly and monthly
    def setStats(self, activityJSONDaily, activityJSONWeekly, activityJSONMonthly):
        try:
            #distance is in metres
            self._dailyGoal = int(activityJSONDaily['stepGoal'])
            self._dailySteps = int(activityJSONDaily['totalSteps'])
            self._dailyTotalDistance = float(activityJSONDaily['totalDistance'])
        except TryFiError as e:
            LOGGER.error(f"Unable to set values Daily Stats for Pet {self.name}.\nException: {e}\nwhile parsing {activityJSONDaily}")
            capture_exception(e)
            raise TryFiError("Unable to set Pet Daily Stats")
        except Exception as e:
            capture_exception(e)
        try:
            self._weeklyGoal = int(activityJSONWeekly['stepGoal'])
            self._weeklySteps = int(activityJSONWeekly['totalSteps'])
            self._weeklyTotalDistance = float(activityJSONWeekly['totalDistance'])
        except TryFiError as e:
            LOGGER.error(f"Unable to set values Weekly Stats for Pet {self.name}.\nException: {e}\nwhile parsing {activityJSONWeekly}")
            capture_exception(e)
            raise TryFiError("Unable to set Pet Weekly Stats")
        except Exception as e:
            capture_exception(e)
        try:
            self._monthlyGoal = int(activityJSONMonthly['stepGoal'])
            self._monthlySteps = int(activityJSONMonthly['totalSteps'])
            self._monthlyTotalDistance = float(activityJSONMonthly['totalDistance'])
        except TryFiError as e:
            LOGGER.error(f"Unable to set values Monthly Stats for Pet {self.name}.\nException: {e}\nwhile parsing {activityJSONMonthly}")
            capture_exception(e)
            raise TryFiError("Unable to set Pet Monthly Stats")
        except Exception as e:
            capture_exception(e)

        self._lastUpdated = datetime.datetime.now()

    # set the Pet's current rest details for daily, weekly and monthly
    def setRestStats(self, restJSONDaily, restJSONWeekly, restJSONMonthly):
        #setting default values to zero in case this feature is not supported by older collars
        self._dailyNap = 0
        self._dailySleep = 0
        self._weeklyNap = 0
        self._weeklySleep = 0
        self._monthlyNap = 0
        self._monthlySleep = 0
        try:
            for sleepAmount in restJSONDaily['restSummaries'][0]['data']['sleepAmounts']:
                if sleepAmount['type'] == 'SLEEP':
                    self._dailySleep = int(sleepAmount['duration'])
                if sleepAmount['type'] == "NAP":
                    self._dailyNap = int(sleepAmount['duration'])
        except TryFiError as e:
            LOGGER.error(f"Unable to set values Daily Rest Stats for Pet {self.name}.\nException: {e}\nwhile parsing {restJSONDaily}")
            capture_exception(e)
            raise TryFiError("Unable to set Pet Daily Rest Stats")
        except Exception as e:
            capture_exception(e)
        try:
            for sleepAmount in restJSONWeekly['restSummaries'][0]['data']['sleepAmounts']:
                if sleepAmount['type'] == 'SLEEP':
                    self._weeklySleep = int(sleepAmount['duration'])
                if sleepAmount['type'] == 'NAP':
                    self._weeklyNap = int(sleepAmount['duration'])
        except TryFiError as e:
            LOGGER.error(f"Unable to set values Weekly Rest Stats for Pet {self.name}.\nException: {e}\nwhile parsing {restJSONWeekly}")
            capture_exception(e)
            raise TryFiError("Unable to set Pet Weekly Rest Stats")
        except Exception as e:
            capture_exception(e)
        try:
            for sleepAmount in restJSONMonthly['restSummaries'][0]['data']['sleepAmounts']:
                if sleepAmount['type'] == 'SLEEP':
                    self._monthlySleep = int(sleepAmount['duration'])
                if sleepAmount['type'] == 'NAP':
                    self._monthlyNap = int(sleepAmount['duration'])
        except TryFiError as e:
            LOGGER.error(f"Unable to set values Monthly Rest Stats for Pet {self.name}.\nException: {e}\nwhile parsing {restJSONMonthly}")
            capture_exception(e)
            raise TryFiError("Unable to set Pet Monthly Rest Stats")
        except Exception as e:
            capture_exception(e)

    # Update the Stats of the pet
    def updateStats(self, sessionId):
        try:
            pStatsJSON = query.getCurrentPetStats(sessionId,self.petId)
            self.setStats(pStatsJSON['dailyStat'],pStatsJSON['weeklyStat'],pStatsJSON['monthlyStat'])
            return True
        except Exception as e:
            LOGGER.error(f"Could not update stats for Pet {self.name}.\n{e}")
            capture_exception(e)

    # Update the Stats of the pet
    def updateRestStats(self, sessionId):
        try:
            pRestStatsJSON = query.getCurrentPetRestStats(sessionId,self.petId)
            self.setRestStats(pRestStatsJSON['dailyStat'],pRestStatsJSON['weeklyStat'],pRestStatsJSON['monthlyStat'])
            return True
        except Exception as e:
            LOGGER.error(f"Could not update rest stats for Pet {self.name}.\n{e}")
            capture_exception(e)

    # Update the Pet's GPS location
    def updatePetLocation(self, sessionId):
        try:
            pLocJSON = query.getCurrentPetLocation(sessionId,self.petId)
            self.setCurrentLocation(pLocJSON)
            return True
        except Exception as e:
            LOGGER.error(f"Could not update Pet: {self.name}'s location.\n{e}")
            capture_exception(e)
            return False
    
    # Update the device/collar details for this pet
    def updateDeviceDetails(self, sessionId):
        try:
            deviceJSON = query.getDevicedetails(sessionId, self.petId)
            self.device.setDeviceDetailsJSON(deviceJSON['device'])
            return True
        except Exception as e:
            LOGGER.error(f"Could not update Device/Collar information for Pet: {self.name}\n{e}")
            capture_exception(e)
            return False

    # Update all details regarding this pet
    def updateAllDetails(self, sessionId):
        self.updateDeviceDetails(sessionId)
        self.updatePetLocation(sessionId)
        self.updateStats(sessionId)
        self.updateRestStats(sessionId)

    # set the color code of the led light on the pet collar
    def setLedColorCode(self, sessionId, colorCode):
        try:
            moduleId = self.device.moduleId
            ledColorCode = int(colorCode)
            setColorJSON = query.setLedColor(sessionId, moduleId, ledColorCode)
            try:  
                self.device.setDeviceDetailsJSON(setColorJSON['setDeviceLed'])
            except Exception as e:
                LOGGER.warning(f"Updated LED Color but could not get current status for Pet: {self.name}\nException: {e}")
                capture_exception(e)
            return True
        except Exception as e:
            LOGGER.error(f"Could not complete Led Color request:\n{e}")
            capture_exception(e)
            return False
    
    # turn on or off the led light. action = True will enable the light, false turns off the light
    def turnOnOffLed(self, sessionId, action):
        try:
            moduleId = self.device.moduleId
            onOffResponse = query.turnOnOffLed(sessionId, moduleId, action)
            try:
                self.device.setDeviceDetailsJSON(onOffResponse['updateDeviceOperationParams'])
            except Exception as e:
                LOGGER.warning(f"Action: {action} was successful however unable to get current status for Pet: {self.name}")
                capture_exception(e)
            return True
        except Exception as e:
            LOGGER.error(f"Could not complete LED request:\n{e}")
            capture_exception(e)
            return False

    # set the lost dog mode to Normal or Lost Dog. Action is true for lost dog and false for normal (not lost)
    def setLostDogMode(self, sessionId, action):
        try:
            moduleId = self.device.moduleId
            petModeResponse = query.setLostDogMode(sessionId, moduleId, action)
            try:
                self.device.setDeviceDetailsJSON(petModeResponse['updateDeviceOperationParams'])
            except Exception as e:
                LOGGER.warning(f"Action: {action} was successful however unable to get current status for Pet: {self.name}")
                capture_exception(e)
            return True
        except Exception as e:
            LOGGER.error(f"Could not complete Lost Dog Mode request:\n{e}")
            LOGGER.error(f"Could not complete turn on/off light where ledEnable is {action}.\nException: {e}")
            capture_exception(e)
            return False

    @property
    def device(self):
        return self._device
    @property
    def petId(self):
        return self._petId
    @property
    def name(self):
        return self._name
    @property
    def homeCityState(self):
        return self._homeCityState
    @property
    def yearOfBirth(self):
        return self._yearOfBirth
    @property
    def monthOfBirth(self):
        return self._monthOfBirth
    @property
    def dayOfBirth(self):
        return self._dayOfBirth
    @property
    def gender(self):
        return self._gender
    @property
    def weight(self):
        return self._weight
    @property
    def breed(self):
        return self._breed
    @property
    def photoLink(self):
        return self._photoLink
    @property
    def currLongitude(self):
        return self._currLongitude
    @property
    def currLatitude(self):
        return self._currLatitude
    @property
    def currStartTime(self):
        return self._currStartTime
    @property
    def currPlaceName(self):
        return self._currPlaceName
    @property
    def currPlaceAddress(self):
        return self._currPlaceAddress
    @property
    def dailyGoal(self):
        return self._dailyGoal
    @property
    def dailySteps(self):
        return self._dailySteps
    @property
    def dailyTotalDistance(self):
        return self._dailyTotalDistance
    @property
    def weeklyGoal(self):
        return self._weeklyGoal
    @property
    def weeklySteps(self):
        return self._weeklySteps
    @property
    def weeklyTotalDistance(self):
        return self._weeklyTotalDistance
    @property
    def monthlyGoal(self):
        return self._monthlyGoal
    @property
    def monthlySteps(self):
        return self._monthlySteps
    @property
    def monthlyTotalDistance(self):
        return self._monthlyTotalDistance

    @property
    def dailySleep(self):
        return self._dailySleep
    @property
    def weeklySleep(self):
        return self._weeklySleep
    @property
    def monthlySleep(self):
        return self._monthlySleep
    @property
    def dailyNap(self):
        return self._dailyNap
    @property
    def weeklyNap(self):
        return self._weeklyNap
    @property
    def monthlyNap(self):
        return self._monthlyNap

    @property
    def lastUpdated(self):
        return self._lastUpdated
    @property
    def isLost(self):
        return self.device.isLost
    @property
    def activityType(self):
        return self._activityType
    @property
    def areaName(self):
        return self._areaName
    
    def getCurrPlaceName(self):
        return self.currPlaceName
    
    def getCurrPlaceAddress(self):
        return self.currPlaceAddress

    def getActivityType(self):
        return self.activityType

    def getBirthDate(self):
        return datetime.datetime(self.yearOfBirth, self.monthOfBirth, self.dayOfBirth)
    
    def getDailySteps(self):
        return self.dailySteps
    
    def getDailyGoal(self):
        return self.dailyGoal

    def getDailyDistance(self):
        return self.dailyTotalDistance

    def getWeeklySteps(self):
        return self.weeklySteps
    
    def getWeeklyGoal(self):
        return self.weeklyGoal

    def getWeeklyDistance(self):
        return self.weeklyTotalDistance

    def getMonthlySteps(self):
        return self.monthlySteps
    
    def getMonthlyGoal(self):
        return self.monthlyGoal

    def getMonthlyDistance(self):
        return self.monthlyTotalDistance
        
