// include libraries
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    // get text from user
    string text = get_string("Text: ");

    // initialize variables
    int letters = 0;
    int words = 0;
    int sentences = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // count letters
        if (isalpha(text[i]))
        {
            letters += 1;
        }

        //count words
        if (text[i + 1] == ' ' || text[i + 1] == '\0')
        {
            words += 1;
        }

        // count sentences
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences += 1;
        }
    }

    /* L = average number of letters per 100 words in the text,
     * S = average number of sentences per 100 words in the text.*/
    float L = ((float) letters / words * 100);
    float S = ((float) sentences / words * 100);

    // calculate readability
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // print result
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

}