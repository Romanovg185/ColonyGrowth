from scipy.spatial import Delaunay, ConvexHull
from scipy.spatial.distance import euclidean as dist
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from Colony_Analysis.Colony_Properties import get_com_colony
from Colony_Analysis.Internal_OP import make_np_dict
from Colony_Analysis.Vector_Tricks import *

def generate_graph_from_triangulation(tri):
    delta_dict = {}
    l = tri.simplices
    for el in l:
        for i in el:
            if tuple(tri.points[i]) not in delta_dict.keys():
                delta_dict[tuple(tri.points[i])] = set()
        delta_dict[tuple(tri.points[el[0]])].add(tuple(tri.points[el[1]]))
        delta_dict[tuple(tri.points[el[0]])].add(tuple(tri.points[el[2]]))
        delta_dict[tuple(tri.points[el[1]])].add(tuple(tri.points[el[0]]))
        delta_dict[tuple(tri.points[el[1]])].add(tuple(tri.points[el[2]]))
        delta_dict[tuple(tri.points[el[2]])].add(tuple(tri.points[el[0]]))
        delta_dict[tuple(tri.points[el[2]])].add(tuple(tri.points[el[1]]))
    return delta_dict


def generate_edges(delta_dict):
    edges = set()
    for key, value in delta_dict.items():
        for val in value:
            if (val, key) not in edges:
                edges.add((key, val))
    return edges


def generate_triangles(tri):
    l = []
    for simplex in tri.simplices:
        l.append((tuple(tri.points[simplex[0]]), tuple(tri.points[simplex[1]]), tuple(tri.points[simplex[2]])))
    return l


def is_long_enough(point_1, point_2, l=0.5):
    if dist(point_1, point_2) > l:
        return True
    return False


def is_exterior(list_of_triangles, edge):
    i = 0
    for triangle in list_of_triangles:
        if edge[0] in triangle and edge[1] in triangle:
            i += 1
    if i == 1:
        return True
    elif i == 2:
        return False
    raise ValueError("Triangulation went wrong, edge shared by more than 2 tris")


def generate_boundary_edges(edges, list_of_triangles):
    boundary_edges = []
    for edge in edges:
        if is_exterior(list_of_triangles, edge):
            boundary_edges.append(edge)
    return boundary_edges


def sort_key(edge):
    return dist(edge[0], edge[1])


def generate_boundary_vertices(boundary_edges):
    s = set()
    for i in boundary_edges:
        s.add(i[0])
        s.add(i[1])
    return list(s)


def sort_on_length(boundary_edges):
    return sorted(boundary_edges, key=sort_key, reverse=True)


def find_third_point_triangle(list_of_triangles, edge):
    for tri in list_of_triangles:
        if edge[0] in tri and edge[1] in tri:
            my_tri = tri
            for el in my_tri:
                if el not in edge:
                    return el
    raise ValueError("Triangle is not in your list")


def is_regular_after_removing(list_of_triangles, edge, boundary_vertices):
    if is_exterior(list_of_triangles, edge):
        v = find_third_point_triangle(list_of_triangles, edge)
        if v not in boundary_vertices:
            return True
    return False


def get_edges_from_triangle_list(triangle_list):
    s = set()
    for triangle in triangle_list:
        s.add((triangle[0], triangle[1]))
        s.add((triangle[1], triangle[2]))
        s.add((triangle[2], triangle[0]))
    return list(s)


def characteristic_shape(points, l):
    tri = Delaunay(points)
    delta_dict = generate_graph_from_triangulation(tri)
    edges = generate_edges(delta_dict)
    triangle_list = generate_triangles(tri)
    boundary_edges = generate_boundary_edges(edges, triangle_list)  # 1.2
    boundary_edges = sort_on_length(boundary_edges)  # 1.3
    boundary_vertices = generate_boundary_vertices(boundary_edges)  # 1.4-1.8
    while len(boundary_edges) != 0:
        e = boundary_edges[0]
        boundary_edges.remove(e)
        if is_long_enough(e[0], e[1], l=l) and is_regular_after_removing(triangle_list, e, boundary_vertices):
            for tri in triangle_list:  # Removing triangle
                if e[0] in tri and e[1] in tri:
                    for i in tri:
                        if i not in e:
                            third_point = i
                    triangle_list.remove(tri)
            boundary_edges.append((e[0], third_point))
            boundary_edges.append((e[1], third_point))
            boundary_vertices.append(third_point)
            boundary_edges = sort_on_length(boundary_edges)

    final_edges = get_edges_from_triangle_list(triangle_list)
    final_boundary_edges = generate_boundary_edges(final_edges, triangle_list)
    s = set()
    for edge in final_boundary_edges:
        s.add(edge[0])
        s.add(edge[1])
    return list(s)

def get_smoothness_particles_ts(ts):
    centers = [i.center for i in ts]
    edge_centers = characteristic_shape(centers, 4)
    com = get_com_colony(ts)
    ans = []
    for center in edge_centers:
        index_particle_of_interest = centers.index(center)
        particle_of_interest = ts[index_particle_of_interest]
        v = make_vector_head_to_tail(particle_of_interest)
        c = particle_of_interest.center
        r = np.array([c[0] - com[0], c[1] - com[1]])
        theta = np.absolute(np.arccos((v@r)/(np.linalg.norm(v) * np.linalg.norm(r))))
        ans.append(theta)
    return ans

def get_smoothness(data):
    ans = []
    data_dict = make_np_dict(data)
    for key, val in data_dict.items():
        if key > 100:
            data_set_per_np = []
            for ts in val:
                angles = get_smoothness_particles_ts(ts)
                for ang in angles:
                    data_set_per_np.append(ang)
            ans.append((key, data_set_per_np))
    return ans


