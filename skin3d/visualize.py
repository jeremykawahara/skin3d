import numpy as np
import pandas as pd


def embed_box_borders(img, x, y, w, h, color, pad):
    p = pad

    img[y:y + h, x - p:x, :] = color
    img[y:y + h, x + w:x + w + p, :] = color
    img[y - p:y, x - p:x + w + p, :] = color
    img[y + h:y + h + p, x - p:x + w + p, :] = color


def embed_annotatations(
        img: np.array,
        annotations: pd.DataFrame,
        color: tuple, pad: int):
    """Embed the annotations in the image.

        Note that `img` is a mutable object and will be changed
        (which is why nothing is returned).

    """
    for _, row in annotations.iterrows():
        embed_box_borders(img, row.x, row.y, row.width, row.height, color, pad)
