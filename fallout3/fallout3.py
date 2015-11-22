#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Fallout 3 Tools

import sys
import terminalhacker


def main():
    option_count = 2
    options = range(1, option_count + 1)
    try:
        while True:
            print """/------------------------\\
|    Fallout 3 Tools     |
|------------------------|
| 1. Terminal Hacker     |
| 2. Quit                |
\\------------------------/"""
            choice = raw_input("Choose a selection: ")
            while True:
                if choice.isdigit():
                    choice = int(choice)
                    if choice in options:
                        break
                print "Not a valid option."
                choice = raw_input("Choose a selection: ")
            if choice == 1:
                try:
                    terminalhacker.TextInterface().main()
                except KeyboardInterrupt:
                    print "\nReturning to main menu..."
            else:
                break
    except KeyboardInterrupt:
        print ""
    print "Exiting..."


if __name__ == "__main__":
    main()
    sys.exit(0)
