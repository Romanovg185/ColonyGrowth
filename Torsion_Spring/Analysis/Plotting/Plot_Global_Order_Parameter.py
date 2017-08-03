import pickle
import matplotlib.pyplot as plt
import numpy as np


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
if aspect_ratio == '0' and plot_type == 'All':
    raise ValueError('You do not want spaghetti on your screen I think!')

# plot for a single AR
if aspect_ratio != '0':
    for i in range(offset, amount_of_files):
        run_name = folder_name + '_' + str(i) + '.p'
        my_data = pickle.load(open(run_name, 'rb'))
        aspect_ratio = int(aspect_ratio)
        data_to_plot = my_data
        data_to_plot = zip(*data_to_plot)
        my_data_to_plot = [[*x] for x in data_to_plot]
        if plot_type == 'All':
            plt.plot(my_data_to_plot[0], np.abs(my_data_to_plot[1]))
            plt.title('Average global order parameter vs #particles')
        elif plot_type == 'Mean':
            data_right_length = np.interp(np.arange(4000), my_data_to_plot[0], my_data_to_plot[1])
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
        plt.plot(np.arange(0, len(mean))[mask], np.abs(mean[mask]))
        plt.title('Mean of average global order parameter vs #particles')

# plot the mean for all AR
if aspect_ratio == '0':
    for ar in [0.001, 0.002, 0.0033, 0.005, 0.008, 0.01, 0.02, 0.033, 0.05]:
        for i in range(offset, amount_of_files):
            run_name = str(ar) + '_' + folder_name + '_' + str(i) + '_gg_5_.p'
            print("Before pickle, ar {}".format(ar))
            my_data = pickle.load(open(run_name, 'rb'))
            print("After pickle")
            aspect_ratio = int(ar)
            data_to_plot = my_data
            del(my_data)
            data_to_plot = zip(*data_to_plot)
            my_data_to_plot = [[*x] for x in data_to_plot]
            interpolated_data = np.interp(np.arange(4000), my_data_to_plot[0], my_data_to_plot[1])
            if i == offset:
                make_mean = np.array(interpolated_data)
            else:
                make_mean = np.vstack((make_mean, interpolated_data))
            print(make_mean)
        mean = np.nanmean(make_mean, 0)
        mask = np.isnan(mean)
        mask = np.array([not i for i in mask])
        x = np.arange(0, len(mean))[mask]
        y = mean[mask]
        interpolated_data = np.interp(x, x, y)
        plt.plot(x, np.abs(interpolated_data), label='κ = {}'.format(ar))
    plt.legend()

plt.xlabel('Number of particles')
plt.ylabel('Global order parameter')
plt.show()
