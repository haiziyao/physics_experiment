# @Version : 1.1
# @Author  : 亥子曜
# @File    : form2.py
# @Time    : 2025/11/3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
def form2_cal():
    # 读取数据
    path = "./data/form2.CSV"
    form = pd.read_csv(path, encoding='GBK', header=None)
    form.iloc[:,0] = ["d", "d^2", "Ih"]
    form = form.set_index(0)

    # 准备数据
    x = form.loc["d^2"].values   # 横坐标
    y = form.loc["Ih"].values    # 纵坐标

    # 线性拟合
    coeff = np.polyfit(x, y, 1)
    slope = coeff[0]
    intercept = coeff[1]
    y_fit = slope * x + intercept

    # 绘图
    plt.figure()
    plt.scatter(x, y, color="blue", label="原始数据")
    plt.plot(x, y_fit, color="red", label=f"拟合直线: y={slope:.2f}x+{intercept:.2f}")
    plt.xlabel("d^2 / mm^2")
    plt.ylabel("Ih / 10^-11 A")
    plt.grid()
    plt.legend()
    plt.savefig("./result/result2.png")

