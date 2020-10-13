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

#this will just update the last reported location of a bet
tryfi.updatePetLocation(tryfi.pets[0].petId)
```

## To Do
* Provide Activity Data History
* Update Current Activity Data
* Submit Dog Lost Action

## Links:
* [TryFi](https://tryfi.com/)