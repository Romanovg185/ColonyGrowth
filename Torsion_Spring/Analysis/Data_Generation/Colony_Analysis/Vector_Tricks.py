import numpy as np


def get_angle_internal(u, v):
    """Probably somewhere in NP, but still useful to have it clamped against floating point error"""
    phi = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    phi1 = np.arctan2(u[1], u[0])
    phi2 = np.arctan2(v[1], v[0])
    d1 = phi1 - phi2
    d2 = phi2 - phi1
    if phi1 > phi2:
        return phi1 - phi2
    return phi2 - phi1


def make_vector(my_particle):
    """Vector generator over pairs since generators are neat"""
    # iterate over pairs, pretty cool and should definitely remember it
    for v, w in zip(my_particle.positions[:-1], my_particle.positions[1:]):
        vec = np.array([w[0] - v[0], w[1] - v[1]])
        yield vec


def make_vector_head_to_tail(my_particle):
    """Makes a vector within the range [-pi/2, pi/2] from a particle"""
    vec = np.array([my_particle.positions[-1][0] - my_particle.positions[0][0],
                    my_particle.positions[-1][1] - my_particle.positions[0][1]])
    if vec[0] < 0:
        return -vec
    return vec
    # if np.pi / -2 <= np.arctan2(vec[1], vec[0]) or np.arctan2(vec[1], vec[0]) <= np.pi / 2:
    #     print(vec)
    #     return vec
    # print(vec)
    # return -1*vec
