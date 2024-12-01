# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====
Solution for the Advent of Code 2024, day XX challenge.
More information from the official website: https://adventofcode.com/2024

==========
HOW TO RUN
==========
You can run the script by calling
    [path-to-python-intepreter] [path-to-this-script] [path-to-input-text-file]
For example:
    python3 ./aoc2023-day01.py ./inputs/day01.txt

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
FILENAME = "./inputs/day01.txt"


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

def format_input_to_lists(input: list):
    '''Formats the input file to two lists, one for each column in the original file.'''
    l1, l2 = list(), list()
    for line in input:
        entries = line.split(" ")
        l1.append(int(entries[0].strip()))
        l2.append(int(entries[-1].strip()))
    return (l1,l2)


# =========================

def part1(data: list) -> int:
    '''Solution for the part 1.'''
    # Collect the two lists from the input file, and sort them
    l1, l2 = format_input_to_lists(data)
    l1.sort()
    l2.sort()
    
    # Loop each pair of elements in the lists, and add their difference to the sum
    ans = 0
    for element1, element2 in zip(l1, l2):
        ans += abs(element1-element2)
    return ans
    

def part2(data: list) -> int:
    '''Solution for the part 2.'''
    # Collect the two lists from the input file
    l1, l2 = format_input_to_lists(data)
    
    # Loop through each element in the first list, multiply it by the number of occurences in the second list, and add that product into the sum
    ans = 0
    for element in l1:
        ans += element * l2.count(element)
    return ans

# =========================

if  __name__ == "__main__":
    # Fetch input text file path, either from the hard-coded variable FILENAME or from command line argument if given
    parser = argparse.ArgumentParser()
    parser.add_argument('input_fn', nargs='?', default=FILENAME, help="Path to the input text file. Optional; if not given, will default to the one hard-coded in the beginning of the script file.")
    args =  parser.parse_args()

    # Load the data
    data = load_file(args.input_fn)

    # Execute and print the solutions
    print(f"Part 1 solution: {part1(data)}")
    print(f"Part 2 solution: {part2(data)}")
