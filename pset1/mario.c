// include libraries
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // recieve user's input
    printf("Height should be between 1 and 8.\n");
    int height = get_int("Insert Height: ");

    // make sure that input is bet. 1 & 8
    while (height <= 0 || height > 8)
    {
        height = get_int("Height: ");
    }


    for (int i = height; i > 0; i--)
    {
        // print spaces
        for (int j = i - 1; j > 0; j--)
        {
            printf(" ");
        }

        // print hashes
        for (int k = height - (i - 1); k > 0; k--)
        {
            printf("#");
        }

        // new line
        printf("\n");
    }
}
