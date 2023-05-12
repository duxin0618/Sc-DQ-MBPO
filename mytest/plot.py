import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range

def standardization(data):
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma

colors = {
	'mbpo': '#1f77b4',
	'src': '#CCFF33'
}

# tasks = ['inverted_pendulum', 'hopper', 'walker2d', 'ant', 'cheetah', 'humanoid']
algorithms = ['mbpo', 'src']
plt.clf()
# for alg in algorithms:
	## load results
fname1 = '../Q_info/Ant/Q_epoch_0_500.npy'
data = np.load(fname1, allow_pickle=True)
# print(data)
data1 = data.item()['h_1']['src_Q_1']

# a = range(len(data))
# plt.plot(a, data, linewidth=1.5, label=algorithms[0], c=colors['mbpo'])

# fname2 = './mean_Q_1_div.npy'
# data2 = np.load(fname2, allow_pickle=True)
data2 = data.item()['h_1']['real_Q_1']
a = range(len(data1))
data2 = data1 - data2
# data2 = normalization(data2)
plt.plot(a, data2, linewidth=1.5, label=algorithms[1], c=colors['src'])
# print("6: ", data2.mean(), data2.var())  # 6:  0.019729968, 0.030064154  # ;0.02568044,0.036305875
plt.grid()
plt.legend()

savepath = 'test_Q_div.png'
plt.savefig(savepath, dpi=400)




