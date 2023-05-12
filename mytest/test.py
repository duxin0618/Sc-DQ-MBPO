import numpy as np
def compute_mean():
    filename = './mean_info.npy'
    data = np.load(filename, allow_pickle=True).item()
    a = list(data.keys())
    a.sort()
    real_Q_1 = []
    real_Q_2 = []
    src_Q_1 = []
    src_Q_2 = []
    for i in a:
        real_Q_1.append(data[i]['real_Q_1'])
        real_Q_2.append(data[i]['real_Q_2'])
        src_Q_1.append(data[i]['src_Q_1'])
        src_Q_2.append(data[i]['src_Q_2'])

    np.save('mean_real_Q_1.npy', real_Q_1)
    np.save('mean_real_Q_2.npy', real_Q_2)
    np.save('mean_src_Q_1.npy', src_Q_1)
    np.save('mean_src_Q_2.npy', src_Q_2)

def compute_div():
    filename = './mean_info.npy'
    data = np.load(filename, allow_pickle=True).item()
    a = list(data.keys())
    a.sort()
    Q_1 = []
    Q_2 = []
    for i in a:
        Q_1.append(data[i]['real_Q_1'] - data[i]['src_Q_1'])
        Q_2.append(data[i]['real_Q_2'] - data[i]['src_Q_2'])

    np.save('mean_Q_1_div.npy', Q_1)
    np.save('mean_Q_2_div.npy', Q_2)

compute_div()


