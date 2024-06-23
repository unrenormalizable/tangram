import math

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
