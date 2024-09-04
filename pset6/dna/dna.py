# modules
import sys
import csv

# ensure proper usage
if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    sys.exit()

database = sys.argv[1]
sequence = sys.argv[2]

run = 0
longrun = 0
STR_Count = []
Count = []

# open database
with open(database, newline='') as csvfile:
    db_reader = csv.reader(csvfile)
    # a list of STRs
    STR = list(next(db_reader))
    STR.pop(0)
    data = list(db_reader)

# open DNA sequence file
with open(sequence, newline='') as txtfile:
    seq_reader = txtfile.read()

# for every STR
for x in range(len(STR)):
    # iterate over the entire sequence
    for y in range(len(seq_reader)):
        # if STR matches sub-string
        if STR[x] == seq_reader[y:y + len(STR[x])]:
            run += 1
            # update index
            y = y + len(STR[x])

            # if STR no longer matches sub-string
            if not STR[x] == seq_reader[y:y + len(STR[x])]:
                if run > longrun:
                    longrun = run
                    run = 0
                else:
                    run = 0
    STR_Count.append(longrun)
    run = 0
    longrun = 0

for z in range(len(data)):
    # The STR count from the database
    count = data[z][1:]
    # Converted into int
    count = [int(v) for(v) in count]

    match = False

    if(STR_Count == count):
        match = True

        name = data[z][0]
        print(name)
        break

if(match == False):
    print("No match")