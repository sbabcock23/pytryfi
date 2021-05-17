from pytryfi.common import query
import datetime
from sentry_sdk import capture_exception

class FiUser(object):
    def __init__(self, userId):
        self._userId = userId
        
    def setUserDetails(self, sessionId):
        try:
            response = query.getUserDetail(sessionId)
            self._email = response['email']
            self._firstName = response['firstName']
            self._lastName = response['lastName']
            self._phoneNumber = response['phoneNumber']
            self._lastUpdated = datetime.datetime.now()
        except Exception as e:
            capture_exception(e)

    def __str__(self):
        return f"User ID: {self.userId} Name: {self.fullName} Email: {self.email}"
        
    @property
    def userId(self):
        return self._userId
    @property
    def email(self):
        return self._email
    @property
    def firstName(self):
        return self._firstName
    @property
    def lastName(self):
        return self._lastName
    @property
    def phoneNumber(self):
        return self._phoneNumber
    @property
    def fullName(self):
        return self.firstName + " "  + self.lastName
    @property
    def lastUpdated(self):
        return self._lastUpdated
    
