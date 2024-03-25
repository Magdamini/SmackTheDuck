import os
from PIL import Image

TILE_WIDTH = 16
TILE_HEIGHT = 16

def crop_tiles(image_path, output_directory):
    image = Image.open(image_path)
    image_width, image_height = image.size

    num_tiles_x = image_width // TILE_WIDTH
    num_tiles_y = image_height // TILE_HEIGHT

    i=0
    for y in range(6, 9):
        for x in range(0, 3):
            left = x * TILE_WIDTH
            upper = y * TILE_HEIGHT
            right = left + TILE_WIDTH
            lower = upper + TILE_HEIGHT
            i += 1

            tile = image.crop((left, upper, right, lower))
            tile.save(os.path.join(output_directory ,f"{i}.png"))

""" GrassFloor""" # y-<12, 13), x-<0, 6)
# image_path = "TilesetFloor.png"
# output_directory = "C:/Users/Admin/PyGame_project/Python_Project_Pabisz_Smyka/data/images/tiles/GrassFloor"
""" Water""" # y-<6, 9), x-<0, 3)
# image_path = "TilesetWater.png"
# output_directory = "C:/Users/Admin/PyGame_project/Python_Project_Pabisz_Smyka/data/images/tiles/Water"
""" Character """
# image_path = "SpriteSheet.png"
# output_directory = "C:/Users/Admin/PyGame_project/Python_Project_Pabisz_Smyka/data/images/character"
""" Trees """
# image_path = ".png"
# output_directory = "C:/Users/Admin/PyGame_project/Python_Project_Pabisz_Smyka/data/images/tiles/Trees"
crop_tiles(image_path, output_directory)
