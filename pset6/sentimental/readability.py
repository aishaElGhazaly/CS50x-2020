from cs50 import get_string

# text from user
text = get_string("text: ")

# No. of letters
letters = 0
for l in text:
    if l.isalpha():
        letters += 1

# No. of words
words = text.count(' ') + 1

# No. of sentences
sentences = text.count('.') + text.count('!') + text.count('?')

# L = average number of letters per 100 words in the text,
# S = average number of sentences per 100 words in the text.
L = float(letters / words * 100)
S = float(sentences / words * 100)

# Calculate readability
index = round(0.0588 * L - 0.296 * S - 15.8)

# Print result
if index >= 16:
    print("Grade 16+")

elif index < 1:
    print("Before Grade 1")

else:
    print("Grade", index)