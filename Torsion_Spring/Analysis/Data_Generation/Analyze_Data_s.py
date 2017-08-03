from Colony_Analysis.Run_Data import RunData
import sys
import pickle

if __name__ == '__main__':
    my_data_set = RunData(sys.argv[1])
    my_data_set.load_raw_data()
    my_data_set.compute_smoothness()
    for i in [4, 5, 6, 7]:
        fil = open(sys.argv[1] + '_ss_' + str(i) + '_.p', "wb")
        pickle.dump(my_data_set.smoothness[i], fil)
        fil.close()
