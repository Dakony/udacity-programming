import time
import pandas as pd
import numpy as np
import datetime as dt
import click

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')


def choice(prompt, choices=('y', 'n')):
    """Return a valid input from the user given an array of possible answers.
    """

    while True:
        choice = input(prompt).lower().strip()
        # terminate the program if the input is end
        if choice == 'end':
            raise SystemExit
        # triggers if the input has only one name
        elif ',' not in choice:
            if choice in choices:
                break
        # triggers if the input has more than one name
        elif ',' in choice:
            choice = [i.strip().lower() for i in choice.split(',')]
            if list(filter(lambda x: x in choices, choice)) == choice:
                break

        prompt = ("\nPlease check formatting and "
                  "be sure to enter a valid option:\n>")

    return choice


def get_filters():
    """Ask user to specify city(ies) and filters, month(s) and weekday(s).
    Returns:
        (str) city -name of the city(ies) to analyze
        (str) month -name of the month(s) to filter
        (str) day -name of the day(s) of week to filter
    """

    print("\n\nLet's explore some US bikeshare data!\n")

    print("Type end at any time if you would like to exit the program.\n")

    while True:
        city = choice("\nWhich of the city(ies) do you want do select data, "
                      "New York City, Chicago or Washington? Use commas "
                      "to list the names.\n>", CITY_DATA.keys()).lower()
        month = choice("\nFrom January to June, for what month(s) do you "
                       "want do filter data? Use commas to list the names.\n>",
                       months)
        day = choice("\nWhich weekday(s) do you want do filter bikeshare "
                     "data? Use commas to list the names.\n>", weekdays)

        # confirm the user input
        confirmation = choice("\nPlease enter that you will like to apply "
                              "the following filter(s) to the bikeshare data."
                              "\n\n City(ies): {}\n Month(s): {}\n Weekday(s)"
                              ": {}\n\n [y] Yes\n [n] No\n\n>"
                              .format(city, month, day))
        if confirmation == 'y':
            break
        else:
            print("\nLet's try this again!")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Load data for the specified filters of city(ies), month(s) and
       day(s) whenever applicable.
    Args:
        (str) city - name of the city(ies) to analyze
        (str) month - name of the month(s) to filter
        (str) day - name of the day(s) of week to filter
    Returns:
        dtf - Pandas DataFrame containing filtered data
    """

    print("\nLoading the data for the filters of your choice.")
    start_time = time.time()

    # filter the data according to the selected city filters
    if isinstance(city, list):
        dtf = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),
                       sort=True)
        # reorganize DataFrame columns after a city concat
        try:
            dtf = dtf.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        dtf = pd.read_csv(CITY_DATA[city])

    # create columns to display statistics
    dtf['Start Time'] = pd.to_datetime(dtf['Start Time'])
    dtf['Month'] = dtf['Start Time'].dt.month
    dtf['Weekday'] = dtf['Start Time'].dt.weekday_name
    dtf['Start Hour'] = dtf['Start Time'].dt.hour

    # filter the data according to month and weekday into two new DataFrames
    if isinstance(month, list):
        dtf = pd.concat(map(lambda month: dtf[dtf['Month'] ==
                           (months.index(month)+1)], month))
    else:
        dtf = dtf[dtf['Month'] == (months.index(month)+1)]

    if isinstance(day, list):
        dtf = pd.concat(map(lambda day: dtf[dtf['Weekday'] ==
                           (day.title())], day))
    else:
        dtf = dtf[dtf['Weekday'] == day.title()]

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

    return dtf


def time_stats(dtf):
    """Display statistics on the most frequent times of travel."""

    print('\nDisplaying the statistics on the most frequent times of '
          'travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = dtf['Month'].mode()[0]
    print('For the filter, the month with the most travels is: ' +
          str(months[common_month-1]).title() + '.')

    # display the most common day of week
    common_day = dtf['Weekday'].mode()[0]
    print('For the filter, the most common day of the week is: ' +
          str(common_day) + '.')

    # display the most common start hour
    common_hour = dtf['Start Hour'].mode()[0]
    print('For the filter, the most common start hour is: ' +
          str(common_hour) + '.')

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def station_stats(dtf):
    """Display statistics on the most popular stations and trip."""

    print('\nPopular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = str(dtf['Start Station'].mode()[0])
    print("For the filters, the most common start station is: " +
          common_start_station)

    # display most commonly used end station
    common_end_station = str(dtf['End Station'].mode()[0])
    print("For the filters, the most common start end is: " +
          common_end_station)

    # display most frequent combination of start station and
    # end station trip
    dtf['Start-End Combination'] = (dtf['Start Station'] + ' - ' +
                                   dtf['End Station'])
    common_start_end_combination = str(dtf['Start-End Combination']
                                            .mode()[0])
    print("For the filters, the most common start-end combination "
          "of stations is: " + common_start_end_combination)

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def trip_duration_stats(dtf):
    """Display statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = dtf['Trip Duration'].sum()
    total_travel = (str(int(total_travel//86400)) +
                         'd ' +
                         str(int((total_travel % 86400)//3600)) +
                         'h ' +
                         str(int(((total_travel % 86400) % 3600)//60)) +
                         'm ' +
                         str(int(((total_travel % 86400) % 3600) % 60)) +
                         's')
    print('For the filters, the total travel time is : ' +
          total_travel + '.')

    # display mean travel time
    mean_travel = dtf['Trip Duration'].mean()
    mean_travel = (str(int(mean_travel//60)) + 'm ' +
                        str(int(mean_travel % 60)) + 's')
    print("For the filters, the mean travel time is : " +
          mean_travel + ".")

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def user_stats(dtf, city):
    """Display statistics on bikeshare users."""

    print('\nCalculating User Statistics...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = dtf['User Type'].value_counts().to_string()
    print("Distribution for user types:")
    print(user_types)

    # Display counts of gender
    try:
        gender_dist = dtf['Gender'].value_counts().to_string()
        print("\nThe Distribution for each gender:")
        print(gender_dist)
    except KeyError:
        print("Sorry! There is no data of user genders for {}."
              .format(city.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        latest_birth_year = str(int(dtf['Birth Year'].min()))
        print("\nThe filter selected, the oldest individual to ride one "
              "bike was born in: " + latest_birth_year)
        recent_birth_year = str(int(dtf['Birth Year'].max()))
        print("The filter selected, the youngest individual to ride one "
              "bike was born in: " + recent_birth_year)
        common_birth_year = str(int(dtf['Birth Year'].mode()[0]))
        print("For the selected filter, the common birth year amongst "
              "riders is: " + common_birth_year)
    except:
        print("Sorry! There is no data of birth year for {}."
              .format(city.title()))

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def raw_data(dtf, mark_place):
    """Display 5 line of sorted raw data each time."""

    print("\nYou want to view raw data.")

    # this variable holds where the user last stopped
    if mark_place > 0:
        cont_place = choice("\nDo you wish to continue from where you "
                            "stopped last time? \n [y] Yes\n [n] No\n\n>")
        if cont_place == 'n':
            mark_place = 0

    # sort data by column
    if mark_place == 0:
        sort_data = choice("\nWhat way will you like the sort data "
                         "displayed in the frame? Press Enter to view "
                         "unsorted.\n \n [st] Start Time\n [et] End Time\n "
                         "[td] Trip Duration\n [ss] Start Station\n "
                         "[es] End Station\n\n>",
                         ('st', 'et', 'td', 'ss', 'es', ''))

        asc_or_desc = choice("\nWill you like it to be sorted in ascending or "
                             "descending? \n [as] Ascending\n [ds] Descending"
                             "\n\n>",
                             ('as', 'ds'))

        if asc_or_desc == 'as':
            asc_or_desc = True
        elif asc_or_desc == 'ds':
            asc_or_desc = False

        if sort_data == 'st':
            dtf = dtf.sort_values(['Start Time'], ascending=asc_or_desc)
        elif sort_data == 'et':
            dtf = dtf.sort_values(['End Time'], ascending=asc_or_desc)
        elif sort_data == 'td':
            dtf = dtf.sort_values(['Trip Duration'], ascending=asc_or_desc)
        elif sort_data == 'ss':
            dtf = dtf.sort_values(['Start Station'], ascending=asc_or_desc)
        elif sort_data == 'es':
            dtf = dtf.sort_values(['End Station'], ascending=asc_or_desc)
        elif sort_data == '':
            pass

    # each loop displays 5 lines of raw data
    while True:
        for i in range(mark_place, len(dtf.index)):
            print("\n")
            print(dtf.iloc[mark_place:mark_place+5].to_string())
            print("\n")
            mark_place += 5

            if choice("Do you wish to keep printing raw data?"
                      "\n\n[y]Yes\n[n]No\n\n>") == 'y':
                continue
            else:
                break
        break

    return mark_place


def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        dtf = load_data(city, month, day)

        mark_place = 0
        while True:
            select_info = choice("\nPlease select the information you will "
                                 "like to retrieve.\n\n [ts] Time Statistics\n [ss] "
                                 "Station Statistics\n [tds] Trip Duration Statistics\n "
                                 "[us] User Statistics\n [rd] Display Raw Data\n "
                                 "[r] Restart\n\n>",
                                 ('ts', 'ss', 'tds', 'us', 'rd', 'r'))
            click.clear()
            if select_info == 'ts':
                time_stats(dtf)
            elif select_info == 'ss':
                station_stats(dtf)
            elif select_info == 'tds':
                trip_duration_stats(dtf)
            elif select_info == 'us':
                user_stats(dtf, city)
            elif select_info == 'rd':
                mark_place = raw_data(dtf, mark_place)
            elif select_info == 'r':
                break

        restart = choice("\nWill you like to restart?\n\n[y]Yes\n[n]No\n\n>")
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
