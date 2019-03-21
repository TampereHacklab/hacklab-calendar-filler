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

# helper method for getting the next weeks thursday
def get_next_thursday(day):
   # delta to next weeks thursday
   delta = rd.relativedelta(days=1, weekday=rd.TH)
   # next week thursday
   day = day + delta
   return day


def main(argv):
   parser = argparse.ArgumentParser(description='txt file to csv format for google calendar import')
   parser.add_argument("inputfile")
   args = parser.parse_args()

   # fields required by google https://support.google.com/calendar/answer/37118?hl=en#
   fieldnames = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'All Day Event', 'Description', 'Location', 'Private']
   writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)

   writer.writeheader()

   # start from today
   day = dt.date.today()

   with open(args.inputfile) as f:
      line = f.readline()
      while line:
         subject = line.strip()
         day = get_next_thursday(day)
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


if __name__ == "__main__":
   main(sys.argv[1:])
