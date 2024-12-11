# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====
Solution for the Advent of Code 2024, day 10 challenge.
More information from the official website: https://adventofcode.com/2024

==========
HOW TO RUN
==========
You can run the script by calling
    [path-to-python-intepreter] [path-to-this-script] [path-to-input-text-file]
For example:
    python3 ./aoc2024-day10.py ./inputs/day10.txt

Alternatively, you can modify the FILENAME constant at the beginning of the script to give the path to the input file.
If both command line argument and hard-coded filename is given, the command line argument takes precedence.

======
GIT REPOSITORY
======
The git repository for my solutions for AoC 2024 challenges can be found here: https://github.com/Aakee/AoC-2024
'''

import argparse
import itertools
import logging

LOGLEVEL = logging.WARNING
logging.basicConfig(level=LOGLEVEL, format="%(asctime)s - %(levelname)s - %(message)s")


# Type the path to your input text file here if you do not wish to use the command line argument
FILENAME = "./inputs/day10.txt"


def load_file(fn: str):
    '''
    Function loads the contents of the given text file and returns the contents as a list.
    @param fn:      path to the file to-be-loaded
    @returns:       contents of the file as a list, one entry corresponding to one line
    '''
    with open(fn,'r') as file:
        lines = [[int(val) for val in line.strip()] for line in file if len(line.strip()) > 0]
    logging.debug(f"No of input lines: {len(lines)}")
    return lines

# =========================

DIRECTIONS = [
    [ 1, 0],
    [-1, 0],
    [ 0, 1],
    [ 0,-1]
]


def trails_from(map, row_start, col_start) -> list:
    '''
    Function determines all trails starting from the starting coordinates and returns the peaks in a list, as strings in format "peak_row,peak_col".
    Any peak can exist in the list multiple times if there are multiple distinct trails leading to said peak.
    '''
    def _traverse_recursively(map, row, col, previous_val, peaks):
        '''Traverses the map recursively, trying to find a trail towards the peaks.'''
        # Not a valid trail if coordinates are out of the map
        if not 0 <= row < len(map) or not 0  <= col < len(map[0]):
            return
        current_val = map[row][col]
        # Not a valid trail if the current height is not exactly one more than the previous height
        if current_val != previous_val + 1:
            return
        # If reached a 9, this is a valid trail
        if current_val == 9:
            peaks.append(f"{row},{col}")
            return
        # Loop through each direction and continue the trails
        for direction in DIRECTIONS:
            _traverse_recursively(map, row+direction[0], col+direction[1], current_val, peaks)
    # Determine height of the starting coordinates and return empty list, if the height is not 0
    val = map[row_start][col_start]
    if val != 0:
        return []
    
    # Collect all trail peaks starting from the starting coordinates into the list peaks and return it
    peaks = list()
    _traverse_recursively(map, row_start, col_start, -1, peaks)
    return peaks
    

# =========================

def part1(data: list) -> int:
    '''
    Solution for the part 1.
    '''
    ans = 0
    for row, col in itertools.product(range(len(data)), range(len(data[0]))):
        peaks = trails_from(data, row, col)
        # Count each peak only once
        ans += len(set(peaks))
    return ans


def part2(data: list) -> int:
    '''
    Solution for the part 2.
    '''
    ans = 0
    for row, col in itertools.product(range(len(data)), range(len(data[0]))):
        peaks = trails_from(data, row, col)
        # Count each peak as many times as there are distinct trails to it
        ans += len(peaks)
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
