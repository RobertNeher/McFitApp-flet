# McFit-App-flet
Trainings companion for McFit Training

## Motivation
Using Flet, instead of pure Flutter/Dart.

# Prerequisites
Python Flet: ``pip install flet`` (https://pub.dev/documentation/flet/latest/index.html)<br/>
Datetime: ``pip install datetime``

# Folder structure
## assets/McFit.db
Local SQLite3 database for persistency.<br/>
Initial fill by importing "assets/datasets" JSON content through ``python.exe ./src/persistence.py``<br/>
WATCH OUT: This is the **only** case that the Persistence class ist initiated with values from JSON datasets. In all other cases the persistence object does what it is named for.
## assets/fonts
There are three font files located:
| Font | Purpose |
|------|---------|
| Raleway | Default font, currently in use via Theming |
| OpenSans | Backup font, as alternative to "Raleway", not in use yet. |
| McFitApp | font being used make user interface nicer. It has been created to provide custom icons into play, like a "Dumpbell".

## assets/datasets
It is similar to a R/O database maintained by "model classes" (see below).
| File | Purpose |
|------|---------|
| Customer.json | List of McFit customers (only one at the moment ;-) |
| Preferences.json | Temporarily used to start from. Dedicated to death |
| Machines.json | All machines available in McFit studios with all their descriptive data, and parameters for setup of the machine before exercise starts. |
| Plans.json | Defines the machines assigned to customer including the settings for each machine's parameters and datails about movement defined by McFit instructor.<br/>

# Development plan
Basing upon release v0.1


