# Whose the Artist?
Capstone 1 project for Galvanize Data Science Immersive, Week 4

*By Abel Desta*

# Introduction
## Data
I found a dataset on kaggle that contains most of the artwork from the 50 influential artist ranging from everytime period. The data came with a csv file that contains information about each artist, such as a small bio, genre and nationality of the artist. The artwork was scraped from [artchallenge](http://artchallenge.ru/?lang=en) website. 

There is around 8500 images scaped. All the images in the files are RGB images in JPG format. RGB images are represented as 3D matrices. The rows and columns give us the number of pixels in eac dimension. The more pixels, the larger the matrix. The depth gives a 2D matrix with the pixel intensity of each color (Red, Green, and Blue) at each pixel. Values range from 0 to 250.

The images came resized but still high resolution. Also, most images came in a various different pixel size and shape.

## Goal
My goal for this capstone is to build a convolution neural network to be able to take an image of artists' artwork and classify the piece to the correct artists. To start, I will try to correctly classify the three artists out the 50 in the dataset.

## EDA
There are 31 different genres in the dataset. Some artists belonged in more than one genre.

|Genres |  Number of Artists|Genres |  Number of Artists|
|--------|----------------|------------|--------|      
|Northern Renaissance|  4| Post-Impressionism   |  4|
|Impressionism        |    4| Baroque    |   4|
 Romanticism|     3| High Renaissance     |                      3|
 Surrealism|      2|Primitivism |    2|
|Impressionism,Post-Impressionism|           2| Early Renaissance |  1|
|Symbolism,Art Nouveau |                     1| Symbolism     |  1|
|Realism                 |       1| Social Realism,Muralism  |   1|
|Pop Art      |                 1| Neoplasticism            |    1|
|Expressionism,Abstractionism,Surrealism|    1| Symbolism,Expressionism   |    1|
|High Renaissance,Mannerism |   1| Surrealism,Impressionism    |               1|
|Cubism        |  1|Suprematism                   |             1|
|Realism,Impressionism        |              1| Expressionism   |        1|
|Symbolism,Post-Impressionism |             1 | Abstract Expressionism |            1|
|Mannerism                    |           1| Primitivism,Surrealism       |        1|
|Expressionism,Abstractionism |              1| Byzantine Art                |      1|
|Proto Renaissance    |                  1|

**Table 1. The number of artist in each genre.**

The number of paintings from each artist varied greatly. Which might come from artist productivity or from difficult finding an artists artwork when the data was collected. Since my goal is to classify artist based on images, the class imbalances will be a problem that needs to be handled. 




<p align="center">
    <img src="img/paintings.png" />
<p/>

**Figure 1. This bar chart shows severe discrepancy in images for artists.**



# Building the Artist CNN

## Pipeline 

The problem with the images I got from kaggle was that all the images varied in pixel size and shape. So I made a pipeline that would be able to take in a list of an artist's work and resize the images to 100 x 100 x 3. 

## CNN 

# Results 

## Future Work