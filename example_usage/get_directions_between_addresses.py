#!/usr/bin/env python3.6
"""
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
"""

# Python Library Imports
import logging
import os
import sys
from argparse import ArgumentParser

# Local Library Imports
from location_helpers import mapquest_helpers


def main():
    """
    Purpose:
        Produce to a Kafka Topic
    """
    logging.info("Starting Process to Get Directions Between Two Addresses")

    opts = get_options()

    mapquest_api_key = mapquest_helpers.get_mapquest_api_key()
    directions_between_two_addresses = mapquest_helpers.get_directions_between_two_addresses(
        mapquest_api_key, opts.start_address, opts.end_address
    )

    logging.info(f"Directions Between: {opts.start_address} and {opts.end_address}")

    travel_time_in_seconds = directions_between_two_addresses["route"]["time"]
    travel_distance_in_miles = directions_between_two_addresses["route"]["distance"]
    logging.info(f"Time in Seconds Between Addresses: {travel_time_in_seconds} seconds")
    logging.info(f"Distance Between Addresses: {travel_distance_in_miles} miles")

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

    parser = ArgumentParser(description="Get Directions Between Two Addresses")
    required = parser.add_argument_group("Required Arguments")
    optional = parser.add_argument_group("Optional Arguments")

    # Optional Arguments
    # N/A

    # Required Arguments
    required.add_argument(
        "--start-address",
        dest="start_address",
        help="Start address for directions",
        required=True,
        type=str,
    )
    required.add_argument(
        "--end-address",
        dest="end_address",
        help="End address for directions",
        required=True,
        type=str,
    )

    return parser.parse_args()


if __name__ == "__main__":

    log_level = logging.INFO
    logging.getLogger().setLevel(log_level)
    logging.basicConfig(
        stream=sys.stdout,
        level=log_level,
        format="[parse_addresses] %(asctime)s.%(msecs)03d %(levelname)s %(message)s",
        datefmt="%a, %d %b %Y %H:%M:%S"
    )

    try:
        main()
    except Exception as err:
        logging.exception(
            "{0} failed due to error: {1}".format(os.path.basename(__file__), err)
        )
        raise err
