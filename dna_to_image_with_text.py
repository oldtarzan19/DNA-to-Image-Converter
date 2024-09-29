import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math
import os

def dna_to_image_with_text(input_file, output_file, block_size=10, image_width=None, image_height=None, font_path=None, font_size=None):
    """
    Convert a DNA sequence to an image with colored blocks and visible nucleotide characters.

    Parameters:
    - input_file (str): Path to the input TXT file containing DNA sequence.
    - output_file (str): Path to the output TIFF image file.
    - block_size (int): Size of each block representing a nucleotide (in pixels).
    - image_width (int, optional): Width of the output image in blocks.
    - image_height (int, optional): Height of the output image in blocks.
    - font_path (str, optional): Path to the TTF font file to use for characters.
    - font_size (int, optional): Font size for nucleotide characters.
    """

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

    if total_chars == 0:
        print("No valid nucleotides found in the input file.")
        return

    # Determine image dimensions in blocks
    if image_width and image_height:
        width_blocks = image_width
        height_blocks = image_height
    elif image_width:
        width_blocks = image_width
        height_blocks = math.ceil(total_chars / width_blocks)
    elif image_height:
        height_blocks = image_height
        width_blocks = math.ceil(total_chars / height_blocks)
    else:
        # Attempt to create a square image
        width_blocks = height_blocks = math.ceil(math.sqrt(total_chars))

    print(f"Image dimensions (blocks): {width_blocks}x{height_blocks}")

    # Initialize a numpy array for the image
    img_array = np.zeros((height_blocks * block_size, width_blocks * block_size, 3), dtype=np.uint8)

    # Map each nucleotide to its color
    for idx, nucleotide in enumerate(dna_sequence):
        row_block = idx // width_blocks
        col_block = idx % width_blocks
        if row_block >= height_blocks:
            break  # In case the last row is incomplete

        # Define the block's pixel range
        start_y = row_block * block_size
        end_y = start_y + block_size
        start_x = col_block * block_size
        end_x = start_x + block_size

        # Assign the color to the block
        img_array[start_y:end_y, start_x:end_x] = color_map.get(nucleotide, (0, 0, 0))  # Default to black

    # Create an image from the array
    img = Image.fromarray(img_array, 'RGB')

    # Prepare to draw text
    draw = ImageDraw.Draw(img)

    # Load a font
    if font_path and os.path.isfile(font_path):
        try:
            font = ImageFont.truetype(font_path, font_size if font_size else block_size - 2)
        except Exception as e:
            print(f"Error loading font '{font_path}': {e}")
            print("Using default font.")
            font = ImageFont.load_default()
    else:
        # Use a default monospaced font
        try:
            font = ImageFont.truetype("arial.ttf", font_size if font_size else block_size - 2)
        except IOError:
            # Fallback to a basic PIL font if arial is not available
            font = ImageFont.load_default()

    # Choose text color contrasting with background
    # For simplicity, use black or white based on the brightness of the background color
    def get_contrasting_text_color(bg_color):
        # Calculate luminance
        luminance = (0.299 * bg_color[0] + 0.587 * bg_color[1] + 0.114 * bg_color[2])
        return (0, 0, 0) if luminance > 128 else (255, 255, 255)

    # Draw nucleotide characters on each block
    for idx, nucleotide in enumerate(dna_sequence):
        row_block = idx // width_blocks
        col_block = idx % width_blocks
        if row_block >= height_blocks:
            break  # In case the last row is incomplete

        start_y = row_block * block_size
        start_x = col_block * block_size

        # Determine the center position for the text
        text = nucleotide
        text_color = get_contrasting_text_color(color_map.get(nucleotide, (0, 0, 0)))
        text_position = (start_x + block_size//4, start_y + block_size//4)

        # Draw the text
        draw.text(text_position, text, fill=text_color, font=font)

    # Save the image as TIFF
    img.save(output_file, format='TIFF')
    print(f"Image saved as {output_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Convert DNA sequence to an image with visible characters.')
    parser.add_argument('input_file', help='Path to the input TXT file containing DNA sequence.')
    parser.add_argument('output_file', help='Path to the output TIFF image file.')
    parser.add_argument('--width', type=int, help='Width of the output image in blocks.')
    parser.add_argument('--height', type=int, help='Height of the output image in blocks.')
    parser.add_argument('--block_size', type=int, default=10, help='Size of each block representing a nucleotide (default: 10).')
    parser.add_argument('--font_path', type=str, help='Path to the TTF font file to use for characters.')
    parser.add_argument('--font_size', type=int, help='Font size for nucleotide characters.')

    args = parser.parse_args()

    dna_to_image_with_text(
        input_file=args.input_file,
        output_file=args.output_file,
        block_size=args.block_size,
        image_width=args.width,
        image_height=args.height,
        font_path=args.font_path,
        font_size=args.font_size
    )
