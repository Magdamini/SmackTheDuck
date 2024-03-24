import os
from PIL import Image

TILE_WIDTH = 16
TILE_HEIGHT = 16

def crop_tiles(image_path, output_directory):
    image = Image.open(image_path)
    image_width, image_height = image.size

    num_tiles_x = image_width // TILE_WIDTH
    num_tiles_y = image_height // TILE_HEIGHT

    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            left = x * TILE_WIDTH
            upper = y * TILE_HEIGHT
            right = left + TILE_WIDTH
            lower = upper + TILE_HEIGHT

            tile = image.crop((left, upper, right, lower))
            tile.save(os.path.join(output_directory ,f"tile_{x}_{y}.png"))

image_path = "TilesetFloor.png"
output_directory = "C:/Users/Admin/Studia/PyGame/Python_Project_Pabisz_Smyka/data/images/tiles/TilesetFloor"
crop_tiles(image_path, output_directory)
