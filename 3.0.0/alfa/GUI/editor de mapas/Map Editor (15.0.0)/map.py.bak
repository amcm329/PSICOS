from OpenGL.GL import *
import pygame
from shader import *
import texture, gl_util, fbo, math_helper

class Map:
    def __init__(self,surf):
        self.resolution = surf.get_size()

        surf2 = pygame.transform.rotate(surf,-90)
        rgb = pygame.surfarray.array3d(surf2).astype(float)
        rgb[:,:,0] += rgb[:,:,1]*(1.0/ 255.0       )
        rgb[:,:,0] += rgb[:,:,2]*(1.0/(255.0*255.0))
        rgb[:,:,1] = rgb[:,:,0]
        rgb[:,:,2] = rgb[:,:,0]
        rgb[:,:,:] *= 1.0/255.0
        self.heightmaps = [texture.Texture2D.from_data(rgb,32),texture.Texture2D.from_data(rgb,32)]
        self.ping_pong = 1

        self.dl = glGenLists(1)
        glNewList(self.dl,GL_COMPILE)
        for x in range(self.resolution[0]-1):
            vert_x0 = float(x  )/float(self.resolution[0]-1)
            vert_x1 = float(x+1)/float(self.resolution[0]-1)
            texc_x0 = float(x+0.5)/float(self.resolution[0])
            texc_x1 = float(x+1.5)/float(self.resolution[0])
            glBegin(GL_QUAD_STRIP)
            for z in range(self.resolution[1]):
                texc_y = float(z+0.5)/float(self.resolution[1])
                vert_y = float(z)/float(self.resolution[1]-1)
                
                glTexCoord2f(texc_x0,texc_y)
                glVertex3f(vert_x0,0.0,vert_y)

                glTexCoord2f(texc_x1,texc_y)
                glVertex3f(vert_x1,0.0,vert_y)
            glEnd()
        glEndList()

        self.fbos = [fbo.FBO2D(self.resolution),fbo.FBO2D(self.resolution)]
        self.fbos[0].attach_color_texture(self.heightmaps[0],0)
        self.fbos[1].attach_color_texture(self.heightmaps[1],0)
##        self.fbos[0].print_error()
##        self.fbos[1].print_error()
    def __del__(self):
        del self.heightmaps
        del self.fbos
        glDeleteLists(self.dl,1)

    def update(self,application):
        tool = application.tools[application.current_tool]
        if tool.on_map:
            self.ping_pong = 3 - self.ping_pong
            
            fbo.FBO2D.set_write(self.fbos[self.ping_pong-1])
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            gl_util.set_view_2D((0,0,self.resolution[0],self.resolution[1]))

            Shader.use(shader_update)
            shader_update.pass_texture(self.heightmaps[(3-self.ping_pong)-1],1)
            tool.pass_to_shader(shader_update,True)
            self.draw_quad((0,0,self.resolution[0],self.resolution[1]))
            Shader.use(None)
            
            fbo.FBO2D.set_write(None)

    def draw(self,application,render_mode):
        tool = application.tools[application.current_tool]
        Shader.use(shader_draw)
        shader_draw.pass_texture(self.heightmaps[self.ping_pong-1],1)
        shader_draw.pass_texture(application.texture_tool_raise,2)
        shader_draw.pass_texture(texture_cell,3)
        tool.pass_to_shader(shader_draw,False)
        shader_draw.pass_bool("on_map",tool.on_map and application.ctrl_pressed!=1)
        shader_draw.pass_int("render_mode",render_mode)
        shader_draw.pass_vec2("res",self.resolution)
        glCallList(self.dl)
        Shader.use(None)
    def draw_quad(self,rect):
        glBegin(GL_QUADS)
        glTexCoord2f(0,0); glVertex3f(rect[0],        rect[1],        0)
        glTexCoord2f(1,0); glVertex3f(rect[0]+rect[2],rect[1],        0)
        glTexCoord2f(1,1); glVertex3f(rect[0]+rect[2],rect[1]+rect[3],0)
        glTexCoord2f(0,1); glVertex3f(rect[0],        rect[1]+rect[3],0)
        glEnd()
    def draw_heightmap_as_inset(self,application):
        self.heightmaps[self.ping_pong-1].bind()
        self.draw_quad((5,50,128,128))
        self.heightmaps[self.ping_pong-1].bind()
        self.draw_quad((140,50,128,128))

    @staticmethod
    def new(resolution):
        print("Creating new blank map with resolution ("+str(resolution[0])+","+str(resolution[1])+") . . .")
        blank = pygame.Surface(resolution)
        blank.fill((127,127,127))
        map = Map(blank)
        print("Map created!")
        return map
    @staticmethod
    def load():
        path = "test.png"
        print("Loading map \""+path+"\" . . .")
        map = Map(pygame.image.load(path))
        print("Map loaded!")
        return map
    @staticmethod
    def save(map):
        path = "test.png"
        print("Saving map to \""+path+"\". . .")
        map.heightmaps[map.ping_pong-1].bind()
        data = glGetTexImage(GL_TEXTURE_2D,0,GL_RGBA,GL_FLOAT)
        surf = pygame.Surface(map.resolution)
        for y in range(map.resolution[1]):
            for x in range(map.resolution[0]):
                height = data[map.resolution[1]-y-1][x][0]
                r = height * 255.0
                g = (r - int(r)) * 255.0
                b = (g - int(g)) * 255.0
                color = (int(r),int(g),math_helper.rndint(b))
                surf.set_at((x,y),color)
        pygame.image.save(surf,path)
        print("Map saved!")
    @staticmethod
    def init():
        global shader_update, shader_draw, texture_cell

        program_fragment = ProgramShaderFragment("""
        uniform sampler2D tex2D_1;

        uniform int tool;
        uniform vec2 tool_coord;
        uniform float tool_radius;
        uniform float tool_strength;
        
        float height;
        
        void lower(float distance) {
            height -= tool_strength*(1.0 - distance);
        }
        void raise(float distance) {
            height += tool_strength*(1.0 - distance);
        }
        
        void main(void) {
            vec2 uv = gl_TexCoord[0].xy;
            vec3 color = texture2D(tex2D_1,uv).xyz;

            vec2 delta_tool = uv - tool_coord;
            vec2 sample_loc = delta_tool/tool_radius;
            float distance = 2.0*length(sample_loc);
            if (distance<1.0) {
                height = color.x;
                
                if      (tool==1) lower(distance);
                else if (tool==2) raise(distance);

                height = clamp(height,0.0,1.0);
                //height = 0.5 + 0.01 * (1.0 - distance);

                color = vec3(height);
            }
            
            gl_FragColor = vec4(color,1.0);
        }""")
