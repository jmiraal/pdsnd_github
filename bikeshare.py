import time
import pandas as pd
import numpy as np
import seaborn as sns
import sys
import multiprocessing as mp
import matplotlib.pyplot as plt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = CITY_DATA.keys()
city_number = ('1', '2', '3')

#options for the initial query.
stat_options = ('none', 'global', 'trip table', 'correlation', 'percentage')
stat_option_number = ('0', '1', '2', '3', '4')

#lists of months, days, type of days...
months = ('all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')
week_days = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
work_days = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday')
weekend_days = ('saturday', 'sunday')
week_day_options = ('all', 'weekends', 'working days')
day_week_options = ('none', 'all days', 'workdays and weekend')
month_number = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
week_day_number = ('0', '1', '2', '3', '4', '5', '6', '7')
week_day_option_number = ('0', '1', '2')
day_week_option_number = ('0', '1', '2')

#types of users, gender.
user_types = ('all', 'subscriber', 'customer')
user_genders = ('all', 'female', 'male')
user_type_number = ('0', '1', '2')
user_gender_number = ('0', '1', '2')

#options for table query.
table_options = ('none', 'birth year', 'user type', 'gender', 'start station', 'month', 'day', 'week_day', 'hour')
table_options_number = ('0', '1', '2', '3', '4', '5', '6', '7','8')

#options for correlation query.
correlation_options = ('none', 'user type', 'gender')
correlation_option_number = ('0', '1', '2')

#options for percentage query.
percentage_options = ('none', 'age group', 'user type', 'gender')
percentage_option_number = ('0', '1', '2', '3')


def get_filters(city, month, week_day, user_type, user_gender):
    """
    Asks user to specify a city, month, week_day, user_type and user_gender to analyze.
    If the default value of de data recieved is "" it means that it must to ask.
    If the default value of de data recieved is "0" it means that we don't want to ask about this filter.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) week_day - name of the day of week to filter by, or "all" to apply no day filter
        (str) user_type - type of user, or "all" to apply no filter
        (str) user_gender - gender of user, or "all" to apply no filter
    """

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while not (city in cities or city in city_number):
        city = input("Enter the name or de number of the city (chicago(1), new york city(2), washington(3)): \n")
        city = city.lower()
    if city not in cities:
        city = list(CITY_DATA.keys())[int(city)-1]

    # TO DO: get user input for month (all, january, february, ... , june).
    while not (month in months or month in month_number):
        month = input("Enter the month or its number (all(0), january(1), february(2), ... , december(12)): \n")
        month = month.lower()
    if month not in months:
        month = months[int(month)]

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday).
    while not (week_day in week_days or week_day in week_day_number):
        week_day = input("Enter the day or its number (all(0), monday(1), tuesday(2), ... sunday(7)): \n")
        week_day = week_day.lower()
    if week_day not in week_days:
        week_day = week_days[int(week_day)]

    #get user input for user type.
    while not (user_type in user_types or user_type in user_type_number):
        user_type = input("Enter the user type or its number (all(0), subscriber(1), customer(2)): \n")
        user_type = user_type.lower()
    if user_type not in user_types:
        user_type = user_types[int(user_type)]

    #get user input for customer gender.
    if city != 'washington':
        while not (user_gender in user_genders or user_gender in user_gender_number):
            user_gender = input("Enter the uesr gender or its number (all(0), female(1), male(2)): \n")
            user_gender = user_gender.lower()
        if user_gender not in user_genders:
            user_gender = user_genders[int(user_gender)]
    print('-'*40)


    return city, month, week_day.title(), user_type.title(), user_gender.title()


