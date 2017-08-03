import pickle
#from Run_Data import RunData
import matplotlib.pyplot as plt
import numpy as np
import struct

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

folder_name = input("Folder name please? ")
amount_of_files = input("Amount of files? ")
amount_of_files = int(amount_of_files)
plot_type = input("Mean or all? ")
aspect_ratio = input("Aspect ratio? ")
if amount_of_files == 1 and plot_type == 'Mean':
    raise ValueError('You cannot take the mean of a single element!')
if aspect_ratio == '0' and plot_type == 'All' and amount_of_files != 1:
    raise ValueError('You do not want spaghetti on your screen I think!')

# plot for a single AR
if aspect_ratio != '0':
    for i in range(offset, amount_of_files):
        run_name = folder_name + '_' + str(i) + '.p'
        print("Before pickle")
        my_data = pickle.load(open(run_name, 'rb'))
        print("After pickle")
        aspect_ratio = int(aspect_ratio)
        data_to_plot = my_data.internal_op_data[aspect_ratio]
        del(my_data)
        data_to_plot = zip(*data_to_plot)
        my_data_to_plot = [[*x] for x in data_to_plot]
        if plot_type == 'All':
            plt.plot(my_data_to_plot[0], my_data_to_plot[1])
            plt.title('Average internal order parameter vs #particles')
        elif plot_type == 'Mean':
            data_right_length = make_data_right_length(my_data_to_plot)
            if i == offset:
                make_mean = np.array(data_right_length)
            else:
                make_mean = np.vstack((make_mean, data_right_length))
    if plot_type == 'Mean':
        mean = np.nanmean(make_mean, 0)
        mask = np.isnan(mean)
        mask = np.array([not i for i in mask])
        x = np.arange(0, len(mean))[mask]
        y = mean[mask]
        plt.plot(np.arange(0, len(mean))[mask], mean[mask])
        plt.title('Mean of average internal order parameter vs #particles')

# plot for all AR the mean
if aspect_ratio == '0':
    erbar = {0.001: [[], [], [], [], [], [], [], []],
             0.002: [[], [], [], [], [], [], [], []], 
             0.0033: [[], [], [], [], [], [], [], []],
             0.005: [[], [], [], [], [], [], [], []],
             0.008: [[], [], [], [], [], [], [], []],
             0.01: [[], [], [], [], [], [], [], []],
             0.02: [[], [], [], [], [], [], [], []],
             0.033: [[], [], [], [], [], [], [], []],
             0.05: [[], [], [], [], [], [], [], []],
             }
    for ar in [0.001, 0.002, 0.0033, 0.005, 0.008, 0.01, 0.02, 0.033, 0.05]:
        for i in range(offset, amount_of_files):
            run_name = str(ar) + '_' + folder_name + '_' + str(i) + '_ii_5_.p'
            print("Ready to load pickle")
            my_data = pickle.load(open(run_name, 'rb'))
            print("Pickle loaded")
            aspect_ratio = int(ar)
            data_to_plot = my_data
            data_to_plot = zip(*data_to_plot)
            my_data_to_plot = [[*x] for x in data_to_plot]
            data_right_length = np.interp(np.arange(4000), my_data_to_plot[0], my_data_to_plot[1])
            if i == offset:
                make_mean = np.array(data_right_length)
            else:
                make_mean = np.vstack((make_mean, data_right_length))
            # Playing for the error bars
            for k, j in enumerate([500, 1000, 1500, 2000, 2500, 3000, 3500, 4000]):
                jj = j
                #print(my_data_to_plot[0])
                while jj not in my_data_to_plot[0]:
                    jj -= 1
                    #print(jj)
                index = my_data_to_plot[0].index(jj)
                erbar[ar][k].append((my_data_to_plot[0][index], my_data_to_plot[1][index], my_data_to_plot[2][index]))
        mean = np.nanmean(make_mean, 0)
        mask = np.isnan(mean)
        mask = np.array([not i for i in mask])
        x = np.arange(0, len(mean))[mask]
        y = mean[mask]


        plt.plot(np.arange(0, len(mean))[mask], mean[mask], label='κ = {}'.format(ar))

    plt.legend()
#print(erbar)
d = {0.001: '#1f77b4', 0.002: '#ff7f0e', 0.0033: '#2ca02c', 0.005: '#d62728', 0.008: '#9467bd', 0.01:'#8c564b', 0.02:'#e377c2', 0.033:'#7f7f7f', 0.05:'#bcbd22', 7:'#17becf'}
for key, el in erbar.items():
    x = []
    y = []
    s = []
    for q, n in enumerate(el):
        #print(n)
        x.append(500*(q+1) + 5*(key-2))
        width_error_bar = 1 - np.mean([o[1] for o in n]) + np.mean([o[2] for o in n])
        y.append(1 - width_error_bar/2)
        s.append(width_error_bar/2)
    plt.errorbar(x, y, yerr=s, fmt="none", ecolor=d[key], capsize=5)
plt.xlabel('Number of particles')
plt.ylabel('Internal order parameter')
plt.show()
