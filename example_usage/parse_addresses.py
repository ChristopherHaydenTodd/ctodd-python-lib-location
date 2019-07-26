#!/usr/bin/env python3.6
"""
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
    logging.info("Starting Parse Addresses")

    opts = get_options()

    for raw_address in opts.addresses:
        parsed_address = address_helpers.convert_string_address_to_dict(raw_address)

    import gnureadline, pdb; pdb.set_trace()

    logging.info("Parse Addresses Complete")


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

    parser = ArgumentParser(description="Parse Addresses")
    required = parser.add_argument_group("Required Arguments")
    optional = parser.add_argument_group("Optional Arguments")

    # Optional Arguments
    # N/A

    # Required Arguments
    required.add_argument(
        "--addresses",
        dest="addresses",
        help="Start address for directions",
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
