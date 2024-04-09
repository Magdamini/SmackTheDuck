
class ItemCollector:
    def __init__(self, player):
        self.player = player
        
    def collect_items(self, tilemap): 
        items = tilemap.items_around(self.player.pos) 
        player_rect = self.player.rect()
        for x, y, rect in items:
            if player_rect.colliderect(rect):
                item = tilemap.get_item(x, y)

                self.player.backpack.update(item)
                print(f"New item collected: {item.name}")

        
    # def show_item(self, item):
    #     self.display.blit(pygame.transform.scale(item.img, (item.big_size, item.big_size)), ((self.display.get_width() - item.big_size) // 2, (self.display.get_height() - item.big_size) // 2))
        
    #     font = pygame.font.SysFont(None, 25)
    #     text = "New item found!"
    #     img = font.render(text, True, (0, 0, 0))
    #     text_rect = img.get_rect(center=(self.display.get_width()//2, (self.display.get_height() + item.big_size * 4 // 3) // 2))
        
    #     self.display.blit(img, text_rect)
        
    #     self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
    #     pygame.display.update()