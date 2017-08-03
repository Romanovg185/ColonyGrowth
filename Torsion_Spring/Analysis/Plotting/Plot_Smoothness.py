import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.optimize import curve_fit

angles = []
folder_name = "np=1"

mu_dict = dict(zip([0.001, 0.002, 0.0033, 0.005, 0.008, 0.02, 0.033, 0.05],
                    [[], [], [], [], [], [], [], [], [], []]))

def gauss(x, A, mu, sigma):
  return A*np.exp(-(x-mu)**2/(2.*sigma**2))

fig, ax = plt.subplots(1, 1)

foo = 0
for run in range(10):
  for ar in [0.001, 0.002, 0.0033, 0.005, 0.008, 0.02, 0.033, 0.05]:
    print("Loading pickle")
    file_name = str(ar) + '_' + folder_name + '_' + str(run)  + '_ss_' + '5_.p'
    print(file_name)
    data = pickle.load(open(file_name, 'rb'))
    my_data = data
    for i, element in enumerate(my_data):
      if i < len(my_data) - 1:
          continue
      for subel in element[1]:
        mu_dict[ar].append(subel)
    foo += 1
  del(data)
print(foo)
d = {0.001: '#1f77b4', 0.002: '#ff7f0e', 0.0033: '#2ca02c', 0.005: '#d62728', 0.008: '#9467bd', 0.01:'#8c564b', 0.02:'#e377c2', 0.033:'#7f7f7f', 0.05:'#bcbd22', 7:'#17becf'}

for ar in sorted(mu_dict):
  y = mu_dict[ar]
  z, binEdges = np.histogram(np.array(y), bins=50)
  bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
  mean = np.mean(y)
  sigma = np.std(y)
  xx = np.linspace(min(y), max(y), 50)
  ax.plot(bincenters, z, c=d[ar], label=r"$\kappa$ = {0:3.3f}, $\sigma$={1:4.3f}".format(ar, sigma))
  p0 = [1., 0., 1.]
  coeff, var_matrix = curve_fit(gauss, bincenters, z)
  hist_fit = gauss(bincenters, coeff[0], coeff[1], coeff[2])
  #plt.plot(xx, z*mlab.normpdf(xx, mean, sigma), ls=':', c=d[ar])
plt.legend()
plt.title("Smoothness for one pivot")
ax.set_ylabel("Frequency")
ax.set_xlabel("Angle")
x_tick = np.array([0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1])
x_label = [r"$0$", r"$\frac{\pi}{8}$",   r"$\frac{\pi}{4}$", r"$\frac{3\pi}{8}$", r"$\frac{\pi}{2}$", r"$\frac{5\pi}{8}$", r"$\frac{3\pi}{4}$",   r"$\frac{7\pi}{8}$", r"$\frac{3\pi}{2}$", r"$\pi$"]
ax.set_xticks(x_tick*np.pi)
ax.set_xticklabels(x_label, fontsize=10)
plt.show()
