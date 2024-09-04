// include libraries
#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // validate user's input
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int k = 0, n = strlen(argv[1]); k < n; k++)
    {
        if (isdigit(argv[1][k]) == 0)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // get key
    int key = atoi(argv[1]);

    // get plaintext
    string plain = get_string("plaintext: ");

    // initialize char array
    char cipher[strlen(plain)];

    for (int i = 0, n = strlen(plain); i < n; i++)
    {
        // encrypt char if alpha
        if (isalpha(plain[i]))
        {
            if (isupper(plain[i]))
            {
                cipher[i] = (((plain[i] - 65) + key) % 26) + 65;
            }
            else
            {
                cipher[i] = (((plain[i] - 97) + key) % 26) + 97;
            }
        }
        // leave it as it is if not
        else
        {
            cipher[i] = plain[i];
        }
    }

    printf("ciphertext: ");

    // print ciphertext
    for (int j = 0, n = strlen(plain); j < n; j++)
    {
        printf("%c", cipher[j]);
    }

    // new line
    printf("\n");
}