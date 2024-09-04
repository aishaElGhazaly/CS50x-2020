// include libraries
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// data type BYTE
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // open card
    FILE *card = fopen(argv[1], "r");

    // check fpointer is not NULL
    if (card == NULL)
    {
        return 1;
    }

    // variables
    int count = 0;
    BYTE buffer[512];
    char name[8];

    // open & name first img file
    sprintf(name, "%03i.jpg", count);
    FILE *img = fopen(name, "w");

    while (fread(buffer, 512, 1, card) == 1)
    {
        // start of a new jpg
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // if first jpg
            if (count == 0)
            {
                count++;

                fwrite(buffer, 512, 1, img);
            }
            // if not
            else
            {
                // close img file
                fclose(img);

                // open & name new img file
                sprintf(name, "%03i.jpg", count);
                img = fopen(name, "w");

                count++;

                fwrite(buffer, 512, 1, img);
            }
        }
        else
        {
            // if file is open
            if (ftell(img) > 0)
            {
                fwrite(buffer, 512, 1, img);
            }
        }
    }
    fclose(img);
    fclose(card);
}