def load_data(city, month, day, user_type, user_gender):
    """
    Loads data for the specified city and filters by month, day, user_type and user_gender if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) user_type - type of user, or "all" to apply no filter
        (str) user_gender - gender of user, or "all" to apply no filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from the Start Time column to create a month column.
    df['month'] = df['Start Time'].dt.month

    # extract week_day from the Start Time column to create a week_day column.
    df['week_day'] = df['Start Time'].dt.weekday_name

    #create a column with the type of day work day or weekend.
    df['day type'] = df['week_day'].apply(lambda x: 'work' if x.lower() in work_days else 'weekend')

    # extract day from the Start Time column to create a day column.
    df['day'] = df['Start Time'].dt.day

    # extract hour from the Start Time column to create a hour column.
    df['hour'] = df['Start Time'].dt.hour

    # extract date from the Start Time column to create a date column.
    df['date'] = df['Start Time'].dt.date

    #create a column with the age and another with the group of age.
    if 'Birth Year' in df.columns:
        df['age'] = df['Start Time'].dt.year - df['Birth Year']
        df['Age Group'] = df['age'].apply(lambda x: 1 if x < 25 else (2 if x in range(25,35) else (3 if x in range(35,45) else (4 if x in range(45,55) else 5))))

    # combine Start Station and End Station to define a trip.
    df['Trip'] = df['Start Station']+ ' <---> ' +  df['End Station']

    # filter df by month and week_day.
    if month.lower() != 'all' and month != 0:
        month = months.index(month)
        df = df[df.month == month]
        month_shape = df.shape

    if day.lower() != 'all' and day != 0:
        df = df[df.week_day == day]
        day_shape = df.shape

    # filter df by user type.
    if user_type.lower() != 'all' and user_type != 0:
        df = df[df['User Type'] == user_type.title()]
        user_type_shape = df.shape

    # filter df by gender.
    if user_gender.lower() != 'all' and user_gender != 0 and user_gender != "" and 'Gender' in df.columns:
        df = df[df.Gender == user_gender.title()]
        gender_shape = df.shape

    #If the result of the filter get no values it will be displayed a message.
    if df.shape[0] == 0:
        print('Maybe you have filtered too much. There are no rows in your query.')
        print('This is the evolution of your filters:')
        if month != 'all' and month != 'All' and month != 0:
            print('After filtering by month you have {} rows.'.format(month_shape[0]))
        if day.lower() != 'all' and day != 0:
            print('After filtering by day of week you have {} rows.'.format(day_shape[0]))
        if user_type.lower() != 'all' and user_type != 0:
            print('After filtering by user type you have {} rows.'.format(user_type_shape[0]))
        if user_gender.lower() != 'all' and user_gender != 0 and user_gender != "":
            print('After filtering by gender you have {} rows.'.format(gender_shape[0]))

    return df

def seconds_to_hours(seconds):
    """
    Convert seconds in hours, minutes and seconds

    Args:
    (int) seconds - Total seconds
    Returns:
    (int) hour - Number of hours
    (int) min - Number of minutes
    (int) sec -  Number of seconds
    """
    sec = int(seconds % 60)
    min = int(((seconds - sec) / 60) % 60)
    hour = int((seconds - (min * 60) -sec) / 3600)
    return hour, min, sec


def save_file(df):
    """save the result df to a file"""
    next = input('\nWould you like to extract this data to csv a file? Enter (y)es or (n)o.\n')
    if next.lower() == 'yes' or next.lower() == 'y':
        file = input('\nEnter the name of the file: ')
        df.to_csv(file + '.csv')


def display_data(df):
    """print a table in groups of 6 rows"""
    i = 0
    next = input('\nDo you want to see raw data? Enter (y)es or (n)o.\n')
    if next.lower() == 'yes' or next.lower() == 'y':
        while True and i < df.shape[0]:
            print(df.iloc[i:i+5])
            i += 5
            print('\n{} rows of {}.'.format(min(i,df.shape[0]),df.shape[0]))
            if i < df.shape[0]:
                next = input('\nWould you like to see the next 5 rows? Enter (y)es or (n)o.\n')
                if not(next.lower() == 'yes' or next.lower() == 'y'):
                    break


def show_plot(df,stat_option):
    """print different plots depending of the stat option"""

    if stat_option == "percentage":
        df.plot.bar(stacked=True, color=sns.color_palette("Blues"))

    if stat_option == "correlation":
        df.plot(kind='scatter', x = 0, y = 1)

    if stat_option == "trip table":
        df.plot(kind='bar', y = 'Trip Duration count')
        df.plot(kind='bar', y = 'Trip Duration sum')
        df.plot(kind='bar', y = 'Trip Duration mean')

    plt.tight_layout()
    plt.show()




def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month.
    popular_month = df['month'].mode()[0]
    popular_month_count = df['month'].value_counts()[popular_month]
    print('{:<30} {:<30}'.format('Most frequent month:', 'Number of Trips:'))
    print('{:<30} {:<30}'.format(months[popular_month].title(), popular_month_count))

    # TO DO: display the most common day of week.
    popular_day_of_week = df['week_day'].mode()[0]
    popular_day_count = df['week_day'].value_counts()[popular_day_of_week]
    print('{:<30} {:<30}'.format('Most Frequent Week Day:', 'Number of Trips:'))
    print('{:<30} {:<30}'.format(popular_day_of_week, popular_day_count))

    # TO DO: display the most common start hour.
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = int(df['hour'].value_counts()[popular_hour])
    print('{:<30} {:<30}'.format('Most frequent hour:', 'Number of Trips:'))
    print('{:<30} {:<30}'.format(str(popular_hour) + ':00', popular_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station.
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = df['Start Station'].value_counts()[popular_start_station]
    print('{:<30} {:<30}'.format('Most Popular Start Estation:', 'Number of Trips:'))
    print('{:<30} {:<30}'.format(popular_start_station, popular_start_station_count))

    # TO DO: display most commonly used end station.
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = df['End Station'].value_counts()[popular_end_station]
    print('{:<30} {:<30}'.format('Most Popular End Estation:', 'Number of Trips:'))
    print('{:<30} {:<30}'.format(popular_end_station, popular_end_station_count))

    # display trip count with same start and end station, and with different start and end stations.
    df['Comp_Stations'] = np.where(df['Start Station'] == df['End Station'], '1', '0')
    print('\nBikes Delivered at the Same Station:')
    try:
        different_station = df['Comp_Stations'].value_counts()['0']
        print('{:<30} {:<30}'.format('Different Stations:', different_station))
    except Exception as e:
        print('{:<30} {:<30}'.format('Different Stations:', '0'))
    try:
        same_station = df['Comp_Stations'].value_counts()['1']
        print('{:<30} {:<30}'.format('Same Station:', same_station))
    except Exception as e:
        print('{:<30} {:<30}'.format('Same Station:', '0'))

    # TO DO: display most frequent combination of start station and end station trip.
    print('-'*20)
    popular_trip = df['Trip'].mode()[0]
    popular_trip_count = df['Trip'].value_counts()[popular_trip]
    print('{:<30} {:<30}'.format('Most Frequent Trip:', popular_trip))
    print('{:<30} {:<30}'.format('Number of Trips:', popular_trip_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time.
    total_time = int(df['Trip Duration'].sum())
    hour, min, sec = seconds_to_hours(total_time)
    print('{:<30} {:<} hours, {:<} minutes and {:<} seconds'.format('Total Time for All Trips:', hour, min, sec))
    print('{:<30} {:<} seconds'.format('',total_time))

    # TO DO: display mean travel time.
    mean_time = int(df['Trip Duration'].mean())
    hour, min, sec = seconds_to_hours(mean_time)
    print('{:<30} {:<} hours, {:<} minutes and {:<} seconds'.format('Mean Time for All Trips:', hour, min, sec))
    print('{:<30} {:<} seconds'.format('',mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types.
    user_types = df['User Type'].value_counts()
    print('{:<30} {:<30}'.format('User Type:','Nº of users:'))
    for i, type in enumerate(user_types.index):
        print('{:<30} {:<30}'.format(user_types.index[i],int(user_types[type])))

    # TO DO: Display counts of gender.
    print('-'*20)
    if 'Gender' in df.columns:
        df['Gender']=df['Gender'].fillna('Not Specified')
        user_gender = df['Gender'].value_counts()
        print('{:<30} {:<30}'.format('Gender:','Nº of users:'))
        for i, gender in enumerate(user_gender.index):
            print('{:<30} {:<30}'.format(user_gender.index[i],int(user_gender[gender])))
    else:
        print('There is no information about the gender.')

    # TO DO: Display earliest, most recent, and most common year of birth.
    print('-'*20)
    if 'Birth Year' in df.columns and df['Birth Year'].count() > 0:
        user_birth_year_min = int(df['Birth Year'].min())
        print('{:<30} {:<30}'.format('Earliest year of birth:',user_birth_year_min))
        user_birth_year_max = int(df['Birth Year'].max())
        print('{:<30} {:<30}'.format('Most recent year of birth:',user_birth_year_max))
        user_birth_year_mode = int(df['Birth Year'].mode()[0])
        print('{:<30} {:<30}'.format('Most common year of birth:',user_birth_year_mode))
    else:
        print('There is no information about the year of birth.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def table_comp_stats(df, table_option):

    """
    sum, count and mean of the trip duration for a city. The data can be extracted for differents years of birth,
    user types, genders, start stations, months, days of the month, days of the week or hours of the day.

    Args:
        (str) table_option - the option choosed for quering the data.
    """

    print('\nCalculating Trip Duration stats...\n')
    start_time = time.time()

    #if the table option is year of birth we make groups of five years.
    if table_option == 'birth year':
        df['Birth Year Agg']= (df['Birth Year']//5*5)
        print('There is {} rows without year of birth.'.format(df['Birth Year Agg'].isnull().sum()))
        print('The result is printed in groups of five years\n')
        df = df.dropna(subset=['Birth Year Agg'])
        df['Birth Year Agg'].astype('int64')
        df = df.groupby('Birth Year Agg').agg({"Trip Duration":['count', 'sum', 'mean']})
    elif table_option in ('start station', 'user type', 'gender'):
        df = df.groupby(table_option.title()).agg({"Trip Duration":['count', 'sum', 'mean']})
    else:
        df = df.groupby(table_option).agg({"Trip Duration":['count', 'sum', 'mean']})
    df.columns = [" ".join(x) for x in df.columns.ravel()]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40 + '\n')

    #display the result data in groups of six rows.
    display_data(df)

    #display the result in a plot with multiprocessing.
    next = input('\nWould you like to see this data in plots? Enter (y)es or (n)o.\n')
    if next.lower() == 'yes' or next.lower() == 'y':
        if table_option == 'start station':
            print('\nWe are going to plot only the 15 Stations with more trips.\n')
            df = df.sort_values(by=['Trip Duration count'], ascending = False).iloc[:15]
        p = mp.Process(target=show_plot, args=(df,'trip table'))
        p.daemon = True
        p.start()
        time.sleep(5)

    save_file(df)


def correlation_stats(df, correlation_option, week_day_option):

    """
    sum, count and mean of the trip duration for a city. The data can be extracted for differents years of birth,
    user types, genders, start stations, months, days of the month, days of the week or hours of the day.

    Args:
        (str) correlation_option - option to calculate the correlation between user types or between gender.
        (str) week_day_option - option to do the calcs for all day, for work days or for weekends.
    """

    print('\nCalculating Correlation stats...\n')
    start_time = time.time()


    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()

    #divide by user type for all week_day_option
    if correlation_option == 'user type':
        df1 = df[df['User Type']=='Subscriber']
        df2 = df[df['User Type']=='Customer']
    #divide by gender for all week_day_option
    elif correlation_option == 'gender':
        df1 = df[df['Gender']=='Male']
        df2 = df[df['Gender']=='Female']

    #filter by type of day (all, work days o weekends)
    #for correlation_option = 'user type' or 'gender'
    if week_day_option == 'weekends':
        df1 = df1[df1['day type']=='weekend']
        df2 = df2[df2['day type']=='weekend']
    elif week_day_option == 'working days':
        df1 = df1[df1['day type']=='work']
        df2 = df2[df2['day type']=='work']

    #count the trips by day.
    df1 = df1.groupby('date').agg({"Trip Duration":['count']})
    df2 = df2.groupby('date').agg({"Trip Duration":['count']})
    df1.columns = [" ".join(x) for x in df1.columns.ravel()]
    df2.columns = [" ".join(x) for x in df2.columns.ravel()]

    #merge the two df's.
    df3 = pd.concat([df1,df2], axis=1, ignore_index=True)
    if correlation_option == 'user type':
        df3.columns = ['Trip Count Subscriber', 'Trip Count Customer']
    if correlation_option == 'gender':
        df3.columns = ['Trip Count Male', 'Trip Count Female']

    #calc and print the correlation.
    print('\nCorrelation: ', df3.iloc[:, 0].corr(df3.iloc[:, 1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40 + '\n' )

    #display the result in a scatter plot with multiprocessing.
    next = input('\nWould you like to see this data in a plot? Enter (y)es or (n)o.\n')
    if next.lower() == 'yes' or next.lower() == 'y':
        p = mp.Process(target=show_plot, args=(df3,'correlation'))
        p.daemon = True
        p.start()
        time.sleep(5)

    save_file(df3)


def percentage_comp_stats(df, percentage_option, day_week_option):

    """
    It calculates the percentage of trips for differente groups of users. The users can be grouped by type, gender or
    age. The precentage will be shown by days of week, or grouping by work days and weekend.

    Args:
        (str) percentage_option - the group type for users (user type, gender, age)
        (str) day_week_option - the group type for days (day by day, work/weekend days)
    """

    print('\nCalculating Percentage stats...\n')
    start_time = time.time()

    #calcs for every percentage_option ('age group', 'user type', 'gender')
    #group the dataframe by (days or day type) and the percentage option
    #calc the percentage on every time period (day or day type)
    #reorder the data frame and make the pivot to pass the df to be displayed and showed in a stacked bar plot
    if day_week_option == 'all days':
        df = df.groupby(['week_day', percentage_option.title()]).agg({"Trip Duration":['count']})
        df = df.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
        df.columns = [" ".join(x) for x in df.columns.ravel()]
        df.reset_index(inplace=True)
        df.columns = ['Week Day', percentage_option.title(), 'Trip Duration(%)']
        df['Week Day'] = pd.Categorical(df['Week Day'], categories = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'], ordered=True)
        df.sort_values(by=['Week Day', percentage_option.title()], ascending = True, inplace=True)
        df = df.pivot(index='Week Day', columns=percentage_option.title(), values='Trip Duration(%)')
    if day_week_option == 'workdays and weekend':
        df = df.groupby(['day type', percentage_option.title()]).agg({"Trip Duration":['count']})
        df = df.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
        df.columns = [" ".join(x) for x in df.columns.ravel()]
        df.reset_index(inplace=True)
        df.columns = ['Type of Day', percentage_option.title(), 'Trip Duration(%)']
        df = df.pivot(index='Type of Day', columns=percentage_option.title(), values='Trip Duration(%)')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40 + '\n' )

    #display the result data in groups of six rows.
    display_data(df)

    #display the result in a stacked bar plot with multiprocessing.
    next = input('\nWould you like to see this data in a plot? Enter (y)es or (n)o.\n')
    if next.lower() == 'yes' or next.lower() == 'y':
        p = mp.Process(target=show_plot, args=(df,'percentage'))
        p.daemon = True
        p.start()
        time.sleep(5)

    save_file(df)


def call_option(stat_option):
    """
    Ask the information necessarry for each calc and call the corresponding functions.
    there is fous main calcs possible "global", "trip table", "correlation", "percentage"

    Args:
        (str) stat_option - the first main calculation.
    """
    #first global stats.
    while stat_option == 'global':

        city, month, day, user_type, user_gender  = get_filters("" ,"" ,"" ,"" ,"")
        df = load_data(city, month, day, user_type, user_gender)
        if df.shape[0] == 0:
            restart = input('\nWould you like to try with another filter? Enter (y)es or (n)o.\n')
            if not(restart.lower() == 'yes' or restart.lower() == 'y'):
                break
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            restart = input('\nWould you like to restart this option? Enter (y)es or (n)o.\n')
            if not(restart.lower() == 'yes' or restart.lower() == 'y'):
                break

    #table with counts, sum and mean of trip duration.
    while stat_option == 'trip table':
        table_option = ""
        while not (table_option in table_options or table_option in table_options_number):
            print('What period or option do you want to use for calculate the sum, count and mean of the duration time?')
            table_option = input('Type (birth year(1), user type(2), gender(3), start station(4), month(5), day(6), week_day(7), hour(8) or none(0)):\n')
        if table_option not in table_options:
            table_option = table_options[int(table_option)]
        if table_option.lower() == 'none':
            break
        else:
            city, month, day, user_type, user_gender  = get_filters("","0" ,"0" , "0", "0")
            df = load_data(city, month, day, user_type, user_gender)
            if not ((table_option == 'gender' and 'Gender' not in df.columns) or (table_option == 'birth year' and 'Birth Year' not in df.columns)):
                table_comp_stats(df, table_option)
            elif table_option == 'gender':
                print('There is no information about the gender in this file.')
            elif table_option == 'birth year':
                print('There is no information about the year of birth in this file.')

            restart = input('\nWould you like to restart this option? Enter (y)es or (n)o.\n')
            if not(restart.lower() == 'yes' or restart.lower() == 'y'):
                break

    #optionc tha calc correlation between different sets of data.
    while stat_option == 'correlation':
        correlation_option = ""
        while not (correlation_option in correlation_options or correlation_option in correlation_option_number):
            print('Do you want to calculate the correlation between the two user types or between the two genders?')
            correlation_option = input('Type (user type(1), gender(2) or none(0)):\n')
        if correlation_option not in correlation_options:
            correlation_option = correlation_options[int(correlation_option)]
        if correlation_option.lower() == 'none':
            break
        else:
            week_day_option = ""
            while not (week_day_option in week_day_options or week_day_option in week_day_option_number):
                print('What kind of days do you want to use to do the correlation?')
                week_day_option = input('Choose (all(0), weekends(1) or working days(2)):\n')
            if week_day_option not in week_day_options:
                week_day_option = week_day_options[int(week_day_option)]
            city, month, day, user_type, user_gender  = get_filters("","0" ,"0" , "0", "0")
            df = load_data(city, month, day, user_type, user_gender)
            if not (correlation_option == 'gender' and 'Gender' not in df.columns):
                correlation_stats(df, correlation_option, week_day_option)
            else:
                print('There is no information about the gender in this file.')
            restart = input('\nWould you like to restart this option? Enter (y)es or (n)o.\n')
            if not(restart.lower() == 'yes' or restart.lower() == 'y'):
                break

    #percentage of trips for different groups of users.
    while stat_option == 'percentage':
        percentage_option = ""
        while not (percentage_option in percentage_options or percentage_option in percentage_option_number):
            print('Choose a group of users to calculate the percentage of total trips.')
            percentage_option = input('Type (age group(1) user type(2), gender(3) or none(0)):\n')
        if percentage_option not in percentage_options:
            percentage_option = percentage_options[int(percentage_option)]
        if percentage_option.lower() == 'none':
            break

        day_week_option = ""
        while not (day_week_option in day_week_options or day_week_option in day_week_option_number):
            print('Choose a group of users to calculate the percentage of total trips.')
            day_week_option = input('Type (all days(1), workdays and weekend(2) or none(0)):\n')
        if day_week_option not in day_week_options:
            day_week_option = day_week_options[int(day_week_option)]
        if day_week_option.lower() == 'none':
            break
        city, month, day, user_type, user_gender  = get_filters("","0" ,"0" , "0", "0")
        df = load_data(city, month, day, user_type, user_gender)
        if not ((percentage_option == 'gender' and 'Gender' not in df.columns) or (percentage_option == 'age group' and 'Age Group' not in df.columns)):
            percentage_comp_stats(df, percentage_option, day_week_option)
        elif percentage_option == 'gender':
            print('There is no information about the gender in this file.')
        elif percentage_option == 'age group':
            print('There is no information about the year of birth in this file.')

        restart = input('\nWould you like to restart this option? Enter (y)es or (n)o.\n')
        if not(restart.lower() == 'yes' or restart.lower() == 'y'):
            break


def main():

    #Explanation of the options developed in the app.

    print('Hello! Let\'s explore some US bikeshare data!\n')
    print('Choose one option:\n')
    print('\033[1m'+'Option 1:' + '\033[0m' + ' Some global statistics. In this case you will be able to extract the next data:\n')
    print('\033[1m' + '\t  Time Stats:' + '\033[0m' + ' Most common month, most common day of week and most common start hour.\n')
    print('\033[1m' + '\t  Station Stats:' + '\033[0m' + ' Most common used start and end station, trips with the same start ')
    print('\t  and end stations and most frequent combination of start and end station.\n')
    print('\033[1m' + '\t  Trip duration Stats:' + '\033[0m' + ' total and mean travel time.\n')
    print('\033[1m' + '\t  User Stats:' + '\033[0m' + ' Count of trips by user by types or by gender. Also the earliest, most ')
    print('\t  recent and most common year of birth.')
    print('\t  You will be able to filter by city, month, day, user type or/and user gender.\n')
    print('\033[1m' + 'Option 2:' + '\033[0m' + ' You will see a table with the sum, count and mean of the trip duration for a city.')
    print('\t  You will be asked to do the operations by the year of birth, the user type, the gender, ')
    print('\t  the start station, the month, the day of the month, the day of the week or the hour of the day.')
    print('\t  You will be able to see the result in a bar plot and save it in a file\n')
    print('\033[1m' + 'Option 3:' + '\033[0m' + ' You will see the correlation of the number of trips by user type or gender.')
    print('\t  The sum of the number of trips is calculated by day and you will be able to choose between')
    print('\t  weekend days or work days. You will see that the correlation is different on weekends and ')
    print('\t  in working days for the two user types and for gender. The result can be showed in a scatter')
    print('\t  plot and save it in a file.\n')
    print('\033[1m' + 'Option 4:' + '\033[0m' + ' You will see the percentage of trips for different groups of users along the days of the week.')
    print('\t  The users will be divided between group of age, user type or gender.')
    print('\t  The groups of ages are: (1) Younger than 25, (2) Between 25 and 35, (3) Between 35 and 45, ')
    print('\t  (4) Between 45 and 55, (5) Older than 55.')
    print('\t  The data will be displayed by day of week or divided in work-days and weekends.')
    print('\t  The result can be showed in a scatter plot and save it in a file.\n')

    #The user choose a type of calc between the main four.

    while True:
        stat_option = ""
        while not (stat_option in stat_options or stat_option in stat_option_number):
            stat_option = input('Type (none(0), global(1), trip table(2), correlation(3), percentage(4)):\n')
        if stat_option not in stat_options:
            stat_option = stat_options[int(stat_option)]
        if stat_option.lower() == 'none':
            break
        else:
            call_option(stat_option)
            print('Would you like to try another option?')


if __name__ == "__main__":
    try:
	    main()
    except (KeyboardInterrupt, EOFError):
        print('\n\nIt seems that you want to leave the script. Thanks for using it and I hope to see you again soon.\n\n')
        sys.exit()
