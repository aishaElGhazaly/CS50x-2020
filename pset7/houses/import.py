# Modules
import sys
import csv
from cs50 import SQL

# Check No. of command-line arguments
if (len(sys.argv) != 2):
    print("Proper Usage: pyhton import.py filename.csv")
    sys.exit()

# Gain access to SQL database
db = SQL("sqlite:///students.db")

# CSV file
characters = sys.argv[1]

# Open CSV file & read it
with open(characters, newline='') as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)

# Import data from CSV file and fill SQL database
for character in range(1, len(data)):
    name = data[character][0].split()
    house = data[character][1]
    year = int(data[character][2])

    if (len(name) == 2):
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
                   name[0], None, name[1], house, year)

    if (len(name) == 3):
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
                   name[0], name[1], name[2], house, year)