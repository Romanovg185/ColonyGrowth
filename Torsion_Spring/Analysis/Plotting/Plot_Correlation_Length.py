import matplotlib.pyplot as plt
ans = []
for i in [0.001, 0.002, 0.0033, 0.005, 0.008, 0.01, 0.02, 0.033, 0.05]:
    my_data = []
    for run in range(10):
        name = "{0}_np=1_{1}_xi5_.txt".format(i, run)
        data = open(name)
        for line in data:
            my_data.append(float(line))
    ans.append(sum(my_data)/10)
plt.semilogx([0.001, 0.002, 0.0033, 0.005, 0.008, 0.01, 0.02, 0.033, 0.5], ans)
plt.xlabel("Torsional spring constant")
plt.ylabel("Correlation length")
plt.show()
