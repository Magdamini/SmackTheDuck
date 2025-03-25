import sys

import pygame

from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0
MOUSE_LEFT_BUTTON = 1
MOUSE_RIGHT_BUTTON = 3
MOUSE_SCROLL_UP = 4
MOUSE_SCROLL_DOWN = 5


class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Editor")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

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

        # self.assets TODO (better)

        self.movement = [False, False, False, False]

        self.tilemap = Tilemap(self, tile_size=16)

        try:
            self.tilemap.load("map.json")
        except FileNotFoundError:
            pass

        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.background_color_list = [
            (0, 0, 0),
            (114, 221, 239),
            (175, 188, 57),
            (136, 84, 71),
        ]
        self.tile_group = 0
        self.tile_variant = 0
        if self.tilemap.tilemap:
            self.background_color = self.background_color_list.index(
                (
                    self.tilemap.tilemap["background_color"]["R"],
                    self.tilemap.tilemap["background_color"]["G"],
                    self.tilemap.tilemap["background_color"]["B"],
                )
            )
        else:
            self.background_color = 0

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
                self.tile_variant = (self.tile_variant - 1) % len(
                    self.assets[self.tile_list[self.tile_group]]
                )
            if event.button == MOUSE_SCROLL_DOWN:
                self.tile_variant = (self.tile_variant + 1) % len(
                    self.assets[self.tile_list[self.tile_group]]
                )
        else:
            if event.button == MOUSE_SCROLL_UP:
                self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                self.tile_variant = 0
            if event.button == MOUSE_SCROLL_DOWN:
                self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                self.tile_variant = 0

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
        if event.key == pygame.K_p:
            self.background_color = (self.background_color + 1) % len(
                self.background_color_list
            )
        if event.key == pygame.K_o:  # o = output
            self.tilemap.save("map.json")
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
            self.display.fill(self.background_color_list[self.background_color])

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 4
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 4
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][
                self.tile_variant
            ].copy()
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
                self.tilemap.tilemap[str(tile_pos[0]) + ";" + str(tile_pos[1])] = {
                    "type": self.tile_list[self.tile_group],
                    "variant": self.tile_variant,
                    "pos": tile_pos,
                }
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ";" + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]

            self.tilemap.tilemap["background_color"] = {
                "R": self.background_color_list[self.background_color][0],
                "G": self.background_color_list[self.background_color][1],
                "B": self.background_color_list[self.background_color][2],
            }

            pygame.draw.rect(self.display, (255, 255, 255), (5, 5, 16, 16))
            pygame.draw.rect(
                self.display,
                self.background_color_list[self.background_color],
                (6, 6, 14, 14),
            )
            self.display.blit(current_tile_img, (5, 26))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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


Editor().run()
