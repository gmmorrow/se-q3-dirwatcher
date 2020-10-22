#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Gabrielle, John, Arianna, Lori"

import sys
import time
import logging
import os
import argparse
import signal
import errno


main_dict = {}
logger = logging.getLogger(__name__)
exit_flag = False


def search_for_magic(path, start_line, magic_word):
    line_number = 0
    with open(path) as f:
        for line_number, line in enumerate(f):
            if line_number >= start_line:
                if magic_word in line:
                    logger.info(f"Match found for {magic_word}"
                                f"found on line {line_number+1} in {path}"
                                )
    return line_number + 1


def watch_directory(args):
    file_list = os.listdir(args.directory)
    detect_dir_changes(file_list, args.extension)
    detect_removed_files(file_list)
    for f in main_dict:
        path = os.path.join(args.directory, f)
        main_dict[f] = search_for_magic(
            path,
            main_dict[f],
            args.magic_word
        )
    return main_dict


def detect_dir_changes(file_dict, ext):
    global main_dict
    for f in file_dict:
        if f.endswith(ext) and f not in main_dict:
            main_dict[f] = 0
            logger.info(f"{f} has been added to watchlist.")
    return file_dict


def detect_removed_files(file_dict):
    # """Checks the directory if a given file was deleted"""
    global main_dict
    for f in list(main_dict):
        if f not in file_dict:
            logger.info(f"{f} removed from watchlist.")
            del main_dict[f]
    return file_dict


def create_parser():
    parser = argparse.ArgumentParser(
        description="Watch for a word to be added.")
    parser.add_argument('directory', help='directory to monitor')
    parser.add_argument('magic_word', help='The magic word/words to watch for')
    parser.add_argument('-i',
                        '--interval',
                        help='Sets the interval in seconds to check the '
                             'directory for magic words',
                        type=float,
                        default=1.0)
    parser.add_argument('-x', '--extension',
                        help='Sets the type of file to watch for',
                        type=str,
                        default='.txt')
    return parser


def signal_handler(sig_num, frame):
    logger.warning('Received ' + signal.Signals(sig_num).name)
    global exit_flag
    exit_flag = True


def main(args):
    parser = create_parser()
    ns = parser.parse_args(args)
    polling_interval = ns.interval
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)-12s '
               '%(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d &%H:%M:%S'
    )
    logger.setLevel(logging.DEBUG)
    start_time = time.time()
    logger.info(
        '\n'
        '-------------------------------------------------\n'
        f'   Running {__file__}\n'
        f'   PID is {os.getpid()}\n'
        f'   Started on {start_time:.1f}\n'
        '-------------------------------------------------\n'
    )
    logger.info(
        f'Watching directory:{ns.directory},'
        f'File Extension:{ns.extension},'
        f'Polling Interval:{ns.interval},'
        f', Magic Text: {ns.magic_word}'
    )
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGUSR1, signal_handler)

    while not exit_flag:
        try:
            watch_directory(ns)
        except OSError as e:
            if e.errno == errno.ENOENT:
                logger.error(f"{ns.directory} directory not found")
                time.sleep(2)
            else:
                logger.error(e)
        except Exception as e:
            logger.error(f"UNHANDLED EXCEPTION:{e}")
        time.sleep(polling_interval)

    full_time = time.time() - start_time
    logger.info(
        '\n'
        '-------------------------------------------------\n'
        f'   Stopped {__file__}\n'
        f'   Uptime was {full_time:.1f}\n'
        '-------------------------------------------------\n'
    )
    logging.shutdown()


if __name__ == '__main__':
    main(sys.argv[1:])
