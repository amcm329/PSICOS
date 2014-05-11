import pygame

class Cursor:
    def __init__(self):
        self.current = pygame.cursors.arrow
    def update(self,ctrl,on_map):
        if ctrl:
            needed = pygame.cursors.diamond
        elif on_map:
            needed = pygame.cursors.broken_x
        else:
            needed = pygame.cursors.arrow
            
        if needed != self.current:
            self.current = needed
            pygame.mouse.set_cursor(*self.current)
