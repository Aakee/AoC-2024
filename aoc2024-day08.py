# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====
Solution for the Advent of Code 2024, day 8 challenge.
More information from the official website: https://adventofcode.com/2024

==========
HOW TO RUN
==========
You can run the script by calling
    [path-to-python-intepreter] [path-to-this-script] [path-to-input-text-file]
For example:
    python3 ./aoc2023-day08.py ./inputs/day08.txt

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
FILENAME = "./inputs/day08.txt"


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

def find_antennas(data):
    '''Function finds all antennas from the list and returns them in a dict.'''
    antennas = {}
    # Find antennas from the lis
    for row_idx, row in enumerate(data):
        for col_idx, char in enumerate(row):
            if len(char.strip()) == 0:
                continue
            if char == '.':
                continue
            if char not in antennas:
                antennas[char] = []
            antennas[char].append([row_idx, col_idx])
    return antennas


def find_antinote_locations(coord1, coord2):
    '''Function finds and returns both antinode locations between two antennas' coordinates for part 1.'''
    # The following equations are the result of simple linear algebra done on paper, trust me bro
    # A=antenna1, B=antenna2, N=antinode, [QW]=vector from Q to W, x_s = x-component of s, y_s = y-component of s
    # For the one closer to A:
    #       2*[NA] = [NB]
    #   ->  2*(x_a - x_n) = x_b - x_n ;     2*(y_a - y_n) = y_b - y_n
    #   ->  x_n = 2*x_a - x_b ;             y_n = 2*y_a -y_b
    # And similarly to the one closer to B:
    #       x_n = 2*x_b - x_a ;             y_n = 2*y_b -y_a
    return [[2*coord1[0]-coord2[0], 2*coord1[1]-coord2[1]], [2*coord2[0]-coord1[0], 2*coord2[1]-coord1[1]]]

def find_antinote_harmonics(coord1, coord2, max_row, max_col):
    '''Function finds and returns all antinode locations between two antennas' coordinates for part 2.'''
    def antinodes_to_direction(row, col, max_row, max_col, delta_row, delta_col):
        '''Finds all antinodes from starting row and col up until max_row and max_col, when each antinode happens every delta_row rows and delta_col cols.'''
        coordinates = []
        while 0 <= row <= max_row and 0 <= col <= max_col:
            coordinates.append([row,col])
            row += delta_row
            col += delta_col
        return coordinates

    # Distances between two antinodes in y- and x-coordinates
    delta_row, delta_col = coord2[0]-coord1[0], coord2[1]-coord1[1]

    # Final antinodes: start from each of the two antennas and proceed until out of bounds
    return antinodes_to_direction(coord2[0], coord2[1], max_row, max_col, delta_row, delta_col) + antinodes_to_direction(coord1[0], coord1[1], max_row, max_col, -delta_row, -delta_col)


# =========================

def part1(data: list) -> int:
    '''
    Solution for the part 1.
    '''
    antennas = find_antennas(data)
    antinodes = {}
    for freq, coords in antennas.items():
        # Loop over every pair of coordinates of the same kind of antenna
        for coord1, coord2 in itertools.combinations(coords,r=2):
            antinode_coordinates = find_antinote_locations(coord1, coord2)
            # Loop through each antinode location and mark it as such, if inside map bounds
            for (row, col) in antinode_coordinates:
                if 0 <= row < len(data) and 0 <= col < len(data[0]):
                    antinodes[f"{row},{col}"] = True
    return len(antinodes)


def part2(data: list) -> int:
    '''
    Solution for the part 2.
    '''
    antennas = find_antennas(data)
    antinodes = {}
    for freq, coords in antennas.items():
        # Loop over every pair of coordinates of the same kind of antenna
        for coord1, coord2 in itertools.combinations(coords,r=2):
            antinode_coordinates = find_antinote_harmonics(coord1, coord2, len(data)-1, len(data[0])-1)
            # Loop through each antinode location and mark it as such (already checked if inside map bounds in find_antinode_harmonics)
            for (row, col) in antinode_coordinates:
                antinodes[f"{row},{col}"] = True
    return len(antinodes)

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
