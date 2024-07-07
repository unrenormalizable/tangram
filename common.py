import os
import math
import pathlib

SHAPES = {
    "LT1": [(0, 0), (math.sqrt(2) / 2, 0), (0, math.sqrt(2) / 2)],
    "LT2": [(0, 0), (math.sqrt(2) / 2, 0), (0, math.sqrt(2) / 2)],
    "MT": [(0, 0), (1 / 2, 0), (0, 1 / 2)],
    "ST1": [(0, 0), (math.sqrt(2) / 4, 0), (0, math.sqrt(2) / 4)],
    "ST2": [(0, 0), (math.sqrt(2) / 4, 0), (0, math.sqrt(2) / 4)],
    "SQ": [(0, 0), (math.sqrt(2) / 4, 0), (math.sqrt(2) / 4, math.sqrt(2) / 4), (0, math.sqrt(2) / 4)],
    "PG": [(0, 0), (1 / 2, 0), (3 / 4, 1 / 4), (1 / 4, 1 / 4)],
}

IDs = {
    "LT1": [(0, 0), (math.sqrt(2) / 2, 0)],
    "LT2": [(0, 0), (math.sqrt(2) / 2, 0)],
    "MT": [(0, 0), (1 / 2, 0)],
    "ST1": [(0, 0), (math.sqrt(2) / 4, 0)],
    "ST2": [(0, 0), (math.sqrt(2) / 4, 0)],
    "SQ": [(0, 0), (math.sqrt(2) / 4, 0)],
    "PG": [(0, 0), (1 / 2, 0), (3 / 8, 1 / 8)],
}


def _get_path(sub_folder):
    path = os.path.dirname(os.path.realpath(__file__))
    path = f"{path}/{sub_folder}"
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    return path


def get_target_path():
    return _get_path("target")


def get_images_path():
    return _get_path("images")


def get_y(fname):
    with open(f"{fname}", encoding="utf8") as f:
        lines = f.readlines()

    polygons = [line.strip().split(",") for line in lines]
    vertices = [
        [tuple(float(x) for x in polygon[i : i + 2]) for i in range(0, len(polygon), 2)] for polygon in polygons
    ]

    return vertices
