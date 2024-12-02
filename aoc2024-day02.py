# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====
Solution for the Advent of Code 2024, day 2 challenge.
More information from the official website: https://adventofcode.com/2024

==========
HOW TO RUN
==========
You can run the script by calling
    [path-to-python-intepreter] [path-to-this-script] [path-to-input-text-file]
For example:
    python3 ./aoc2023-day01.py ./inputs/day02.txt

Alternatively, you can modify the FILENAME constant at the beginning of the script to give the path to the input file.
If both command line argument and hard-coded filename is given, the command line argument takes precedence.

======
GIT REPOSITORY
======
The git repository for my solutions for AoC 2024 challenges can be found here: https://github.com/Aakee/AoC-2024
'''

import argparse
import logging

LOGLEVEL = logging.WARNING
logging.basicConfig(level=LOGLEVEL, format="%(asctime)s - %(levelname)s - %(message)s")


# Type the path to your input text file here if you do not wish to use the command line argument
FILENAME = "./inputs/day02.txt"


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

def line2levels(line):
    '''Splits one line in the input file into levels (i.e. splits by spaces) and converts entries to integers'''
    return [int(level) for level in line.split(" ") if len(level) > 0]

def is_safe(levels: list[int]):
    '''Determines if the input list is safe according to the rules (strictly ascending or descending, max 3 steps between adjacent entries)'''
    # For each pair of adjacent entries in the list, calculate their difference
    diffs = [second - first for first, second in zip(levels[:-1], levels[1:])]
    # Safe is each difference is between 1 and 3 (inclusive) for ascending sequence, or between -3 and -1 (inclusive) for descending sequence
    return all(3 >= diff >= 1 for diff in diffs) or all(-3 <= diff <= -1 for diff in diffs)

def is_safe_with_removal(levels: list[int]):
    '''Determines if the input list is safe according to the rules, if at most one entry is removed'''
    # Check if the line is safe even without any entries removed
    if is_safe(levels):
        return True
    # Loop through each element in the line and check if the line is safe if that entry is removed
    for removed_idx in range(len(levels)):
        if is_safe(levels[:removed_idx] + levels[removed_idx+1:]):
            return True
    # If none of the previous apply, the line is not safe
    return False


# =========================

def part1(data: list) -> int:
    '''Solution for the part 1'''
    safe_lines = [line for line in data if is_safe(line2levels(line))]
    return len(safe_lines)


def part2(data: list) -> int:
    '''Solution for the part 2'''
    safe_lines = [line for line in data if is_safe_with_removal(line2levels(line))]
    return len(safe_lines)

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
