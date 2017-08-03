from Colony_Analysis.Particle_Data import format_data
from Colony_Analysis.Colony_Properties import *
from Colony_Analysis.Vector_Tricks import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from Colony_Analysis.Internal_OP import make_np_dict
from scipy.spatial.distance import euclidean as dist


def distance_particles(my_particle, particles):
    """Returns the distance between the centres of mass of two particles"""
    v = [dist(my_particle.center, p.center) for p in particles]
    return np.array(v)


def in_annulus(v, r, dr):
    """Takes a vector of all distances to a single particle
    Returns a tuple of indices of all particles within the annulus"""
    rvec = r*np.ones_like(v)
    mask = (rvec <= v)
    mask2 = (v < rvec+dr)
    my_mask = mask & mask2
    indices = np.where(my_mask)
    return indices

def get_op_particle(n, particle):
    """Gets the scalar order parameter of a particle with respect to vector n"""
    ans = 0
    for v in make_vector(particle):
        theta = get_angle_internal(n, v)
        ans += 2 * (np.cos(theta)) ** 2 - 1
    ans /= len(particle.positions) - 1
    return ans

def exponential_fit(x, A, xi):
    return A*np.exp(-x/xi)

def make_data():
    """Returns the data well-formatted"""
    filename = input("Give file name please: ")
    file_stream = open(filename, 'r')
    f = open(filename, 'r')
    g = open(filename, 'r')
    findPropertiesData(f, g)
    data = formatData(file_stream)
    return data

def compute_correlation_length_per_particle(my_particle, r, dr, timestep):
    """Returns an array of correlation lengths corresponding to a radius array r"""
    a = set()
    b = set(np.arange(0, len(timestep), 1))
    ans = [[0, 0] for i in r]
    n = make_vector_head_to_tail(my_particle)
    distances = distance_particles(my_particle, timestep)
    for i, radius in enumerate(r):
        indices_to_check = in_annulus(distances, radius, dr)
        for my_radius in indices_to_check:
            for index in my_radius:
                ans[i][0] += get_op_particle(n, timestep[index])
                ans[i][1] += 1
                a.add(index)
    if len(a.difference(b)) != 0:
        print("Point missed!!")
    sum_op = np.array([i[0] for i in ans])
    num_hits = np.array([i[1] for i in ans])
    return sum_op/num_hits

def get_mean_gop_per_radius(data):
    dr = 0.2
    ts = data[-1]
    d = 2*get_radius_colony(ts, get_com_colony(ts))
    r = list(np.arange(0, d, dr))
    ans = compute_correlation_length_per_particle(my_particle=ts[0], r=r, dr=dr, timestep=ts)
    for i, particle_of_interest in enumerate(ts[1:]):
        my_arr = compute_correlation_length_per_particle(my_particle=particle_of_interest, r=r, dr=dr, timestep=ts)
        ans = np.vstack((ans, my_arr))
        pdone = int( (i+1)/len(ts) * 40 )
        print("|" + pdone*'#' + (40 - pdone)*'-' + '|')
    mean = np.nanmean(ans, 0)
    std = np.nanstd(ans, 0)
    mean[np.isnan(mean)] = 1
    std[np.isnan(std)] = 0
    final = []
    for r, m, s in zip(r, mean, std):
        final.append((r, m, s))
    return final

def fit_exponential(data):
    x = []
    y = []
    for i in data:
        if 0.2 < i[1] < 0.9:
            x.append(i[0])
            y.append(i[1])
    popt, pcov = curve_fit(exponential_fit, x, y)
    return_list = []
    for i in x:
        return_list.append((i, exponential_fit(i, popt[0], popt[1])))
    return (popt[1], return_list)


if __name__ == "__main__":
    dr = 0.2
    data = make_data()
    ts = data[-1]
    D = 2 * get_radius_colony(ts, get_com_colony(ts))
    r = list(np.arange(0, D, dr))
    ans = compute_correlation_length_per_particle(my_particle=ts[0], r=r, timestep=ts)
    for i, particle_of_interest in enumerate(ts[1:]):
        my_arr = compute_correlation_length_per_particle(my_particle=particle_of_interest, r=r, timestep=ts)
        ans = np.vstack((ans, my_arr))
        pdone = int( (i+1)/len(ts) * 40 )
        print("|" + pdone*'#' + (40 - pdone)*'-' + '|')
    mean = np.nanmean(ans, 0)
    mean[np.isnan(mean)] = 1
    plt.plot(r, mean, label="Mean Global Order Parameter within annulus")
    mask = 0.9 > mean
    mask2 = mean > 0.2
    mask &= mask2
    data_for_fit = mean[mask]
    r = np.array(r)
    x_for_fit = r[mask]
    popt, pcov = curve_fit(exponential_fit, x_for_fit, data_for_fit)
    plt.plot(r, exponential_fit(r, popt[0], popt[1]),
             label=("Exponential fit with " + r'$\xi$' +
                    " = {:4.2f}".format(popt[1])))
    plt.title("Correlation length analysis")
    plt.xlabel("Inner radius of annulus with width {:f}".format(dr))
    plt.ylabel("Mean global order parameter within annulus")
    plt.legend()
    plt.show()
