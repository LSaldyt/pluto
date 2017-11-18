# Pluto

Pluto is a dirt-simple python3 semantic database

Pluto is importable, but also has a command line interface:

To install, add this directory to your path or just copy database.py into your repository

### Help
``` bash
pluto init [optional filename]       # Create a database file in the current directory
pluto add  [optional filename] *args # Add keychain:value to the database file
pluto get  [optional filename] *args # Get keychains that reference the value or keychain *args
```

### Example usage (Python):
``` python3
db = Database()
db.add('a has sides three')
db.add('a has color green')
db.get('three')     # {('a', 'has', 'sides')}
db.get('green')     # {('a', 'has', 'color')}
db.get('has color') # {('a', 'has', 'color')}
db.get('has sides') # {('a', 'has', 'sides')} 
db.get('three')     # {('a', 'has', 'sides')}
db.get('a')         # {('a', 'has', 'color'), ('a', 'has', 'sides')}
```

### Example usage (CLI):
``` bash
$ pluto init
Initialized empty pluto database
$ pluto add a has sides three
Added a has sides three
$ pluto add a has color green
Added a has color green
$ pluto get three
{('a', 'has', 'sides')}
$ pluto get green
{('a', 'has', 'color')}
$ pluto get has color
{('a', 'has', 'color')}
$ pluto get has sides
{('a', 'has', 'sides')}
$ pluto get a
{('a', 'has', 'sides'), ('a', 'has', 'color')}
```
