"""SMHI institute module."""

import csv
from datetime import datetime
from itertools import islice
from io import StringIO

import requests

SMHI_API_ENDPOINT = "https://opendata-download.smhi.se/stream"

class SMHI():
    """SMHI API helper class."""

    @staticmethod
    def download(station_id, period):
        """Download data for a given station and period."""
        parameters = {
            "type": "metobs",
            "parameterIds": 1,
            "stationId": station_id,
            "period": period
        }

        request = requests.get(SMHI_API_ENDPOINT, params=parameters)
        # Force the request to be encoded in UTF-8
        request.encoding = "utf-8"

        return request.text

    @staticmethod
    def download_corrected_archive(station_id):
        """Download the corrected archive for a specific station."""
        return SMHI.download(station_id, "corrected-archive")

    @staticmethod
    def download_latest_day(station_id):
        """Download data for the past day for a specific station."""
        return SMHI.download(station_id, "latest-day")

    @staticmethod
    def download_latest_hour(station_id):
        """Download data for the past hour for a specific station."""
        return SMHI.download(station_id, "latest-hour")

    @staticmethod
    def download_latest_months(station_id):
        """Download data for the past months for a specific station."""
        return SMHI.download(station_id, "latest-months")

    @staticmethod
    def normalize_row(row):
        """Normalize a single CSV row."""
        timestamp = datetime.strptime("{} {}".format(row[0], row[1]), "%Y-%m-%d %H:%M:%S")
        temperature = float(row[2])
        return (timestamp, temperature)

    @staticmethod
    def normalize(data):
        """Normalize a given CSV data string previously downloaded from this class."""
        # Create a file for the data
        input_file = StringIO(data)
        # Skip the first 10 rows as the only contain header information
        skipped_file = islice(input_file, 10, None)
        # Parse the CSV data
        reader = csv.reader(skipped_file, delimiter=';')
        # Return a normalized list of the data
        non_empty_rows = [row for row in reader if row[0] and row[1]]
        normalized_rows = list(map(SMHI.normalize_row, non_empty_rows))
        # Sort the normalized rows ascending by temperature
        normalized_rows.sort(key=lambda entry: entry[0])
        return normalized_rows
