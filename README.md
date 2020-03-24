# Where To Restaurant?
What is the best place to build a new restaurant in New York City?

The final product can be found at wheretorestaurant.pythonanywhere.com

# Purpose
This tool helps restaurateurs decide in which zip code in New York City to open a new restaurant. The tool takes the user's cuisine type and target age group as inputs and produces a map with each zip code's color determined by its value on the "Opportunity Metric".

# Files list
Data - Copy.zip  :  Contains all of the raw data needed to create the tool

Gathering Data.ipynb  :  Combines the raw data and performs some basic data cleaning

Data Analysis-Cleaning.ipynb  :  Further prepares the data for use by the tool as well as some graphical analysis

Mapping.ipynb  :  Creates choropleth maps out of the final data

zip_recommender.py  :  Simple UI that takes user input and creates an appropriate map in a web browser

website folder  :  Contains the HTML/CSS code to create the website that houses the tool
