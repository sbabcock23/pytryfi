import datetime
from sentry_sdk import capture_exception

class FiBase(object):
    def __init__(self, baseId):
        self._baseId = baseId
    
    def setBaseDetailsJSON(self, baseJSON):
        try:
            self._name = baseJSON['name']
            self._latitude = baseJSON['position']['latitude']
            self._longitude = baseJSON['position']['longitude']
            self._online = baseJSON['online']
            self._onlineQuality = baseJSON['onlineQuality']
            self._lastUpdated = baseJSON['infoLastUpdated']
            self._networkName = baseJSON['networkName']
            self._lastUpdated = datetime.datetime.now()
        except Exception as e:
            capture_exception(e)

    def __str__(self):
        return f"Last Updated - {self.lastUpdated} - Base ID: {self.baseId} Name: {self.name} Online Status: {self.online} Wifi Network: {self.networkname} Located: {self.latitude},{self.longitude}"
        
    @property
    def baseId(self):
        return self._baseId
    @property
    def name(self):
        return self._name
    @property
    def latitude(self):
        return self._latitude
    @property
    def longitude(self):
        return self._longitude
    @property
    def online(self):
        return self._online
    @property
    def onlineQuality(self):
        return self._onlineQuality
    @property
    def lastupdate(self):
        return self._lastUpdated
    @property
    def networkname(self):
        return self._networkName
    @property
    def lastUpdated(self):
        return self._lastUpdated