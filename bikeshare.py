import time
import pandas as pd
import numpy as np
import datetime as dt
from IPython.display import display
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = {"january":1, "february":2, "march":3, "april":4, "may":5, "june":6}
filter_choice=''

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze..

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!!')
    print('\nPlease select/enter a city: Chicago, New York City, Washington')
    
    city=""
    cities=["chicago", "new york city", "washington"]
    
    """Prompts user to enter a city correctly."""    
    while city not in cities:
        city = input().lower()
        if city not in cities:
            print("Invalid City Entry! Please type Chicago, New York or Washington")
            
    """prompts user to enter a filter choice"""
    print("")
    msg='How would you like to filter your data? By month, day, both or not filtered at all?\nPlease select/type one the choices: month, day, both, none'
    print(msg)
    global filter_choice
    date_entry_types=["month","day","both","none"]
    
    while filter_choice not in date_entry_types:
        filter_choice = input()
        if filter_choice not in date_entry_types:
            print("Invalid Entry! Please type month,day,both or none")
            
    month=""    
    avail_months=["january", "february", "march", "april", "may", "june"]
    
    """prompts users to enter a valid month (january, february, ... , june) and retries until input is entered correctly"""

    if filter_choice in ("month","both"):
        print("")
        print("Please, select a month: January, February, March, April, May or June")
        while month not in avail_months:
            month = input().lower()
            if month not in avail_months:
                print("Invalid month! Please type January, February, March, April, May or June")  
                
    """asks to user to enter an input for day of week as an integer and retries untill inut is entered correctly. """
    day = 0
    if filter_choice in ("day","both"):
        print("")
        print("Please specify the day of the week? Enter your response as an integer(e.g., 1=Monday).")
        check_day = False
        while check_day == False:
            try:
                day = int(input ())
                if day > 0 and day < 8:
                    check_day=True
                else:
                    print("Invalid day! Type your response as an integer between 1 and 7")
            except:
                print("Invalid day! Type your response as an integer between 1 and 7")
                
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    """loads from csvs according to selected city"""
    if city == "new york city":
        df = pd.read_csv("./"+CITY_DATA[city.lower()])
    elif city =="chicago":
        df = pd.read_csv("./chicago.csv")
    else :
        df = pd.read_csv("./washington.csv")
               
    
    """asks users if they would like to see following 5 lines from csv until a negative answer"""
    list_data_answer=''
    i=0
    while list_data_answer not in ('yes','no'):
        print("\nWould you like to see next 5 lines of data? Please answer Yes/No")
        list_data_answer=input().lower()
        if list_data_answer not in ('yes','no'):
            print("Invalid Entry! Please Yes or No")
        elif list_data_answer == 'no':            
            break
        else:
             lines=df.iloc[i:i+5,:]
             print(lines)
             print("i=", i)
             list_data_answer=''   
        i+=5

    """formats start and end time with given format"""
    format = '%b %d %Y %I:%M%p' # The format 
    df['Start Time']= pd.to_datetime(df['Start Time']) 
    df['End Time']= pd.to_datetime(df['End Time']) 
    
    """Gets only entered month from dataset if a month is selected"""
    if month != "":
        df = df[df['Start Time'].dt.month==MONTH_DATA[month]]
    
    """Gets only entered day from data set if a day is selected"""
    if day !=0:
        df = df[df['Start Time'].dt.dayofweek==((day+5)%7)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df["Start Time"])

    """ displays the most common month"""
    df['month'] = df["Start Time"].dt.month
    month = df['month'].mode()[0]
 

    """ displays the most common day of week"""
    df['dayofweek'] = df["Start Time"].dt.dayofweek
    dayofweek = df['dayofweek'].mode()[0]

    """displays the most common start hour"""
    df['hour'] = df["Start Time"].dt.hour
    start_hour = df['hour'].mode()[0]
    
    df2 = df[df['Start Time'].dt.hour==start_hour] 
    
    print("Most popular month:{}".format(month))
    print("Most popular day:{}".format(dayofweek))
    print("Most popular hour:{}".format(start_hour))
    print("Count:{}".format(df2["Start Time"].count()))
    print("Filter:{}".format(filter_choice)) 
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    

    """ displays most commonly used start station"""
    start_station = df['Start Station'].mode()[0]
    print("start_station:{}".format(start_station))
    df3 = df[df['Start Station']==start_station] 
    print("Count:{}".format(df3['Start Station'].count()))
   


    """ displays most commonly used end station"""
    end_station = df["End Station"].mode()[0]
    print("end_station:{}".format(end_station))
    df4 = df[df['End Station']==end_station] 
    print("Count:{}".format(df4['End Station'].count()))
    

    """display most frequent combination of start station and end station trip"""
    counts = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    print("Trip :{}".format(counts.index[0]))
    print("Count : {}".format(counts[0]))
    print("Filter:{}".format(filter_choice))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    """displays total travel time"""
    total_trip_duration=df["Trip Duration"].sum()
    reslt= dt.timedelta(seconds =int(total_trip_duration))
    print("Total duration:{}".format(reslt))
    print("Count:{}".format(df['Trip Duration'].count()))


    """ display mean travel time"""
    avg_duration=df["Trip Duration"].mean()
    reslt= dt.timedelta(seconds =avg_duration)
    print("Avg duration:{}".format(reslt))
    print("Filter:{}".format(filter_choice))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    """ Displays counts of user types"""
    counts = df.groupby(['User Type']).size().sort_values(ascending=False)
    for i in range(len(counts)) : 
        print("{}:{}".format(counts.index[i],counts[i]))
    print("Filter:{}".format(filter_choice))


    """ Displays counts of gender"""
    if 'Gender' in df.columns:
        counts = df.groupby(['Gender']).size().sort_values(ascending=False)
        for i in range(len(counts)) : 
            print("{}:{}".format(counts.index[i],counts[i]))
    else:
        print("No gender data to share.")
    print("Filter:{}".format(filter_choice))


    """ Display earliest, most recent, and most common year of birth"""
    if 'Birth Year' in df.columns:
        print("Earliest year of birth:{}".format(df["Birth Year"].min()))
        print("Most recent year of birth:{}".format(df["Birth Year"].max()))
        print("Most common year of birth:{}".format(df["Birth Year"].mode()[0]))
    else:
        print("No birth year data to share.")
    print("Filter:{}".format(filter_choice))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        """displays the calculated data"""
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()