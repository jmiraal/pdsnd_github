### Date created
7/29/2019

### Project Title
# Explore US Bikeshare Data

### Description
This project was created as the final work for the Nanodegree Programming for Data Science.
The objective of this project is to use Python to explore data related to bike share systems for three major cities in the United States: Chicago, New York City, and Washington.

The program ask the user about what kind of statistics wants to see. It asks the user also about the filters to apply and the city they want to explore.

After some calculations the result can be displayed on the screen, viewed in a plot or saved to a file according the user election.

Description of statistics:

**Option 1: Global Statistics.** In this case the user will be able to extract the next data:
* Time Stats: Most common month, most common day of week and most common start hour.
* Station Stats: Most common used start and end station, trips with the same start and end stations and most frequent combination of start and end station.
* Trip duration Stats: total and mean travel time.    
* User Stats: Count of trips by user by types or by gender. Also the earliest, most recent and most common year of birth. The user will be able to filter by city, month, day, user type or/and user gender.

**Option 2: Sum, Count, Mean Stats** It will be displayed a table with the sum, count and mean of the trip duration for a city. The user will be asked to do the operations by the year of birth, the user type, the gender, the start station, the month, the day of the month, the day of the week or the hour of the day. The user will be able to see the result in a bar plot and save it in a file

**Option 3: Correlation Stats:** It will be calculated the correlation between the number of trips by user type or gender. The sum of the number of trips is calculated by day and the user will be able to choose between weekend days or work days. The user will see that the correlation is different on weekends and in working days for the two user types and for gender. The result can be showed in a scatter plot and save it in a file.

**Option 4: Percentage Stats:** It will be displayed the percentage of trips for different groups of users along the days of the week. The users will be divided between group of age, user type or gender. The groups of ages are: *(1) Younger than 25, (2) Between 25 and 35, (3) Between 35 and 45, (4) Between 45 and 55, (5) Older than 55.* The data will be displayed by day of week or divided in work-days and weekends. The result can be showed in a stacked bar plot and save it in a file.

### Files used
**Main program:**  
bikeshare.py 

**Cities bikeshare data, provided by the Udacity Nanodegree:** 
* chicago.csv
* new_york_city.csv
* washington.csv 

**Git administration:**
* .gitignore
* README.md 

### Credits
1. As part of the Nanodegree course, It has been used the documentation provided by Udacity:

[Udacity Nanodegree Programming for Data Science](https://eu.udacity.com/course/programming-for-data-science-nanodegree--nd104)

2. The rest of the information, solutions to problems, etc, was taken from the official pages:

[Panda API Reference](https://pandas.pydata.org/pandas-docs/stable/reference/index.html)

[Python Documentation](https://docs.python.org/3/contents.html)


3. And the in the blogspot:

[Stack Overflow](https://stackoverflow.com/questions)
