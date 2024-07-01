# Introduction

This project was under development during second semester of Master's studies in Embedded Systems field on Warsaw Universitiy of Technology, Poland. The main goal was to write a piece of software capable of identifying coins denominals and count them respectively for a certain sum.

## Important:
This project was heavily inspired by the video given below and its creator, [Murtaza Hassan](https://github.com/murtazahassan):\
[Money/Coin Counter using Computer Vision](https://www.youtube.com/watch?v=-iN7NDbDz3Q)


# About
This project, as mentioned in the Introdcution focuses on recognition and identification of coins, specifically PLN (Polish Zloty New) denominal. All the code written was related to a total of three libraries:
- OpenCv
- numpy
- cvzone (which is a wrapper library for OpenCV)

## Requirements

Althoguh the GitHub repository contains folder with coins photos, this software was not used on them. Main focus was placed on using an image got from th Internet camera. Moreover, coin recognition based on sharp, high quality images does not work.

To make the software do its job, specific threshold values were defined, different for each coin. This requires camera to be mounted on a **constant high** which in this case was **16 centimeters**. Although there is a simple trackbar menu made specifically for setting coins sizes it is recommended to keep the distance between camera and coins at around 10 - 18 centimeters.

There is a total of two "debug" functions ```AdjustCannyThresholdsWindow()``` and ```AdjustCoinSizesWindow()``` which are responsible for displaying both trackbar windows and handling all the possible adjustments. To make them appear at the program's start-up ```is_debug``` flag has to be set (```is_debug = 1```).

## Sugestions
High quality camera is not necessary as the identification is based solely on coin sizes. To be honest, it's even not recomended because of Canny filter "catchig" all the symbols, eg. eagle, text.

Make sure that the background is not reflective as sometimes the additional bright reflections cause the coins being not visible for the software (Canny filter to be precise). Personally, I recommend using black, non-reflective background.
