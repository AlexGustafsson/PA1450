import csv
from argparse import FileType
from statistics import mean
from datetime import datetime

from  application.visualizations import warming_stripes
from application.institutes.smhi import SMHI

def average_months(normalized_data, months):
    """Average the normalized data for the given number of months."""
    # A dictionary over each month
    absolute_months = {}
    timestamps = [timestamp for (timestamp, _) in normalized_data]
    start = min(timestamps)

    for (timestamp, temperature) in normalized_data:
        absolute_month = (timestamp.year - start.year) * 12 + timestamp.month - start.month - 1
        # Create an entry for the month if it does not already exist
        if absolute_month not in absolute_months:
            absolute_months[absolute_month] = []

        # Add the temperature to the year
        absolute_months[absolute_month].append(temperature)

    # Create a list following the same format as the normalized data
    averaged_months = []
    for (absolute_month, temperatures) in absolute_months.items():
        # Create a timestamp for the first day of each month
        year = start.year + (absolute_month + 1) // 12
        month = (absolute_month + start.month) % 12 + 1
        timestamp = datetime(year, month, 1)
        average = mean(temperatures)
        averaged_months.append((timestamp, average))

    # Reduce the dataset with the average for every given months
    result = []
    for i in range(0, len(averaged_months), months):
        # Pick months number of entries from the full list
        month_set = averaged_months[i:i + months]
        # Extract the temperatures from the set
        temperatures = [temperature for (_, temperature) in month_set]
        # Use the first date of the set as the date for the calculated average
        date = month_set[0][0]
        result.append((date, mean(temperatures)))

    return result

def visualize(options):
    """Visualize weather data."""
    normalized_data = []
    with open(options.input, 'r') as input_file:
        reader = csv.reader(input_file, delimiter=',')
        for row in reader:
            date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            temperature = float(row[1])
            normalized_data.append((date, temperature))

    if options.months is not None:
        normalized_data = average_months(normalized_data, options.months)

    if options.visualization == "warming_stripes":
        image = warming_stripes.create_visualization(normalized_data, (options.width, options.height))
        image.save(options.output, "PNG")

def create_parser(subparsers):
    """Create an argument parser for the "visualize" command."""
    parser = subparsers.add_parser("visualize")
    parser.set_defaults(command=visualize)
    # Add a required parameter, "visualization" which can be the name of any implemented visualization
    parser.add_argument("--visualization", required=True, choices=["warming_stripes"], help="The name of the visualization to use, such as \"barcode\"")
    # Add a required parameter, "input" which specifies the input CSV file
    parser.add_argument("-i", "--input", required=True, help="Input CSV file")
    # Add an optional parameter, "output" which specifies the path of the output image
    parser.add_argument("-o", "--output", help="Directory in which to place the downloaded files")
    # Add an optional parameter, "months" which specifies the number of months to group in averages
    parser.add_argument("--months", type=int, help="Number of months to group together and use as average")
    # Add optional parameters to control the size of the image
    parser.add_argument("--width", default=1024, type=int, help="Width of the resulting image")
    parser.add_argument("--height", default=720, type=int, help="Height of the resulting image")
