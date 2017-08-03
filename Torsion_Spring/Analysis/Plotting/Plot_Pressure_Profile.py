import numpy as np
import pickle
import matplotlib.pyplot as plt

n_runs = 10
folder_name = 'np=1'
Nparticles = 3500

x = np.arange(0, Nparticles, 1)
y = {0.001:{}, 0.002:{}, 0.0033:{}, 0.005:{}, 0.008:{}, 0.01:{}, 0.02:{}, 0.033:{}, 0.05:{}}
for z in [0.001, 0.002, 0.0033, 0.005, 0.008, 0.01, 0.02, 0.033, 0.05]:
    for i in x:
        y[z][i] = []

for i in range(n_runs):
    for k, v in y.items():
        run_name = str(k) + '_' + folder_name + '_' + str(i) + '_pp_5_.p'
        print("Start pickling")
        my_data = pickle.load(open(run_name, 'rb'))
        for j, ts in enumerate(my_data):
            if len(ts) > Nparticles:
                l = j
                break
        for el in my_data[l]:
            y[k][int(np.floor(el[0]))].append(el[1])
    del(my_data)

print(y)

for ar in y:
    xplot = []
    yplot = []
    for key, val in y[ar].items():
        if len(val) != 0:
            xplot.append(key)
            yplot.append(np.mean(val))
    plt.plot(xplot, yplot, label='κ = {}'.format(ar))
plt.legend()
plt.title("Mean pressure profile of a colony of {} particles".format(Nparticles))
plt.xlabel("Distance from the center of the colony")
plt.ylabel("Mean pressure")
plt.show()
