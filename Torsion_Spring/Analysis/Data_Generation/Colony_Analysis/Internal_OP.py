import numpy as np
from Colony_Analysis.Vector_Tricks import *


def get_internal_op_particle(particle):
    """Calculates the internal order parameter of a particle with respect to the average vector"""
    n = np.array([0.0, 0.0])
    for v in make_vector(particle):
        n += v
    theta = []
    for v in make_vector(particle):
        theta.append(get_angle_internal(v, n))
    theta = np.array(theta)
    sop = 2 * (np.cos(theta)) ** 2 - 1
    sop = np.mean(sop)
    return sop


def get_internal_op(data):
    """Returns a list of arrays of internal order parameters per time step per particle"""
    ans = []
    for time_step in data:
        time_ans = []
        for particle in time_step:
            time_ans.append(get_internal_op_particle(particle))
        time_ans = np.array(time_ans)
        ans.append(time_ans)
    return ans


def make_np_dict(data):
    np_dict = {}
    for ts in data:
        if len(ts) not in np_dict:
            np_dict[len(ts)] = [ts]
        else:
            np_dict[len(ts)].append(ts)
    return np_dict


def get_mean_internal_op_per_n(np_dict):
    op_per_n = {}
    sigma_per_n = {}
    for key, value in np_dict.items():
        op = []
        for ts in value:
            for particle in ts:
                op.append(get_internal_op_particle(particle))
        op = np.array(op)
        op_per_n[key] = np.mean(op)
        sigma_per_n[key] = np.std(op)
    ans = []
    for k, v in op_per_n.items():
        ans.append((k, v, sigma_per_n[k]))
    return ans


def get_mean_internal_op(data):
    """Returns iOP as (number of particles, mean iOP, std iOP) """
    my_dict = make_np_dict(data)
    iop = get_mean_internal_op_per_n(my_dict)
    sorted_iop = sorted(iop, key=lambda tup: tup[0])
    return sorted_iop
