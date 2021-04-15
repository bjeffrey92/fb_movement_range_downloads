#!/usr/bin/env python3

import argparse
from fb_geoinsights import FbGeoinsights


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download movement range maps data from Facebook Data for Good"  # noqa: E501
    )

    parser.add_argument(
        "--start_date",
        help="Date of earliest day's data to import. Must be in format: YYYY-MM-DD (default = 2021-04-11)",  # noqa: E501
        default="2021-04-11",
        type=str,
    )
    parser.add_argument(
        "--location_name",
        help="Name of location to download data for (default = Addis Ababa)",
        default="Addis Ababa",
        type=str,
    )
    parser.add_argument(
        "--location_id",
        help="ID of location to download data for (default = 642750926308152)",
        default="642750926308152",
        type=str,
    )

    return parser.parse_args()


def main(args):
    fb_downloader = FbGeoinsights()
    fb_downloader.fetch(
        start_date=args.start_date,
        name=args.location_name,
        loc_id=args.location_id,
    )


if __name__ == "__main__":
    main(parse_args())
