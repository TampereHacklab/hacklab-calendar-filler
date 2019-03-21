# Simple txt => csv generator for google calendar imports
# takes a txt file with just the names of the events and pushes out a csv format with events
# for each thursday from 7pm to 8pm
#
# written (in a hurry) by tsw

import sys
import argparse
import csv
import datetime as dt
import dateutil.relativedelta as rd
import dateutil.parser
from datestuff import DateRange
import io

# helper method for getting the next weeks thursday
def get_next_thursday(day):
   # delta to next weeks thursday
   delta = rd.relativedelta(days=1, weekday=rd.TH)
   # next week thursday
   day = day + delta
   return day

# validate day (for now checks for just the skipranges), TODO: add holidays
# returns true if day is valid and false if day is not valid
def valid_date(day, skipranges):
   valid = True
   # check the skipranges

   for sr in skipranges:
      if day in sr:
         valid = False

   # TODO: other checks

   return valid

# get the next valid thursday
def get_next_valid_thursday(day, skipranges):
   day = get_next_thursday(day)
   while not valid_date(day, skipranges):
      day = get_next_thursday(day)
   return day

# parse skiprange parameter to DateRange
def parse_skiprange(s):
   try:
      start, end = s.split('-')
   except ValueError:
      # handle one day as a range of one day
      start = s
      end = s

   try:
      startdate = dateutil.parser.parse(start)
      # important to add one day to end date, the check is still time specific and this way
      # we will check from 2019-01-01 00:00 to 2019-01-02 00:00
      enddate = dateutil.parser.parse(end) + dt.timedelta(days=1)
      return DateRange(start=startdate, stop=enddate, step=dt.timedelta(hours=1))
   except ValueError:
      msg = "Not a valid date range: '{0}'.".format(s)
      raise argparse.ArgumentTypeError(msg)

def get_parser():
   """
   Define the input arguments and returns the parser for them
   """
   parser = argparse.ArgumentParser(description='txt file to csv format for google calendar import')
   parser.add_argument("inputfile")
   parser.add_argument("-s", "--startdate", help="start from future date instead of next week thursday. format: YYYY/MM/DD (and whatever dateutil.parser.parse feeds on)", type=dateutil.parser.parse)
   parser.add_argument("--skiprange", help="skipranges for dates. something like 2019/06/01-2019/07/30 can be set multiple times. if only one day is given only that day is skipped", nargs='*', type=parse_skiprange)
   return parser

def get_csv(args):
   """
   do our thing, read the file and write out lines of csv
   """
   output = io.StringIO()
   # fields required by google https://support.google.com/calendar/answer/37118?hl=en#
   fieldnames = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'All Day Event', 'Description', 'Location', 'Private']
   writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator='\n')

   # start from startdate or today
   day = args["startdate"] if args["startdate"] else dt.date.today()

   writer.writeheader()
   with open(args["inputfile"]) as f:
      line = f.readline()
      while line:
         subject = line.strip()
         day = get_next_valid_thursday(day, args["skiprange"])
         fmt = "%m/%d/%Y"

         writer.writerow({
            'Subject': subject,
            'Start Date': day.strftime(fmt),
            'Start Time': '7:00 PM',
            'End Date': day.strftime(fmt),
            'End Time': '8:00 PM',
            'All Day Event': 'False',
            'Description': 'Workshop aiheella: {}'.format(subject),
            'Location': 'Tampere Hacklab, Ahlmanintie, Tampere',
            'Private': 'False',
         })

         # next line please
         line = f.readline()

   return output.getvalue()

def main(argv):
   parser = get_parser()
   args = parser.parse_args()
   print(get_csv(vars(args)), end='')

if __name__ == "__main__":
   main(sys.argv[1:])
