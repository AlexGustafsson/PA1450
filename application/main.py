"""Main module of the application"""

from argparse import ArgumentParser

from application.commands import download, visualize

def main():
    """Main method of the application."""
    # Create an argument parser for parsing CLI arguments
    parser = ArgumentParser(description="An application for retrieving and handling weather data")
    # Create collection of subparsers, one for each command such as "download"
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    # Add the parser for each specific command
    download.create_parser(subparsers)
    visualize.create_parser(subparsers)

    # Parse the arguments and execute the chosen command
    options = parser.parse_args()
    options.command(options)

if __name__ == "__main__":
    main()
