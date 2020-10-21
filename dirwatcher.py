#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Gabrielle, John, Arianna"

import sys
import time
import logging
import os
import argparse
import signal



main_dict = {}
logger = logging.getLogger(__name__)

def search_for_magic(ns):
    try:
        for file in main_dict:
            with open(ns.dir + "/" + file, 'r') as f:
                lines = f.readlines()
                for index, line in enumerate(lines):
                    if ns.magicword in line:
                        if index not in main_dict[file]:
                            main_dict[file].append(index)
                            logger.info(
                                "The magic word, " +
                                ns.magicword.upper() + " was found on line "
                                + str(index + 1) + " in " + file)
                        if ns.magicword not in line:
                            logger.info(
                                "The magic word, " +
                                ns.magicword.upper() + " is not found")
    except Exception as e:
        logger.info(e)

def watch_directory(path, magic_string, extension, interval):
    # Your code here
    return


def create_parser():
    # Your code here
    return


def signal_handler(sig_num, frame):
    # Your code here
    return


def main(args):
    # Your code here
    return




# def create_parser():
#     """Create a command line parser object with 2 argument definitions."""
#     parser = argparse.ArgumentParser(
#         description="Extracts and alphabetizes baby names from html.")
#     parser.add_argument(
#         '-e', help='extension of searching file name')
#     parser.add_argument(
#         '-i', help='polling interval program')
#     parser.add_argument(
#         'magic', help='summary file that magic text can be found')
#     parser.add_argument(
#         'path', help='Director to search')
#     parser.add_argument('files', help='filename(s) to parse')
#     return parser





if __name__ == '__main__':
    main(sys.argv[1:])
