// include libraries
#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    // define coins' values
    int quarter = 25;
    int dime = 10;
    int nickel = 5;
    int penny = 1;
    int coins = 0;

    //recieve user's input and check that it's not negative
    float change_owed = get_float("Change owed: ");

    while (change_owed < 0)
    {
        change_owed = get_float("Change owed: ");
    }

    // turn dollars into cents and round to the nearest penny
    int change = round(change_owed * 100);

    while (change >  0)
    {
        // use a quarter
        if (change >= quarter)
        {
            change -= quarter;
            coins++;
        }
        // use a dime
        else if (change >= dime)
        {
            change -= dime;
            coins++;
        }
        // use a nickel
        else if (change >= nickel)
        {
            change -= nickel;
            coins++;
        }
        // use a penny
        else
        {
            change -= penny;
            coins++;
        }
    }

    // print number of coins
    printf("%i\n", coins);
}
