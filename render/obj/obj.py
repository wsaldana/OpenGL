"""
Load OBJs to render.
"""
import numpy as np

from render.texture.texture import Texture


class Obj:
    """Load OBJ and create a buffer
    representation.

    Args:
        file (str): Path and filemane of the object to load
    """
    def __init__(self, filename, texture: Texture = None):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.tvertices = []
        self.normales = []
        self.faces = []
        self.texture = texture
        self.read()

    def read(self):
        for line in self.lines:
            if line and (line[0] != '#'):
                try:
                    prefix, value = line.split(' ', 1)
                except:
                    prefix = ''

                if prefix == 'v':
                    self.vertices.append(
                        list(map(float, value.split(' ')))
                    )
                elif prefix == 'vt':
                    vts = value.split(' ')
                    if len(vts) == 3:
                        self.tvertices.append(
                            list(map(float, value.split(' ')))
                        )
                    else:
                        self.tvertices.append(
                            list(map(float, value.split(' '))) + [0.0000]
                        )
                elif prefix == 'vn':
                    self.normales.append(
                        list(map(float, value.split(' ')))
                    )
                elif prefix == 'f':
                    faces = value.split(' ')

                    for i in range(len(faces)-2):
                        triangle = [faces[0], faces[i+1], faces[i+2]]
                        self.faces.append(
                            [
                                list(map(int, face.split('/')))
                                for face in triangle
                                if len(face) > 2
                            ]
                        )

    def to_numpy(self) -> np.array:
        vectors_array = []

        for face in self.faces:
            for i in range(len(face)):
                vertex = self.vertices[face[i][0] - 1]
                vectors_array += vertex

                tvertex = self.tvertices[face[i][1] - 1]
                if self.texture:
                    t = self.texture.get_color(tvertex[0], tvertex[1])
                    vectors_array += t
                else:
                    vectors_array += tvertex

                normal = self.normales[face[i][2] - 1]
                vectors_array += normal

        np_vectors_array = np.array(vectors_array, dtype=np.float32)
        return np_vectors_array

    def index_np(self) -> np.array:
        index_data = np.array(
            [
                [vertex[0] - 1 for vertex in face]
                for face
                in self.faces
            ],
            dtype=np.uint32
        )

        return index_data.flatten()
