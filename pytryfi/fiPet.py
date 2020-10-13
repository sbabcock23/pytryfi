import logging
from pytryfi.fiDevice import FiDevice
from pytryfi.common import query

LOGGER = logging.getLogger(__name__)

class FiPet(object):
    def __init__(self, petId):
        self._petId = petId

    def setPetDetailsJSON(self, petJSON):
        self._name = petJSON['name']
        self._homeCityState = petJSON['homeCityState']
        self._yearOfBirth = petJSON['yearOfBirth']
        self._monthOfBirth = petJSON['monthOfBirth']
        self._dayOfBirth = petJSON['dayOfBirth']
        self._gender = petJSON['gender']
        #weight is in kg
        self._weight = petJSON['weight']
        self._breed = petJSON['breed']['name']
        #TOFIx need to add try catch 
        try:
            self._photoLink = petJSON['photos']['first']['image']['fullSize']
        except:
            LOGGER.warning(f"Cannot find photo of your pet. Defaulting to empty string.")
            self._photoLink = ""

        self._device = FiDevice(petJSON['device']['id'])
        self._device.setDeviceDetailsJSON(petJSON['device'])

    def __str__(self):
        return f"Pet ID: {self.petId} Name: {self.name} From: {self.homeCityState} Located: {self.currLatitude},{self.currLongitude} Last Updated: {self.currStartTime}\n \
            using Device/Collar: {self._device}"
    
    def setCurrentLocation(self, activityJSON):
        self._currLongitude = activityJSON['position']['longitude']
        self._currLatitude = activityJSON['position']['latitude']
        self._currStartTime = activityJSON['start']
        self._currPlaceName = activityJSON['place']['name']
        self._currPlaceAddress = activityJSON['place']['address']

    def setStats(self, activityJSONDaily, activityJSONWeekly, activityJSONMonthly):
        #distance is in metres
        self._dailyGoal = activityJSONDaily['stepGoal']
        self._dailySteps = activityJSONDaily['totalSteps']
        self._dailyTotalDistance = activityJSONDaily['totalDistance']

        self._WeeklyGoal = activityJSONWeekly['stepGoal']
        self._WeeklySteps = activityJSONWeekly['totalSteps']
        self._WeeklyTotalDistance = activityJSONWeekly['totalDistance']

        self._MonthlyGoal = activityJSONMonthly['stepGoal']
        self._MonthlySteps = activityJSONMonthly['totalSteps']
        self._MonthlyTotalDistance = activityJSONMonthly['totalDistance']

    def updatePetLocation(self, sessionId,):
        pLocJSON = query.getCurrentPetLocation(sessionId,self.petId)
        self.setCurrentLocation(pLocJSON)

    def setLedColorCode(self, sessionId, colorCode):
        try:
            moduleId = self.device.moduleId
            ledColorCode = int(colorCode)
            query.setLedColor(sessionId, moduleId, ledColorCode)
            return True
        except Exception as e:
            LOGGER.warning(f"Could not complete request:\m {e}")
            return False
    
    def turnOnOffLed(self, sessionId, action):
        try:
            moduleId = self.device.moduleId
            mode = "NORMAL"
            if action.upper() == "ON":
                ledEnabled = True
            else:
                ledEnabled = False
            query.turnOnOffLed(sessionId, moduleId, mode, ledEnabled)
            return True
        except Exception as e:
            LOGGER.warning(f"Could not complete request:\m {e}")
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
