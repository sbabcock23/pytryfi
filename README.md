# pytryfi - Python Interface for TryFi
This python interface enables you to gather information about your dogs whereabouts, your user details and any bases you may have.

NOTE: Since this interacts with undocumented APIs, this may change without notice.

## Installation
TBD

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

#this will update the last reported location of a bet
tryfi.pets[0].updatePetLocation(tryfi.session)

#this will update the stats of the pet 
tryfi.pets[0].updateStats(tryfi.session)

#this will set the light color of the collar
tryfi.pets[0].setLedColorCode(tryfi.session, 2)

#this will turn on the LED light on the color
tryfi.pets[0].turnOnOffLed(tryfi.session,"ON")
#or turn it off
tryfi.pets[0].turnOnOffLed(tryfi.session,"OFF")
```

## To Do
* Provide Activity Data History
* Submit Dog Lost Action

## Links:
* [TryFi](https://tryfi.com/)

# Version History
## 0.0.3
The following updates/enhancements were made:
* moved updated pet location from base object to pet class
* created function to update the stats of the pet
* converted approriate variables to integers, floats and dates
* created function to set the LED color on the collar
* created function to turn on/off LED on a collar

## 0.0.2
Initial version of the TryFi interface that gathered basic information about the pets, collars and bases.