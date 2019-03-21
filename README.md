# Hacklab Calendar workshop filler

Takes a list of event names and distributes them to thursdays starting from next week. All the events will be marked to start 19:00 and end 20:00.

## Usage

```
pipenv shell
python gencsvfile.py workshoplist.txt | tee import_to_google_calendar.csv
```

Where workshoplist.txt contains something like this

```
$ cat workshoplist.txt
GitHub
Puutyöt
Fusion 360
```

You can then modify the csv file (for example write some nice descriptions for the events) and then import to google calendar https://support.google.com/calendar/answer/37118?hl=en

Optionally you can add -s parameter for setting the first day of calculation (defaults to today)

You can also define skipranges to keep for example christmas and summer out from valid days. Skiprange can have multiple ranges and also handles one day ranges, for example:

```
--skiprange 2019/04/11 2019/06/01-2019/07/31
```

# Somewhat univeral command example

Check the start day (-s parameter) from the current calendar (the last workshop defined currently). And add skiprange for summer and christmas / new year.

```
python gencsvfile.py workshoplist.txt -s 2019/04/05 --skiprange `date +%Y`/06/01-`date +%Y`/07/31 `date +%Y`/12/23-`date +%Y -d 'next year'`/01/6| tee import_to_google_calendar.csv
```

# TODO:

* use the calendar api
* check that the day is "empty" and skip if it is
* check that the day is not a holiday and skip if it is