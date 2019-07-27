#!/usr/bin/env python3.6
"""
    Purpose:
        Get address from Google (if possible) based on a query string

        Note: Works best with a company name, city, state if the company has
        an address posted

        Examples of Working Queries:
            - "Deptford Best Buy"
            - "Two Six Labs Mount Laurel NJ"
            - "Taco Bell Mantua"
    Steps:
        - Parse Args
        - Call libs to get address if possible
        - Return address

    function call:
        python3.6 get_addresses_from_google.py \
            [-h] \
            --searches SEARCHES

    example script call:
        python3.6 example_usage/get_directions_between_addresses.py \
            --searches="Deptford Best Buy"
            --searches="Two Six Labs Mount Laurel NJ"
            --searches="Taco Bell Mantua"
"""

# Python Library Imports
import logging
import os
import sys
from argparse import ArgumentParser

# Local Library Imports
from location_helpers import address_helpers


def main():
    """
    Purpose:
        Produce to a Kafka Topic
    """
    logging.info("Starting Process to Get Directions Between Two Addresses")

    opts = get_options()

    for search in opts.searches:
        address = address_helpers.search_google_for_address(search)
        import gnureadline, pdb; pdb.set_trace()

    import gnureadline, pdb; pdb.set_trace()

    logging.info("Process to Get Directions Between Two Addresses Complete")


###
# General/Helper Methods
###


def get_options():
    """
    Purpose:
        Parse CLI arguments for script
    Args:
        N/A
    Return:
        N/A
    """

    parser = ArgumentParser(description="Get address based on search")
    required = parser.add_argument_group("Required Arguments")
    optional = parser.add_argument_group("Optional Arguments")

    # Optional Arguments
    # N/A

    # Required Arguments
    required.add_argument(
        "--searches",
        dest="searches",
        help="String to Search for Address",
        required=True,
        type=str,
        action="append",
    )

    return parser.parse_args()


if __name__ == "__main__":

    log_level = logging.INFO
    logging.getLogger().setLevel(log_level)
    logging.basicConfig(
        stream=sys.stdout,
        level=log_level,
        format="[get_addresses_from_google] %(asctime)s.%(msecs)03d %(levelname)s %(message)s",
        datefmt="%a, %d %b %Y %H:%M:%S"
    )

    try:
        main()
    except Exception as err:
        logging.exception(
            "{0} failed due to error: {1}".format(os.path.basename(__file__), err)
        )
        raise err
