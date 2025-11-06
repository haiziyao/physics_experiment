# @Version : 1.0
# @Author  : 亥子曜
# @File    : form1.py.py
# @Time    : 2025/10/23 13:08
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
def form1_cal():
    path = './data/frame1.CSV'
    form = pd.read_csv(path,encoding='GBK')
    form.columns = ['Ich', 'U1', 'U2', 'U3', 'U4','U']
    print(form.columns)
    form['U'] =  ((form['U1'].abs() +form['U2'].abs() +form['U3'].abs()+form['U4'].abs())/4).round(2)
    form.to_excel('./results/from1.xlsx')
    Im = 600 #  单位mA\
    x = form['Ich'].values
    y = form['U'].values
    cof  = np.polyfit(x,y,1)
    k = cof[0]
    b = cof[1]
    y_fit = k*x+b
    plt.figure()
    plt.scatter(x, y, label='原始数据', color='blue')
    plt.plot(x,y_fit,label=f"拟合直线y = {k:.2f}x {b:.2f} ",color='red' )
    plt.xlabel('Ich / mA')
    plt.ylabel('U / mV')
    plt.title('Ich与U的关系及线性拟合')
    plt.legend()
    plt.grid(True)
    plt.savefig("./results/result1.png")
    return k