import pickle
from collections import defaultdict, OrderedDict
import pandas



def combine_turnstiles(daily_counts):
    """
    Combines entry and exit counts across SCP key.
    :param daily_counts: dictionary {(C/A, UNIT, SCP, STATION): [[day, entries, exits],...]}
    :return: dictionary {(C/A, UNIT, STATION): [[day, entries, exits],...]}
    """
    daily_station_counts = defaultdict(OrderedDict)
    for turnstile, data in daily_counts.items():
        unique = (turnstile[0],turnstile[1],turnstile[3])
        if unique in daily_station_counts:
            existing_data = daily_station_counts.get(unique)
            for day in data:
                # print existing_data[day[0]]
                existing_data[day[0]] = existing_data.get(day[0], 0) + day[1][0] + day[1][1]
        else:
            temp_d = OrderedDict()
            for day in sorted(data):
                temp_d[day[0]] = [day[1][0], day[1][1]]
            daily_station_counts[unique] = temp_d
    return daily_station_counts


def combine_stations(daily_counts):
    """
    Combines entry and exit counts across STATION key.
    :param daily_counts: dictionary {(C/A, UNIT, STATION): [[day, entries, exits],...]}
    :return: dictionary {(STATION): [[day, entries, exits],...]}
    """
    daily_station_counts = defaultdict(dict)
    for turnstile, data in daily_counts.items():
        unique = turnstile[3]
        if unique in daily_station_counts:
            existing_data = daily_station_counts.get(unique)
            for day in data:
                existing_data[day[0]] = existing_data.get(day[0], 0) + day[1][0] + day[1][1]
        else:
            temp_d = OrderedDict()
            for day in sorted(data):
                temp_d[day[0]] = day[1][0] + day[1][1]
            daily_station_counts[unique] = temp_d
    return daily_station_counts


def create_five_week_total(daily_counts):
    five_week_counts_dict = {}
    for station, day_dict in daily_counts.items():
        for day, counts in day_dict.items():
            five_week_counts_dict[station] = five_week_counts_dict.get(station, 0) + counts[0] + counts[1]
    return five_week_counts_dict


def check_zero_entries(d):
    """
    Checks how many entry data points are equal to zero.
    :param d: dictionary
    :return: None
    """
    zero_entry_count = 0
    zero_exit_count = 0
    tot_entry_count = 0
    tot_exit_count = 0
    for key, value in d.items():
        for key2, value2 in value.items():
            if value2[0] == 0: zero_entry_count += 1
            if value2[1] == 0: zero_exit_count += 1
            tot_entry_count += 1
            tot_exit_count += 1

    print 'There are %d data points with zero entries.' % zero_entry_count
    print 'There are %d entry data points total.' % tot_entry_count
    print 'There are %d data points with zero exits.' % zero_exit_count
    print 'There are %d exit data points total.' % tot_exit_count


def print_small_dict(d, n):
    """
    Print n keys from the dictionary d.
    :param d: dictionary
    :param n: int
    :return: None
    """
    small = {k: d[k] for k in d.keys()[:n]}
    print small


def load_into_df(d):
    """
    Loads dictionary into pandas dataframe.
    :param d: dictionary
    :return:
    """
    df = pandas.DataFrame(d)
    print df.head()


def main():
    # Load dictionary of daily number of entries by turnstile
    with open('daily_entry_final.pickle', 'rb') as handle:
        daily_counts = pickle.load(handle)

    # Testing
    # print_small_dict(daily_counts, 2)
    # check_zero_entries(pickle_check)

    # daily_turnstile_counts = combine_turnstiles(daily_counts)
    # print_small_dict(daily_station_counts, 5)

    daily_station_counts = combine_stations(daily_counts)
    # print_small_dict(daily_station_counts, 2)
    # check_zero_entries(daily_station_counts)

    # five_week_counts_dict = create_five_week_total(daily_station_counts)
    # print_small_dict(five_week_counts_dict, 10)

    with open('daily_station_counts.pickle','wb') as handle:
        pickle.dump(daily_station_counts, handle)

    load_into_df(daily_station_counts)


if __name__ == '__main__':
    main()
