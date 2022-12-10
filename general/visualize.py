from PIL import Image, ImageDraw


def visualize_grid(grid, dimensions, colors, background="white", box_size=6.0, flip=True, outline=(128, 128, 128)):
    """
    Visualizes a grid to an image. Colors is a lookup table that contains the colors for each item in the grid.
    """

    height, width = dimensions

    img = Image.new("RGB", (height * box_size, width * box_size), background)

    draw = ImageDraw.Draw(img)

    for y in range(height):
        for x in range(width):
            ch = grid[(y, x)]
            draw.rectangle([(y * box_size, x * box_size), (y * box_size + box_size, x * box_size + box_size)],
                           outline=outline, fill=colors[ch])

    if flip:
        img = img.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)
    return img
