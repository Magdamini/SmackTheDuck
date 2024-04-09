class Camera:
    def __init__(self, display, player, tilemap):
        self.width = display.get_width()
        self.height = display.get_height()
        self.player = player
        self.bounds = tilemap.get_bounds()
        self.pos = [0, 0]
        
    def update(self):
        # powinno wyłączać przesuwanie kamery dla małych map

        # left/right
        if self.bounds[1] - self.bounds[0] > self.width:
            self.pos[0] = int(self.player.pos[0] - self.width / 2 + self.player.size[0] / 2)
            if self.pos[0] < self.bounds[0]:
                self.pos[0] = self.bounds[0]
            elif self.pos[0] + self.width > self.bounds[1]:
                self.pos[0] = self.bounds[1] - self.width
     
        # down/up       
        if self.bounds[3] - self.bounds[2] > self.height:
            self.pos[1] = int(self.player.pos[1] - self.height / 2 + self.player.size[1] / 2)
            if self.pos[1] + self.height> self.bounds[3]:
                self.pos[1] = self.bounds[3] - self.height
            elif self.pos[1] < self.bounds[2]:
                self.pos[1] = self.bounds[2]
