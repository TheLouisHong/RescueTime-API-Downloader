from datetime import *
from dateutil.relativedelta import *
from os import environ
from urllib.request import urlretrieve
import pandas as pd
import glob

__author__ = "Louis Hong"
__date__ = "2-13-2021"


def iterate_monthrange(start, end):
    while start < end:
        yield start, start + relativedelta(months=+1) + relativedelta(days=-1)
        start = start + relativedelta(months=+1)


def iterate_rescuetimeapi_url_hourly_bymonth_csv(apikey, start, end):
    """
    Generator for rescuetime api url, for hourly activity per month (maximum allowed time restriction hourly data is
    a single month for rescuetime api).

    Will iterate through month's start date and end date until end date, but not including end date.


    :param apikey: This function requires the apikey from RescueTime (https://www.rescuetime.com/anapi/manage)
    :param start: datetime start date. For example "2019-1-1"
    :param end: datetime end date. For example "2021-1-1"
    :return: yield tuple of data start date, and the url of the https request for the hourly activity, on a month by
    month basis until end is passed, but not including end.
    """
    for start, end in iterate_monthrange(start, end):
        yield start, "https://www.rescuetime.com/anapi/data" \
                     "?key={}&perspective=interval" \
                     "&restrict_kind=activity" \
                     "&interval=hour&restrict_begin={}" \
                     "&restrict_end={}" \
                     "&format=csv".format(apikey, start.strftime("%Y-%m-%d"),
                                          end.strftime("%Y-%m-%d"))


def download_rescuetime_file_hourly_bymonth_csv(apikey, start, end, dry=False):
    """
    Downloader for RescueTime api url, for hourly activity per month (maximum allowed time restriction hourly data is
    a single month for rescuetime api).

    Will iterate through month's start date and end date until end date, but not including end date.

    :param apikey: This function requires the apikey from RescueTime (https://www.rescuetime.com/anapi/manage)
    :param start: datetime start date. For example "2019-1-1"
    :param end: datetime end date. For example "2021-1-1"
    """
    for monthdate, url in iterate_rescuetimeapi_url_hourly_bymonth_csv(apikey, start, end):
        filename = "rescuetime_hourly_bymonth {}.csv".format(monthdate.strftime("%Y-%m"))
        if dry:
            print(url)
            print(filename)
            print()
        else:
            print("Downloading... " + filename)
            urlretrieve(url, filename)


def merge_downloaded_csv(dry=False):
    all_files = [i for i in glob.glob("rescuetime_hourly_bymonth *.csv")]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_files])
    if dry:
        for f in all_files:
            print(f)
    else:
        combined_csv.to_csv("merged.csv")


def download_command(args):
    print("Downloading...")
    download_rescuetime_file_hourly_bymonth_csv(args.apikey,
                                                datetime.strptime(args.start, "%Y-%m-%d"),
                                                datetime.strptime(args.end, "%Y-%m-%d"))
    print("Done!")
    pass


def merge_command(args):
    print("Merging...")
    merge_downloaded_csv(dry=args.dry)
    print("Done! (merged.csv)")


def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="download data from rescuetime.")
    parser.add_argument("--dry", action="store_true")

    command_parser = parser.add_subparsers()

    download_parser = command_parser.add_parser("download")
    download_start_arg = download_parser.add_argument("apikey",
                                                      help="RescueTime API Key from "
                                                           "https://www.rescuetime.com/anapi/manage")
    download_start_arg = download_parser.add_argument("start", help="Start Date")
    download_end_arg = download_parser.add_argument("end", help="End Date")
    download_parser.set_defaults(func=download_command)

    merge_parser = command_parser.add_parser("merge")
    merge_parser.set_defaults(func=merge_command)

    args = parser.parse_args()
    args.func(args)


    # download_rescuetime_file_hourly_bymonth_csv(datetime.strptime("2016-4-1", "%Y-%m-%d"),
    #                                             datetime.strptime("2021-2-1", "%Y-%m-%d"), dry=False)
    # merge_downloaded_csv(True)


if __name__ == '__main__':
    main()
