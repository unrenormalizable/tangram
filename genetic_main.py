import random
import numpy as np
from shapely import geometry, affinity
from PIL import Image, ImageDraw
import common

MAX_SIDE_LENGTH = 512
TO_CHANGE_SCALE_FACTOR = MAX_SIDE_LENGTH / 3
MARKER_COLOR = 0xff0000ff

def normalize_image(img):
    """Convert to 512x512 without scaling cropping or any other mods."""
    img1 = np.full((MAX_SIDE_LENGTH, MAX_SIDE_LENGTH, 4), 255, dtype=np.uint8)
    x = int((img1.shape[0] - img.shape[0]) / 2)
    y = int((img1.shape[1] - img.shape[1]) / 2)
    img1[x : x + img.shape[0], y : y + img.shape[1]] = img
    return img1


def read_image(img_id):
    """Read image from disk."""
    img_data = np.asarray(Image.open(f"{common.get_images_path()}/{img_id}"))
    if img_data.shape[0] >= 512 or img_data.shape[1] >= 512:
        raise NotImplementedError(f"Not implemented for shape: {img_data.shape}")
    return img_data


def show_image_from_data(data):
    """Show the image from the image data."""
    img = Image.fromarray(data)
    img.show()


def load_image_data(img_id):
    """Return preprocessed image data. This will serve as the base image data."""
    img = read_image(img_id)
    img = normalize_image(img)
    return img

# https://stackoverflow.com/a/37123933/6196679
def generate_image(img_data, cfg):
    """Generate image from tangram cfg & base image."""
    img = Image.fromarray(img_data)
    for i, shape_vertices in enumerate(common.SHAPES.values()):
        i_cfg = cfg[i]
        p = geometry.Polygon(shape_vertices)
        p = affinity.scale(p, TO_CHANGE_SCALE_FACTOR, TO_CHANGE_SCALE_FACTOR, origin="centroid")
        p = affinity.translate(p, i_cfg[0], i_cfg[1])
        p = affinity.rotate(p, i_cfg[2], origin="centroid")
        if len(i_cfg) == 4:
            p = affinity.scale(p, xfact=-1, origin="centroid") if i_cfg[3] else p
        ImageDraw.Draw(img, 'RGBA').polygon(p.exterior.coords, outline=0, fill=MARKER_COLOR)
    return img


def evaluate_match():
    """Given an image with superimposed tangram cfg, what is the match level?"""
    raise NotImplementedError


def get_piece_id():
    return (random.randint(0, MAX_SIDE_LENGTH - 1), random.randint(0, MAX_SIDE_LENGTH - 1), random.randint(0, 360))


def run_the_brain(_img, _cfg):
    """The brain
    Given an image with superimposed tangram cfg AND corresponding tangram coordinates,
    return new tangram coordinates that best fit the image.
    """

    return [
        get_piece_id(),
        get_piece_id(),
        get_piece_id(),
        get_piece_id(),
        get_piece_id(),
        get_piece_id(),
        (*get_piece_id(), random.choice([False, True])),
    ]


def main():
    img0 = load_image_data("10.png")
    # show_image_from_data(img0)
    # XTODO: Move this into structured format for exact match with common.SHAPES
    cfg0 = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0, False)]

    for _ in range(10000):
        cfg1 = run_the_brain(img0, cfg0)
        img1 = generate_image(img0, cfg1)
        print(cfg1)
        show_image_from_data(np.asarray(img1))

    raise NotImplementedError


if __name__ == "__main__":
    random.seed(3141)
    main()
