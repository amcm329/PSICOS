from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import sys, os, traceback
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
from math import *
from math_helper import *
import gl_util, texture, fbo, map, tools, ui, cursor
from shader import *
pygame.display.init()
pygame.font.init()

resolution = [64,64] #The resolution of the map (I have tested up to 1024x1024, which will take about 10s to load)
screen_size = [800,600]
multisample = 16
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("Map Editor - Ian Mallett - v.15.0.0 - 2012")
if multisample:
    pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS,1)
    pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES,multisample)
pygame.display.set_mode(screen_size,OPENGL|DOUBLEBUF)
pygame.display.set_icon(pygame.transform.smoothscale(pygame.image.load("data/icon.png"),[24,24]))

gl_util.init_gl()
ui.init(screen_size)

glPointSize(5)
glLineWidth(2)
glHint(GL_LINE_SMOOTH_HINT,GL_NICEST)

class Application:
    def __init__(self):
        map.Map.init()
        
        self.reset_camera()

        self.map = map.Map.new(resolution)

        self.tools = {"raise":tools.ToolRaise(),"lower":tools.ToolLower()}
        self.current_tool = "lower"
        self.render_mode = 0x01 | 0x02
        self.ui_components = [
            ui.Radio( #Tool selection controls
                [
                    ui.ButtonRadio((10,screen_size[1]-33-10,49,33),"data/tool_lower.png","data/tool_halo.png",self.callback_set_tool_lower),
                    ui.ButtonRadio((70,screen_size[1]-33-10,49,33),"data/tool_raise.png","data/tool_halo.png",self.callback_set_tool_raise)
                ],0
            ),
            ui.Radio( #Render mode controls
                [
                    ui.ButtonRadio((screen_size[0]-75,screen_size[1]- 49,65,39),      "data/render_fill.png","data/render_halo.png",self.callback_set_render_f),
                    ui.ButtonRadio((screen_size[0]-75,screen_size[1]- 94,65,39),     "data/render_lines.png","data/render_halo.png",self.callback_set_render_l),
                    ui.ButtonRadio((screen_size[0]-75,screen_size[1]-139,65,39),"data/render_lines_fill.png","data/render_halo.png",self.callback_set_render_lf),
                ],2
            ),
            ui.Button((10,10,34,34),"data/file_save.png","data/file_halo.png",self.callback_save),
            ui.Button((50,10,34,34),"data/file_load.png","data/file_halo.png",self.callback_load)
        ]
        self.ctrl_pressed = False

        self.cursor = cursor.Cursor()

        self.texture_tool_raise = texture.Texture2D.from_path("data/map_highlight.png")
        self.texture_tool_raise.set_nicest()
    def __del__(self):
        del self.map
        del self.texture_tool_raise
        map.Map.deinit()
    def reset_camera(self):
        self.camera_rot = [180+22,30]
        self.camera_radius = 1.0
        self.camera_center = [0.5,0.5,0.5]
    def callback_set_tool_lower(self): self.current_tool = "lower"
    def callback_set_tool_raise(self): self.current_tool = "raise"
    def  callback_set_render_f(self): self.render_mode = 0x01
    def  callback_set_render_l(self): self.render_mode = 0x02
    def callback_set_render_lf(self): self.render_mode = 0x03
    def callback_load(self):
        try:
            map2 = map.Map.load()
        except:
            print("Could not load the map!")
            return
        del self.map
        self.map = map2
    def callback_save(self):
        map.Map.save(self.map)
        
    def get_input(self):
        keys_pressed = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_rel = pygame.mouse.get_rel()
        self.mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if   event.type == QUIT: return False
            elif event.type == KEYDOWN:
                if   event.key == K_ESCAPE: return False
                elif event.key == K_LCTRL or event.key == K_RCTRL:
                    self.ctrl_pressed = True
                    self.cursor.update(self.ctrl_pressed,self.tools[self.current_tool].on_map)
                elif event.key == K_r:
                    self.reset_camera()
            elif event.type == KEYUP:
                if event.key == K_LCTRL or event.key == K_RCTRL:
                    self.ctrl_pressed = False
                    self.cursor.update(self.ctrl_pressed,self.tools[self.current_tool].on_map)
            elif event.type == MOUSEBUTTONDOWN:
                if not self.ctrl_pressed:
                    if   event.button == 4: self.tools[self.current_tool].radius /= 0.9
                    elif event.button == 5: self.tools[self.current_tool].radius *= 0.9
                else:
                    if   event.button == 4: self.camera_radius *= 0.9
                    elif event.button == 5: self.camera_radius /= 0.9
                for ui_component in self.ui_components:
                    ui_component.click()
        over_ui = False
        for ui_component in self.ui_components:
            if ui_component.get_hovering():
                over_ui = True
                break
        if not over_ui:
            if self.ctrl_pressed:
                if mouse_buttons[0]:
                    self.camera_rot[0] += mouse_rel[0]
                    self.camera_rot[1] += mouse_rel[1]
            else:            
                if mouse_buttons[0]:
                    self.map.update(self)
        for ui_component in self.ui_components:
            ui_component.move(self.mouse_pos)
        return True
    def draw(self):
        gl_util.set_view_3D(screen_size, 45.0, 0.1,100.0)

        gl_util.set_camera_spherical(self.camera_center, self.camera_radius, self.camera_rot[0],self.camera_rot[1])

        #Pass 1: for the benefit of the editing and movement cursor
        glClear(GL_DEPTH_BUFFER_BIT)
        self.map.draw(self,0x01)
        tool_pos = gl_util.unproject(self.mouse_pos)
        self.tools[self.current_tool].pos = tool_pos
        on_map = (tool_pos[0]>0.0 and tool_pos[0]<1.0) and (tool_pos[1]>0.0 and tool_pos[1]<1.0) and (tool_pos[2]>0.0 and tool_pos[2]<1.0)
        self.tools[self.current_tool].on_map = on_map
        self.cursor.update(self.ctrl_pressed,on_map)

        #Pass 2: draw everything for the benefit of the user
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        self.map.draw(self,self.render_mode)

        glBegin(   GL_POINTS); glVertex3f(0,0,0); glVertex3f(1,0,0); glVertex3f(1,0,1); glVertex3f(0,0,1); glEnd()
        glBegin(GL_LINE_LOOP); glVertex3f(0,0,0); glVertex3f(1,0,0); glVertex3f(1,0,1); glVertex3f(0,0,1); glEnd()

        #Pass 3: draw UI
        gl_util.view_push()
        gl_util.set_view_2D((0,0,screen_size[0],screen_size[1]))
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)
        glDepthMask(False)
        
        for ui_component in self.ui_components:
            ui_component.draw()
        
        #self.map.draw_heightmap_as_inset(self)

        glDepthMask(True)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        gl_util.view_pop()

        #Flip
        pygame.display.flip()
    def run(self):
        clock = pygame.time.Clock()
        while True:
            if not self.get_input(): break
            self.draw()
            clock.tick(60)
        
def main():
    application = Application()
    application.run()
    del application

    pygame.quit()
if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()
