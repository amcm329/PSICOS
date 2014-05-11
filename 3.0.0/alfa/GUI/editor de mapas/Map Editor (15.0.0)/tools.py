class Tool:
    def __init__(self,shader_action):
        self.pos = [0.5,0.5,0.5]
        self.radius = 0.5
        self.strength = 0.005

        self.on_map = False
        
        self.shader_action = shader_action
    def pass_to_shader(self,shader,all_info):
        shader.pass_vec2("tool_coord",[self.pos[0],self.pos[2]])
        shader.pass_float("tool_radius",self.radius)
        if all_info:
            shader.pass_float("tool_strength",self.strength)
            shader.pass_int("tool",self.shader_action)
class ToolLower(Tool):
    def __init__(self):
        Tool.__init__(self,1)
class ToolRaise(Tool):
    def __init__(self):
        Tool.__init__(self,2)
