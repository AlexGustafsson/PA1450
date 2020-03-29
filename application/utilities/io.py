"""IO utilities."""

import csv
from datetime import datetime

def read_normalized_data(path):
    """Read normalized data from a file."""
    normalized_data = []
    with open(path, 'r') as input_file:
        reader = csv.reader(input_file, delimiter=',')
        for row in reader:
            date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            temperature = float(row[1])
            normalized_data.append((date, temperature))

    return normalized_data
