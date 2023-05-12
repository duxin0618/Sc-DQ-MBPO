import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def div(a, b):
    return np.array(a) - np.array(b)

def add(a, b):
    return np.array(a) + np.array(b)

data = np.load('../Q_info/Q_epoch_19_750.npy', allow_pickle=True).item()
print(data.keys())
h_real_Q_1_mean = []
h_src_Q_1_mean = []
h_real_Q_1_var = []
h_src_Q_1_var = []
h_real_Q_1_var2 = []
for k in data.keys():
    # h_real_Q_1_mean.append(data[k]['real_Q_1'].mean())
    # h_real_Q_1_var.append(data[k]['real_Q_1'].var())
    # h_src_Q_1_mean.append(data[k]['src_Q_1'].mean())
    # h_src_Q_1_var.append(data[k]['src_Q_1'].var())

    h_real_Q_1_mean.append((data[k]['real_Q_1'] - data[k]['src_Q_1']).mean())
    h_real_Q_1_var.append((data[k]['real_Q_1'] - data[k]['src_Q_1']).var())
    # h_real_Q_1_var2.append((data[k]['real_Q_1'] - data[k]['src_Q_1']).var())
# print(h_real_Q_1_mean)
# print(h_real_Q_1_var)
# print(h_real_Q_1_var2)
# print(div(h_real_Q_1_mean, h_real_Q_1_var))
# print(add(h_real_Q_1_mean, h_real_Q_1_var))

a = range(len(data.keys()))
# div = np.array(h_real_Q_1_mean) - np.array(h_src_Q_1_mean)
plt.plot(a, h_real_Q_1_mean, linewidth=1.5, label='mbpo', c="#1f77b4")
# plt.plot(a, h_src_Q_1_mean, linewidth=1.5, label='src', c="#CCFF33")
# plt.plot(a, div, linewidth=1.5, label='src', c="#CCFF33")
plt.fill_between(a, div(h_real_Q_1_mean, h_real_Q_1_var), add(h_real_Q_1_mean, h_real_Q_1_var), color="#1f77b4", alpha=0.25)
# plt.fill_between(a, div(h_src_Q_1_mean, h_src_Q_1_var), add(h_src_Q_1_mean, h_src_Q_1_var), color="#CCFF33", alpha=0.25)
plt.grid()
plt.legend()

savepath = 'test_h_mean_div_var.png'
plt.savefig(savepath, dpi=400)
