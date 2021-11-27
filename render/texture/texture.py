import struct


class Texture:
    def __init__(self, path):
        self.path = path
        self.pixels = []
        self.read()

    def read(self):
        with open(self.path, 'rb') as image:
            image.seek(10)
            headerSize = struct.unpack('=l', image.read(4))[0]
            image.seek(18)
            self.width = struct.unpack('=l', image.read(4))[0]
            self.height = struct.unpack('=l', image.read(4))[0]
            image.seek(headerSize)

            for y in range(self.height):
                self.pixels.append([])
                for x in range(self.width):
                    b = ord(image.read(1)) / 255
                    g = ord(image.read(1)) / 255
                    r = ord(image.read(1)) / 255
                    self.pixels[y].append([r, g, b])

    def get_color(self, tx, ty):
        return self.pixels[int(ty * self.height)][int(tx * self.width)]
