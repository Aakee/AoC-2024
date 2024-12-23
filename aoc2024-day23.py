# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====
Solution for the Advent of Code 2024, day 23 challenge.
More information from the official website: https://adventofcode.com/2024

==========
HOW TO RUN
==========
You can run the script by calling
    [path-to-python-intepreter] [path-to-this-script] [path-to-input-text-file]
For example:
    python3 ./aoc2024-day23.py ./inputs/day23.txt

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
FILENAME = "./inputs/day23.txt"


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

def construct_graph(data:list) -> dict:
    '''
    Converts the given connections into dictionary, where keys are the node names.
    The dictionary entries are lists including the neighbours of the node in the dict key.
    '''
    nodes = {}
    # Construct node connections
    for connection in data:
        n1, n2 = connection.split("-")
        n1, n2 = n1.strip(), n2.strip()
        if n1 not in nodes:
            nodes[n1] = list()
        if n2 not in nodes:
            nodes[n2] = list()
        nodes[n1].append(n2)
        nodes[n2].append(n1)
    logging.debug(f"Nof nodes: {len(nodes)}")
    return nodes


# =========================

def part1(data: list) -> int:
    '''
    Solution for the part 1.
    '''
    nodes = construct_graph(data)
    
    # Find the triplets
    triplets = []
    for first, neighbours in nodes.items():
        if first[0] != 't':
            continue
        # Loop for each neighbour in the first, and for each neighbour in the second
        for second in neighbours:
            for third in nodes[second]:
                # If the third is the first's neighbour, this is a valid triplet
                if third in nodes[first]:
                    trip = [first, second, third]
                    trip.sort()
                    key = ','.join(trip)
                    if key not in triplets:
                        triplets.append(key)
    return len(triplets)


def part2(data: list) -> str:
    '''
    Solution for the part 2.
    '''
    def _traverse_recursively(all_nodes: dict, current_subgraph: list, all_subgraphs: dict):
        '''Function recursively tries to add new nodes to the subgraph and adds the new (valid) subgraphs to the dict all_subgraphs.'''
        # Loop through all neighbours in the first node in the subgraph (could be all nodes, but this is to reduce number of iterations, as all new nodes must be neighbours of the first, too)
        for node_candidate in all_nodes[current_subgraph[0]]:
            # Skip if the new node is already in the subgraph
            if node_candidate in current_subgraph:
                continue
            # Check whether the new candidate node is a neighbour of all existing nodes, and skip if it is not
            is_applicable = [node_candidate in all_nodes[existing_node] for existing_node in current_subgraph]
            if not all(is_applicable):
                continue
            # Add the new node to the subgraph, sort the subgraph, and convert the subgraph to a string
            new_subgraph = list(current_subgraph)
            new_subgraph.append(node_candidate)
            new_subgraph.sort()
            key = ','.join(new_subgraph)
            # Process the new subgraph only if it has not previously been processed
            if key not in all_subgraphs:
                all_subgraphs[key] = True
                _traverse_recursively(all_nodes, new_subgraph, all_subgraphs)

    nodes = construct_graph(data)
    
    # Collect all subgraphs to this dictionary (subgraph as key, entries are just dummies :D)
    all_subgraphs_dict = {}
    # Loop through with every node as the starting point of the subgraph
    for num,node in enumerate(nodes, start=1):
        logging.debug(f"{num} / {len(nodes)}")
        _traverse_recursively(nodes,[node],all_subgraphs_dict)

    # Collect the subgraphs to a list, sort it by the subgraph length, and return the longest subgraph
    all_subgraphs = [subgraph for subgraph in all_subgraphs_dict]
    all_subgraphs.sort(key=lambda x: len(x), reverse=True)
    return all_subgraphs[0]

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
