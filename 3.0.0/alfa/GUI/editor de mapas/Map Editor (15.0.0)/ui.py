from OpenGL.GL import *
import texture

def init(new_screen_size):
    global screen_size
    screen_size = list(new_screen_size)
    
class Button:
    def __init__(self, rect, path_button,path_halo, callback):
        self.rect = rect
        self.hovering = False
        self.selected = False
        self.texture_button = texture.Texture2D.from_path(path_button)
        self.texture_halo   = texture.Texture2D.from_path(  path_halo)
        self.callback = callback
    def __del__(self):
        del self.texture_button
        del self.texture_halo

    def get_hovering(self):
        return self.hovering
    
    def move(self,mouse_pos):
        self.hovering = False
        if mouse_pos[0] > self.rect[0] and mouse_pos[0] < self.rect[0]+self.rect[2]:
            if screen_size[1]-mouse_pos[1] > self.rect[1] and screen_size[1]-mouse_pos[1] < self.rect[1]+self.rect[3]:
                self.hovering = True
    def click(self):
        if self.hovering:
            self.callback()
            return True
        return False
    def draw(self):
        def draw_rect(rect):
            glBegin(GL_QUADS)
            glTexCoord2f(0,0); glVertex3f(rect[0],        rect[1],        0)
            glTexCoord2f(1,0); glVertex3f(rect[0]+rect[2],rect[1],        0)
            glTexCoord2f(1,1); glVertex3f(rect[0]+rect[2],rect[1]+rect[3],0)
            glTexCoord2f(0,1); glVertex3f(rect[0],        rect[1]+rect[3],0)
            glEnd()
        
        self.texture_halo.bind()
        if self.hovering or self.selected:
            if self.hovering: glColor3f(1,1,0)
            elif self.selected: glColor3f(0,1,1)
            draw_rect((self.rect[0]-5,self.rect[1]-5,self.rect[2]+10,self.rect[3]+10))
            glColor3f(1,1,1)
        draw_rect(self.rect)

        self.texture_button.bind()
        draw_rect(self.rect)
        
class ButtonRadio(Button):
    def __init__(self, rect, path_button,path_halo, callback):
        Button.__init__(self, rect, path_button,path_halo, callback)
##class ButtonCheck(Button):
##    def __init__(self, rect, path_button,path_halo, callback):
##        Button.__init__(self, rect, path_button,path_halo, callback)
##    def click(self):
##        self.selected = not self.selected
##        if self.selected:
##            self.callback()
        
class Radio:
    def __init__(self,radio_buttons,initial_index):
        self.buttons = radio_buttons
        self.buttons[initial_index].selected = True
    def get_hovering(self):
        result = False
        for button in self.buttons:
            result = result or button.get_hovering()
        return result
    def move(self,mouse_pos):
        for button in self.buttons:
            button.move(mouse_pos)
    def click(self):
        for button in self.buttons:
            if button.hovering:
                if not button.selected:
                    for button2 in self.buttons:
                        button2.selected = False
                    button.selected = True
                    button.click()
                    return True
        return False
    def draw(self):
        for button in self.buttons:
            button.draw()
