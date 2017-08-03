import numpy as np
import matplotlib.pyplot as plt
import pickle

def mu(data_defects, raw_data):
    """Pass in a list of defects as returned by Run_Data and a list of raw_data"""
    for i in range(len(data_defects)):
        N = len(raw_data[i])
        timestep = data_defects[i]
        plus = 0
        minus = 0
        for defect in timestep:
            if defect[3]:
                plus += 1
            elif not defect[3]:
                minus += 1
        yield (N, plus, minus)

def interpolate_through_points(mu):
    X = []
    P = []
    N = []
    for i in mu:
        if i not in X:
            X.append(i[0])
            P.append(i[1])
            N.append(i[2])
    P_int = np.interp(np.arange(0, 4000), X, P)
    N_int = np.interp(np.arange(0, 4000), X, N)
    return (P_int, N_int)


plus_dict = {}
minus_dict = {}
for ii in [0.002, 0.005, 0.01, 0.05]:
  plus_dict[ii] = []
  minus_dict[ii] = []
  for i in range(10):
      plus_dict[ii].append([])
      minus_dict[ii].append([])
for run in range(10):
    for kappa in [0.002, 0.005, 0.01, 0.05]:
        print("Loading pickle")
        name_defects = '{}_np=1_{}_dd_5_.p'.format(kappa, run)
        name_iop = '{}_np=1_{}_zz_5_.p'.format(kappa, run)
        data_defects = pickle.load(open(name_defects, 'rb'))
        data_iop = pickle.load(open(name_iop, 'rb'))
        a = interpolate_through_points(mu(data_defects, data_iop))
        plus_dict[kappa][run] = a[0]
        minus_dict[kappa][run] = a[1]

print("Got halfway")

plusmean = {}
minusmean = {}
for i in plus_dict:
    M = np.array(plus_dict[i])
    plusmean[i] = np.mean(M, 0)
    print(plusmean[i])
    M = np.array(minus_dict[i])
    minusmean[i] = np.mean(M, 0)

d = {0.01: '#1f77b4', 0.02: '#ff7f0e', 0.033: '#2ca02c', 0.05: '#d62728', 0.001: '#9467bd'}
d = {0.002: '#1f77b4', 0.005: '#ff7f0e', 0.01: '#2ca02c', 0.05: '#d62728', 0.008: '#9467bd', 0.01:'#8c564b', 0.02:'#e377c2', 0.033:'#7f7f7f', 0.05:'#bcbd22', 7:'#17becf'}

for i in plusmean:
    plt.plot(np.arange(0, 4000), plusmean[i], ls='-', c=d[i], label='Plus defect, κ = {}'.format(i))
    plt.plot(np.arange(0, 4000), minusmean[i], ls=':', c=d[i], label='Minus defects, κ = {}'.format(i))
plt.title("Mean amount of defects vs number of particles for an aspect ratio of 5 and a single pivot")
plt.legend()
plt.xlabel("Amount of particles")
plt.ylabel("Amount of defects")
plt.show()
#
# for ar in range(3, 8):
#     plus = plus_dict[ar]
#     print(plus)
#     minus = minus_dict[ar]
#     m = 0
#     for el in plus_dict[ar]:
#         if len(el) > m:
#             m = len(el)
#     for el in plus:
#         while len(el) != m:
#             el.append(np.nan)
#     begin = np.array(plus[0])
#     for el in plus[1:]:
#         next = np.array(el)
#         begin = np.vstack((begin, next))
#     plusmean = np.nanmean(begin, 0)
#
#     for el in minus_dict[ar]:
#         if len(el) > m:
#             m = len(el)
#     for el in minus:
#         while len(el) != m:
#             el.append(np.nan)
#     begin = np.array(minus[0])
#     for el in minus[1:]:
#         next = np.array(el)
#         begin = np.vstack((begin, next))
#     minusmean = np.nanmean(begin, 0)
#
#     plt.plot(1000*np.arange(0, len(plusmean)), plusmean, ':')
#     plt.plot(1000*np.arange(0, len(minusmean)), minusmean, '-')
#     print(plusmean)
#     print(minusmean)
#     print(ar)
# plt.show()
