# -*- coding: utf-8 -*-
# File  : MCR.py
# Author: xinyuLu
# Date  : 2021/4/28

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.preprocessing import MinMaxScaler

import logging
from pymcr.mcr import McrAR

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
max_iter = 10
oil_path = r'D:\ProgrammingProjects\Dataset\YXX\background\oil.txt'
glass_path = r'D:\ProgrammingProjects\Dataset\YXX\background\glass.txt'
dir_path = r'D:\ProgrammingProjects\Dataset\SLT\20210425'
save_dir = r'D:\ProgrammingProjects\Dataset\SLT\20210425\img_set'
files = ['n-6-1', 'n-6-2', 'n-6-3', 'n-6-4', 'a-8-1', 'a-8-2', 'a-8-3', 'a-8-4', 'a-8-5']


# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
def main():
    for item in files:
        cell_path = os.path.join(dir_path, item+'.txt')

        def preprocess(x):
            min_max = MinMaxScaler()
            x = min_max.fit_transform(x)
            return x

        oil = np.loadtxt(oil_path)[:, -1]
        glass = np.loadtxt(glass_path)[:, -1]

        def load_data(data_path):
            df = pd.read_csv(data_path, delimiter='\t')

            Wave = df.iloc[:, 0].to_numpy()
            data = df.iloc[:, 1:-1].to_numpy()

            data = preprocess(data)

            fig = plt.figure()
            ax1 = fig.add_subplot(2, 2, 1)
            ax1.plot(Wave, data.mean(1))
            ax2 = fig.add_subplot(2, 2, 3)
            ax2.imshow(data[1255, :].reshape(-1, 400))
            ax2.set_title('2900cm')
            ax3 = fig.add_subplot(2, 2, 4)
            ax3.imshow(data[79, :].reshape(-1, 400))
            ax3.set_title('750cm')
            return data, Wave

        cell, wave = load_data(cell_path)

        init_st = np.c_[cell.mean(1), oil, glass]

        # MCR

        logger = logging.getLogger('pymcr')
        logger.setLevel(logging.DEBUG)

        # StdOut is a "stream"; thus, StreamHandler
        stdout_handler = logging.StreamHandler(stream=sys.stdout)

        # Set the message format. Simple and removing log level or date info
        stdout_format = logging.Formatter('%(message)s')  # Just a basic message akin to print statements
        stdout_handler.setFormatter(stdout_format)
        logger.addHandler(stdout_handler)

        mcrar = McrAR(max_iter=max_iter, tol_increase=1e3)
        mcrar.fit(cell.T, ST=init_st.T, verbose=True)
        print('\nFinal MSE: ', mcrar.err[-1])
        fig2 = plt.figure(figsize=(60, 60))
        for i in range(mcrar.C_opt_.shape[1]):
            ax1 = fig2.add_subplot(mcrar.C_opt_.shape[1], 2, i * 2 + 1)
            ax1.imshow(mcrar.C_opt_[:, i].reshape(-1, 400))
            ax1.set_title('%d th mcr pic' % (i + 1))
            # fig2.colorbar(ax1, ax=ax1)
            ax2 = fig2.add_subplot(mcrar.C_opt_.shape[1], 2, i * 2 + 2)
            ax2.plot(wave, mcrar.ST_opt_[i, :])
            ax2.set_title('%d th mcr spec' % (i + 1))
            ax2.set_yticks([])
        fig2.savefig(os.path.join(save_dir, item))
        plt.figure()
        plt.plot(range(len(mcrar.err)), mcrar.err)
        plt.title('MCR Error')
        # plt.show()


if __name__ == '__main__':
    main()
