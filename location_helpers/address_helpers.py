"""
    Purpose:
        Address Helpers

        This library is used to interact with address strings/dicts and
        convert/handle these addresses
"""

# Python Library Imports
import logging
import usaddress
import re
import requests
from bs4 import BeautifulSoup
from streetaddress import StreetAddressFormatter, StreetAddressParser


###
# Address Parsers
###


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

    # Setting Local Scope
    parsed_address = {}
    missing_fields = []
    if not expected_fields:
        expected_fields = []

    address_parsers = {
        "usaddress": parse_address_using_lib_usaddress,
        "streetaddress": parse_address_using_lib_streetaddress,
    }

    for parser_name, parser_function in address_parsers.items():

        lib_parser_address = parser_function(address_string)

        # Check for Missing Fields
        for expected_field in expected_fields:
            if expected_field not in lib_parser_address:
                missing_fields.append(expected_field)

        if not lib_parser_address:
            logging.error(f"Failed to Parse Address: {address_string}")
        elif missing_fields:
            logging.error(
                f"Parsed Address ({address_string}), but missing fields"
                f" ({missing_fields})"
            )
            logging.error(f"Partial Results ({parser_name}): {parsed_address}")
        else:
            parsed_address = lib_parser_address
            break

    return parsed_address


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

    field_mapping = {
        "AddressNumber": "address_number",
        "PlaceName": "city",
        "Recipient": "ignore",
        "StateName": "state",
        "StreetName": "street_name",
        "StreetNamePostType": "street_type",
        "ZipCode": "zip_code",
    }
    regex_remove_nonmatching_characters = r"[^A-Za-z0-9\-]+"
    usaddress_result = {}

    raw_usaddress_result = usaddress.parse(address_string)
    for field_tuple in raw_usaddress_result:

        # Break Tuple
        address_value = field_tuple[0]
        raw_address_key = field_tuple[1]

        # Parsing Raw into wanted form
        address_key = field_mapping.get(raw_address_key, None)
        if not address_key:
            raise Exception(f"Missing Field Mapping: {raw_address_key}")
        elif address_key == "ignore":
            continue

        if isinstance(address_value, str):
            usaddress_result[address_key] =\
                re.sub(regex_remove_nonmatching_characters, " ", address_value).strip()
        else:
            usaddress_result[address_key] = address_value


    return usaddress_result


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

    field_mapping = {
        "house": "address_number",
        "other": "ignore",
        "PlaceName": "city",
        "StateName": "state",
        "street_full": "ignore",
        "street_name": "street_name",
        "street_type": "street_type",
        "suite_num": "suite_num",
        "suite_type": "suite_type",
        "ZipCode": "zip_code",
    }
    regex_remove_nonmatching_characters = r"[^A-Za-z0-9\-]+"
    streetaddress_result = {}

    streetaddress_parser = StreetAddressParser()
    raw_streetaddress_result = streetaddress_parser.parse(address_string)

    for raw_address_key, address_value in raw_streetaddress_result.items():

        # Parsing Raw into wanted form
        address_key = field_mapping.get(raw_address_key, None)
        if not address_key:
            raise Exception(f"Missing Field Mapping: {raw_address_key}")
        elif address_key == "ignore":
            continue

        if isinstance(address_value, str):
            streetaddress_result[address_key] =\
                re.sub(regex_remove_nonmatching_characters, " ", address_value).strip()
        else:
            streetaddress_result[address_key] = address_value

    return streetaddress_result


###
# Address Locators
###


def search_google_for_address(address_query_string):
    """
    Purpose:
        Get address from Google (if possible) based on a query string

        Note: Works best with a company name, city, state if the company has
        an address posted

        Examples of Working Queries:
            - "Deptford Best Buy"
            - "Two Six Labs Mount Laurel NJ"
            - "Taco Bell Mantua"
    Args:
        raw_query (String): Raw string for searching on Google
    Returns:
        raw_search_html (Dict): Raw HTML of the Google search
    """
    logging.info(f"Searching for Address for: {address_query_string}")

    address = None

    # Preparing Search
    regex_remove_characters = r"[^A-Za-z0-9]+"
    address_query_string = re.sub(
        regex_remove_characters, " ", address_query_string
    ).replace(" ", "+").strip().lower()

    # Requesting HTML From Google
    google_search_url = f"https://www.google.com/search?q={address_query_string}"
    google_search_response = requests.get(google_search_url)

    # import gnureadline, pdb; pdb.set_trace()
    if google_search_response.status_code == 200:
        raw_search_html = google_search_response.text
    else:
        logging.error(
            f"Got Failure Response from Google.com: {search_url}"
            f"{google_search_response.status_code}"
        )
        raw_search_html = None


    google_search_soup = BeautifulSoup(raw_search_html, "html.parser")
    details_spans = google_search_soup.findAll("span", {"class": "BNeawe"})

    details = {}
    for idx in range(0, len(details_spans), 2):
        details[details_spans[idx].text.lower()] = details_spans[idx+1].text

    return details.get("address", None)
