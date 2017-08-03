import pickle
#from Run_Data import RunData
import matplotlib.pyplot as plt
import numpy as np
import gc

def make_data_right_length(data):
    ans = []
    j = 0
    for i in range(4000):
        if i in data[0]:
            ans.append(data[1][j])
            j += 1
        else:
            ans.append(np.nan)
    return ans

offset = 0

amount_of_files = input("Amount of files? ")
amount_of_files = int(amount_of_files)
plot_type = input("Mean or all? ")
aspect_ratio = input("Aspect ratio? ")
if amount_of_files == 1 and plot_type == 'Mean':
    raise ValueError('You cannot take the mean of a single element!')
if aspect_ratio == '0' and plot_type == 'All':
    raise ValueError('You do not want spaghetti on your screen I think!')



d = {0.001: [], 0.002: [], 0.0033: [], 0.005: [], 0.008: [], 0.01: [], 0.02: [], 0.033:[], 0.05:[]}
for i in range(offset, amount_of_files+offset):
    for ar in [0.001, 0.002, 0.0033, 0.005, 0.008, 0.01, 0.02, 0.033, 0.05]:
        file_name = "{}_np=1_{}_cc_5_.p".format(ar, i)
        print("Start pickling")
        data_to_plot = pickle.load(open(file_name, 'rb'))
        print("Done pickling")
        data_to_plot = zip(*data_to_plot)
        my_data_to_plot = [[*x] for x in data_to_plot]
        data_right_length = my_data_to_plot[1][0:int(0.8 * len(my_data_to_plot[0]))]
        data_right_length = np.array(data_right_length)
        print(data_right_length.shape)
        if i == offset:
            d[ar] = np.array(data_right_length)
        elif i == offset + 1:
            mmshape = d[ar].shape
            print(mmshape)
            dshape = data_right_length.shape
            print(dshape)
            if dshape[0] < mmshape[0]:
                d[ar] = d[ar][0:dshape[0]]
            elif dshape[0] > mmshape[0]:
                data_right_length = data_right_length[0:mmshape[0]]
            d[ar] = np.vstack((d[ar], data_right_length))
        else:
            mmshape = d[ar].shape
            dshape = data_right_length.shape
            if dshape[0] < mmshape[1]:
                d[ar] = d[ar][:, 0:dshape[0]]
            elif dshape[0] > mmshape[1]:
                data_right_length = data_right_length[0:mmshape[1]]
            make_mean = np.vstack((d[ar], data_right_length))

for j in [0.001, 0.002, 0.0033, 0.005, 0.008, 0.01, 0.02, 0.033, 0.05]:
    mean = np.nanmean(d[j], 0)
    mask = np.isnan(mean)
    mask = np.array([not i for i in mask])
    x = np.arange(0, len(mean))[mask]
    y = mean[mask]
    plt.plot(0.2*x, y, label='κ = {}, '.format(j))

plt.title('Mean of global order parameter vs annulus radius for different torsion spring constants and one pivot')
plt.xlabel('Radius annulus [bacterial diameters]')
plt.ylabel('Mean global order parameter within annulus')
plt.legend()
plt.show()
