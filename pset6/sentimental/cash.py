from cs50 import get_float

# define coins' values
quarter = 25
dime = 10
nickel = 5
cent = 1
coins = 0

# Non-negative input from user
change_owed = get_float("Change owed: ")

while change_owed < 0:
    change_owed = get_float("Change owed: ")

# dollars to cents..rounded to the nearest penny
change = round(change_owed * 100)

while change > 0:
    # Use quarter
    if change >= quarter:
        change -= quarter
        coins += 1
    
    # Use dime
    elif change >= dime:
        change -= dime
        coins += 1
        
    # Use nickel
    elif change >= nickel:
        change -= nickel
        coins += 1
    
    # Use penny
    else:
        change -= cent
        coins += 1

print(coins)