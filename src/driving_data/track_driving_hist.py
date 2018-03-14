#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Input File: input.txt
 run `python setup.py install` to use the command `driving_data <input filename>`


"""
from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging

from driving_data import __version__

from datetime import datetime

__author__ = "atarla"
__copyright__ = "atarla"
__license__ = "mit"

_logger = logging.getLogger(__name__)

OUT_FILE = "output.txt"
MIN_AVG_SPEED = 5
MAX_AVG_SPEED = 100
FMT = '%H:%M'


def process_input(n):
    """get input

    Args:
      n (string): string

    Returns:
      nothing
    """
    with open(n) as f:
        drivers = []
        trips = {}
        # make a list of all drivers
        for line in f:
            if line.startswith('D'):
                d_name = line.split()[1]
                drivers.append(d_name)
            else:
                d_name_dict = line.split()[1]
                key, value = d_name_dict, []
                trips.setdefault(key, []).append(line.rstrip())
    total_miles, mph = calculate_miles(drivers, trips)
    final_report = {}
    for name in drivers:
        final_report.setdefault(name, []).append(total_miles.get(name, 0))
        if total_miles.get(name) is not None:
            speed = round(total_miles.get(name) / mph.get(name))
            if MIN_AVG_SPEED < speed < MAX_AVG_SPEED:
                final_report.setdefault(name, []).append(speed)
    # sort report according to decreasing miles
    sorted_x = sorted(final_report.items(), key=lambda e: e[1][0], reverse=True)
    create_report(sorted_x)

    return 'no'


def calculate_miles(drivers, trips):
    """calculate total miles and average speed

        Args:
          drivers (list): list of strings
          trips (dict): trips taken by each driver

        Returns:
          total miles travelled and average speed
        """
    total_miles = {}
    mph = {}
    miles = 0.0

    for k, dk in trips.items():
        if k in drivers:
            individual_trips = [listitem for listitem in dk]
            # calculate total trip time
            miles = [float(token.split()[4]) for token in individual_trips]
            # calculate average speed
            tdelta = [(datetime.strptime(str(token.split()[3]), FMT) - datetime.strptime(str(token.split()[2]),
                                                                                         FMT)).seconds / 3600.0 for
                      token in individual_trips]
            total_miles.setdefault(k, round(sum(miles)))
            mph.setdefault(k, sum(tdelta))
    return total_miles, mph


def create_report(sorted_x):
    """create report and save it in output file

        Args:
          sorted_x (dict): dict

        Returns:
          nothing
        """
    output = open(OUT_FILE, 'w')
    for key, value in sorted_x:
        try:
            output.write(key + ": " + str(value[0]) + " miles")
            output.write(" @ " + str(value[1]) + " mph")
            output.write('\n')
        except:
            pass

def setup_logging():
    # Setup basic logging
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=20, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    filename = sys.argv[-1]
    print(filename)
    setup_logging()
    _logger.debug("Starting program...")
    process_input(filename)
    print('Report generated in output.txt')
    _logger.info("Program ends here")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
