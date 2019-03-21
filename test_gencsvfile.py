import unittest
from datetime import date, timedelta
from datestuff import DateRange
from argparse import ArgumentTypeError

from gencsvfile import get_parser
from gencsvfile import get_next_thursday
from gencsvfile import get_next_valid_thursday
from gencsvfile import valid_date
from gencsvfile import parse_skiprange
from gencsvfile import get_csv


class CommandLineTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = get_parser()
        cls.parser = parser


class TestMethods(CommandLineTestCase):
    def test_with_empty_args(self):
        """
        No args, should fail as input file is mandatory
        """
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

    def test_get_next_thursday(self):
        # next thursday of 2019
        expected = date(2019, 1, 10)

        # first day of the year is too soon for the second thursday
        self.assertNotEqual(expected, get_next_thursday( date(2019, 1, 1) ))
        # previous thursday, should get next weeks
        self.assertEqual(expected, get_next_thursday( date(2019, 1, 3) ))
        # day before, shoudl get the same
        self.assertEqual(expected, get_next_thursday( date(2019, 1, 9) ))
        # same, should get the next week
        self.assertNotEqual(expected, get_next_thursday( date(2019, 1, 10) ))
        # after, should get the next week
        self.assertNotEqual(expected, get_next_thursday( date(2019, 1, 11) ))

    def test_valid_date(self):
        # january and february as two different ranges (plus one for the end dates)
        # and one single day (midsummer)
        skipranges = [
            DateRange(start=date(2019, 1, 1), stop=date(2019, 2, 1), step=timedelta(days=1)),
            DateRange(start=date(2019, 2, 1), stop=date(2019, 3, 1), step=timedelta(days=1)),
            DateRange(start=date(2019, 6, 21), stop=date(2019, 6, 22), step=timedelta(days=1))
        ]
        # before our ranges
        self.assertTrue(valid_date(date(2018,12,31), skipranges))
        # just on the range start, middle and ends
        self.assertFalse(valid_date(date(2019,1,1), skipranges))
        self.assertFalse(valid_date(date(2019,1,12), skipranges))
        self.assertFalse(valid_date(date(2019,1,31), skipranges))

        # second range
        self.assertFalse(valid_date(date(2019,2,1), skipranges))
        self.assertFalse(valid_date(date(2019,2,12), skipranges))
        self.assertFalse(valid_date(date(2019,2,28), skipranges))

        # just after the ranges
        self.assertTrue(valid_date(date(2019,3,1), skipranges))

        # random day not in ranges
        self.assertTrue(valid_date(date(2019,5,6), skipranges))

        # single day, just before, at the day and after
        self.assertTrue(valid_date(date(2019,6,20), skipranges))
        self.assertFalse(valid_date(date(2019,6,21), skipranges))
        self.assertTrue(valid_date(date(2019,6,22), skipranges))

    def test_get_next_valid_thursday(self):
        skipranges = [
            DateRange(start=date(2019, 1, 1), stop=date(2019, 2, 1), step=timedelta(days=1)),
            DateRange(start=date(2019, 2, 1), stop=date(2019, 3, 1), step=timedelta(days=1)),
            DateRange(start=date(2019, 6, 21), stop=date(2019, 6, 22), step=timedelta(days=1))
        ]
        expected = date(2019, 3, 7)
        # start from 1.1 skipranges should push this to first thursday of march
        self.assertEqual(expected, get_next_valid_thursday( date(2019, 1, 1), skipranges))

    def test_parse_skiprange(self):
        # not parseable date
        with self.assertRaises(ArgumentTypeError):
            parse_skiprange("foobar")

        self.assertIsInstance(parse_skiprange('2019/01/01-2019/02/02'), DateRange)
        self.assertIsInstance(parse_skiprange('2019/01/01'), DateRange)


class TestGeneration(CommandLineTestCase):
    def test_get_csv(self):
        args = {
            "inputfile": "workshoplist.txt",
            "startdate": date(2019, 1, 1),
            "skiprange": []
        }

        # get our csv
        csv = get_csv(args)

        header = csv.splitlines()[0]
        self.assertEqual("Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private", header)

        # get our source data
        with open(args["inputfile"]) as f:
            sourcelines = f.readlines()

        # next thursday for the first line
        nextthursday = get_next_valid_thursday(args["startdate"], args["skiprange"])

        for l in csv.split('\n'):
            # empty string
            if not l:
                continue

            # skip the first one as it is the header
            if(header):
                header = None
                continue

            # next line from our source
            expected = sourcelines.pop(0).strip()

            # check that it is found on our generated csv line in about the correct place. should be at 0 as it is the subject
            self.assertEqual(l.find(expected), 0)
            # check that the next thursday date is somewhere on the line
            self.assertNotEqual( l.find(nextthursday.strftime("%m/%d/%Y")), -1)
            # and get the next thursday for the next line
            nextthursday = get_next_valid_thursday(nextthursday, args["skiprange"])

        # check that we used all of our sourcelines for checking
        self.assertEqual(len(sourcelines), 0)

if __name__ == "__main__":
    unittest.main(buffer=True)
