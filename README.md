# pytryfi - Python Interface for TryFi
This python interface enables you to gather information about your dogs whereabouts, your user details and any bases you may have.

NOTE: Since this interacts with undocumented APIs, this may change without notice.

## Installation
To install this package, use pip
```python
python -m pip install "pytryfi"
```

## Usage
TryFi uses Graphql for its APIs. Essentially, you will use your username (email address) and password to retrieve a unique username specific for API calls which in turn will be used for the duration to retrieve data.

### Example
```python
#this will create the object and gather all the necessary data
tryfi = PyTryFi(username, password)
print(tryfi)

#this will perform a complete refresh of all Pets and data points
tryfi.updatePets()

#this will perform a complete refresh of all Bases and data points
tryfi.updateBases()

#this will perform an update on both Pets and Bases and their associated data points
tryfi.update()

#this will update the last reported location of a bet
tryfi.pets[0].updatePetLocation(tryfi.session)

#this will update the stats of the pet 
tryfi.pets[0].updateStats(tryfi.session)

#update the device/collar details for the given pet
tryfi.pets[0].updateDeviceDetails(tryfi.session)

#update the all details for a given pet
tryfi.pets[0].updateAllDetails(tryfi.session)

#this will set the light color of the collar
tryfi.pets[0].setLedColorCode(tryfi.session, 2)

#this will turn on the LED light on the color
tryfi.pets[0].turnOnOffLed(tryfi.session,True)
#or turn it off
tryfi.pets[0].turnOnOffLed(tryfi.session,False)

#this will turn on the lost dog mode
tryfi.pets[0].setLostDogMode(tryfi.session,True)
#or turn it off
tryfi.pets[0].setLostDogMode(tryfi.session,False)

#this will get the lost dog mode status/state currently in the object
tryfi.pets[0].isLost
```

## To Do
* Provide Activity Data History

## Links:
* [TryFi](https://tryfi.com/)

# Version History
# 0.0.13
* Enhancement - removed error logging where not required
* Fix - resolved issue where the variables are unbound in the login function

## 0.0.12
* Enhancement - added Sentry for capturing errors by further only capturing exceptions

## 0.0.11
* Enhancement - added Sentry for capturing errors

## 0.0.10
* Enhancement - added areaName property that could be used to idenitfy a location (tryfi.pets[0].areaName)
* Bugfix - fixed longitude and latitude while Pet is on a walk

## 0.0.9
* Bugfix - get LED status based on additional logic that compares the ledOffAt date with the current date/time. Update the boolean to True or False base on the additional date comparison.

## 0.0.8
* Bugfix - handle unknown location

## 0.0.7
* Bug fixes when updating objects

## 0.0.6
* Added function to submit Lost Dog Action
* Added isLost property to Pet
* Code cleanup

## 0.0.5
* Added global update function that updates both pets and bases (pytryfi.update())
* Added better error handling

## 0.0.4
* created update functions for various pet and device objects and a global update for the pet
* added last updated date/time to the objects to track when the data was last updated
* changed turn on/off action to boolean
* when performing an action on the collar, update the data that is retrieved at the same time

## 0.0.3
The following updates/enhancements were made:
* moved updated pet location from base object to pet class
* created function to update the stats of the pet
* converted approriate variables to integers, floats and dates
* created function to set the LED color on the collar
* created function to turn on/off LED on a collar

## 0.0.2
Initial version of the TryFi interface that gathered basic information about the pets, collars and bases.