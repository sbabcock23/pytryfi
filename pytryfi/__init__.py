import logging
import requests

from pytryfi.const import (API_HOST_URL_BASE, API_LOGIN, PYTRYFI_VERSION, HEADER)
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
            #set Headers only after login for use going forward.
            self.setHeaders()

            self._currentUser = FiUser(self._userId)
            self._currentUser.setUserDetails(self._session)

            petListJSON = query.getPetList(self._session)
            h = 0
            self._pets = []
            for house in petListJSON:
                for pet in petListJSON[h]['household']['pets']:
                    #If pet doesn't have a collar then ignore it. What good is a pet without a collar!
                    if pet['device'] is not None:
                        p = FiPet(pet['id'])
                        p.setPetDetailsJSON(pet)
                        #get the current location and set it
                        pLocJSON = query.getCurrentPetLocation(self._session,p._petId)
                        p.setCurrentLocation(pLocJSON)
                        #get the daily, weekly and monthly stats and set
                        pStatsJSON = query.getCurrentPetStats(self._session,p._petId)
                        p.setStats(pStatsJSON['dailyStat'],pStatsJSON['weeklyStat'],pStatsJSON['monthlyStat'])
                        #get the daily, weekly and monthly rest stats and set
                        pRestStatsJSON = query.getCurrentPetRestStats(self._session,p._petId)
                        p.setRestStats(pRestStatsJSON['dailyStat'],pRestStatsJSON['weeklyStat'],pRestStatsJSON['monthlyStat'])
                        LOGGER.debug(f"Adding Pet: {p._name} with Device: {p._device._deviceId}")
                        self._pets.append(p)
                    else:
                        LOGGER.debug(f"Pet {pet['name']} - {pet['id']} has no collar. Ignoring Pet!")
                h = h + 1
            
            self._bases = []
            baseListJSON = query.getBaseList(self._session)
            h = 0
            for house in baseListJSON:
                for base in baseListJSON[h]['household']['bases']:
                    b = FiBase(base['baseId'])
                    b.setBaseDetailsJSON(base)
                    LOGGER.debug(f"Adding Base: {b._name} Online: {b._online}")
                    self._bases.append(b)
                h = h + 1
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
    
    #set the headers for the session
    def setHeaders(self):
        self.session.headers = HEADER

    #refresh pet details for all pets
    def updatePets(self):
        try:
            petListJSON = query.getPetList(self._session)
            updatedPets = []
            for house in petListJSON:
                for pet in house['household']['pets']:
                    # Skip pets without collars
                    if pet['device'] is None:
                        LOGGER.debug(f"Pet {pet['name']} - {pet['id']} has no collar. Ignoring Pet!")
                        continue
                    p = FiPet(pet['id'])
                    p.setPetDetailsJSON(pet)
                    #get the current location and set it
                    pLocJSON = query.getCurrentPetLocation(self._session,p._petId)
                    p.setCurrentLocation(pLocJSON)
                    #get the daily, weekly and monthly stats and set
                    pStatsJSON = query.getCurrentPetStats(self._session,p._petId)
                    p.setStats(pStatsJSON['dailyStat'],pStatsJSON['weeklyStat'],pStatsJSON['monthlyStat'])
                    #get the daily, weekly and monthly rest stats and set
                    pRestStatsJSON = query.getCurrentPetRestStats(self._session,p._petId)
                    p.setRestStats(pRestStatsJSON['dailyStat'],pRestStatsJSON['weeklyStat'],pRestStatsJSON['monthlyStat'])
                    LOGGER.debug(f"Adding Pet: {p._name} with Device: {p._device._deviceId}")
                    updatedPets.append(p)
            self._pets = updatedPets
        except Exception as e:
            LOGGER.error(f"Error updating pets: {e}", exc_info=True)
            capture_exception(e)
            raise

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
            for house in baseListJSON:
                for base in house['household']['bases']:
                    b = FiBase(base['baseId'])
                    b.setBaseDetailsJSON(base)
                    updatedBases.append(b)
            self._bases = updatedBases
        except Exception as e:
            LOGGER.error(f"Error fetching bases: {e}", exc_info=True)
            capture_exception(e)
            raise

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
        """Update all data - both bases and pets"""
        errors = []
        retry_auth = False
        
        try:
            self.updateBases()
        except Exception as e:
            if self._is_auth_error(e):
                retry_auth = True
            errors.append(f"Base update failed: {e}")
            
        try:
            self.updatePets()
        except Exception as e:
            if self._is_auth_error(e):
                retry_auth = True
            errors.append(f"Pet update failed: {e}")
            
        # If we got auth errors, try to re-authenticate once
        if retry_auth:
            LOGGER.info("Authentication error detected, attempting to re-authenticate")
            try:
                self.login()
                # Retry the updates after re-authentication
                errors = []
                try:
                    self.updateBases()
                except Exception as e:
                    errors.append(f"Base update failed after re-auth: {e}")
                    
                try:
                    self.updatePets()
                except Exception as e:
                    errors.append(f"Pet update failed after re-auth: {e}")
                    
            except Exception as e:
                errors.append(f"Re-authentication failed: {e}")
            
        if errors:
            error_msg = "; ".join(errors)
            raise Exception(f"TryFi update failed: {error_msg}")
    
    def _is_auth_error(self, error):
        """Check if an error is authentication related"""
        error_str = str(error).lower()
        auth_indicators = ['401', '403', 'unauthorized', 'forbidden', 'authentication', 'auth']
        return any(indicator in error_str for indicator in auth_indicators)

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
            raise e
