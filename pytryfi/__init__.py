import logging
import requests

from pytryfi.const import (API_HOST_URL_BASE, API_LOGIN, API_GRAPHQL)
from pytryfi.fiUser import FiUser
from pytryfi.fiPet import FiPet
from pytryfi.fiBase import FiBase
from pytryfi.common import query


LOGGER = logging.getLogger(__name__)

class PyTryFi(object):
    """base object for TryFi"""

    def __init__(self, username=None, password=None):

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

    def updatePetObject(self, petObj):
        petId = petObj.petId
        count = 0
        for p in self.pets:
            if p.petId == petId:
                self._pets.pop(count)
                self._pets.append(petObj)
                LOGGER.debug(f"Updating Existing Pet: {petId}")
                break
            count = count + 1

    # return the pet object based on petId
    def getPet(self, petId):
        for p in self.pets:
            if petId == p.petId:
                return p
        LOGGER.error(f"Cannot find Pet: {petId}")
        return None
    
    #refresh base details
    def updateBases(self):
        updatedBases = []
        baseListJSON = query.getBaseList(self._session)
        for base in baseListJSON:
            b = FiBase(base['baseId'])
            b.setBaseDetailsJSON(base)
            updatedBases.append(b)
        self._bases = updatedBases

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
        url = API_HOST_URL_BASE + API_LOGIN
        params={
                'email' : self._username,
                'password' : self._password,
            }
        
        LOGGER.debug(f"Logging into TryFi")
        
        response = self._session.post(url, data=params)
        error = None
        try:
            error = response.json()['error']
        except:
            error = None
        if error or not response.ok:
            errorMsg = error['message']
            LOGGER.error(f"Cannot login, response: ({response.status_code}): {errorMsg} ")
        #storing cookies but don't need them. Handled by session mgmt
        self._cookies = response.cookies
        #store unique userId from login for future use
        self._userId = response.json()['userId']
        self._sessionId = response.json()['sessionId']
        LOGGER.debug(f"Successfully logged in. UserId: {self._userId}")