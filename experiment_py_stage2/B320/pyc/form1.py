# @Version : 1.0
# @Author  : 亥子曜
# @File    : form1.py
# @Time    : 2025/10/30 9:19

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from scipy.interpolate import make_interp_spline


plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def form1_cal():
    path = "./data/form1.CSV"
    form = pd.read_csv(path,encoding='GBK',header=None)

    form.iloc[:,0] = ["Ua","Id2","Id4"]
    form = form.set_index(0)

    x2 = form.iloc[1,:].values
    x4 = form.iloc[2,:].values
    Ua = form.iloc[0,:].values
    xnew = np.linspace(Ua.min(), Ua.max(), 200)

    spl2 = make_interp_spline(Ua, x2, k=3)
    x2_smooth = spl2(xnew)

    spl4 = make_interp_spline(Ua, x4, k=3)
    x4_smooth = spl4(xnew)

    plt.figure()
    plt.scatter(Ua,x2,label="d=2mm",color="red")
    plt.scatter(Ua,x4,label="d=4mm",color="blue")
    plt.plot(xnew, x2_smooth, color="red")   # 拟合曲线
    plt.plot(xnew, x4_smooth, color="blue")  # 拟合曲线
    plt.grid()
    plt.ylabel("I/10^-11 A")
    plt.xlabel("Uak / V")
    plt.title("作者还没看标题")
    plt.legend()

    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:.2f}'))
    plt.savefig("./result/result1.png")
