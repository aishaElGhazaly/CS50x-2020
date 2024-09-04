# Modules
import sys
from cs50 import SQL

# Check No. of command-line arguments
if (len(sys.argv) != 2):
    print("Proper Usage: pyhton roster.py house")
    sys.exit()

# House
dorm = sys.argv[1]

# Gain access to
db = SQL("sqlite:///students.db")

# Query the table for students in house
students = db.execute("SELECT * FROM students WHERE house = :house ORDER BY last, first", house=dorm)

# Print info of students
for student in students:
    if (student["middle"] == None):
        print(student["first"], student["last"] + ", born " + str(student["birth"]))
    else:
        print(student["first"], student["middle"], student["last"] + ", born " + str(student["birth"]))
