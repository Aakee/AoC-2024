# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====
Solution for the Advent of Code 2024, day 22 challenge.
More information from the official website: https://adventofcode.com/2024

==========
HOW TO RUN
==========
You can run the script by calling
    [path-to-python-intepreter] [path-to-this-script] [path-to-input-text-file]
For example:
    python3 ./aoc2024-day22.py ./inputs/day22.txt

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
FILENAME = "./inputs/day22.txt"


def load_file(fn: str):
    '''
    Function loads the contents of the given text file and returns the contents as a list.
    @param fn:      path to the file to-be-loaded
    @returns:       contents of the file as a list, one entry corresponding to one line
    '''
    with open(fn,'r') as file:
        lines = [int(line.strip()) for line in file if len(line.strip()) > 0]
    logging.debug(f"No of input lines: {len(lines)}")
    return lines

# =========================

def mix(val1: int, val2: int) -> int:
    '''Does the mix operation as per the assignment'''
    return val1 ^ val2

def prune(val: int) -> int:
    '''Does the prune operation as per the assignment'''
    return val % 16777216

def next_secret_number(val: int) -> int:
    '''Calculates the next pseudorandom value based on the previous one'''
    val = prune(mix(val, val*64))
    val = prune(mix(val, math.floor(val/32)))
    val = prune(mix(val, val*2048))
    return val

# =========================

def part1(data: list) -> int:
    '''
    Solution for the part 1.
    '''
    ans = 0
    for val in data:
        for _ in range(2000):
            val = next_secret_number(val)
        ans += val
    return ans


def part2(data: list) -> int:
    '''
    Solution for the part 2.
    '''
    # Dict holding the total prices for each combination of four price changes
    all_changes = {}
    for idx, val in enumerate(data):
        # Latest 4 price changes
        latest_changes = []
        # Prices for the four price-change combinations, if given to this monkey
        changes_for_this_monkey = {}
        old_price = val % 10
        # Loop 2000 times
        for _ in range(2000):
            val = next_secret_number(val)
            new_price = val % 10
            # Add the new price difference to the list latest_changes, and drop first element if there are more than four elements
            latest_changes.append(new_price-old_price)
            if len(latest_changes) > 4:
                latest_changes = latest_changes[1:]
            # If the list is full (four entries)
            if len(latest_changes) >= 4:
                key = ','.join([str(change) for change in latest_changes])
                # Save the price, if the change combintion had not been encountered before
                if key not in changes_for_this_monkey:
                    changes_for_this_monkey[key] = new_price
            old_price = new_price
        # For each entry in this monkey's haggle dictionary, add the price to total price
        for key, price in changes_for_this_monkey.items():
            if key not in all_changes:
                all_changes[key] = 0
            all_changes[key] += price
    # Find and return the maximum price
    max_price = 0
    for key, total_price in all_changes.items():
        if total_price > max_price:
            max_price = total_price
    return max_price

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
