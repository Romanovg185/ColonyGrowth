import numpy as np
from Colony_Analysis.Particle_Data import *
from Colony_Analysis.Vector_Tricks import *
from numpy import pi
from scipy.spatial.distance import euclidean as dist


def make_adjacency_matrix(ts, n_pivot):
    """Makes a n_pivot by n_pivot binary matrix that is true when at least 1 point in i and j
    are less than sqrt(3) apart"""
    n_points = n_pivot + 2
    l = []
    for i in ts:
        for j in i.positions:
            l.append(j)
    v = np.array(l)
    w = v.reshape(v.shape[0], 1, 2)
    w = ((w - v)**2).sum(2)
    m = w < 3
    for i in range(m.shape[0]//n_points):
        m[n_points*i: n_points*i + n_points, n_points*i: n_points*i + n_points] = np.zeros((n_points, n_points))
    n = np.zeros((len(ts), len(ts)))*42
    for i in range(len(ts)):
        for j in range(len(ts)):
            n[i, j] = m[n_points*i:n_points*i+n_points, n_points*j:n_points*j+n_points].any()
    return n


def find_triples(m):
    """Walks every 2-walk through the adjacency graph and determines 3-cycles"""
    ans = []
    s = m.shape[0]
    for i in range(s):
        for j in range(i + 1, s):
            if m[i][j]:
                for k in range(j + 1, s):
                    if m[j, k] and m[k, i]:
                        ans.append((i, j, k))
    return ans


def get_angles(particle):
    """Determines the angle between the positive x-axis and a particle"""
    v = make_vector_head_to_tail(particle)
    theta = np.arctan2(v[1], v[0])
    return theta


def pairs(lst):
    n = len(lst)
    for i in range(n):
        yield lst[i],lst[(i+1)%n]


def is_defect_vertical(t):
    """Determines a defect with the discontinuity at [+- pi/2]"""
    k = 0
    angles = [get_angles(i) for i in t]
    for i, j in pairs(angles):
        if abs(i - j) > pi/2:
            k += 1
    if k == 1:
        return True
    return False


def is_defect_horizontal(t):
    """Determines a defect with the discontinuity in angle periodicity at [0, pi, ...]"""
    angles = [get_angles(i) for i in t]
    corrected_angles = [i + pi if i < 0 else i for i in angles]
    for i, j in pairs(corrected_angles):
        if abs(i - j) > pi/2:
            return True
    return False


def is_defect(t):
    if is_defect_vertical(t):
        return True
    return False


def correct_angle(angle):
    if angle > pi/2:
        angle -= pi
    elif angle < -pi/2:
        angle += pi
    return angle


def find_sign(t):
    angles = []
    center_defect = np.array([0.0, 0.0])
    for particle in t:
        center_defect += np.array(particle.center)
    center_defect /= 3
    print(center_defect)
    center_pointing_vectors = []
    for particle in t:
        center_pointing_vectors.append([particle, np.array([particle.center[0] - center_defect[0],
                                                 particle.center[1] - center_defect[1]]), 0])
    for c in center_pointing_vectors:
        v = c[1]
        c[2] = np.arctan2(v[1], v[0])
    center_pointing_vectors.sort(key=lambda x: x[2])
    particles_ordered = []
    for c in center_pointing_vectors:
        particles_ordered.append(c[0])
    ## Ordering works
    v = np.array([make_vector_head_to_tail(i) for i in particles_ordered])
    d_theta = 0
    for first, second in pairs(v):
        print(first)
        print(second)
        alpha = np.arctan2(second[1], second[0]) - np.arctan2(first[1], first[0])
        print(alpha)
        d_theta += correct_angle(alpha)
        print(correct_angle(alpha))
    print(d_theta)
    if d_theta < 1E-15:
        return False
    return True


def return_defect_particles(ts, n_p):
    n = make_adjacency_matrix(ts, n_pivot=n_p)
    trp = find_triples(n)
    z = []
    for i in trp:
        if is_defect((ts[i[0]], ts[i[1]], ts[i[2]])):
            sign = find_sign((ts[i[0]], ts[i[1]], ts[i[2]]))
            z.append((ts[i[0]], ts[i[1]], ts[i[2]], sign))
    return z


def return_defect_indices(ts, n_p):
    n = make_adjacency_matrix(ts, n_pivot=n_p)
    trp = find_triples(n)
    z = []
    for i in trp:
        if is_defect((ts[i[0]], ts[i[1]], ts[i[2]])):
            sign = find_sign((ts[i[0]], ts[i[1]], ts[i[2]]))
            z.append((i[0], i[1], i[2], sign))
    return z

def get_defects(data, n_p):
    ans = []
    for ts in data:
        defect_data = return_defect_indices(ts, n_p)
        ans.append(defect_data)
    return ans

if __name__ == '__main__':
    f = open('goodie.txt')
    data = format_data(f, n_pivot=1)
    ts = data[-1]
    ind = return_defect_indices(ts)
    s = set()
    for el in ind:
        for e in el:
            if type(e) == int:
                s.add(e)
