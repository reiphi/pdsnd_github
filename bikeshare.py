import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington).
    city = ''
    while city not in CITY_DATA.keys():
        city = input('Would you like to see data for Chicago, New York City, or Washington?\nPlease type out the full city name:\n').lower()
    print('OK, so you will get information for {}.\n'.format(city.title()))
    
    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in months[:6] and month != 'all':
        month = input('Which month - January, February, March, April, May, or June?\nPlease type out the full month name (type "all" for no time filter on months):\n').lower()
    if month == 'all':
        print('OK, so we\'ll use no time filter on months.\n')
    else:
        print('OK, so you will get information from {}.\n'.format(month.title()))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in days and day != 'all':
        day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\nPlease type out the full day name (type "all" for no time filter on days of the week):\n').lower()
    if day == 'all':
        print('OK, so we\'ll use no time filter on days of the week.\n')
    else:
        print('OK, so you will get information from {}.\n'.format(day.title()))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start and End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month 
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    # display raw data if desired
    see_raw_data = input('\nWould you like to see the raw data (yes, no with any other answer)?\n').lower()
    raw_data_counter = 0
    while see_raw_data == 'yes':
        print(df.iloc[6*raw_data_counter:5 + 6*raw_data_counter])
        raw_data_counter += 1
        see_raw_data = input('\nWould you like to see five more rows (yes, no with any other answer)?\n').lower()

    print('-'*40)
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        most_common_month = df['month'].mode()[0]
        print('The most common month is {}.'.format(months[most_common_month - 1].title()))

    # display the most common day of week
    if day == 'all':
        most_common_day = df['day_of_week'].mode()[0]
        print('The most common day of the week is {}.'.format(most_common_day))

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    if most_common_start_hour >= 12:
        print('The most common start hour is {} pm.'.format(most_common_start_hour - 12))
    else:
        print('The most common start hour is {} am.'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is {}.'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is {}.'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    most_common_combination = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print('The most frequent combination of start station and end station trip is {}.'.format(most_common_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = (df['End Time'] - df['Start Time']).sum()
    print('The total travel time is {}.'.format(total_travel_time))

    # display mean travel time
    average_travel_time = (df['End Time'] - df['Start Time']).mean()
    print('The average travel time is {}.'.format(average_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('What is the breakdown of users?')
    print('{}\n'.format(df.groupby(['User Type'])['User Type'].count()))

    # Display counts of gender
    print('What is the breakdown of gender?')
    if 'Gender' in df.columns:
        print('{}\n'.format(df.groupby(['Gender'])['Gender'].count()))
    else:
        print('Sorry, no gender data available.\n')

    # Display earliest, most recent, and most common year of birth
    print('What is the earliest, most recent, and most common year of birth?')
    if 'Birth Year' in df.columns:
        most_common_birth_year = df['Birth Year'].mode()[0]
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        print('The earliest year of birth is {}.'.format(int(earliest_birth_year)))
        print('The most recent year of birth is {}.'.format(int(most_recent_birth_year)))
        print('The most common year of birth is {}.\n'.format(int(most_common_birth_year)))
    else:
        print('Sorry, no birth year data available.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
