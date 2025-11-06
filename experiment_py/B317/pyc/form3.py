# @Version : 1.0
# @Author  : 亥子曜
# @File    : form3.py
# @Time    : 2025/10/23 13:10
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.interpolate import make_interp_spline
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def form3_cal(k):
    path = './data/frame3.CSV'
    form = pd.read_csv(path,encoding='GBK')
    form  = form.drop(index=0)
    form.columns = ['X','U1l','U1r','U2l','U2r','U3l','U3r','U4l','U4r','Uhl','Uhr','Bl','Br',]
    form = form.astype(float)
    form['Uhl'] = ((form['U1l'].abs() + form['U2l'].abs() + form['U3l'].abs() + form['U4l'].abs()) / 4).round(2)
    form['Uhr'] = ((form['U1r'].abs() + form['U2r'].abs() + form['U3r'].abs() + form['U4r'].abs()) / 4).round(2)

    mu0 = 4 * math.pi * 10 ** (-7)  # 真空磁导率（H/m）
    N = 3000  # 总匝数
    L = 276 * 10 ** (-3)  # 螺线管长度（m，原276mm）
    r = 40 * 10 ** (-3)  # 内径（m，原40mm，补充单位转换）
    R = 56 * 10 ** (-3)  # 外径（m，原56mm）
    Im = 800 * 10 ** (-3)  # 电流（A，原800mA）
    Ich = 5 * 10 ** (-3)  # 电流（A，原5mA）
    n = N / L  # 单位长度匝数（匝/m）
    q = 1.602 * 10**(-19)
    d = 260* 10**(-6)
    B0= (mu0 * N * Im)/math.sqrt(math.pow(L,2)+math.pow(R,2))
    KH = k/B0
    n = 1/(KH*q*d)
    form['Bl'] = (form['Uhl']/(KH*Ich)).round(2)
    form['Br'] = (form['Uhr']/(KH*Ich)).round(2)
    form.to_excel('./results/from3.xlsx')
    B = ((form['Bl'].abs() + form['Br'].abs()) / 2).values
    X = form['X']

    x_smooth = np.linspace(X.min(), X.max(), 300)  # 生成更多的点以保证平滑
    spl = make_interp_spline(X, B, k=3)  # 3次样条插值
    B_smooth = spl(x_smooth)


    plt.figure()
    plt.scatter(X, B, label='原始数据', color='blue')
    plt.plot(x_smooth, B_smooth, label='平滑曲线', color='red', linewidth=2)
    plt.xlabel('X / mm')
    plt.ylabel('B / T')
    plt.title('B-X的关系  平滑曲线采用三次插值')
    plt.legend()
    plt.grid(True)
    plt.savefig("./results/result3.png")
    return KH,n