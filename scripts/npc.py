import pygame
from scripts.utils import load_image
from scripts.map_handler import ITEM_TYPES
from random import choice
from scripts.fighter_statictics import Stats


class NPC:
    def __init__(self, name, img_name, active_dialogue, dialogue, pos, active_lvls, size=16):
        self.name = name
        self.img = load_image(f"NPC/Basic/{img_name}.png")
        self.active_dialogue = self.load_dialogue(active_dialogue)
        self.dialogue = self.load_dialogue(dialogue)
        self.pos = [int(p) * size for p in pos]
        self.active_lvls = [int(lvl) for lvl in active_lvls]
        self.size = size
        self.active = 1 in self.active_lvls

    
    def render(self, surf, offset=(0,0)):
        surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
    
    def rect(self):
        offset = 3
        rect = pygame.Rect(0, 0, self.size + 2 * offset, self.size + 2 * offset)
        rect.center = (self.pos[0] + self.size // 2, self.pos[1] + self.size // 2)
        return rect
    
    def activate(self, new_lvl):
        if new_lvl in self.active_lvls:
            self.active = True

            
    def load_dialogue(self, d_name):
        if d_name == "n": return None
        with open(f"data/npc/dialogues/{d_name}") as data_file:
            return data_file.readlines()
        
    def get_curr_dialogue(self):
        if self.dialogue is None or self.active:
            return self.active_dialogue
        return self.dialogue

#########################################################################

class NPCManager:
    def __init__(self, data, map_handler):
        self.npc_list = {} # słownik podobny do tego w map handlerze
        for k in ["0", "1", "2", "3", "4", "4a", "5", "5a"]:
            self.npc_list[k] = []
            
        self.load_data(data, map_handler)

    
    def load_data(self, data, map_handler):
        with open(data) as data_file:
            lines = data_file.readlines()
            for line in lines:
                split_data = line.split("-")
                pos = split_data[5].split()
                active_lvls = split_data[6].split()
                map = split_data[4]
                npc = NPC(split_data[0], split_data[1], split_data[2], split_data[3], pos, active_lvls, map_handler.get_curr_map().tile_size)
                self.npc_list[map].append(npc)
                map_handler.maps[map].add_npc(npc)
                
                
    def activate_npc(self, new_lvl):
        vals = list(self.npc_list.values())
        for npc_on_map in vals:
            for npc in npc_on_map:
                npc.activate(new_lvl)
    
    
    def talk_with_npc(self, surf, offset, player, curr_map_name):
        for npc in self.npc_list[curr_map_name]:
            if player.rect().colliderect(npc.rect()):
                text_font = pygame.font.Font("data/fonts/Retro.ttf", size=8)
                talk_text = text_font.render("[T]", True, "black")
                rect = pygame.Rect(0, npc.pos[1] - offset[1], talk_text.get_width(), talk_text.get_height())
                rect.centerx = npc.pos[0] - offset[0] + npc.size // 2

                rect.y += talk_text.get_height() + 4
                surf.blit(talk_text, (rect.x, rect.y))
                return npc
            
            
            
######################################

class DialogueWindow:
    def __init__(self, npc, backpack, animal) -> None:
        self.img_size = 32
        self.img = pygame.transform.scale(npc.img, (self.img_size, self.img_size))
        self.name = npc.name
        self.dialogue = npc.get_curr_dialogue()
        self.npc = npc
        self.backpack = backpack
        self.animal = animal

        self.curr_line = 0
        self.end = False
        self.last_click = True
        self.extra_line = None
        
        # draw
        self.width = 300
        self.height = 180
        self.border_width = 2
        self.border_offset = 10
        self.font_size = 10
        self.line_size = 16
        self.header_height = 40
        self.player_dialogue_height = 80
        
                
                
                
    def render_dialogue(self, surf, scale):
        # header
        background = pygame.Rect(0, 0, self.width, self.height)
        background.center = (surf.get_width() // 2, surf.get_height() // 2)
        pygame.draw.rect(surf, (255, 255, 255), background) 
        pygame.draw.rect(surf, (0, 0, 0),  background, self.border_width)

        
        big_text_font = pygame.font.Font("data/fonts/Retro.ttf", size=16)
        name_text = big_text_font.render(self.name, True, "black")
        surf.blit(name_text, (background.x + self.border_offset, background.y + self.header_height // 2 - name_text.get_height() // 2))
        left = background.x + self.border_offset
        

        big_img = pygame.transform.scale(self.img, (self.img_size, self.img_size))
        surf.blit(big_img, (background.right - self.border_offset - self.img_size,  background.y + self.header_height // 2 - self.img_size // 2))
        
        curr_y = background.y + self.header_height
        
        line_offset = 3
        pygame.draw.line(surf, (0, 0, 0), (background.x + self.border_offset - line_offset, curr_y), (background.right - self.border_offset + line_offset, curr_y))
        
        # line
        line_y = background.bottom - self.player_dialogue_height
        pygame.draw.line(surf, (0, 0, 0), (background.x + self.border_offset - line_offset, line_y), (background.right - self.border_offset + line_offset, line_y))
        
        
        # dialogue line
        self.set_next_line()

            
        curr_y += 8
        curr_y = self.render_npc_text(surf, curr_y, left, self.dialogue[self.curr_line])
        if self.extra_line is not None:
            self.render_npc_text(surf, curr_y, left, self.extra_line)
        self.render_player_text(surf, left, scale, line_y + 8)
        
        
        
        
    def render_npc_text(self, surf, curr_y, left, txt_line):
        lines = txt_line.split("|")
        
        txt = "\n".join(lines)
        text_font = pygame.font.Font("data/fonts/Retro.ttf", self.font_size)
        npc_text = text_font.render(txt, True, 'black')
        surf.blit(npc_text, (left, curr_y))
        return curr_y + npc_text.get_height() + 3
        
        
    def render_player_text(self, surf, left, scale, curr_y):
        options = self.dialogue[self.curr_line + 1][1:].split("/")
        text_font = pygame.font.Font("data/fonts/Retro.ttf", self.font_size)
        next_lines = []
        texts = []
        
        for o in options:
            option = o.split("-")
            lines = option[0].split("|")
            next_line = str(self.curr_line + 3)
            if len(option) > 1:
                next_line = option[-1]
            next_lines.append(next_line.strip())
            
            txt = "\n".join(lines)
            player_text = text_font.render("-" + txt, True, 'black')
            texts.append((player_text, left, curr_y))
            surf.blit(player_text, (left, curr_y))
            curr_y += 3 + player_text.get_height()
        
        pos = [p // scale for p in pygame.mouse.get_pos()]
        
        for i in range(len(texts)):
            txt, x, y = texts[i]
            rect = pygame.Rect(x, y, self.width - 2 * self.border_offset, txt.get_height())
            rect.x = x
            rect.y = y
            
            if rect.collidepoint(pos):
                pygame.draw.rect(surf, (232, 227, 176), rect)
                surf.blit(txt, (x, y))
                if pygame.mouse.get_pressed()[0]:
                    if not self.last_click:
                        
                        self.last_click = True
                        self.extra_line = None
                        if next_lines[i] == 'end':
                            self.end = True
                            if self.npc.dialogue is not None:
                                self.npc.active = False
                        else:
                            self.curr_line = int(next_lines[i]) - 1
                else:
                    self.last_click = False

            
      
    # ustawia self.curr_line na koljeną część dialogu do narysowania
    def set_next_line(self):
        while True:
            curr_txt = self.dialogue[self.curr_line]
            if curr_txt == "\n":
                self.curr_line += 1
            elif curr_txt[0] == "!":
                self.command(curr_txt.split())
            else:
                break
    
    def command(self, line):
        if line[1] == "rand":
            self.curr_line = int(choice(line[2:])) - 1
        elif line[1] == "item":
            items = list(ITEM_TYPES.keys())
            items.remove("14")
            new_item_type = choice(items)
            new_item = ITEM_TYPES[new_item_type](0, 0)
            self.extra_line = f"[{self.namesplit()[1]} gives you {new_item.name}]"
            self.backpack.update(new_item)
            self.curr_line += 1

        elif line[1] == "stat":
            stat_str = line[2]
            val = int(line[3])
            chosen_stat = Stats.__getitem__(stat_str)
            self.animal.stats[chosen_stat] += val
            
            self.curr_line += 1
      
        
    def dialogue_end(self):
        return self.end
    
    
# TODO
# komenda na statsy
# porobić i przetestować dialogi
# ustawić ludziki
    
