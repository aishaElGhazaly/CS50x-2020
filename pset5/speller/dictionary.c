// Implements a dictionary's functionality
#include <stdio.h>

#include <stdlib.h>

#include <ctype.h>

#include <stdbool.h>

#include <string.h>

#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 100;

int count = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // hash index
    int x = hash(word);

    node *cursor = table[x];

    // compare strings
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }
    return false;
}

// Hashes word to a number
/* A case-insensitive implementation of the djb2 hash function.
 * Adapted by Neel Mehta from
 * http://stackoverflow.com/questions/2571683/djb2-hash-function.
 */
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;

    for (const char *ptr = word; *ptr != '\0'; ptr++)
    {
        hash = ((hash << 5) + hash) + tolower(*ptr);
    }

    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // open dictionary file
    FILE *dic = fopen(dictionary, "r");

    if (dic == NULL)
    {
        return false;
    }

    node *n = NULL;
    char term[LENGTH + 1];

    // read strings from file one at a time
    while (fscanf(dic, "%s", term) != EOF)
    {
        n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }

        // copy term into node
        strcpy(n->word, term);

        // hash index
        int x = hash(n->word);

        // insert term into linked list
        n->next = table[x];
        table[x] = n;

        count++;

    }
    // close dictionary file
    fclose(dic);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        node *temp = NULL;

        while (cursor != NULL)
        {
            temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
