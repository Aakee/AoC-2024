# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====
Solution for the Advent of Code 2024, day 3 challenge.
More information from the official website: https://adventofcode.com/2024

==========
HOW TO RUN
==========
You can run the script by calling
    [path-to-python-intepreter] [path-to-this-script] [path-to-input-text-file]
For example:
    python3 ./aoc2023-day01.py ./inputs/day03.txt

Alternatively, you can modify the FILENAME constant at the beginning of the script to give the path to the input file.
If both command line argument and hard-coded filename is given, the command line argument takes precedence.

======
GIT REPOSITORY
======
The git repository for my solutions for AoC 2024 challenges can be found here: https://github.com/Aakee/AoC-2024
'''

import argparse
import logging
import re

LOGLEVEL = logging.WARNING
logging.basicConfig(level=LOGLEVEL, format="%(asctime)s - %(levelname)s - %(message)s")


# Type the path to your input text file here if you do not wish to use the command line argument
FILENAME = "./inputs/day03.txt"


def load_file(fn: str):
    '''
    Function loads the contents of the given text file and returns the contents as a list.
    @param fn:      path to the file to-be-loaded
    @returns:       contents of the file as a list, one entry corresponding to one line
    '''
    with open(fn,'r') as file:
        data = ''.join([line.strip() for line in file if len(line.strip()) > 0])
    return data

# =========================

def find_matches(s:str) -> list:
    '''
    Function finds and returns in a list all valid 'mul' commands from as per the assignment,
    i.e. all substrings of format 'mul(X,Y)', where X and Y are integers with 1-3 digits.
    '''
    pattern = r"mul\(\d{1,3},\d{1,3}\)"
    return re.findall(pattern, s)

def mul(s: str) -> int:
    '''
    Function executes a 'mul' command as per the assignment. Function takes as a parameter one valid 'mul' command,
    i.e. a string with format 'mul(X,Y)', where X and Y are integers with 1-3 digits.
    Function returns the product of the command, that is, X*Y.
    '''
    pattern = r"\d{1,3}"
    values = re.findall(pattern, s)
    return int(values[0]) * int(values[1])


# =========================
        
def part1(data: str) -> int:
    '''
    Solution for the part 1.
    '''
    # Find all valid 'mul' commands from the data, and execute the command on each of them
    mults = [mul(cmd) for cmd in find_matches(data)]
    # Calculate and return the sum of the products
    return sum(mults)


def part2(data: str) -> int:
    '''
    Solution for the part 2.
    '''
    # Parse the data:
    # 1. Split the data with 'don't()'.
    # 2. Split each of these substrings with the first 'do()'. 
    # 3. The valid segments are everything after the first do() in every segments, i.e. the second element in the segments splitted by 'do()' in step 2.
    #    (If there are multiple do()'s in the segment, the rest apart the first don't do anything.)
    applicable_data = [segment.split("do()",1)[1] for segment in data.split("don't()") if "do()" in segment]
    # Add the very first segment (the segment before any 'don't()'s)
    applicable_data = [data.split("don't()")[0]] + applicable_data
    applicable_data = ''.join(applicable_data)
    # Calculate the products and their sum as in part 1
    mults = [mul(cmd) for cmd in find_matches(applicable_data)]
    return sum(mults)

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
