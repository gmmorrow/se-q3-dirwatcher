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
                                ns.magicword.upper() + " can be found on line "
                                + str(index + 1) + " in " + file)
                        if ns.magicword not in line:
                            logger.info(
                                "The magic word, " +
                                ns.magicword.upper() + " cannot be found")
    except Exception as e:
        logger.info(e)

def watch_directory(ns):
    file_dict = {}
    # while not exit_flag:
    # time.sleep(interval)
    try:
        if os.path.isdir(ns.dir):
            directories = os.listdir(os.path.abspath(ns.dir))
            for files in directories:
                if files.endswith(ns.file):
                    file_dict.setdefault(files, [])
        else:
            logger.info('No directory found')
    except Exception as e:
        logger.info(e)
    detect_dir_changes(file_dict, ns)


def detect_dir_changes(file_dict, ns):
        try:
            for files in file_dict:
                if files not in main_dict:
                    logger.info(files + " has been added to " + ns.dir)
                    main_dict[files] = []
            for files in main_dict:
                if files not in file_dict:
                    logger.info(files + " has been removed from " + ns.dir)
                    del main_dict[files]
        except Exception as e:
            logger.info(e)
        search_for_magic(ns)


def create_parser():
    parser = argparse.ArgumentParser(
        description="Watch for a word to be added.")
    parser.add_argument(
        '-e', help='extension of searching file name')
    parser.add_argument(
        '-i', help='polling interval program')
    parser.add_argument(
        'magic', help='summary file that magic text can be found')
    parser.add_argument(
        'path', help='Director to search')
    parser.add_argument('files', help='filename(s) to parse')
    return parser


def signal_handler(sig_num, frame):
    # Your code here
    return


def main(args):
    # Your code here
    return


if __name__ == '__main__':
    main(sys.argv[1:])
