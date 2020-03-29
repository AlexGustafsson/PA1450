import pathlib

from application.institutes.smhi import SMHI

SMHI_KARLSKRONA_STATION_ID = "65090"

def save_file(directory, institute, name, content):
    """Save a file to a specified directory. Creates a directory for the institute if it does not exist."""
    # Create the directory if it does not exist
    pathlib.Path("{}/{}".format(directory, institute)).mkdir(parents=True, exist_ok=True)
    # Save the file
    with open("{}/{}/{}".format(directory, institute, name), 'w') as output_file:
        if isinstance(content, str):
            # If the content is a string, write it immediately
            output_file.write(content)
        elif isinstance(content, list):
            # If the content is a list, write it as CSV
            for row in content:
                timestamp, temperature = row
                output_file.write("{},{}\n".format(str(timestamp), str(temperature)))

def download(options):
    """Download weather data."""
    if options.institute == "all" or options.institute == "smhi":
        # Download and save data for the last hour
        latest_hour = SMHI.download_latest_hour(SMHI_KARLSKRONA_STATION_ID)
        save_file(options.output, "smhi", "latest-hour.csv", latest_hour)
        normalized_lastest_hour = SMHI.normalize(latest_hour)
        save_file(options.output, "smhi", "normalized-latest-hour.csv", normalized_lastest_hour)

        # Download and save data for the last day
        latest_day = SMHI.download_latest_day(SMHI_KARLSKRONA_STATION_ID)
        save_file(options.output, "smhi", "latest-day.csv", latest_day)
        normalized_latest_day = SMHI.normalize(latest_day)
        save_file(options.output, "smhi", "normalized-latest-day.csv", normalized_latest_day)

        # Download and save data for the last months
        latest_months = SMHI.download_latest_months(SMHI_KARLSKRONA_STATION_ID)
        save_file(options.output, "smhi", "latest-months.csv", latest_months)
        normalized_latest_months = SMHI.normalize(latest_months)
        save_file(options.output, "smhi", "normalized-latest-months.csv", normalized_latest_months)

        # Download and save corrected archive data
        corrected_archive = SMHI.download_corrected_archive(SMHI_KARLSKRONA_STATION_ID)
        save_file(options.output, "smhi", "corrected-archive.csv", corrected_archive)
        normalized_corrected_archive = SMHI.normalize(corrected_archive)
        save_file(options.output, "smhi", "normalized-corrected-archive.csv", normalized_corrected_archive)

def create_parser(subparsers):
    """Create an argument parser for the "download" command."""
    parser = subparsers.add_parser("download")
    parser.set_defaults(command=download)
    # Add a required parameter, "institute" which can be the name of any implemented institute
    parser.add_argument("--institute", required=True, choices=["all", "smhi"], help="The name of the institute to download, such as \"SMHI\"")
    # Add an optional parameter, "output" which specifies the directory to place the downloads in
    parser.add_argument("-o", "--output", default="./data", help="Directory in which to place the downloaded files")
