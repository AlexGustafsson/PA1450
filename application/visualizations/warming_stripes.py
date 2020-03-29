"""Warming stripes visualization module. See https://en.wikipedia.org/wiki/Warming_stripes."""

from math import floor

from PIL import Image, ImageDraw

# The color map is taken from the following site:
# https://matplotlib.org/matplotblog/posts/warming-stripes/
COLOR_MAP = [
    '#08306b', '#08519c', '#2171b5', '#4292c6',
    '#6baed6', '#9ecae1', '#c6dbef', '#deebf7',
    '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a',
    '#ef3b2c', '#cb181d', '#a50f15', '#67000d',
]

def create_visualization(normalized_data, image_size):
    """Create a barcode visualization from normalized_data."""
    image = Image.new("RGB", (len(normalized_data), image_size[1]))
    draw = ImageDraw.Draw(image)

    # Calculate the mean temperature in the dataset
    temperatures = [temperature for (_, temperature) in normalized_data]
    minimum = min(temperatures)
    maximum = max(temperatures)

    for i, (_, temperature) in enumerate(normalized_data):
        # Calculate color of the stripe
        scale = (len(COLOR_MAP) - 1) / (maximum - minimum)
        temperature_index = floor((temperature - minimum) * scale)
        color = COLOR_MAP[temperature_index]

        # Draw a stripe
        lower_left = (i, 0)
        upper_right = ((i + 1), image.height)
        draw.rectangle([lower_left, upper_right], fill=color)

    # Scale the width of the image to fit the wanted size
    image = image.resize(image_size, Image.NEAREST)

    return image
