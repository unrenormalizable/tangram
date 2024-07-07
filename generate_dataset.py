import math
import statistics
import random
import numpy as np
from shapely import geometry, affinity, wkt
from PIL import Image, ImageDraw
import common

# NOTE: 1: All pics should have the shapes of the same sizes


def is_square(coords):
    a = (coords[1][0] - coords[0][0]) ** 2 + (coords[1][1] - coords[0][1]) ** 2
    b = (coords[3][0] - coords[0][0]) ** 2 + (coords[3][1] - coords[0][1]) ** 2
    return math.isclose(a, b, rel_tol=1e-5)


def get_identifying_points(vertices):
    coords = list(zip(vertices[0], vertices[1]))
    if len(coords) == 4 or is_square(coords):
        return [coords[0][0], coords[0][1], coords[1][0], coords[1][1]]
    # For parallelogram
    return [
        coords[0][0],
        coords[0][1],
        coords[1][0],
        coords[1][1],
        statistics.fmean(vertices[0][:4]),
        statistics.fmean(vertices[1][:4]),
    ]


def get_centroid(vertices):
    return [
        statistics.fmean(vertices[0][:4]),
        statistics.fmean(vertices[1][:4]),
    ]


def get_vertices(vertices):
    coords = [x for xs in zip(vertices[0], vertices[1]) for x in xs][:-2]
    return coords


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


def render_polygons(name, polygons: geometry.MultiPolygon, img_size):
    img = Image.new("L", (img_size, img_size))
    ceil_approx_factor = 1.01  #
    bound_max = ceil_approx_factor * max(
        polygons.bounds[2] - polygons.bounds[0], polygons.bounds[3] - polygons.bounds[1]
    )
    #scalef = 5
    #polygons = affinity.scale(polygons, img_size / bound_max / scalef, img_size / bound_max / scalef)  # TODO delete
    polygons = affinity.scale(polygons, img_size / 1, img_size / 1)  # TODO delete
    # polygons = affinity.scale(polygons, img_size / bound_max, img_size / bound_max)
    polygons = affinity.translate(
        polygons,
        img_size / 2 - random.uniform(polygons.bounds[0], polygons.bounds[2]) * 1,
        img_size / 2 - random.uniform(polygons.bounds[1], polygons.bounds[3]) * 1,
    )
    # polygons = affinity.translate(
    #     polygons,
    #     img_size / 2 - (polygons.bounds[2] + polygons.bounds[0]) / 2,
    #     img_size / 2 - (polygons.bounds[3] + polygons.bounds[1]) / 2,
    # )
    for p in list(polygons.geoms):
        x, y = p.exterior.coords.xy
        x = np.array(x, dtype=np.float32)
        y = np.array(y, dtype=np.float32)
        order = np.argsort(np.arctan2(y - y.mean(), x - x.mean()))
        order_points = list(zip(x[order], y[order]))
        ImageDraw.Draw(img).polygon(order_points, outline=255, fill=255)
    # img.show()
    path = common.get_target_path()
    img.convert("1").save(f"{path}/{name}.bmp")
    ids = [",".join([str(x) for x in get_vertices(p.exterior.coords.xy)]) for p in list(polygons.geoms)]
    with open(f"{path}/{name}.csv", "w", encoding="utf8") as f:
        f.write("\n".join(ids))


random.seed(3141)
IMAGE_LEN = 256
for i in range(2048):
    shapes = list(common.SHAPES.values())[5:6]
    mp = arrange_polygons([geometry.Polygon(p) for p in shapes])
    render_polygons(f"{i:04d}", mp, IMAGE_LEN)
