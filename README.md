# PA1450
### Complete application
***

## Quick Start

You're currently viewing the branch `complete`. This branch contains a complete example project for retrieval and presentation of weather data.

To use the application, you will first need to make sure that your environment supports it. Please see the `virtual-lab-environment` branch for a complete and tested environment for use with this project.

When you're ready to download and start the application, follow these steps:

```shell
# Clone the repository
git clone https://github.com/AlexGustafsson/PA1450
# Enter the repository and checkout this branch
cd PA1450
git checkout complete

# Install dependencies
make install

# Start the application by using the wrapper script
./application.sh
```

To download weather data, you can use the `download` command like so:

```shell
./application.sh download --institute smhi --output ./data
```

This will create the directory structure as needed, download all weather data and normalize it for further use.

To serve the weather data using the built-in development server, use the `serve` command like so:

```shell
./application.sh serve --input data/smhi/normalized-latest-months.csv
```

## Contributing

### Quick Start

First start by downloading the repository:

```shell
# Clone the repository
git clone https://github.com/AlexGustafsson/PA1450
```

You can now enter the directory and install the dependencies:

```shell
# Enter the repository and checkout this branch
cd PA1450
git checkout complete

# Install dependencies
make install
```

You're now ready to develop the application.

### Project structure

The main entrypoint of the application is the `application/main.py` file. It contains the command line argument parser which is in charge of interfacing with the user in order to start the application.

Each available command is located within the `application/commands` directory. Each command file defines a `create_parser` method which sets up the command's command line argument parser.

Logic for each institute such as SMHI is available as a separate module within the `application/institutes` directory. Each module contains a class which is in charge of retrieving and normalizing weather data.

Logic for visualizations is defined as separate modules within the `application/visualizations`. The visualizations define methods for creating in-memory images using normalized data.

Shared utilities, such as utilities revolving around file manipulation are located in the `application/utilities` directory.

Lastly, the `www` directory contains the static web files used for the demonstrational website.
