import numpy as np
from PIL import Image
import math

def dna_to_image(input_file, output_file, image_width=None, image_height=None):
    # Define RGB colors for each nucleotide
    color_map = {
        'A': (255, 0, 0),       # Red
        'T': (0, 255, 0),       # Green
        'C': (0, 0, 255),       # Blue
        'G': (255, 255, 0),     # Yellow
        # You can add more mappings if needed
    }

    # Read DNA sequence from file
    with open(input_file, 'r') as file:
        dna_sequence = file.read().strip().upper()

    # Filter out any non-ATCG characters
    dna_sequence = ''.join(filter(lambda x: x in color_map, dna_sequence))
    total_chars = len(dna_sequence)
    print(f"Total valid nucleotides: {total_chars}")

    # Determine image dimensions
    if image_width and image_height:
        width = image_width
        height = image_height
    elif image_width:
        width = image_width
        height = math.ceil(total_chars / width)
    elif image_height:
        height = image_height
        width = math.ceil(total_chars / height)
    else:
        # Attempt to create a square image
        width = height = math.ceil(math.sqrt(total_chars))

    print(f"Image dimensions: {width}x{height}")

    # Initialize a numpy array for the image
    img_array = np.zeros((height, width, 3), dtype=np.uint8)

    # Map each nucleotide to its color
    for idx, nucleotide in enumerate(dna_sequence):
        row = idx // width
        col = idx % width
        if row >= height:
            break  # In case the last row is incomplete
        img_array[row, col] = color_map.get(nucleotide, (0, 0, 0))  # Default to black

    # Create an image from the array
    img = Image.fromarray(img_array, 'RGB')

    # Save the image as TIFF
    img.save(output_file, format='TIFF')
    print(f"Image saved as {output_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Convert DNA sequence to an image.')
    parser.add_argument('input_file', help='Path to the input TXT file containing DNA sequence.')
    parser.add_argument('output_file', help='Path to the output TIFF image file.')
    parser.add_argument('--width', type=int, help='Width of the output image in pixels.')
    parser.add_argument('--height', type=int, help='Height of the output image in pixels.')

    args = parser.parse_args()

    dna_to_image(args.input_file, args.output_file, args.width, args.height)
