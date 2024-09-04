// include libraries
#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // recieve and store user's input then print a greeting
    string name = get_string("What's your name? ");
    printf("hello, %s\n", name);
}
