class FiDevice(object):
    def __init__(self, deviceId):
        self._deviceId = deviceId
    
    def setDeviceDetailsJSON(self, deviceJSON):
        self._moduleId = deviceJSON['moduleId']
        self._buildId = deviceJSON['info']['buildId']
        self._batteryPercent = deviceJSON['info']['batteryPercent']
        self._isCharging = deviceJSON['info']['isCharging']
        self._batteryHealth = deviceJSON['info']['batteryHealth']
        self._ledOn = deviceJSON['operationParams']['ledEnabled']
        self._ledOffAt = deviceJSON['operationParams']['ledOffAt']
        self._ledColor = deviceJSON['ledColor']['name']
        self._ledColorHex = deviceJSON['ledColor']['hexCode']
        self._connectionStateDate = deviceJSON['lastConnectionState']['date']
        self._connectionStateType = deviceJSON['lastConnectionState']['__typename']

    def __str__(self):
        return f"Device ID: {self.deviceId} Battery Left: {self.batteryPercent} LED State: {self.ledOn} Last Connected: {self.connectionStateDate} by: {self.connectionStateType}"


    @property
    def deviceId(self):
        return self._deviceId
    @property
    def moduleId(self):
        return self._moduleId
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
        