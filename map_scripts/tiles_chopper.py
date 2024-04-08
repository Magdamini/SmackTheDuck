import os
from PIL import Image

TILE_WIDTH = 16
TILE_HEIGHT = 16

def crop_tiles(image_path, output_directory):
    image = Image.open(image_path)
    image_width, image_height = image.size

    num_tiles_x = image_width // TILE_WIDTH
    num_tiles_y = image_height // TILE_HEIGHT

    i=-1
    for y in range(2):
        for x in range(2):
            left = x * TILE_WIDTH
            upper = y * TILE_HEIGHT
            right = left + TILE_WIDTH
            lower = upper + TILE_HEIGHT
            i += 1

            tile = image.crop((left, upper, right, lower))
            tile.save(os.path.join(output_directory ,f"0{i}.png"))


image_path = "C:/Users/Admin/PyGame_project/Python_Project_Pabisz_Smyka/data/images/tiles/HouseIndoor/01.png"
output_directory = "C:/Users/Admin/PyGame_project/Python_Project_Pabisz_Smyka/data/images/tiles/HouseIndoor/01111"
crop_tiles(image_path, output_directory)
