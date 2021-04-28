import time
import calendar
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # gets user input for city (chicago, new york city, washington).
    while True:
        cities = ('chicago', 'new york city', 'washington')
        city = input('\nPlease select a city with the galactic republic. Destinations include: \n\nchicago --- new york city --- washington \n\nSELECTION: ' ).lower().strip()
        if city not in cities:
            print('\nCity not found in this galaxy.')
        else:
            print('\nYou selected {}. Gooood'.format(city))
            break
    print('-'*80)

    # gets user input for month (all, january, february, ... , june)
    while True:
        months = ('january','february','march','april','may','june')
        unincluded = ('july','august','september','october','november','december')
        month = input('\nI can filter by month or show all. Which would you prefer? (type all or the month) \n\nSELECTION: ').lower().strip()
        if month in months:
            print('\n\nYou picked {}. Superb decision!'.format(month))
            break
        elif month == 'all':
            print('\nYou picked {}. Coming right up.'.format(month))
            break
        elif month in unincluded:
            print('\nNo data available for that month. Try January - June.')
        else:
            print('\nI\'m having a hard time finding {}. Are you sure that is on the Gregorian calendar? Try again'.format(month))
    print('-'*80)
    # gets user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ('sunday','monday','tuesday','wednesday','thursday','friday','saturday')
        day = input('\nAre you interested in a specific day or shall I grab the whole week? (type all or day of the week) \n\nSELECTION: ' ).lower().strip()
        if day in days:
            print('\nYou picked {}. Retrieving data now.'.format(day))
            break
        elif day == 'all':
            print('You picked {}. Compiling as we speak.'.format(day))
            break
        else:
            print('\nIs {} really a day of the week? Shall I recommend a calendar?. Try again.'.format(day))
    print('-'*80)
    print('Coordinates Received! \nDestination: {} \nMonth: {} \nDay: {} \n\nYou know sometimes I amaze even myself.'.format(city,month,day))

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.
       You will see that some comments have a Star Wars theme.

       Information for converting from a number to a month name was found here:
       https://stackoverflow.com/questions/6557553/get-month-name-from-number"""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # displays the most common month with conversion for int to month name
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    month_name = calendar.month_name[popular_month].title()
    print('\nMost frequent rentals occurred in {}'.format(month_name))


    # displays the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0].title()
    print('\nMost popular day for rentals was {}'.format(popular_day))

    # displays the most common start hour with conversion for 24 to 12 hour time
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    if popular_hour < 12:
        converted_hour = (12 - popular_hour)
        print('\nThe most common hour for rentals was {} AM'.format(converted_hour))
    elif popular_hour == 12:
        print('\nThe most common hour for rentals was {} PM'.format(popular_hour))
    elif popular_hour > 12:
        converted_hour = (popular_hour - 12)
        print('\nThe most common hour for rentals was {} PM'.format(converted_hour))
    else:
        print('Unable to retrieve the requested information')

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displays most commonly used start station
    df['Pickup Station'] = df['Start Station'].mode()[0].strip()
    pick_up =  df['Pickup Station'].mode()[0]
    print('\nThe hot spot for rentals is {}'.format(pick_up))

    # displays most commonly used end station
    df['Dropoff Station'] = df['End Station'].mode()[0].strip()
    the_drop =  df['Dropoff Station'].mode()[0]
    print('\nThe most drop offs occur at {}'.format(the_drop))

    # displays most frequent combination of start station and end station trip
    popular_route = df.groupby(['Start Station', 'End Station']).size().idxmax()
    beginning = popular_route[0]
    end = popular_route[1]
    print('\nThe most popular rental combination appears to be Start: {} and End: {}.'.format(beginning,end))

    # displays top 5 most popular rental locations with rental counts
    station_count = df['Start Station'].value_counts().nlargest(5)
    print('\nHere are your top 5 rental stations and how many times they were used \n{}'.format(station_count))

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # displays total travel time
    df['Total Duration'] = df['Trip Duration'].sum()
    total_run = df['Total Duration'].sum()
    years = int(total_run / 3.154E+7)
    print('Total travel time for all rentals is {} seconds (or {} years)'.format(total_run,years))

    # displays mean travel time
    df['Avg Duration'] = df['Trip Duration'].mean()
    average_run = df['Avg Duration'].mean()
    modified = int(average_run)
    minutes = modified / 60
    print('\nAverage travel time is {} minutes'.format(minutes))

    # displays the shortest travel time
    df['Shortest Duration'] = df['Trip Duration'].min()
    shortest_run = df['Shortest Duration'].min()
    modified_2 = int(shortest_run)
    minutes_2 = modified_2 / 60
    print('\nShortest travel time is {} minutes'.format(minutes_2))

    # displays the longest travel time
    df['Longest Duration'] = df['Trip Duration'].max()
    longest_run = df['Longest Duration'].max()
    modified_3 = int(longest_run)
    minutes_3 = int(modified_3 / 60)
    print('\nLongest travel time is {} minutes'.format(minutes_3))

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # displays counts of user types
    try:
        user_types = df['User Type'].value_counts()
        print('User Types found: \n{}'.format(user_types))
    except:
        print('No user information available.  I got a bad feeling about this.')
    # displays counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('\nComparsion of rentals by gender: \n{}'.format(gender))
    except:
        print('\nPower! Unlimited power! Oh, sorry I couldn\'t find gender data.')
    # displays earliest, most recent, and most common year of birth
    try:
        earliest_by = df['Birth Year'].min()
        earliest_by = int(earliest_by)
        print('\nThe oldest renter was born in {}'.format(earliest_by))

        most_recent_by = df['Birth Year'].max()
        most_recent_by = int(most_recent_by)
        print('\nThe youngest renter was born in {}'.format(most_recent_by))

        most_common_by = df['Birth Year'].mode()
        most_common_by = int(most_common_by)
        print('\nThe typical renter was born in {}'.format(most_common_by))
    except:
        print('\nNo beginning existance date available. I find the lack of data disturbing.')

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)

def raw_data(df):

    """Asks the user if they would like to see raw data.  If 'Y', 5 rows of raw data will
       appear followed by a prompt to display more data.

       Information gained from the Udacity Knowledge Base was used to improve this module."""

    answers = ('y','n')
    start_loc = 0
    while True:
        rd = input('Would you like to see the raw data? (Y or N) ').lower()
        if rd == 'n':
            break
        if rd not in answers:
            print('Did you type Y or N? Try again.')
        if rd == 'y':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
    print('-'*80)

def main():

    """Contains all modules for performing statistical analysis of bike sharing data with the ability to restart.
       If the user decides to exit the program they will be left with an encouraing quote from Yoda and a keyboard art
       lightsaber

       lightsaber keyboard art found here:
       https://www.answers.com/Q/How_do_you_make_a_lightsaber_on_the_keyboard"""

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'no':
                print('\n"Do. Or do not. There is no try". — Yoda')
                print('\n<:::::::::::::::::::::::::::::::::::::|]=[]=:==:| |]\n')
                return
            if restart.lower() == 'yes':
                break
            if restart.lower() not in ('yes','no'):
                print('\nInvalid input. Please enter yes or no.')

if __name__ == "__main__":
    main()
