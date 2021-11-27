"""
UNIVERSIDAD DEL VALLE DE GUATEMALA
Gráficas por computadora

Walter Saldaña #19897
"""


__author__ = "Walter Saldaña"
__version__ = '0.1.0'


from render.o import Compiler


def main():
    vertex = './render/glsl/vertex_shader.glsl'
    fragment = './render/glsl/fragment_shader.glsl'
    obj = './models/charizard3.obj'
    texture = './models/charizard2.bmp'

    compiler = Compiler(vertex, fragment, obj, texture)

    compiler.start()
    compiler.run()


if __name__ == "__main__":
    main()
