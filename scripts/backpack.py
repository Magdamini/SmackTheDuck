class Backpack:
    def __init__(self):
        self.items = {}
        
    def update(self, new_item):
        if self.items.get(new_item.name) is None:
            self.items[new_item.name] = [1, new_item]
        else:
            self.items[new_item.name][0] += 1
        
        
    
    def render(self, surf):
        print(self.items)