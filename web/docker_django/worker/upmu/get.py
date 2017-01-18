import btrdb
import datetime
import numpy
import uuid
import pytz
import pandas
import argparse
import pdb


def convert_datetime_to_epoch_ns(dt):
    #converts the datetime object to epoch time in nanoseconds
    return (int(dt.strftime('%s')) * 1e6 + dt.microsecond) * 1e3


def get_upmu_data(dates, PMU_name):
    """Retrieves instantaneous P, Q, and voltage magnitude for specified datetime.

    Args:
        dates (datetime): list of datetime objects
        PMU_name (str): e.g., 'grizzly_bus1'
    Returns:
        {'P_A': , 'Q_A': , 'P_B': , 'Q_B': , 'P_C': , 'Q_C': ,
         'units': ('kW', 'kVAR'),
         'VMag_A': , 'VMag_B': , 'VMag_C': }
    """

    # Change all the dates into epoch time in nanoseconds
    event_times = []
    for value in dates:
        event_times.append(convert_datetime_to_epoch_ns(value))

    # Get the ids of the parameters to retrieve (each id is location and measure type unique)
    path = "CyDER/web/docker_django/worker/upmu/"
    ids = str(numpy.genfromtxt(path + PMU_name + '_uuids.txt', dtype='str')).split(',')
    ids = [uuid.UUID(value) for value in ids]
    names = ["L1Mag", "L2Mag", "L3Mag", "C1Mag", "C2Mag", "C3Mag",
            "L1Ang", "L2Ang", "L3Ang", "C1Ang", "C2Ang", "C3Ang"]

    # Create the frame holding the results
    frame = pandas.DataFrame(index=event_times, columns=names)

    # Query the values
    for value_time in event_times:
        for value_id in ids:
            results = connection.queryNearestValue(value_id, value_time, True, version=0)
            pdb.set_trace()


    df_full['P_A'] = (df_full['L1Mag']*df_full['C1Mag']*np.cos(np.radians(df_full['L1Ang'] - df_full['C1Ang'])))*1e-3
    df_full['Q_A'] = (df_full['L1Mag']*df_full['C1Mag']*np.sin(np.radians(df_full['L1Ang'] - df_full['C1Ang'])))*1e-3

    df_full['P_B'] = (df_full['L2Mag']*df_full['C2Mag']*np.cos(np.radians(df_full['L2Ang'] - df_full['C2Ang'])))*1e-3
    df_full['Q_B'] = (df_full['L2Mag']*df_full['C2Mag']*np.sin(np.radians(df_full['L2Ang'] - df_full['C2Ang'])))*1e-3

    df_full['P_C'] = (df_full['L3Mag']*df_full['C3Mag']*np.cos(np.radians(df_full['L3Ang'] - df_full['C3Ang'])))*1e-3
    df_full['Q_C'] = (df_full['L3Mag']*df_full['C3Mag']*np.sin(np.radians(df_full['L3Ang'] - df_full['C3Ang'])))*1e-3

    return df_full


connection = btrdb.BTrDBConnection("miranda.cs.berkeley.edu", 4410)
context = connection.newContext()

western = pytz.timezone('America/Los_Angeles')
time_period = western.localize(datetime(2016,11,1,12,0,0))

print("Retrieving data...")
upmudata = get_upmu_data([time_period], 'grizzly_bus1')
print(upmudata)


# # Retrieve model name
# try:
#     parser = argparse.ArgumentParser(description='Select dates and location')
#     parser.add_argument('date_from')
#     parser.add_argument('date_to')
#     # parser.add_argument('location')
#     args = parser.parse_args()
#     date_from = str(args.date_from)
#     date_to = str(args.date_to)
#     # location = str(args.location)
# except:
#     sys.exit('Error: could not retrieve argument')
#
# # Create datetimes every minutes
# date_from = d.datetime.strptime(date_from, "%Y-%m-%d_%H:%M:%S")
# if not date_to in "False":
#     date_to = d.datetime.strptime(date_to, "%Y-%m-%d_%H:%M:%S")
#     delta_minutes = int((date_to - date_from).total_seconds() / 60)
#     if delta_minutes < 1:
#         raise Exception('Needs at least a minute between date_to and date_from')
#     dates = [date_from + d.timedelta(minutes=x) for x in range(0, delta_minutes)]
# else:
#     dates = [date_from]
#
# for date in dates:
#     udata = {'date': date.strftime("%Y-%m-%d_%H:%M:%S"),
#              'VMAG_A': 7287.4208984375,
#              'VMAG_B': 7299.921875,
#              'VMAG_C': 7318.2822265625,
#              'P_A': 7272.5364248477308,
#              'P_B': 2118.3817519608633,
#              'P_C': 6719.1867010705246,
#              'Q_A': -284.19075651498088,
#              'Q_B': -7184.1189935099919,
#              'Q_C': 3564.4269660296022,
#              'units': ('kW', 'kVAR', 'V')}
#     print(udata)  # upmu data