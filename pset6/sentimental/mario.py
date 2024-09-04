from cs50 import get_int

# Recieve user's input 
print("Height should be between 1 and 8.")
height = get_int("Insert Height: ")

# Check that input is bet. 1 & 8
while height <= 0 or height > 8:
    height = get_int("Height: ")

for i in range(height, 0, -1):
    # Print spaces
    x = i - 1
    for j in range(x, 0, -1):
        print(" ", end='')

    # Print hashes
    y = height - x
    for k in range(y, 0, -1):
        print("#", end='')
    
    # new line
    print()