import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def div(a, b):
    return np.array(a) - np.array(b)

def add(a, b):
    return np.array(a) + np.array(b)

filenames = ['../Q_info/Q_epoch_19_750.npy', '../Q_info/Q_epoch_19_500.npy']
data_arr = []
for i in filenames:
    data_arr.append(np.load(i, allow_pickle=True).item())

h_real_Q_1_mean = []
h_src_Q_1_mean = []
h_real_Q_1_var = []
h_src_Q_1_var = []
h_real_Q_1_var2 = []

h_div_Q_1_mean = []
h_div_Q_1_var = []

data1_h_div_Q_1_mean = []
data1_h_div_Q_1_var = []
std_data = []
keys = ['h_1', 'h_2', 'h_3', 'h_4', 'h_5', 'h_6', 'h_7', 'h_8']
for k in keys:
    # h_div_Q_1_mean.append((data[k]['real_Q_1'] - data[k]['src_Q_1']).mean())
    for da in data_arr:
        std_data.append((da[k]['real_Q_1'] - da[k]['src_Q_1']).mean())

# 计算均值
mean_a = np.mean(np.array(std_data).reshape(-1, len(filenames)), axis=1)
print(mean_a)

# 计算方差
std_a = np.std(np.array(std_data).reshape(-1, len(filenames)), axis=1)
print(std_a)


# a = range(len(data.keys()))
# div = np.array(h_real_Q_1_mean) - np.array(h_src_Q_1_mean)
a = range(len(keys))
plt.plot(a, mean_a, linewidth=1.5, label='mbpo', c="#1f77b4")
plt.fill_between(a, div(mean_a, std_a), add(mean_a, std_a), color="#1f77b4", alpha=0.25)
#
plt.grid()
plt.legend()

savepath = 'test_h_div_mean.png'
plt.savefig(savepath, dpi=400)