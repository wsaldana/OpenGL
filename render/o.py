from math import sin, pi

import pygame as pg
import numpy as np
import OpenGL.GL as GL
from OpenGL.GL.shaders import compileProgram, compileShader
import glm

from render.glsl.glsl import Glsl
from render.obj.obj import Obj
from render.texture.texture import Texture


class Compiler:

    glsl = Glsl()

    def __init__(
            self,
            vertex_shader: str,
            fragment_shader: str,
            model: str,
            texture: str = None):
        self.vertex_shader_path = vertex_shader
        self.fragment_shader_path = fragment_shader
        self.model_path = model
        self.texture = texture
        self.shader = None

    @property
    def vertex_shader(self):
        return self.read_shaders(self.vertex_shader_path)

    @property
    def fragment_shader(self):
        return self.read_shaders(self.fragment_shader_path)

    @property
    def model(self):
        return self.load_obj(self.model_path)

    def read_shaders(self, path: str) -> str:
        return self.glsl.read(path)

    def load_obj(self, path: str) -> np.array:
        obj = Obj(path, Texture(self.texture))
        return obj

    def start(self):
        pg.init()

        screen = pg.display.set_mode(
            (1080, 720),
            pg.OPENGL | pg.DOUBLEBUF
        )

        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)

        # clock = pg.time.Clock()

        cvs = compileShader(
            self.vertex_shader,
            GL.GL_VERTEX_SHADER
        )
        cfs = compileShader(
            self.fragment_shader,
            GL.GL_FRAGMENT_SHADER
        )
        self.shader = compileProgram(cvs, cfs)

        vertex_buffer_object = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vertex_buffer_object)
        model_np = self.model.to_numpy()
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            model_np.nbytes,
            model_np,
            GL.GL_STATIC_DRAW
        )

        vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vertex_array_object)
        # Location, size, type, norm, stride, ctype
        GL.glVertexAttribPointer(
            0, 3, GL.GL_FLOAT, GL.GL_FALSE, 4 * 9, GL.ctypes.c_void_p(0)
        )
        GL.glEnableVertexAttribArray(0)

        element_buffer_object = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
        indexing = self.model.index_np()
        GL.glBufferData(
            GL.GL_ELEMENT_ARRAY_BUFFER,
            indexing.nbytes,
            indexing,
            GL.GL_STATIC_DRAW
        )

        GL.glVertexAttribPointer(
            1, 3, GL.GL_FLOAT, GL.GL_FALSE, 4 * 9, GL.ctypes.c_void_p(4 * 3)
        )
        GL.glEnableVertexAttribArray(1)

        element_buffer_object = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
        GL.glBufferData(
            GL.GL_ELEMENT_ARRAY_BUFFER,
            indexing.nbytes,
            indexing,
            GL.GL_STATIC_DRAW
        )

        GL.glVertexAttribPointer(
            2, 3, GL.GL_FLOAT, GL.GL_FALSE, 4 * 9, GL.ctypes.c_void_p(4 * 6)
        )
        GL.glEnableVertexAttribArray(2)

        GL.glUseProgram(self.shader)

    def run(self):
        GL.glViewport(0, 0, 1080, 720)
        clock = pg.time.Clock()

        a = 0
        rotation = 0
        speed = 5
        zoom = 0.4
        toggle_view = False

        running = True
        while running:
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            self.transform(rotation, zoom)

            a += 1
            GL.glUniform1i(
                GL.glGetUniformLocation(self.shader, 'clock'), a
            )
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.model.faces) * 3)

            pg.display.flip()
            clock.tick(15)

            for event in pg.event.get():

                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT or event.key == pg.K_a:
                        rotation -= speed

                    if event.key == pg.K_RIGHT or event.key == pg.K_d:
                        rotation += speed

                    if event.key == pg.K_UP or event.key == pg.K_w:
                        if speed < 360:
                            speed += 1

                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        if speed > 0:
                            speed -= 1

                    if event.key == pg.K_x:
                        toggle_view = not toggle_view

                        if toggle_view:
                            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
                        else:
                            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)

                elif (
                    event.type == pg.MOUSEBUTTONDOWN
                    or event.type == pg.MOUSEBUTTONUP
                ):
                    if event.button == 4:
                        if zoom < 1:
                            zoom += 0.05
                    if event.button == 5:
                        if zoom > 0.1:
                            zoom -= 0.05

    def transform(self, rotation: int, zoom: int):
        i = glm.mat4(1)

        translate = glm.translate(i, glm.vec3(0, -3, -5))
        rotate = glm.rotate(i, glm.radians(rotation), glm.vec3(0, -1, 0))
        scale = glm.scale(i, glm.vec3(zoom, zoom, zoom))

        model = translate * rotate * scale
        view = glm.lookAt(
            glm.vec3(0, 0, 15),
            glm.vec3(0, 0, 0),
            glm.vec3(0, 1, 0)
        )
        projection = glm.perspective(glm.radians(30), 1080/720, 0.1, 1000.0)

        matrix = projection * view * model

        GL.glUniformMatrix4fv(
            GL.glGetUniformLocation(self.shader, 'matrix'),
            1,
            GL.GL_FALSE,
            glm.value_ptr(matrix)
        )
