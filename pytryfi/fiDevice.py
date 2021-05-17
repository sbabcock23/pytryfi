import logging
import datetime
from pytryfi.ledColors import ledColors
from pytryfi.const import PET_MODE_NORMAL, PET_MODE_LOST

LOGGER = logging.getLogger(__name__)

class FiDevice(object):
    def __init__(self, deviceId):
        self._deviceId = deviceId
    
    def setDeviceDetailsJSON(self, deviceJSON):
        try:
            self._moduleId = deviceJSON['moduleId']
            self._buildId = deviceJSON['info']['buildId']
            self._batteryPercent = int(deviceJSON['info']['batteryPercent'])
            self._isCharging = bool(deviceJSON['info']['isCharging'])
            self._batteryHealth = deviceJSON['info']['batteryHealth']
            self._ledOffAt = self.setLedOffAtDate(deviceJSON['operationParams']['ledOffAt'])
            self._ledOn = self.getAccurateLEDStatus( bool(deviceJSON['operationParams']['ledEnabled']))
            self._mode = deviceJSON['operationParams']['mode']
            self._ledColor = deviceJSON['ledColor']['name']
            self._ledColorHex = deviceJSON['ledColor']['hexCode']
            self._connectionStateDate = datetime.datetime.fromisoformat(str(deviceJSON['lastConnectionState']['date']).replace('Z', '+00:00'))
            self._connectionStateType = deviceJSON['lastConnectionState']['__typename']
            self._availableLedColors = []
            self._lastUpdated = datetime.datetime.now()
            for cString in deviceJSON['availableLedColors']:
                c = ledColors(int(cString['ledColorCode']),cString['hexCode'], cString['name'] )
                self._availableLedColors.append(c)
        except Exception as e:
            capture_exception(e)

    def __str__(self):
        return f"Last Updated - {self.lastUpdated} - Device ID: {self.deviceId} Device Mode: {self.mode} Battery Left: {self.batteryPercent}% LED State: {self.ledOn} Last Connected: {self.connectionStateDate} by: {self.connectionStateType}"

    @property
    def deviceId(self):
        return self._deviceId
    @property
    def moduleId(self):
        return self._moduleId
    @property
    def mode(self):
        return self._mode
    @property
    def buildId(self):
        return self._buildId
    @property
    def batteryPercent(self):
        return self._batteryPercent
    @property
    def batteryHealth(self):
        return self._batteryHealth
    @property
    def isCharging(self):
        return self._isCharging
    @property
    def ledOn(self):
        return self._ledOn
    @property
    def ledOffAt(self):
        return self._ledOffAt
    @property
    def ledColor(self):
        return self._ledColor
    @property
    def ledColorHex(self):
        return self._ledColorHex
    @property
    def connectionStateDate(self):
        return self._connectionStateDate
    @property
    def connectionStateType(self):
        return self._connectionStateType
    @property
    def availableLedColors(self):
        return self._availableLedColors
    @property
    def lastUpdated(self):
        return self._lastUpdated
    @property
    def isLost(self):
        if self._mode == PET_MODE_LOST:
            return True
        else:
            return False

#This is created because if TryFi automatically turns off the LED, the status is still set to true in the api.
#This will compare the dates to see if the current date/time is greater than the turnoffat time in the api.
    def getAccurateLEDStatus(self, ledStatus):
        if ledStatus is False:
            LOGGER.debug("getAccurateLedStatus: LED Status is False")
            return False
        else:
            LOGGER.debug("getAccurateLedStatus: LED Status is True... comparing date/times")
            currentDateTime = datetime.datetime.now(datetime.timezone.utc)
            if currentDateTime > self.ledOffAt:
                LOGGER.debug(f"Current datetime: {currentDateTime} is greater than ledOffAt: {self.ledOffAt}, Returning False")
                return False
            else:
                LOGGER.debug(f"Current datetime: {currentDateTime} is less than ledOffAt: {self.ledOffAt}, Returning False")
                return True
#Created function to return a date/time regardless.
    def setLedOffAtDate(self, ledOffAt):
        if ledOffAt == None:
            ## if object is null, return current date/time in UTC
            LOGGER.debug("LedOffAt is None, returning current datetime in UTC")
            return datetime.datetime.now(datetime.timezone.utc)
        else:
            LOGGER.debug(f"LedOffAt has date/time of {ledOffAt}. Returning this in ISO Format.")
            return datetime.datetime.fromisoformat(str(ledOffAt).replace('Z', '+00:00'))