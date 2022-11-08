import numpy as np
from typing import List, Tuple


def to_grayscale(img: np.ndarray) -> np.ndarray:
    """
    Convert an image to grayscale. The image is a numpy array (usually of type np.uint8).
    :param img: The input image, in a numpy array with dimensions [x, y, color] where the color components
        are the RGB values
    :return:
    """
    # First convert to a np.uint32 so our calculations don't overflow:
    gr_img = img.astype(np.uint32)
    # Now calculate the Pythagoras formula - the root of the sum of squares of the red, green and blue.
    # Clip the values to be between 0 and 255 (so a number over 255 becomes 255, under 0 becomes 0)
    gr_img = np.clip(np.sqrt(gr_img[:,:,0]**2 + gr_img[:,:,1]**2 + gr_img[:,:,2]**2), 0, 255).astype(np.uint8)
    return gr_img

def edge_detect(img: np.ndarray, thr: int = 35) -> np.ndarray:
    """
    Simple edge detection. Detects edges with a difference formula. Difference between consecutive pixels
    :param img: The image. Should be a grayscale image with dimensions [x,y]
    :param thr: The threshold. if not 0, then numbers above this become an edge.
    :return:
    """
    diff_img = (abs(np.diff(img[:,1:], axis=0)) + abs(np.diff(img[1:,:], axis=1))) / 2

    # Apply the threshold if provided (not 0):
    if thr > 0:
        diff_img[diff_img < thr] = 0
        diff_img[diff_img >= thr] = 255

    return diff_img


def get_circle(R: int, N: int = 100) -> (np.ndarray, np.ndarray):
    """
    Return N points around the circle with radius R. Returns two numpy arrays - one for X, one for Y.
    For a circle around a specific point x,y add x to the X results, and y to the Y results.
    """
    angles = np.linspace(0, 2 * np.pi, N)
    x_ind = (R * np.cos(angles)).astype(int)
    y_ind = (R * np.sin(angles)).astype(int)
    return x_ind, y_ind


def expand_polygon(xy: List[Tuple[int, int]], by: int = 1, by_top: int = None, by_bottom: int = None):
    """
    Expand (or shrink) a polygon. Can also make different changes to the top and the bottom of the polygon
    :param xy: A list of tuples (x,y) which are the coordinates of the polygon
    :param by: Number of pixels to grow (or shrink if negative)
    :param by_top: If not None, this is the number of pixels to grow the top part upwards. For example if by_top=0 then
        the top part isn't changed.
    :param by_bottom: If not None, this is the number of pixels to grow the bottom part down. For example if by_bottom=0 then
        the bottom part isn't changed.
    :return:
    """
    # Find the center using a mean:
    mean_x = sum(p[0] for p in xy) / float(len(xy))
    mean_y = sum(p[1] for p in xy) / float(len(xy))

    if by_top is None:
        by_top = by
    if by_bottom is None:
        by_bottom = by
    # Now for every point if x is less than the center decrease it by 1, if it is over the center increase by 1. Same for y:
    res = []
    for x, y in xy:
        if x > mean_x:
            x += by
        else:
            x -= by
        if y > mean_y:
            y += by_bottom
        else:
            y -= by_top
        res.append((x, y))
    return res
