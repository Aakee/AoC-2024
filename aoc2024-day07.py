# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====
Solution for the Advent of Code 2024, day 7 challenge.
More information from the official website: https://adventofcode.com/2024

==========
HOW TO RUN
==========
You can run the script by calling
    [path-to-python-intepreter] [path-to-this-script] [path-to-input-text-file]
For example:
    python3 ./aoc2023-day07.py ./inputs/day07.txt

Alternatively, you can modify the FILENAME constant at the beginning of the script to give the path to the input file.
If both command line argument and hard-coded filename is given, the command line argument takes precedence.

======
GIT REPOSITORY
======
The git repository for my solutions for AoC 2024 challenges can be found here: https://github.com/Aakee/AoC-2024
'''

import argparse
import collections
import itertools
import logging
import math

LOGLEVEL = logging.WARNING
logging.basicConfig(level=LOGLEVEL, format="%(asctime)s - %(levelname)s - %(message)s")


# Type the path to your input text file here if you do not wish to use the command line argument
FILENAME = "./inputs/day07.txt"


def load_file(fn: str):
    '''
    Function loads the contents of the given text file and returns the contents as a list.
    @param fn:      path to the file to-be-loaded
    @returns:       contents of the file as a list, one entry corresponding to one line
    '''
    with open(fn,'r') as file:
        lines = [line.strip() for line in file if len(line.strip()) > 0]
    logging.debug(f"No of input lines: {len(lines)}")
    return lines

# =========================

def check_values(test_value, current_total, calibration_values, idx, concatenation_allowed=False) -> bool:
    '''
    Recursively checks whether the test value can be achieved with any operations from the calibration values.
    @param test_value:              The goal value
    @param current_total:           The intermediate total thus far
    @param calibration_values:      The list of all calibration values to be used
    @param idx:                     The index from calibration_values to be used next
    @param concatenation_allowed:   Whether to allow also concatenation operation (in part 2)
    '''
    # Base case: all calibration values used
    if idx >= len(calibration_values):
        return current_total == test_value
    # Stop early if test value exceeded. The total cannot decrease, meaning that exactly the total can no longer be achieved
    if current_total > test_value:
        return False
    # Check addition
    success = check_values(test_value, current_total + calibration_values[idx], calibration_values, idx+1, concatenation_allowed=concatenation_allowed)
    # Check multiplication
    if not success:
        success = check_values(test_value, current_total * calibration_values[idx], calibration_values, idx+1, concatenation_allowed=concatenation_allowed)
    # Check concatenation (if allowed by the assignment)
    if not success and concatenation_allowed:
        success = check_values(test_value, int(str(current_total)+str(calibration_values[idx])), calibration_values, idx+1, concatenation_allowed=concatenation_allowed)
    return success



# =========================

def part1(data: list) -> int:
    '''
    Solution for the part 1.
    '''
    ans = 0
    for row in data:
        test_value, calibration_values = row.split(':')
        test_value = int(test_value)
        calibration_values = [int(val.strip()) for val in calibration_values.split(" ") if len(val) > 0]
        success = check_values(test_value, calibration_values[0], calibration_values, 1, concatenation_allowed=False)
        if success:
            ans += test_value
    return ans


def part2(data: list) -> int:
    '''
    Solution for the part 2.
    '''
    ans = 0
    for row in data:
        test_value, calibration_values = row.split(':')
        test_value = int(test_value)
        calibration_values = [int(val.strip()) for val in calibration_values.split(" ") if len(val) > 0]
        success = check_values(test_value, calibration_values[0], calibration_values, 1, concatenation_allowed=True)
        if success:
            ans += test_value
    return ans

# =========================

if  __name__ == "__main__":
    # Fetch input text file path, either from the hard-coded variable FILENAME or from command line argument (if given)
    parser = argparse.ArgumentParser()
    parser.add_argument('input_fn', nargs='?', default=FILENAME, help="Path to the input text file. Optional; if not given, will default to the one hard-coded in the beginning of the script file.")
    args =  parser.parse_args()

    # Load the data
    data = load_file(args.input_fn)

    # Execute and print the solutions
    print(f"Part 1 solution: {part1(data)}")
    print(f"Part 2 solution: {part2(data)}")
