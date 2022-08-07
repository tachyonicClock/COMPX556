from PIL import Image, ImageDraw, ImageFont
from random import randint, seed
import click

SCALE = 5
STRIP_WIDTH = 100
STRIP_HEIGHT = 200


def to_screen_coords(x: int, y: int):
    """
    Convert coordinates to screen coordinates.
    scale and flip y-axis.
    """
    y = (STRIP_HEIGHT-int(y))
    return (int(x)*SCALE, y*SCALE)


def rect_to_screen_coords(x: int, y: int, xx: int, yy: int):
    return *to_screen_coords(x, y), *to_screen_coords(xx, yy)


@click.command()
@click.option('--input', '-i', help='Input file', required=True)
@click.option('--output', '-o', help='Output file', required=True)
@click.option('--height', '-h', default=STRIP_HEIGHT, help='Height of the image')
def main(output: str, input: str, height: int):
    # Set global constants
    global STRIP_HEIGHT
    STRIP_HEIGHT = height

    # Setup PIL image and font
    font = ImageFont.load_default()
    img = Image.new('RGB', (STRIP_WIDTH*SCALE, STRIP_HEIGHT*SCALE),
                    color=(255, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    # Read input file
    with open(input, 'r') as f:
        for line in f:
            # Ignore lines starting with #
            if line[0] == "#":
                continue

            # Load rectangle information
            id, left, top, right, bottom = list(map(int, line.split()))
            left, top, right, bottom = rect_to_screen_coords(
                left, top, right, bottom)
            # The seed is set, such that the same rectangle is always drawn in the
            # same colour
            seed(id)

            # Draw rectangle
            draw.rectangle(
                xy=(left, top, right, bottom),
                fill=(randint(0, 255), randint(0, 255), randint(0, 255), 125),
                outline=(100, 100, 100),
                width=SCALE//4
            )

            # Label rectangles
            label = f"{id}"
            # This is used to center the text
            offset = font.getbbox(label)
            bbox_width, bbox_height = offset[2] - offset[0], offset[3] - offset[1]
            draw.text(((left+right-bbox_width)/2, (top+bottom-bbox_height)/2),
                      label, font=font, fill=(0, 0, 0, 255))

    # Draw grid
    for i in range(0, STRIP_WIDTH, 5):
        draw.line(rect_to_screen_coords(
            i, 0, i, STRIP_HEIGHT), fill=(0, 0, 0, 50))
    for i in range(0, STRIP_HEIGHT, 5):
        draw.line(rect_to_screen_coords(
            0, i, STRIP_WIDTH, i), fill=(0, 0, 0, 50))

    img.save(output)


if __name__ == '__main__':
    main()