##        program_fragment.print_errors()
        shader_update = Shader([program_fragment])
##        shader_update.print_errors()
        
        program_vertex = ProgramShaderVertex("""
        uniform sampler2D tex2D_1;
        void main(void) {
            vec3 vert = gl_Vertex.xyz;
            vert.y = texture2D(tex2D_1,gl_MultiTexCoord0.xy).r;
            gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * vec4(vert,1.0);
            gl_TexCoord[0] = gl_MultiTexCoord0;
            gl_TexCoord[1] = vec4(vert.xz,0,0);
        }""")
##        program_vertex.print_errors()
        program_fragment = ProgramShaderFragment("""
        uniform sampler2D tex2D_2;
        uniform sampler2D tex2D_3;
        uniform bool on_map;
        uniform vec2 tool_coord;
        uniform vec2 res;
        uniform float tool_radius;
        uniform int render_mode;
        vec2 rnd(vec2 v) { return floor(v + 0.5); }
        void main(void) {
            vec2 uv = gl_TexCoord[0].xy;
            vec4 color = vec4(0.0,0.0,0.0,1.0);
            
            color.r += 1.0;

            if (on_map) {
                vec2 delta_tool = uv - tool_coord;
                vec2 sample_loc = delta_tool/tool_radius + vec2(0.5);
                if (sample_loc.x>0.0&&sample_loc.x<1.0&&sample_loc.y>0.0&&sample_loc.y<1.0) {
                    vec4 sample = texture2D(tex2D_2,sample_loc);
                    color.rgb += sample.rgb * sample.a;
                }
            }

            vec2 cell = gl_TexCoord[1].xy * (res-vec2(1));
            vec4 sample = texture2D(tex2D_3,cell);
            if      (render_mode==0x02) {
                if (sample.a<0.01) discard;
                color     *= vec4((vec3(1.0)-sample.rgb),sample.a);
            }
            else if (render_mode==0x03) color.rgb *= sample.rgb;
            
            gl_FragColor = color;
        }""")
##        program_fragment.print_errors()
        shader_draw = Shader([program_vertex,program_fragment])
##        shader_draw.print_errors()

        texture_cell = texture.Texture2D.from_path("data/cell.png")
        texture_cell.set_nicest()
    @staticmethod
    def deinit():
        global shader_update, shader_draw, texture_cell
        del shader_update
        del shader_draw
        del texture_cell
