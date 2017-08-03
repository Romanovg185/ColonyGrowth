from Colony_Analysis.Particle_Data import ParticleData, format_data
from Colony_Analysis.Internal_OP import get_mean_internal_op
from Colony_Analysis.Global_OP import get_mean_global_op
from Colony_Analysis.Correlation_Length import get_mean_gop_per_radius, fit_exponential
from Colony_Analysis.Pressure_Profile import get_pressure_profile
from Colony_Analysis.Edge_Smoothness import get_smoothness
from Colony_Analysis.Find_Defects import get_defects


class RunData(object):
    """Object that stores all possible data related to a single run"""
    dictionary_np_to_ar = {
        1: [3, 4, 5, 6, 7],
        3: [4, 5, 6, 7]
    }

    def __init__(self, folder):
        self.folder = folder
        self.n_pivot = int(folder[folder.find('np=') + 3])  # Find character after "np=" in folder name
        self.raw_data = {}
        self.internal_op_data = {}
        self.global_op_data = {}
        self.correlation_length_data = {}
        self.exponential_fit = {}
        self.xi = {}
        self.pressure_profile = {}
        self.smoothness = {}
        self.defects = {}

    def load_raw_data(self):
        """Gets raw data in the format of dicts with key AR to whole datasets"""
        for i in self.dictionary_np_to_ar[self.n_pivot]:
            file_name = (self.folder + '/result' + str(i) + '.txt')
            f = open(file_name)
            data = format_data(f, self.n_pivot)
            self.raw_data[i] = data

    def compute_internal_op(self):
        """Data in the format of AR mapping to list of (N, mean(iOP), std(iOP))"""
        for i in self.dictionary_np_to_ar[self.n_pivot]:
            data = self.raw_data[i]
            self.internal_op_data[i] = get_mean_internal_op(data)

    def compute_global_op(self):
        """Data in the format of AR mapping to list of (N, mean(gOP), std(gOP))"""
        for i in self.dictionary_np_to_ar[self.n_pivot]:
            data = self.raw_data[i]
            self.global_op_data[i] = get_mean_global_op(data)

    def compute_correlation_length(self):
        """Data in the format of AR mapping to list of (r, mean(gOP), std(gOP))"""
        for i in self.dictionary_np_to_ar[self.n_pivot]:
            data = self.raw_data[i]
            self.correlation_length_data[i] = get_mean_gop_per_radius(data)

    def fit_exponential(self):
        for i in self.dictionary_np_to_ar[self.n_pivot]:
            data = self.correlation_length_data[i]
            ans = fit_exponential(data)
            self.xi[i] = ans[0]
            self.exponential_fit[i] = ans[1]

    def compute_pressure_profile(self):
        for i in self.dictionary_np_to_ar[self.n_pivot]:
            data = self.raw_data[i]
            self.pressure_profile[i] = get_pressure_profile(data)

    def compute_smoothness(self):
        """Data in the format (N, [ang1, ang2, ...])"""
        for i in self.dictionary_np_to_ar[self.n_pivot]:
            data = self.raw_data[i]
            self.smoothness[i] = get_smoothness(data)

    def compute_defects(self):
        """Data in the format of AR mapping to list of lists of (index1, index2, index3, sign)"""
        for i in self.dictionary_np_to_ar[self.n_pivot]:
            data = self.raw_data[i]
            self.defects[i] = get_defects(data, self.n_pivot)


    def compute_all(self):
        self.load_raw_data()
        print("Loading raw data done")
        self.compute_internal_op()
        print("Internal OP done")
        self.compute_global_op()
        print("Global OP done")
        self.compute_correlation_length()
        print("Correlation length done")
        self.fit_exponential()
        print("Fitting done")
        self.compute_pressure_profile()
        print("Pressure profile done")
        self.compute_smoothness()
        print("Smoothness done")
        #self.compute_defects()
        #print("Defects done")
