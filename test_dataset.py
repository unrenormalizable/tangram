import numpy as np
from PIL import Image
import common


def make_square(ids):
    x1 = ids[0][0]
    y1 = ids[0][1]
    x2 = ids[1][0]
    y2 = ids[1][1]
    return [ids[0], ids[1], (x2 + (y1 - y2), y2 - (x1 - x2)), (x1 - (y2 - y1), y1 + (x2 - x1))]


def make_right_triangle(ids):
    vs = make_square(ids)
    return [vs[0], vs[1], vs[3]]


def make_parallelogram(ids):
    x1 = ids[0][0]
    y1 = ids[0][1]
    x2 = ids[1][0]
    y2 = ids[1][1]
    xc = ids[2][0]
    yc = ids[2][1]
    v3 = (x1 + 2 * (xc - x1), y1 + 2 * (yc - y1))
    v4 = (x2 + 2 * (xc - x2), y2 + 2 * (yc - y2))
    return [ids[0], ids[1], v3, v4]


path = common.get_target_path()
im = Image.open(f"{path}/0000.bmp")
p = np.array(im)

vertices = common.get_vertices(f"{path}/0000.csv")
print(p.dtype)
