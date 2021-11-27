"""
Read files with extension .glsl
"""


class Glsl:
    def __init__(self):
        self.dir = __name__[0:-4].replace('.', '/')

    def vertex_shader(self) -> str:
        with open(self.dir+'vertex_shader.glsl', 'r') as shader:
            code = shader.read()
        return code

    def read(self, file: str) -> str:
        with open(file, 'r') as shader:
            code = shader.read()
        return code
