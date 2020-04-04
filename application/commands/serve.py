"""Module for serving an API."""

from io import BytesIO

from flask import Flask, abort, jsonify, request, send_file

from application.visualizations import warming_stripes
from application.utilities.io import read_normalized_data

def serve(options):
    """Serve weather data as an API."""

    # Create a Flask application
    app = Flask(__name__)

    # Load normalized data to keep it in memory for faster access
    normalized_data = read_normalized_data(options.input)

    @app.route("/")
    def index():
        """Return the index page of the website."""
        return send_file("../www/index.html")

    @app.route("/data")
    def data():
        """Return the normalized data currently in use."""
        # Create a base JSON result
        json_result = {
            "entries": []
        }

        # Convert all entries to JSON
        for (timestamp, temperature) in normalized_data:
            json_entry = {
                "timestamp": str(timestamp),
                "temperature": temperature
            }
            json_result["entries"].append(json_entry)

        return jsonify(json_result)

    @app.route("/visualization/warming-stripes")
    def visualization_warming_stripes():
        """Return a warming stripe visualization."""
        try:
            # Get the size parameters from the request
            width = int(request.args.get("width"))
            height = int(request.args.get("height"))
        except (TypeError, ValueError):
            # Abort the request if the parameters were not given
            abort(400, "Missing or invalid parameters. Expected \"width\" and \"height\" to be set.")

        # Create the visualization image
        image = warming_stripes.create_visualization(normalized_data, (width, height))

        # Save the image to a buffer
        image_buffer = BytesIO()
        image.save(image_buffer, 'PNG')
        image_buffer.seek(0)

        # Return the image to the client
        return send_file(image_buffer, mimetype='image/png')

    app.run(host=options.address, port=options.port, debug=True)

def create_parser(subparsers):
    """Create an argument parser for the "serve" command."""
    parser = subparsers.add_parser("serve")
    parser.set_defaults(command=serve)
    # Add a required parameter for controlling the weather data to serve
    parser.add_argument("-i", "--input", required=True, help="Path to the normalized weather data to serve")
    # Add optional parameters to control the server configuration
    parser.add_argument("-p", "--port", default=8080, type=int, help="The port to listen on")
    parser.add_argument("--address", default="0.0.0.0", help="The address to listen on")
