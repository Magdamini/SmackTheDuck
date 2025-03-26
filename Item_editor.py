import sys

import pygame
import json

from scripts.utils import load_images, load_image, load_json
from scripts.tilemap import Tilemap
import scripts.items as items

RENDER_SCALE = 2.0
MOUSE_LEFT_BUTTON = 1
MOUSE_RIGHT_BUTTON = 3
MOUSE_SCROLL_UP = 4
MOUSE_SCROLL_DOWN = 5

ITEM_TYPES = {
    "00": items.Plaster,
    "01": items.Bandage,
    "02": items.MedicalKit,
    "03": items.DuckLeg,
    "04": items.RawMeat,
    "05": items.Shoes,
    "06": items.Jacket,
    "07": items.Blood,
    "09": items.SmallAggressionPotion,
    "10": items.AggressionPotion,
    "11": items.Flowers,
    "12": items.Clover,
    "13": items.Stones,
    "14": items.Letter,
    "15": items.SmallAgilityPotion,
    "16": items.AgilityPotion,
}


it_list = list(ITEM_TYPES.keys())

map_list = ["0", "1", "2", "3", "4", "4a", "5", "5a"]


class ItemEditor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Place items")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.images = {
            "00": load_image("tiles/Items/00.png"),
            "01": load_image("tiles/Items/01.png"),
            "02": load_image("tiles/Items/02.png"),
            "03": load_image("tiles/Items/03.png"),
            "04": load_image("tiles/Items/04.png"),
            "05": load_image("tiles/Items/05.png"),
            "06": load_image("tiles/Items/06.png"),
            "07": load_image("tiles/Items/07.png"),
            "08": load_image("tiles/Items/08.png"),
            "09": load_image("tiles/Items/09.png"),
            "10": load_image("tiles/Items/10.png"),
            "11": load_image("tiles/Items/11.png"),
            "12": load_image("tiles/Items/12.png"),
            "13": load_image("tiles/Items/13.png"),
            "14": load_image("tiles/Items/14.png"),
            "15": load_image("tiles/Items/15.png"),
            "16": load_image("tiles/Items/16.png"),
        }

        self.assets = {
            "Cave": load_images("tiles/Cave"),
            "CaveOutside": load_images("tiles/CaveOutside"),
            "CaveOutside00": load_images("tiles/CaveOutside/00"),
            "CaveOutside01": load_images("tiles/CaveOutside/01"),
            "CaveOutside02": load_images("tiles/CaveOutside/02"),
            "GrassFloor": load_images("tiles/GrassFloor"),
            "GrassGoose": load_images("tiles/GrassGoose"),
            "GrassTrees": load_images("tiles/GrassTrees"),
            "GrassTrees00": load_images("tiles/GrassTrees/00"),
            "GrassTrees01": load_images("tiles/GrassTrees/01"),
            "GrassBuildings": load_images("tiles/GrassBuildings"),
            "GrassBuildings00": load_images("tiles/GrassBuildings/00"),
            "GrassBuildings01": load_images("tiles/GrassBuildings/01"),
            "GrassBuildings02": load_images("tiles/GrassBuildings/02"),
            "GrassBuildings03": load_images("tiles/GrassBuildings/03"),
            "GrassBuildings04": load_images("tiles/GrassBuildings/04"),
            "GrassBushes": load_images("tiles/GrassBushes"),
            "GrassDecor": load_images("tiles/GrassDecor"),
            "GrassDecor00": load_images("tiles/GrassDecor/00"),
            "GrassDecor02": load_images("tiles/GrassDecor/02"),
            "GrassDecor03": load_images("tiles/GrassDecor/03"),
            "GrassIndoorDecor": load_images("tiles/GrassIndoorDecor"),
            "GrassIndoorDecor05": load_images("tiles/GrassIndoorDecor/05"),
            "GrassIndoorDecor06": load_images("tiles/GrassIndoorDecor/06"),
            "GrassIndoorDecor07": load_images("tiles/GrassIndoorDecor/07"),
            "GrassIndoorDecor08": load_images("tiles/GrassIndoorDecor/08"),
            "WaterFloor": load_images("tiles/WaterFloor"),
            "WaterCatwalk": load_images("tiles/WaterCatwalk"),
            "HouseFloor": load_images("tiles/HouseFloor"),
            "HouseIndoor": load_images("tiles/HouseIndoor"),
            "HouseIndoor00": load_images("tiles/HouseIndoor/00"),
            "HouseIndoor01": load_images("tiles/HouseIndoor/01"),
            "Items": load_images("tiles/Items"),
        }

        self.maps = {}
        for i in range(6):
            self.maps[str(i)] = Tilemap(self)
            self.maps[str(i)].load(f"data/maps/{i}.json")
        self.maps["5a"] = Tilemap(self)
        self.maps["5a"].load("data/maps/5a.json")
        self.maps["4a"] = Tilemap(self)
        self.maps["4a"].load("data/maps/4a.json")

        self.tilemap = self.maps["0"]
        self.curr_img = 0
        self.curr_map = 0
        self.load_items()

        self.scroll = [0, 0]
        self.movement = [False, False, False, False]

        self.clicking = False
        self.right_clicking = False
        self.shift = False

    def mouse_button_down(self, event):
        if event.button == MOUSE_LEFT_BUTTON:
            self.clicking = True
        if event.button == MOUSE_RIGHT_BUTTON:
            self.right_clicking = True

        if self.shift:
            if event.button == MOUSE_SCROLL_UP:
                self.curr_map = (self.curr_map - 1) % len(map_list)
            if event.button == MOUSE_SCROLL_DOWN:
                self.curr_map = (self.curr_map + 1) % len(map_list)
            self.tilemap = self.maps[map_list[self.curr_map]]
            self.scroll = [0, 0]

        else:
            if event.button == MOUSE_SCROLL_UP:
                self.curr_img = (self.curr_img - 1) % len(it_list)
            if event.button == MOUSE_SCROLL_DOWN:
                self.curr_img = (self.curr_img + 1) % len(it_list)

    def mouse_button_up(self, event):
        if event.button == MOUSE_LEFT_BUTTON:
            self.clicking = False
        if event.button == MOUSE_RIGHT_BUTTON:
            self.right_clicking = False

    def key_down(self, event):
        if event.key == pygame.K_a:
            self.movement[0] = True
        if event.key == pygame.K_d:
            self.movement[1] = True
        if event.key == pygame.K_w:
            self.movement[2] = True
        if event.key == pygame.K_s:
            self.movement[3] = True
        if event.key == pygame.K_o:  # o = output
            self.save()
        if event.key == pygame.K_LSHIFT:
            self.shift = True

    def key_up(self, event):
        if event.key == pygame.K_a:
            self.movement[0] = False
        if event.key == pygame.K_d:
            self.movement[1] = False
        if event.key == pygame.K_w:
            self.movement[2] = False
        if event.key == pygame.K_s:
            self.movement[3] = False
        if event.key == pygame.K_LSHIFT:
            self.shift = False

    def run(self):
        while True:
            self.display.fill(
                (
                    self.tilemap.tilemap["background_color"]["R"],
                    self.tilemap.tilemap["background_color"]["G"],
                    self.tilemap.tilemap["background_color"]["B"],
                )
            )

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 4
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 4
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.images[it_list[self.curr_img]].copy()
            current_tile_img.set_alpha(100)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (
                int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size),
                int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size),
            )

            self.display.blit(
                current_tile_img,
                (
                    tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                    tile_pos[1] * self.tilemap.tile_size - self.scroll[1],
                ),
            )

            if self.clicking:
                self.place_item(tile_pos)
            if self.right_clicking:
                self.del_item(tile_pos)

            self.display.blit(current_tile_img, (5, 26))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    q = input("Do you want leave? (SAVE FILE FIRST) ")
                    if q == "y":
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_button_down(event)

                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_button_up(event)

                if event.type == pygame.KEYDOWN:
                    self.key_down(event)

                if event.type == pygame.KEYUP:
                    self.key_up(event)

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)

    def place_item(self, pos):
        self.tilemap.add_item(ITEM_TYPES[it_list[self.curr_img]], pos[0], pos[1])

    def del_item(self, pos):
        try:
            self.tilemap.get_item(pos[0], pos[1])
        except:
            pass

    def save(self):
        path = "data/maps/items.json"
        it_dict = {}
        for m in map_list:
            map_dict = {}
            for item in self.maps[m].items.values():
                x, y = (
                    item.x // self.maps["0"].tile_size,
                    item.y // self.maps["0"].tile_size,
                )
                map_dict[str(x) + ";" + str(y)] = {
                    "x": x,
                    "y": y,
                    "type": item.img_name,
                }
            it_dict[m] = map_dict

        file = open(path, "w")
        json.dump(it_dict, file)
        file.close()
        print("File saved sucesfully!")

    def load_items(self):
        items_data = load_json("data/maps/items.json")
        for key in items_data:
            for values in items_data[key].values():
                x = values["x"]
                y = values["y"]
                item_type = ITEM_TYPES[values["type"]]
                self.maps[key].add_item(item_type, x, y)


ItemEditor().run()
