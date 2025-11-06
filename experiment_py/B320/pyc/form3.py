# @Version : 1.0
# @Author  : 亥子曜
# @File    : form3.py
# @Time    : 2025/10/30 9:36
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def form3_cal():
    path = "./data/form3.CSV"
    form = pd.read_csv(path,encoding='GBK',header=None)
    form.iloc[:,0] = ['lambda','f','Ua']
    form = form.set_index(form.columns[0])
    c = 3*10**8  # m
    form.loc['f'] = c/form.loc['lambda'] *10**(-5)
    form.loc['f'] = form.loc['f'].round(2)
    form.to_excel("./result/from3.xlsx")
    x = abs(form.loc["f"])
    y = abs(form.loc["Ua"])
    cof = np.polyfit(x,y,1)
    k = cof[0]
    b = cof[1]
    y_fit = k*x+b
    plt.figure()
    plt.scatter(x,y,label='原始数据',color='blue')
    plt.plot(x,y_fit,label=f"拟合直线Ua = {k:.2f}x + {b:.2f}",color = 'red')
    plt.xlabel('f/10^14Hz')
    plt.ylabel('Ua/V')
    plt.legend()
    plt.grid(True)
    plt.savefig("./result/result3.png")
    e = 1.602
    h = k*e*10
    h_ = 6.626
    percent_error_h = abs(h-h_)/h_*100
    return k.round(3),b.round(3),h.round(3),percent_error_h.round(2)
