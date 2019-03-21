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