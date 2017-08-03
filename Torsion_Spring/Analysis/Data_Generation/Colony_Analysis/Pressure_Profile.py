import numpy as np
from Colony_Analysis.Colony_Properties import *
from scipy.spatial.distance import euclidean as dist
from Colony_Analysis.Particle_Data import format_data
import matplotlib.pyplot as plt

def get_average_pressure_particle(part):
    return sum(part.pressures)/len(part.pressures)

def get_pressure_distance_tuple(part, com):
    return (dist(part.center, com), get_average_pressure_particle(part))

def yield_all_pressure_distance_tuples(ts):
    com = get_com_colony(ts)
    for particle in ts:
        yield get_pressure_distance_tuple(particle, com)

def get_pressure_profile(data):
    ans = []
    for ts in data:
        l = sorted(yield_all_pressure_distance_tuples(ts), key=lambda x: x[0])
        ans.append(l)
    return ans


