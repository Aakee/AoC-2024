# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====
Solution for the Advent of Code 2024, day 4 challenge.
More information from the official website: https://adventofcode.com/2024

==========
HOW TO RUN
==========
You can run the script by calling
    [path-to-python-intepreter] [path-to-this-script] [path-to-input-text-file]
For example:
    python3 ./aoc2023-day04.py ./inputs/day04.txt

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
import re

LOGLEVEL = logging.WARNING
logging.basicConfig(level=LOGLEVEL, format="%(asctime)s - %(levelname)s - %(message)s")


# Type the path to your input text file here if you do not wish to use the command line argument
FILENAME = "./inputs/day04.txt"


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

def nof_xmas(line:str) -> int:
    '''Returns the number of 'XMAS' written on the line, normally or backwards.'''
    return len(re.findall("XMAS",line)) + len(re.findall("SAMX",line))

def get_columns(data: list[str]) -> list[str]:
    '''Returns columns from the matrix.'''
    return [''.join(list(x)) for x in zip(*data)]

def get_diagonals(data: list[str]) -> list[str]:
    '''Returns all diagonals from the matrix.'''
    def _get_downwards_diagonals(data):
        '''Returns all 'downwards' diagonals, i.e. diagonals travelling from top left to bottom right (or parallel to it).'''
        diags = []
        # Determine each diagonal starting from the first row, travelling to down and right
        for start_col_idx in range(len(data[1])):
            diags.append(''.join( [ data[row_idx][col_idx] for  row_idx, col_idx in zip(range(len(data)), range(start_col_idx, len(data[0])))] ) )
        # Determine each diagonal starting from the first column, travelling to down and right, except the first row (which was taken in the last step)
        for start_row_idx in range(1,len(data)):
            diags.append(''.join( [ data[row_idx][col_idx] for  row_idx, col_idx in zip(range(start_row_idx, len(data)), range(len(data[0])))] ) )
        return diags
    data_flipped = data[::-1]
    return _get_downwards_diagonals(data) + _get_downwards_diagonals(data_flipped)


# =========================

def part1(data: list) -> int:
    '''
    Solution for the part 1.
    '''
    ans = 0
    
    # Check rows
    for row in data:
        ans += nof_xmas(row)

    # Check columns
    for col in get_columns(data):
        ans += nof_xmas(col)

    # Check diagonals
    for diag in get_diagonals(data):
        ans += nof_xmas(diag)

    return ans


def part2(data: list) -> int:
    '''
    Solution for the part 2.
    '''
    def _has_x_mas(data,row_idx, col_idx):
        '''Checks if the character specified by the row_idx and col_idx is the center of a x-mas'''
        if not data[row_idx][col_idx] == 'A':
            return False
        # Top left to down right
        if not (data[row_idx-1][col_idx-1] == 'M' and data[row_idx+1][col_idx+1] == 'S') and not (data[row_idx-1][col_idx-1] == 'S' and data[row_idx+1][col_idx+1] == 'M'):
            return False
        # Down left to top right
        if not (data[row_idx+1][col_idx-1] == 'M' and data[row_idx-1][col_idx+1] == 'S') and not (data[row_idx+1][col_idx-1] == 'S' and data[row_idx-1][col_idx+1] == 'M'):
            return False
        return True
    
    ans = 0
    # Iterate over all characters in the grid, except for the edge rows and columns (as they canmnot contain the center character of a x-mas)
    for row_idx, col_idx in itertools.product(range(1,len(data)-1), range(1,len(data[0])-1)):
        if _has_x_mas(data, row_idx, col_idx):
            ans += 1
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
