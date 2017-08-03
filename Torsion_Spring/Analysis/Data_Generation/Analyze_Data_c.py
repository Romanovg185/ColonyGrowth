from Colony_Analysis.Run_Data import RunData
import sys
import pickle

if __name__ == '__main__':
    my_data_set = RunData(sys.argv[1])
    my_data_set.load_raw_data()
    my_data_set.compute_correlation_length()
    my_data_set.fit_exponential()
    for i in [4, 5, 6, 7]:
        fil = open(sys.argv[1] + '_cc_' + str(i) + '_.p', "wb")
        pickle.dump(my_data_set.correlation_length_data[i], fil)
        fil.close()
        f = open(sys.argv[1] + '_xi' + str(i) + '_.txt', 'w')
        f.write(str(my_data_set.xi[i]))
        f.close()
