import logging
import requests

from pytryfi.const import (API_HOST_URL_BASE, API_LOGIN, API_GRAPHQL, PYTRYFI_VERSION)
from pytryfi.fiUser import FiUser
from pytryfi.fiPet import FiPet
from pytryfi.fiBase import FiBase
from pytryfi.common import query
from pytryfi.const import SENTRY_URL
import sentry_sdk
from sentry_sdk import capture_message, capture_exception



LOGGER = logging.getLogger(__name__)

class PyTryFi(object):
    """base object for TryFi"""

    def __init__(self, username=None, password=None):
        try:
            sentry = sentry_sdk.init(
                    SENTRY_URL,
                    release=PYTRYFI_VERSION,
                )
            self._api_host = API_HOST_URL_BASE
            self._session = requests.Session()
            self._user_agent = "pyTryFi"
            self._username = username
            self._password = password
            self.login()

            self._currentUser = FiUser(self._userId)
            self._currentUser.setUserDetails(self._session)
            petListJSON = query.getPetList(self._session)
            self._pets = []
            for pet in petListJSON:
                p = FiPet(pet['id'])
                p.setPetDetailsJSON(pet)
                #get the current location and set it
                pLocJSON = query.getCurrentPetLocation(self._session,p._petId)
                p.setCurrentLocation(pLocJSON)
                #get the daily, weekly and monthly stats and set
                pStatsJSON = query.getCurrentPetStats(self._session,p._petId)
                p.setStats(pStatsJSON['dailyStat'],pStatsJSON['weeklyStat'],pStatsJSON['monthlyStat'])
                LOGGER.debug(f"Adding Pet: {p._name} with Device: {p._device._deviceId}")
                self._pets.append(p)
            
            self._bases = []
            baseListJSON = query.getBaseList(self._session)
            for base in baseListJSON:
                b = FiBase(base['baseId'])
                b.setBaseDetailsJSON(base)
                LOGGER.debug(f"Adding Base: {b._name} Online: {b._online}")
                self._bases.append(b)
        except Exception as e:
            capture_exception(e)

    def __str__(self):
        instString = f"Username: {self.username}"
        userString = f"{self.currentUser}"
        baseString = ""
        petString = ""
        for b in self.bases:
            baseString = baseString + f"{b}"
        for p in self.pets:
            petString = petString + f"{p}"
        return f"TryFi Instance - {instString}\n Pets in Home:\n {petString}\n Bases In Home:\n {baseString}"
        
    #refresh pet details for all pets
    def updatePets(self):
        try:
            petListJSON = query.getPetList(self._session)
            updatedPets = []
            for pet in petListJSON:
                p = FiPet(pet['id'])
                p.setPetDetailsJSON(pet)
                #get the current location and set it
                pLocJSON = query.getCurrentPetLocation(self._session,p._petId)
                p.setCurrentLocation(pLocJSON)
                #get the daily, weekly and monthly stats and set
                pStatsJSON = query.getCurrentPetStats(self._session,p._petId)
                p.setStats(pStatsJSON['dailyStat'],pStatsJSON['weeklyStat'],pStatsJSON['monthlyStat'])
                LOGGER.debug(f"Adding Pet: {p._name} with Device: {p._device._deviceId}")
                updatedPets.append(p)
            self._pets = updatedPets
        except Exception as e:
            capture_exception(e)

    def updatePetObject(self, petObj):
        try:
            petId = petObj.petId
            count = 0
            for p in self.pets:
                if p.petId == petId:
                    self._pets.pop(count)
                    self._pets.append(petObj)
                    LOGGER.debug(f"Updating Existing Pet: {petId}")
                    break
                count = count + 1
        except Exception as e:
            capture_exception(e)

    # return the pet object based on petId
    def getPet(self, petId):
        try:
            for p in self.pets:
                if petId == p.petId:
                    return p
            LOGGER.error(f"Cannot find Pet: {petId}")
            return None
        except Exception as e:
            capture_exception(e)

    #refresh base details
    def updateBases(self):
        try:
            updatedBases = []
            baseListJSON = query.getBaseList(self._session)
            for base in baseListJSON:
                b = FiBase(base['baseId'])
                b.setBaseDetailsJSON(base)
                updatedBases.append(b)
            self._bases = updatedBases
        except Exception as e:
            capture_exception(e)

    # return the pet object based on petId
    def getBase(self, baseId):
        try:
            for b in self.bases:
                if baseId == b.baseId:
                    return b
            LOGGER.error(f"Cannot find Base: {baseId}")
            return None
        except Exception as e:
            capture_exception(e)

    def update(self):
        self.updateBases()
        self.updatePets()

    @property
    def currentUser(self):
        return self._currentUser
    @property
    def pets(self):
        return self._pets
    @property
    def bases(self):
        return self._bases
    @property
    def username(self):
        return self._username
    @property
    def session(self):
        return self._session
    @property
    def cookies(self):
        return self._cookies
    @property
    def userID(self):
        return self._userID
    @property
    def session(self):
        return self._session

    # login to the api and get a session
    def login(self):
        error = None
        url = API_HOST_URL_BASE + API_LOGIN
        params={
                'email' : self._username,
                'password' : self._password,
            }
        
        LOGGER.debug(f"Logging into TryFi")
        try:
            response = self._session.post(url, data=params)
            response.raise_for_status()
            #validate if the response contains error or not
            try:
                error = response.json()['error']
            except Exception as e:
                #capture_exception(e)
                error = None
            #if error set or response is non-200
            if error or not response.ok:
                errorMsg = error['message']
                LOGGER.error(f"Cannot login, response: ({response.status_code}): {errorMsg} ")
                capture_exception(errorMsg)
                raise Exception("TryFiLoginError")
            
            #storing cookies but don't need them. Handled by session mgmt
            self._cookies = response.cookies
            #store unique userId from login for future use
            self._userId = response.json()['userId']
            self._sessionId = response.json()['sessionId']
            LOGGER.debug(f"Successfully logged in. UserId: {self._userId}")
        except requests.RequestException as e:
            LOGGER.error(f"Cannot login, error: ({e})")
            capture_exception(e)
            raise requests.RequestException(e)
        except Exception as e:
            capture_exception(e)
