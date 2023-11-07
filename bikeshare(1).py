import pandas as pd
import numpy as np
import time

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = None
    month = 'all'
    day = 'all'
    """User to Specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    while True:
        city = input("Would you like to see data for Chicago, New York, or Washington? ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city name. Please choose Chicago, New York, or Washington.")
            """User to Specify a city"""
            
    while True:
        filter_choice = input("Would you like to filter the data by month, day, or not at all? ").lower()
        if filter_choice in ['month', 'day', 'not at all']:
            break
        else:
            print("Invalid choice. Please enter 'month', 'day', or 'not at all'.")
            """User to Specify a month, and day to analyze"""

    if filter_choice == 'month':
        while True:
            month = input("Which month - January, February, March, April, May, or June? ").lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print("Invalid month. Please choose from the options provided.")
                """ get user input for month"""
                
    
    if filter_choice == 'day':
        while True:
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ").lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print("Invalid day. Please choose from the options provided.")
                """ get user input for day"""
                
    
    print('-'*40)
    return city, month, day    
     
def load_data(city, month, day):
    file_path = CITY_DATA[city]
     
    """Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # Specify the date format used in your CSV file
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Read the CSV file and parse the 'start_time' column using the specified format
    df = pd.read_csv(file_path, parse_dates=['Start Time'], date_parser=lambda x: pd.to_datetime(x, format=date_format))
    
    if month != 'all':
        df = df[df['Start Time'].dt.month == MONTHS.index(month) + 1]  # Convert month name to a numerical value

    if day != 'all':
        df = df[df['Start Time'].dt.weekday_name == day]
         # Load data for the selected day

    return df
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if 'Start Time' in df:
        common_month = df['Start Time'].dt.month.mode()
        if not common_month.empty:
            common_month = common_month[0]
            print(f"The most common month is {MONTHS[common_month - 1]}")  # Convert the numerical month to the corresponding name
        else:
            print("No data for the most common month.")

        common_day = df['Start Time'].dt.day_name().mode()
        if not common_day.empty:
            common_day = common_day[0]
            print(f"The most common day of the week is {common_day}")
        else:
            print("No data for the most common day of the week.")

        df['hour'] = df['Start Time'].dt.hour
        common_hour = df['hour'].mode()
        if not common_hour.empty:
            common_hour = common_hour[0]
            print(f"The most common start hour is {common_hour}")
        else:
            print("No data for the most common start hour.")

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print("The 'Start Time' column is missing in the dataset. Please check your data.") 
        
def display_raw_data(df, start_idx):
    start_idx = 0

    while True:
        view_data = input("Do you want to see 5 lines of raw data? Enter 'yes' or 'no': ").lower()

        if view_data != 'yes':
            break

        end_idx = start_idx + 5
        print(df.iloc[start_idx:end_idx])
        start_idx = end_idx

        if start_idx >= len(df):
            print("No more raw data to display.")
            break
def popular_start_station(df):
    if 'Start Station' in df:
        start_station_counts = df['Start Station'].value_counts()
        if not start_station_counts.empty:
            most_popular_start_station = start_station_counts.idxmax()
            print(f"The most popular start station is: {most_popular_start_station}")
        else:
            print("No data for the most popular start station.")
    else:
        print("The 'Start Station' column is missing in the dataset. Please check your data.")
        #displays most popular start station
           
    
def user_stats(df):
    user_types = df['User Type'].value_counts()
    
    if 'Subscriber' in user_types:
        subscribers = user_types['Subscriber']
        print(f"Number of Subscribers: {subscribers}")

    if 'Customer' in user_types:
        customers = user_types['Customer']
        print(f"Number of Customers: {customers}")# calculates types of users       
def main():
    start_idx = 0  # Initialize start_idx
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)

        # Ask the user if they want to see raw data
        start_idx = 0
        while True:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            time_stats(df)
          
            
            popular_start_station(df)
            user_stats(df)  
            
    
            start_idx = display_raw_data(df, start_idx)  # Pass both df and start_idx
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()            