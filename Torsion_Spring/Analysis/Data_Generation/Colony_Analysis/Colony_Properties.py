import numpy as np


def get_com_colony(ts):
    i = 0
    com = [0, 0]
    for particle in ts:
        for point in particle.positions:
            com[0] += point[0]
            com[1] += point[1]
            i += 1
    com[0] /= i
    com[1] /= i
    return tuple(com)


def get_radius_colony(ts, com):
    radius = 0
    for particle in ts:
        for point in particle.positions:
            if radius < np.linalg.norm(np.array(com) - np.array(point)):
                radius = np.linalg.norm(np.array(com) - np.array(point))
    return radius
