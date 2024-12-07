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
import collections
import itertools
import logging
import math
import random

LOGLEVEL = logging.WARNING
logging.basicConfig(level=LOGLEVEL, format="%(asctime)s - %(levelname)s - %(message)s")


# Type the path to your input text file here if you do not wish to use the command line argument
FILENAME = "./inputs/day05.txt"


def load_file(fn: str):
    '''
    Function loads the contents of the given text file and returns the contents as a list.
    @param fn:      path to the file to-be-loaded
    @returns:       contents of the file as a string
    '''
    with open(fn,'r') as file:
        lines = ''.join(file.readlines())
    #logging.debug(f"No of input lines: {len(lines)}")
    return lines

# =========================

class Rule:
    '''Data class represents one rule.'''
    def __init__(self, first, second) -> None:
        self.first  = first
        self.second = second
    def __repr__(self):
        return f"{self.first}|{self.second}"


def parse_input(data):
    '''Parses the input data into rules and sets of pages.'''
    rules_data, pages_data = data.split("\n\n")
    rules_data = [rule.strip() for rule in rules_data.split("\n") if len(rule.strip()) > 0]
    pages_data = [page.strip() for page in pages_data.split("\n") if len(page.strip()) > 0]

    # Parse the rules
    rules = []
    for rule in rules_data:
        first, second = rule.split("|")
        rules.append(Rule(int(first), int(second)))
    
    # Parse the sets of pages
    pages_list = []
    for pages in pages_data:
        pages_list.append([int(page) for page in pages.split(',')])

    return rules, pages_list


def check_rule(rule: Rule, pages: list):
    '''Checks the given rule against the given list of pages.'''
    second_page_reached = False
    for page in pages:
        if page == rule.first and second_page_reached:
            return False
        if page == rule.second:
            second_page_reached = True
    return True


def check_pages_against_all_rules(pages: list[int], rules: list[Rule]):
    '''Function checks the set of pages against all rules and returns if pages satisfied all rules.'''
    rules_satisfied = [check_rule(rule,pages) for rule in rules]
    return all(rules_satisfied)


def reorder_pages(pages: list[int], rules: list[Rule]):
    '''Reorders the given pages such that the order satisfy all rules.'''
    def unordered_pages(all_pages, ordered_pages):
        return [page for page in all_pages if page not in ordered_pages]
    # Relevant rules => rules whose both pages exist in the list of pages
    relevant_rules = [rule for rule in rules if rule.first in pages and rule.second in pages]

    # The list where the pages are collected in the correct order
    ordered_pages = [pages[0]]

    # Algorithm description:
    # 1. Get the next page that is not yet in the ordered list.
    # 2. Go through the ordered list from the beginning. If there is a rule that specifies an order of (new_page|ordered_page), place the new page immediately before the already ordered page.
    # 3. Get the next page that is not yet in the ordered list.
    # 4. Go through the ordered list from the end. If there is a rule that specifies an order of (ordered_page|new_page), place the new page immediately after the already ordered page.
    # 5. Loop steps 1-4, until all pages have been ordered.
    # The algorithm assumes that there is only one correct order, implicating that there exists always at least one unordered page and one rule, which together determine the position of the
    # new page relative to the already placed pages.
    while len(ordered_pages) < len(pages):
        for new_page, (idx, ordered_page), rule in itertools.product(unordered_pages(pages, ordered_pages), enumerate(ordered_pages), relevant_rules):
            if rule.first == new_page and rule.second == ordered_page:
                ordered_pages.insert(idx, new_page)
                break
        for new_page, idx, rule in itertools.product(unordered_pages(pages, ordered_pages), range(len(ordered_pages)-1,-1,-1), relevant_rules):
            ordered_page = ordered_pages[idx]
            if rule.second == new_page and rule.first == ordered_page:
                ordered_pages.insert(idx+1, new_page)
                break
    return ordered_pages

# =========================

def part1(rules: list, pages_list: list) -> int:
    '''
    Solution for the part 1.
    '''
    ans = 0
    for pages in pages_list:
        if check_pages_against_all_rules(pages, rules):
            ans += pages[int((len(pages)-1)/2)]
    return ans


def part2(rules: list, pages_list: list) -> int:
    '''
    Solution for the part 2.
    '''
    ans = 0
    for pages in pages_list:
        if not check_pages_against_all_rules(pages, rules):
            reordered_pages = reorder_pages(pages, rules)
            ans += reordered_pages[int((len(reordered_pages)-1)/2)]
    return ans

# =========================

if  __name__ == "__main__":
    # Fetch input text file path, either from the hard-coded variable FILENAME or from command line argument (if given)
    parser = argparse.ArgumentParser()
    parser.add_argument('input_fn', nargs='?', default=FILENAME, help="Path to the input text file. Optional; if not given, will default to the one hard-coded in the beginning of the script file.")
    args =  parser.parse_args()

    # Load and parse the data
    data = load_file(args.input_fn)
    rules, pages = parse_input(data)

    # Execute and print the solutions
    print(f"Part 1 solution: {part1(rules, pages)}")
    print(f"Part 2 solution: {part2(rules, pages)}")
