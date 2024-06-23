import math
import random
import numpy as np
from shapely import geometry, affinity, wkt
from PIL import Image, ImageDraw

LT1 = geometry.Polygon([(0, 0), (math.sqrt(2) / 2, 0), (0, math.sqrt(2) / 2)])
LT2 = geometry.Polygon([(0, 0), (math.sqrt(2) / 2, 0), (0, math.sqrt(2) / 2)])
MT = geometry.Polygon([(0, 0), (1 / 2, 0), (0, 1 / 2)])
ST1 = geometry.Polygon([(0, 0), (math.sqrt(2) / 4, 0), (0, math.sqrt(2) / 4)])
ST2 = geometry.Polygon([(0, 0), (math.sqrt(2) / 4, 0), (0, math.sqrt(2) / 4)])
SQ = geometry.Polygon([(0, 0), (math.sqrt(2) / 4, 0), (math.sqrt(2) / 4, math.sqrt(2) / 4), (0, math.sqrt(2) / 4)])
PG = geometry.Polygon([(0, 0), (1 / 2, 0), (3 / 4, 1 / 4), (1 / 4, 1 / 4)])

SHAPES = {
    "LT1": LT1,
    "LT2": LT2,
    "MT": MT,
    "ST1": ST1,
    "ST2": ST2,
    "SQ": SQ,
    "PG": PG,
}

for s in SHAPES.values():
    print(s)


def arrange_polygon(polygon):
    translate_max = 1.0
    polygon = affinity.translate(
        polygon, random.uniform(-translate_max, translate_max), random.uniform(-translate_max, translate_max)
    )
    polygon = affinity.rotate(polygon, random.uniform(0, 360))
    polygon = affinity.scale(polygon, xfact=-1, origin=(1, 0)) if random.choice([True, False]) else polygon
    return polygon


def arrange_polygons(polygons):
    polygons = [arrange_polygon(p) for p in polygons]
    ps = [wkt.loads(p.wkt) for p in polygons]
    return geometry.MultiPolygon(ps)


def render_polygons(polygons: geometry.MultiPolygon, img_size):
    img = Image.new("L", (img_size, img_size))
    ceil_approx_factor = 1.01  #
    bound_max = ceil_approx_factor * max(
        polygons.bounds[2] - polygons.bounds[0], polygons.bounds[3] - polygons.bounds[1]
    )
    polygons = affinity.scale(polygons, img_size / bound_max, img_size / bound_max)
    polygons = affinity.translate(
        polygons,
        img_size / 2 - (polygons.bounds[2] + polygons.bounds[0]) / 2,
        img_size / 2 - (polygons.bounds[3] + polygons.bounds[1]) / 2,
    )
    for p in list(polygons.geoms):
        x, y = p.exterior.coords.xy
        x = np.array(x, dtype=np.float32)
        y = np.array(y, dtype=np.float32)
        order = np.argsort(np.arctan2(y - y.mean(), x - x.mean()))
        order_points = list(zip(x[order], y[order]))
        ImageDraw.Draw(img).polygon(order_points, outline=255, fill=255)
    # img.save("d:/src/delme/1.polygon.bmp")
    img.show()


# random.seed(2178)
IMAGE_LEN = 512
mp = arrange_polygons(SHAPES.values())
render_polygons(mp, IMAGE_LEN)
