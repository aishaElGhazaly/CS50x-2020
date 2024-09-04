// include libraries
#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int avg = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // calculate the average
            avg = round((float)(image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3);

            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed = 0;
    int sepiaGreen = 0;
    int sepiaBlue = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // calculate the sepia value
            sepiaRed = round((float)0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue);
            sepiaGreen = round((float)0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue);
            sepiaBlue = round((float)0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue);

            // sepia Red
            if (sepiaRed > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = sepiaRed;
            }

            // sepia Green
            if (sepiaGreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = sepiaGreen;
            }

            // sepia Blue
            if (sepiaBlue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = sepiaBlue;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            // current pixel's counterpart
            int index = (width - 1) - j;

            // swap the two pixels
            RGBTRIPLE temp = image[i][j];

            image[i][j] = image[i][index];

            image[i][index] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int avgRed = 0;
    int avgGreen = 0;
    int avgBlue = 0;

    // place holder
    RGBTRIPLE pixels[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // first row
            if (i == 0)
            {
                // first column
                if (j == 0)
                {
                    // upper left corner pixel
                    // avg. of surrounding 3 pixels (incl. the current pixel)
                    avgRed = round(((float)image[i][j].rgbtRed +
                                    image[i][j + 1].rgbtRed +
                                    image[i + 1][j].rgbtRed +
                                    image[i + 1][j + 1].rgbtRed) / 4);

                    avgGreen = round(((float)image[i][j].rgbtGreen +
                                      image[i][j + 1].rgbtGreen +
                                      image[i + 1][j].rgbtGreen +
                                      image[i + 1][j + 1].rgbtGreen) / 4);

                    avgBlue = round(((float)image[i][j].rgbtBlue +
                                     image[i][j + 1].rgbtBlue +
                                     image[i + 1][j].rgbtBlue +
                                     image[i + 1][j + 1].rgbtBlue) / 4);

                    pixels[i][j].rgbtRed = avgRed;
                    pixels[i][j].rgbtGreen = avgGreen;
                    pixels[i][j].rgbtBlue = avgBlue;
                }
                // last column
                else if (j == width - 1)
                {
                    // upper right corner pixel
                    // avg. of surrounding 3 pixels (incl. the current pixel)
                    avgRed = round(((float)image[i][j].rgbtRed +
                                    image[i][j - 1].rgbtRed +
                                    image[i + 1][j].rgbtRed +
                                    image[i + 1][j - 1].rgbtRed) / 4);

                    avgGreen = round(((float)image[i][j].rgbtGreen +
                                      image[i][j - 1].rgbtGreen +
                                      image[i + 1][j].rgbtGreen +
                                      image[i + 1][j - 1].rgbtGreen) / 4);

                    avgBlue = round(((float)image[i][j].rgbtBlue +
                                     image[i][j - 1].rgbtBlue +
                                     image[i + 1][j].rgbtBlue +
                                     image[i + 1][j - 1].rgbtBlue) / 4);

                    pixels[i][j].rgbtRed = avgRed;
                    pixels[i][j].rgbtGreen = avgGreen;
                    pixels[i][j].rgbtBlue = avgBlue;
                }
                // the in-between
                else
                {
                    // avg. of surrounding 5 pixels (incl. the current pixel)
                    avgRed = round(((float)image[i][j].rgbtRed +
                                    image[i][j + 1].rgbtRed +
                                    image[i][j - 1].rgbtRed +
                                    image[i + 1][j].rgbtRed +
                                    image[i + 1][j + 1].rgbtRed +
                                    image[i + 1][j - 1].rgbtRed) / 6);

                    avgGreen = round(((float)image[i][j].rgbtGreen +
                                      image[i][j + 1].rgbtGreen +
                                      image[i][j - 1].rgbtGreen +
                                      image[i + 1][j].rgbtGreen +
                                      image[i + 1][j + 1].rgbtGreen +
                                      image[i + 1][j - 1].rgbtGreen) / 6);

                    avgBlue = round(((float)image[i][j].rgbtBlue +
                                     image[i][j + 1].rgbtBlue +
                                     image[i][j - 1].rgbtBlue +
                                     image[i + 1][j].rgbtBlue +
                                     image[i + 1][j + 1].rgbtBlue +
                                     image[i + 1][j - 1].rgbtBlue) / 6);

                    pixels[i][j].rgbtRed = avgRed;
                    pixels[i][j].rgbtGreen = avgGreen;
                    pixels[i][j].rgbtBlue = avgBlue;
                }
            }
            // last row
            else if (i == height - 1)
            {
                // first column
                if (j == 0)
                {
                    // lower left corner pixel
                    // avg. of surrounding 3 pixels (incl. the current pixel)
                    avgRed = round(((float)image[i][j].rgbtRed +
                                    image[i - 1][j].rgbtRed +
                                    image[i - 1][j + 1].rgbtRed +
                                    image[i][j + 1].rgbtRed) / 4);

                    avgGreen = round(((float)image[i][j].rgbtGreen +
                                      image[i - 1][j].rgbtGreen +
                                      image[i - 1][j + 1].rgbtGreen +
                                      image[i][j + 1].rgbtGreen) / 4);

                    avgBlue = round(((float)image[i][j].rgbtBlue +
                                     image[i - 1][j].rgbtBlue +
                                     image[i - 1][j + 1].rgbtBlue +
                                     image[i][j + 1].rgbtBlue) / 4);

                    pixels[i][j].rgbtRed = avgRed;
                    pixels[i][j].rgbtGreen = avgGreen;
                    pixels[i][j].rgbtBlue = avgBlue;
                }
                // last column
                else if (j == width - 1)
                {
                    // lower right corner pixel
                    // avg. of surrounding 3 pixels (incl. the current pixel)
                    avgRed = round(((float)image[i][j].rgbtRed +
                                    image[i - 1][j].rgbtRed +
                                    image[i - 1][j - 1].rgbtRed +
                                    image[i][j - 1].rgbtRed) / 4);

                    avgGreen = round(((float)image[i][j].rgbtGreen +
                                      image[i - 1][j].rgbtGreen +
                                      image[i - 1][j - 1].rgbtGreen +
                                      image[i][j - 1].rgbtGreen) / 4);

                    avgBlue = round(((float)image[i][j].rgbtBlue +
                                     image[i - 1][j].rgbtBlue +
                                     image[i - 1][j - 1].rgbtBlue +
                                     image[i][j - 1].rgbtBlue) / 4);

                    pixels[i][j].rgbtRed = avgRed;
                    pixels[i][j].rgbtGreen = avgGreen;
                    pixels[i][j].rgbtBlue = avgBlue;
                }
                // the in-between
                else
                {
                    // avg. of surrounding 5 pixels (incl. the current pixel)
                    avgRed = round(((float)image[i][j].rgbtRed +
                                    image[i][j + 1].rgbtRed +
                                    image[i][j - 1].rgbtRed +
                                    image[i - 1][j].rgbtRed +
                                    image[i - 1][j + 1].rgbtRed +
                                    image[i - 1][j - 1].rgbtRed) / 6);

                    avgGreen = round(((float)image[i][j].rgbtGreen +
                                      image[i][j + 1].rgbtGreen +
                                      image[i][j - 1].rgbtGreen +
                                      image[i - 1][j].rgbtGreen +
                                      image[i - 1][j + 1].rgbtGreen +
                                      image[i - 1][j - 1].rgbtGreen) / 6);

                    avgBlue = round(((float)image[i][j].rgbtBlue +
                                     image[i][j + 1].rgbtBlue +
                                     image[i][j - 1].rgbtBlue +
                                     image[i - 1][j].rgbtBlue +
                                     image[i - 1][j + 1].rgbtBlue +
                                     image[i - 1][j - 1].rgbtBlue) / 6);

                    pixels[i][j].rgbtRed = avgRed;
                    pixels[i][j].rgbtGreen = avgGreen;
                    pixels[i][j].rgbtBlue = avgBlue;
                }
            }
            // the in-between
            else
            {
                // first coulmn
                if (j == 0)
                {
                    // edge pixel on the left
                    // avg. of surrounding 5 pixels (incl. the current pixel)
                    avgRed = round(((float)image[i][j].rgbtRed +
                                    image[i - 1][j].rgbtRed +
                                    image[i + 1][j].rgbtRed +
                                    image[i - 1][j + 1].rgbtRed +
                                    image[i + 1][j + 1].rgbtRed +
                                    image[i][j + 1].rgbtRed) / 6);

                    avgGreen = round(((float)image[i][j].rgbtGreen +
                                      image[i - 1][j].rgbtGreen +
                                      image[i + 1][j].rgbtGreen +
                                      image[i - 1][j + 1].rgbtGreen +
                                      image[i + 1][j + 1].rgbtGreen +
                                      image[i][j + 1].rgbtGreen) / 6);

                    avgBlue = round(((float)image[i][j].rgbtBlue +
                                     image[i - 1][j].rgbtBlue +
                                     image[i + 1][j].rgbtBlue +
                                     image[i - 1][j + 1].rgbtBlue +
                                     image[i + 1][j + 1].rgbtBlue +
                                     image[i][j + 1].rgbtBlue) / 6);

                    pixels[i][j].rgbtRed = avgRed;
                    pixels[i][j].rgbtGreen = avgGreen;
                    pixels[i][j].rgbtBlue = avgBlue;
                }
                else if (j == width - 1)
                {
                    // edge pixels on the right
                    // avg. of surrounding 5 pixels (incl. the current pixel)
                    avgRed = round(((float)image[i][j].rgbtRed +
                                    image[i - 1][j].rgbtRed +
                                    image[i + 1][j].rgbtRed +
                                    image[i - 1][j - 1].rgbtRed +
                                    image[i + 1][j - 1].rgbtRed +
                                    image[i][j - 1].rgbtRed) / 6);

                    avgGreen = round(((float)image[i][j].rgbtGreen +
                                      image[i - 1][j].rgbtGreen +
                                      image[i + 1][j].rgbtGreen +
                                      image[i - 1][j - 1].rgbtGreen +
                                      image[i + 1][j - 1].rgbtGreen +
                                      image[i][j - 1].rgbtGreen) / 6);

                    avgBlue = round(((float)image[i][j].rgbtBlue +
                                     image[i - 1][j].rgbtBlue +
                                     image[i + 1][j].rgbtBlue +
                                     image[i - 1][j - 1].rgbtBlue +
                                     image[i + 1][j - 1].rgbtBlue +
                                     image[i][j - 1].rgbtBlue) / 6);

                    pixels[i][j].rgbtRed = avgRed;
                    pixels[i][j].rgbtGreen = avgGreen;
                    pixels[i][j].rgbtBlue = avgBlue;
                }
                else
                {
                    // middle pixels
                    // avg. of surrounding 8 pixels (incl. the current pixel)
                    avgRed = round(((float)image[i][j].rgbtRed +
                                    image[i - 1][j].rgbtRed +
                                    image[i + 1][j].rgbtRed +
                                    image[i - 1][j - 1].rgbtRed +
                                    image[i + 1][j - 1].rgbtRed +
                                    image[i][j - 1].rgbtRed +
                                    image[i - 1][j + 1].rgbtRed +
                                    image[i + 1][j + 1].rgbtRed +
                                    image[i][j + 1].rgbtRed) / 9);

                    avgGreen = round(((float)image[i][j].rgbtGreen +
                                      image[i - 1][j].rgbtGreen +
                                      image[i + 1][j].rgbtGreen +
                                      image[i - 1][j - 1].rgbtGreen +
                                      image[i + 1][j - 1].rgbtGreen +
                                      image[i][j - 1].rgbtGreen +
                                      image[i - 1][j + 1].rgbtGreen +
                                      image[i + 1][j + 1].rgbtGreen +
                                      image[i][j + 1].rgbtGreen) / 9);

                    avgBlue = round(((float)image[i][j].rgbtBlue +
                                     image[i - 1][j].rgbtBlue +
                                     image[i + 1][j].rgbtBlue +
                                     image[i - 1][j - 1].rgbtBlue +
                                     image[i + 1][j - 1].rgbtBlue +
                                     image[i][j - 1].rgbtBlue +
                                     image[i - 1][j + 1].rgbtBlue +
                                     image[i + 1][j + 1].rgbtBlue +
                                     image[i][j + 1].rgbtBlue) / 9);

                    pixels[i][j].rgbtRed = avgRed;
                    pixels[i][j].rgbtGreen = avgGreen;
                    pixels[i][j].rgbtBlue = avgBlue;
                }
            }
        }
    }

    // change the original picture
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = pixels[i][j];
        }
    }
    return;
}