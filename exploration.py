import pickle
from collections import defaultdict, OrderedDict


# def create_five_week_total(daily_counts):
#     for turnstile, days in daily_counts.items():
#         pass


def combine_turnstiles(daily_counts):
    daily_station_counts = defaultdict(OrderedDict)
    for turnstile, data in daily_counts.items():
        unique = (turnstile[0],turnstile[1],turnstile[3])
        if unique in daily_station_counts:
            existing_data = daily_station_counts.get(unique)
            for day in data:
                existing_data[day[0]] = existing_data.get(day[0], 0) + day[1]
        else:
            temp_d = OrderedDict()
            for day in sorted(data):
                temp_d[day[0]] = day[1]
            daily_station_counts[unique] = temp_d
    return daily_station_counts

def check_zero_entries(d):
    zero_count = 0
    tot_count = 0
    for key in d.keys():
        for day in d[key]:
            if day[1][0] == 0: zero_count += 1
            tot_count += 1
    print 'There are %d data points with zero entries.' % zero_count
    print 'There are %d data points total' % tot_count
    print 'This represents %.9f of the data' % (zero_count//tot_count)


def main():
    # Load dictionary of daily number of entries by turnstile
    with open('daily_entry_mta_mod.pickle', 'rb') as handle:
        daily_counts = pickle.load(handle)

    pickle_check = {k: daily_counts[k] for k in daily_counts.keys()}
    # print pickle_check
    check_zero_entries(pickle_check)


    # daily_station_counts = combine_turnstiles(daily_counts)
    # small_print = {k: daily_station_counts[k] for k in daily_station_counts.keys()[:5]}
    #print(small_print)

    # create_five_week_total(daily_counts)

if __name__ == '__main__':
    main()
