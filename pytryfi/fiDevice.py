import logging
import datetime
from pytryfi.ledColors import ledColors
from pytryfi.const import PET_MODE_LOST

LOGGER = logging.getLogger(__name__)

class FiDevice(object):
    def __init__(self, deviceId):
        self._deviceId = deviceId
        self._moduleId = None
        self._buildId = None
        self._batteryPercent = None
        self._isCharging = None
        self._availableLedColors = []
        self._connectedTo = None
        self._connectionSignalStrength = None
        self._temperature = None
    
    def setDeviceDetailsJSON(self, deviceJSON: dict):
        self._moduleId = deviceJSON['moduleId']
        self._buildId = deviceJSON['info']['buildId']
        self._batteryPercent = int(deviceJSON['info']['batteryPercent'])
        
        #V1 of the collar has this parameter but V2 it is missing
        if 'isCharging' in deviceJSON['info']:
            self._isCharging = bool(deviceJSON['info']['isCharging'])
        else:
            self._isCharging = None

        #self._batteryHealth = deviceJSON['info']['batteryHealth']  
        self._ledOffAt = self.setLedOffAtDate(deviceJSON['operationParams']['ledOffAt'])
        self._ledOn = self.getAccurateLEDStatus( bool(deviceJSON['operationParams']['ledEnabled']))
        self._mode = deviceJSON['operationParams']['mode']
        self._ledColor = deviceJSON['ledColor']['name']
        self._ledColorHex = deviceJSON['ledColor']['hexCode']
        self._connectionStateDate = datetime.datetime.fromisoformat(str(deviceJSON['lastConnectionState']['date']).replace('Z', '+00:00'))
        self._connectionStateType = deviceJSON['lastConnectionState']['__typename']
        self._connectedTo = self.setConnectedTo(deviceJSON['lastConnectionState'])
        self._lastUpdated = datetime.datetime.now()
        if 'temperature' in deviceJSON['info']:
            self._temperature = float(deviceJSON['info']['temperature']) / 100 # celcius
        if 'availableLedColors' in deviceJSON:
            for cString in deviceJSON['availableLedColors']:
                c = ledColors(int(cString['ledColorCode']),cString['hexCode'], cString['name'] )
                self._availableLedColors.append(c)

    def __str__(self):
        return f"Last Updated - {self.lastUpdated} - Device ID: {self.deviceId} Device Mode: {self.mode} Battery Left: {self.batteryPercent}% LED State: {self.ledOn} Last Connected: {self.connectionStateDate} by: {self.connectionStateType}"

    def setConnectedTo(self, connectedToJSON):
        connectedToString = ""
        typename = connectedToJSON['__typename']
        self._connectionSignalStrength = None
        if typename == 'ConnectedToUser':
            connectedToString = connectedToJSON['user']['firstName'] + " " + connectedToJSON['user']['lastName']
        elif typename == 'ConnectedToCellular':
            connectedToString = "Cellular"
            self._connectionSignalStrength = connectedToJSON['signalStrengthPercent']
        elif typename == 'ConnectedToBase':
            connectedToString = "Base ID - " + connectedToJSON['chargingBase']['id']
        else:
            connectedToString = None
        return connectedToString

    @property
    def deviceId(self) -> str:
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
    def temperature(self):
        return self._temperature
    #This was deprecated in the newer collars
    #@property
    #def batteryHealth(self):
    #    return self._batteryHealth
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
    def ledColor(self) -> ledColors:
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
    def connectedTo(self):
        return self._connectedTo
    @property
    def availableLedColors(self) -> list[ledColors]:
        return self._availableLedColors
    @property
    def lastUpdated(self) -> datetime.datetime:
        return self._lastUpdated
    @property
    def isLost(self) -> bool:
        if self._mode == PET_MODE_LOST:
            return True
        else:
            return False

    #This is created because if TryFi automatically turns off the LED, the status is still set to true in the api.
    #This will compare the dates to see if the current date/time is greater than the turnoffat time in the api.
    def getAccurateLEDStatus(self, ledStatus: bool):
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