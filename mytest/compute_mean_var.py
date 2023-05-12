import os

import numpy as np

file_dir = '../Q_info/'

def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range

mean_info = {}
var_info = {}
for filepath, dir_names, filenames in os.walk(file_dir):
    for filename in filenames:
        name = filepath+filename
        data = np.load(name, allow_pickle=True).item()

        save_name = int(filename.split('.')[0].split('_')[2]) * 1000 + int(filename.split('.')[0].split('_')[3])
        real_Q_1 = data['h_1']['real_Q_1']
        real_Q_2 = data['h_1']['real_Q_2']
        src_Q_1 = data['h_1']['src_Q_1']
        src_Q_2 = data['h_1']['src_Q_2']

        real_Q_1 = normalization(real_Q_1)
        real_Q_2 = normalization(real_Q_2)
        src_Q_1 = normalization(src_Q_1)
        src_Q_2 = normalization(src_Q_2)

        real_Q_1_mean = real_Q_1.mean()
        real_Q_2_mean = real_Q_2.mean()
        src_Q_1_mean = src_Q_1.mean()
        src_Q_2_mean = src_Q_2.mean()

        real_Q_1_var = real_Q_1.var()
        real_Q_2_var = real_Q_2.var()
        src_Q_1_var = src_Q_1.var()
        src_Q_2_var = src_Q_2.var()

        # {文件名:{real_Q_1: value}}
        mean_data = {}
        mean_data['real_Q_1'] = real_Q_1_mean
        mean_data['real_Q_2'] = real_Q_2_mean
        mean_data['src_Q_1'] = src_Q_1_mean
        mean_data['src_Q_2'] = src_Q_2_mean

        var_data = {}
        var_data['real_Q_1'] = real_Q_1_var
        var_data['real_Q_2'] = real_Q_2_var
        var_data['src_Q_1'] = src_Q_1_var
        var_data['src_Q_2'] = src_Q_2_var

        mean_info[save_name] = mean_data
        var_info[save_name] = var_data

np.save('./mean_info', mean_info)
np.save('./var_info', var_info)
