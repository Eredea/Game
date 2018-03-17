import math
import itertools
import Tiles
import random

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

colors = [white, black, red, green, blue]

def pixel_to_offset(pixelTuple):

    x,y = pixelTuple
    #q = (x - math.sqrt((.5 * Hexagon.height) ** 2 + (.5 * Hexagon.width) ** 2)) * 2 / 3 / Hexagon.size
    q = (x - .5*Hexagon.width) * 2 / 3 / Hexagon.size
    r = (-(x- .5*Hexagon.width) / 3 + math.sqrt(3)/3 * (y- .5* Hexagon.height)) / Hexagon.size
    return cube_to_offset(round_cube_coords(axial_to_cube((q,r))))


def round_cube_coords(cubeCoords):
    x,y,z = cubeCoords
    roundedX, roundedY, roundedZ = [round(number) for number in cubeCoords]
    xDiff, yDiff, zDiff = [abs(round(number) - number) for number in cubeCoords]

    if xDiff > yDiff and xDiff > zDiff:
        roundedX = -roundedY - roundedZ
    elif yDiff > zDiff:
        roundedY = -roundedX - roundedZ
    else:
        roundedZ = -roundedX - roundedY

    return roundedX, roundedY, roundedZ


"""These are all means of converting between different coordinate systems. Some algorithms are better using one or another."""
def cube_to_offset(cubeCoords):
    # This is right
    cubeX, cubeY, cubeZ = cubeCoords
    x = cubeX
    y = cubeZ + (cubeX - cubeX % 2) / 2
    return x, y

def offset_to_cube(offsetCoords):
    # Good
    x,y = offsetCoords
    z = y - (x - (x % 2)) / 2
    y = -x - z
    return x, y, z

def cube_to_axial(cubeCoords):
    #Good
    x, y, z = cubeCoords
    q = x
    r = z
    return q, r

def axial_to_cube(axialCoords):
    # Good
    q, r = axialCoords
    x = q
    z = r
    y = -x -z
    return x,y,z

def offset_to_axial(offsetCoords):
    x, y, z = offset_to_cube(offsetCoords)
    return cube_to_axial((x,y,z))

def axial_to_offset(axialCoords):
    x,y,z = axial_to_cube(axialCoords)
    return cube_to_offset((x,y,z))


class Hexagon():
    size = 50
    verticesAngles = [math.radians(angle) for angle in [0, 60, 120, 180, 240, 300]]

    width = size * 2
    xDist = width*3/4

    height = math.sqrt(3)/2 * width
    yDist = height

    def __init__(self, coordinate, color = (255,255,255)):
        self.xCoord, self.yCoord = coordinate
        self.xPixel, self.yPixel = self.get_center()

        self.vertices = [(self.xPixel + Hexagon.size * math.cos(angle), self.yPixel + Hexagon.size * math.sin(angle)) for angle in self.verticesAngles]
        self.color = color
        self.inhabited = False
        self.tilePic = Tiles.tiles[random.randrange(4)]
        self.color = colors[random.randrange(5)]


    def get_center(self):
        """Returns the pixel values of the center of the hexagon, dependent on the hexagons offset coordinates."""
        xCenter = Hexagon.width / 2 + self.xCoord * Hexagon.xDist

        if self.xCoord % 2 == 1:
            yCenter = Hexagon.height + self.yCoord * Hexagon.yDist
        else:
            yCenter = Hexagon.height / 2 + self.yCoord * Hexagon.yDist
        return xCenter, yCenter


    def get_cube_coordinates(self):
        """Returns the cube coordinates of the hexagon dependent upon its offset coordinates. Makes some algorithms easier."""
        return offset_to_cube((self.xCoord, self.yCoord))

    @classmethod
    def distance(cls, hex1, hex2):
        x1,y1,z1 = hex1.get_cube_coordinates()
        x2,y2,z2 = hex2.get_cube_coordinates()
        return (abs(x1 - x2) + abs(y1 - y2) + abs(z1- z2)) / 2

    def __sub__(self, other):
        """Returns the distance between this hexagon and another hexagon given a hexagon object or (x,y) tuple."""
        return Hexagon.distance(self, other)



class map():

    fullMapCoords = list(itertools.product(range(15), range(16)))

    def __init__(self):
        self.tiles = [Hexagon(coord) for coord in map.fullMapCoords]
        self.hasChanged = False

    def place_char(self, character, hex):
        hex.inhabited = True
        hex.character = character
        self.hasChanged = True

    def move_char(self, fromHex, toHex):
        if not toHex.inhabited:
            if fromHex.character.movementSpeed >= abs(toHex - fromHex):
                toHex.character = fromHex.character
                toHex.inhabited = True

                fromHex.character = None
                fromHex.inhabited = False
                self.hasChanged = True


something = map()




