# Christopher H. Todd's Python Library For Interacting With Locations

The ctodd-python-lib-location project is responsible for manging location information, geocoding addresses, and getting directions.

## Table of Contents

* [Dependencies](#dependencies)
* [Libraries](#libraries)
* [Example Scripts](#example-scripts)
* [Notes](#notes)
* [TODO](#todo)

## Dependencies

### Python Packages

* geocoder==1.38.1
* requests==2.22.0
* street-address==0.4.0
* usaddress==0.5.10

## Libraries

### [address_helpers.py](https://github.com/ChristopherHaydenTodd/ctodd-python-lib-location/blob/master/location_helpers/address_helpers.py)

Address Helpers. This library is used to interact with address strings/dicts and convert/handle these addresses.

Functions:

```
def convert_string_address_to_dict(address_string, expected_fields=None):
    """
    Purpose:
        Parse a string into an address dict with specific fields
    Args:
        address_string (String): Raw address string to try and parse
        expected_fields (List): List of fields that are needed to be parsed to be
            considered successful
    Return:
        parsed_address (Dict): Dict of the parsed address with fields that could be
            determined from a string
    """
```

```
def parse_address_using_lib_usaddress(address_string):
    """
    Purpose:
        Use the usaddress library to parse a string into a dict
    Args:
        address_string (String): Raw address string to try and parse
    Return:
        parsed_address (Dict): Dict of the parsed address with fields that could be
            determined from a string
    """
```

```
def parse_address_using_lib_streetaddress(address_string):
    """
    Purpose:
        Use the street-address library to parse a string into a dict
    Args:
        address_string (String): Raw address string to try and parse
    Return:
        parsed_address (Dict): Dict of the parsed address with fields that could be
            determined from a string
    """
```

### [mapquest_helpers.py](https://github.com/ChristopherHaydenTodd/ctodd-python-lib-location/blob/master/location_helpers/mapquest_helpers.py)

Mapquest Helpers. This library is used to wrap mapquest API calls and handle authentication

Functions:

```
def get_mapquest_api_key(public_key_file="~/.mapquest/public_key.txt"):
    """
    Purpose:
        Get the mapquest API from the environment
    Args:
        public_key_file (String): filename of the public key token file
    Return:
        mapquest_api_key (String): MapQuest public key
    """
```

```
def get_directions_between_two_addresses(mapquest_api_key, address_1, address_2):
    """
    Purpose:
        Get directions between two addresses

        Leverages Mapquest API:
            https://developer.mapquest.com/documentation/directions-api/route/get/
    Args:
        address_1 (String): Address to use as start point of travel
        address_2 (String): Address to use as end destination of travel
    Return:
        directions (Dict): Dict of the directions between the two locations
    """
```

## Example Scripts

Example executable Python scripts/modules for testing and interacting with the library. These show example use-cases for the libraries and can be used as templates for developing with the libraries or to use as one-off development efforts.

### [parse_addresses.py](https://github.com/ChristopherHaydenTodd/ctodd-python-lib-location/blob/master/example_usage/parse_addresses.py)

```
    Purpose:
        Parse some set addresses

    Steps:
        - Parse Args
        - Call libs to parse addresses

    function call:
        python3.6 parse_addresses \
            [-h] \
            --addresses ADDRESSES

    example script call:
        python3.6 example_usage/parse_addresses.py \
            --address="REDACTED" \
            --address="REDACTED"
```

### [get_directions_between_addresses.py](https://github.com/ChristopherHaydenTodd/ctodd-python-lib-location/blob/master/example_usage/get_directions_between_addresses.py)

```
    Purpose:
        Get Directions between two addresses.

    Steps:
        - Parse Args
        - Call libs to get directions from args
        - Parse directions for some valuable information

    function call:
        python3.6 get_directions_between_addresses.py \
            [-h] \
            --start-address START_ADDRESS \
            --end-address END_ADDRESS

    example script call:
        python3.6 example_usage/get_directions_between_addresses.py \
            --start-address="REDACTED" \
            --end-address="REDACTED"
```

## Notes

 - Relies on f-string notation, which is limited to Python3.6.  A refactor to remove these could allow for development with Python3.0.x through 3.5.x

## TODO

 - Unittest framework in place, but lacking tests
