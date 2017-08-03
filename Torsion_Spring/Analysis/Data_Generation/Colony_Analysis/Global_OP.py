import numpy as np
from Colony_Analysis.Vector_Tricks import *


def correct_angle(n, p):
    """Makes sure the smallest angle between n and p is always taken"""
    ang = get_angle_internal(n, p)
    if ang > np.pi/2:
        return np.pi - ang
    if ang < -np.pi/2:
        return -np.pi + ang
    return ang


def get_global_op_ts(time_step):
    average_angle = []
    for particle in time_step:
        v = make_vector_head_to_tail(particle)
        average_angle.append(np.arctan2(v[1], v[0]))
    average_angle = 1/len(average_angle)*sum(average_angle)
    n = np.array([np.cos(average_angle), np.sin(average_angle)])
    theta = []
    for particle in time_step:
        v = make_vector_head_to_tail(particle)
        ang = correct_angle(n, v)
        theta.append(ang)
    theta = np.array(theta)
    sop = 2 * ((np.cos(theta)) ** 2) - 1
    sop = np.mean(sop)
    return sop, theta


def get_global_op_per_ts(dat):
    """Returns a list of the global SOP per time step"""
    ans = []
    for time_step in dat:
        sop = get_global_op_ts(time_step)[0]
        ans.append(sop)
    return ans


def make_per_n(sop, dat):
    """Conversion from time steps to number of particles"""
    my_dict = {}
    for j, el in enumerate(sop):
        if len(dat[j]) not in my_dict:
            my_dict[len(dat[j])] = [el]
        else:
            my_dict[len(dat[j])].append(el)
    ans = []
    for k, v in my_dict.items():
        ans.append((k, np.mean(v), np.std(v)))
    sorted_ans = sorted(ans, key=lambda tup: tup[0])
    return sorted_ans


def get_mean_global_op(data):
    """Returns a list of (np, mean(gOP) per number of particles"""
    gop = get_global_op_per_ts(data)
    my_list = make_per_n(gop, data)
    return my_list
