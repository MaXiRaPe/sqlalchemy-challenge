# sqlalchemy-challenge
UNCC Data Science Bootcamp - Module 10 Advanced SQL

The purpose of this challenge is to use SQLAlchemy to run queries on a data set in two different applications:

# Part 1 - Analyze and Explopre Climate Data using Python and Matplotlib
An SQLite file is used as source to query and create the API (Resources folder).
The automap_base() function is used to reflect the SQLite database into classes and the references are saved 
as "station" and "measurement" in the Resources folder.
The resulting script file "climate_starter.ipynb" can be found in the "SurfsUp" folder.
The data includes precipitation and temperature records for a range of dates from 9 different stations.
The data was queried to:
1- Complete an analysis on the precipitation records for the last 12 months of data and
summarized in a bar plot.
2- Identify the most active station based on the highest count of records and describe the subset by the min, 
max and avg temperatures observed.
3- Complete an analysis on the Temperature observations for the last 12 months of data and
create a histogram plot.


# Part 2 - Design a Climate App using Flask
An SQLite file is used as source to query and create the API (Resources folder).
The script file "app.py" can be found in the "SurfsUp" folder.
The API consists of 6 different pages:
1- Index/Home
2- Precipitation data for the last 12 months of data.
3- A list of Stations from which the data is collected.
4- A list of the Temperature observations for the most active station for the last 12 months of data.
5- Return of Min, Max and Avg Temperatures for all dates greater than or equal to a given date.
6- Return of Min, Max and Avg Temperatures for all dates between two given dates.
