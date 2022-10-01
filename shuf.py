#!/usr/bin/python

"""
Output lines selected randomly from a file

Copyright 2005, 2007 Paul Eggert.
Copyright 2010 Darrell Benjamin Carbajal.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Please see <http://www.gnu.org/licenses/> for a copy of the license.

$Id: randline.py,v 1.4 2010/04/05 20:04:43 eggert Exp $
"""

import random, sys
from argsparse import ArgumentParser

class randline:
    def __init__(self, filename):
        f = open(filename, 'r')
        self.lines = f.readlines()
        f.close()

    def chooseline(self):
        return random.choice(self.lines)

def main():
    version_msg = "%prog 2.0"
    usage_msg = """%prog [OPTION]... FILE

Output randomly selected lines from FILE."""

    parser = ArgumentParser(version=version_msg,
                          usage=usage_msg)
    parser.add_argument("-n", "--head-count=COUNT",
                        dest="head-count", nargs="1", type=int,
                      help="output at most COUNT lines")
    parser.add_argument("-r", "--repeat:", dest="repeat", help="output lines can be repeated")
    parser.add_argument("-e", "--echo", nargs="+", dest="echo", help="treat each ARG as an input line")
    parser.add_argument("-i", "--input-range=LO-HI", nargs='1', dest="rangeArg", help="treat each number LO through HI as an input line")
    parser.add_argument("--help", dest="helpArg", help="display this help and exit")

    class C:
        pass
    c=C()
    options, args = parser.parse_args(sys.argv[1:], namespace=c)

    try:
        numlines = int(options.numlines)
    except:
        parser.error("invalid NUMLINES: {0}".
                     format(options.numlines))
    if numlines < 0:
        parser.error("negative count: {0}".
                     format(numlines))
    if len(args) != 1:
        parser.error("wrong number of operands")

    try:
        if c.echo != None:
            input_file = args[1]
            generator = randline(input_file)
            for index in range(numlines):
                sys.stdout.write(generator.chooseline())
        elif c.rangeArg != None:
            rangeNums = c.rangeArg
            input_file = args[2]
            match rangeNums.split("-"):
                case []:
                    print("Please input two numbers.")
                case [userInput]:
                    print("Please input two numbers.")
                case [lowNum, highNum]:
                    n = int(higherNum) - int(lowerNum)
                    for eachNum in n:
                        sys.stdout.write(random.randint(int(lowerNum), int(higherNum)))
                case [lowNum, highNum, *other]:
                    print("Please input two numbers.")
            
        elif c.repeat != None and c.head_count != None:
            input_file = args[3]
            generator = randline(input_file)
            for eachNum in int(c.head_count):
                sys.stdout.write(generator.chooseline())
        elif(c.repeat != None and args.head-count == None:
            while True:
             sys.stdout.write(generator.chooseline())
        elif(c.head_count != None):
             for(x in range(c.head_count)):
              sys.stdout.write(generator.chooseline())
        elif c.helpArg != None:
            sys.stdout.write("Usage: shuf [OPTION]... [FILE]\n
  or:  shuf -e [OPTION]... [ARG]...\n
  or:  shuf -i LO-HI [OPTION]...\n
Write a random permutation of the input lines to standard output.\n
\n
With no FILE, or when FILE is -, read standard input.\n
\n
Mandatory arguments to long options are mandatory for short options too.\n
  -e, --echo                treat each ARG as an input line\n
  -i, --input-range=LO-HI   treat each number LO through HI as an input line\n
  -n, --head-count=COUNT    output at most COUNT lines\n
  -r, --repeat              output lines can be repeated\n
  --help     display this help and exit")
            
    except IOError as (errno, strerror):
        parser.error("I/O error({0}): {1}".
                     format(errno, strerror))

if __name__ == "__main__":
    main()
