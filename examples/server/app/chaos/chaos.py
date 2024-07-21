import numpy as np


rng = np.random.default_rng()


def move_from_to(p_from, p_to, p, q):
    return p * p_to + q * p_from


def chaotic_moves(p_from, corners, k, p, q):
    """ Starting in p_from randomly choose a corner and move a fraction p towards it. Repeat k times.
    Returns the points visited along the way. """
    result = np.empty((k, 2), dtype=corners.dtype)
    choice = rng.choice(corners, size=k)
    for idx in range(k):
        p_to = choice[idx]
        p_from = move_from_to(p_from, p_to, p, q)
        result[idx] = p_from
    return result


def generate_chaos(corners, momentum):
    k = 64  # Nr of points to generate per iteration
    p = momentum  # Attraction to the corners
    q = 1. - p
    p_from = rng.choice(corners)
    while True:
        points = chaotic_moves(p_from, corners, k, p, q)
        p_from = points[-1]
        yield points


class ChaosConfig:
    def __init__(self, corners, momentum):
        self.corners = corners
        self.momentum = momentum


configs = {"Sierpinski": ChaosConfig(corners=np.array([[0., 0.], [100., 0.], [50., 50. * np.sqrt(3)]]), momentum=0.5),
           "Snowflake": ChaosConfig(corners=np.array([[0., 0.], [100., 0.], [150., 50. * np.sqrt(3)],
           [100., 100. * np.sqrt(3)], [0., 100. * np.sqrt(3)], [-50., 50. * np.sqrt(3)]]), momentum=0.6667), }
