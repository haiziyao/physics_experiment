# @Version : 1.0
# @Author  : 亥子曜
# @File    : main2.py.py
# @Time    : 2025/9/27 23:45

# 电子质荷比的测定
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 数据定义
# 不同阳极加速电压Ua 和 励磁电流Is 下的阳极电流 Ia
# 不同电压下数据个数可能不一样，只需要测量到Ia=1/4I0         (I0为Is=0.100下的Ia)
U_list = {
    '10V': [(0.100,164),(0.350,147),(0.360,127),(0.370,90),(0.380,60),(0.390,40)],
    '15V': [(0.100,180),(0.430,153),(0.440,132),(0.450,96),(0.460,64),(0.470,44)],
    '20V': [(0.100,187),(0.490,164),(0.500,154),(0.510,128),(0.520,91),(0.530,61),(0.540,40)],
    '25V': [(0.100,192),(0.540,173),(0.550,167),(0.560,158),(0.570,142),(0.580,110),(0.590,78),(0.600,52),(0.610,41)],
    '30V': [(0.100,196),(0.620,162),(0.630,141),(0.640,110),(0.650,86),(0.660,62),(0.670,49),(0.680,40)]
}

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 1. 绘制Ia-Is曲线并找到临界点Q
plt.figure(figsize=(12, 8))

# 存储临界电流值
critical_points = {}

for voltage, data in U_list.items():
    # 提取电流和阳极电流数据
    Is_values = [point[0] for point in data]
    Ia_values = [point[1] for point in data]

    # 绘制曲线
    plt.plot(Is_values, Ia_values, marker='o', label=f'{voltage}')

    # 找到I0 (Is=0.100时的Ia值)
    i0_index = Is_values.index(0.100)
    I0 = Ia_values[i0_index]

    # 计算1/4 I0
    quarter_I0 = I0 / 4

    # 找到阳极电流首次小于等于1/4 I0的点作为临界点
    # 从I0点之后开始查找
    critical_Ic = None
    for i in range(i0_index, len(Ia_values)):
        if Ia_values[i] <= quarter_I0:
            # 线性插值找到更精确的临界点
            if i > i0_index:  # 确保不是第一个点
                x1, y1 = Is_values[i - 1], Ia_values[i - 1]
                x2, y2 = Is_values[i], Ia_values[i]

                # 计算线性方程 y = mx + b
                m = (y2 - y1) / (x2 - x1)
                b = y1 - m * x1

                # 求解 y = quarter_I0 时的x值
                critical_Ic = (quarter_I0 - b) / m
            else:
                critical_Ic = Is_values[i]
            break

    if critical_Ic is not None:
        critical_points[voltage] = (critical_Ic, quarter_I0)
        # 标记临界点
        plt.plot(critical_Ic, quarter_I0, 'rs', markersize=8)
        plt.text(critical_Ic, quarter_I0, f' Q{voltage}', fontsize=10)

plt.xlabel('励磁电流 Is (A)')
plt.ylabel('阳极电流 Ia')
plt.title('不同阳极加速电压下的Ia-Is曲线及临界点Q')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("result1.png")

# 2. 输出临界点信息
print("各电压下的临界点信息:")
for voltage, (Ic, quarter_I0) in critical_points.items():
    print(f"{voltage}: 临界电流 Ic = {Ic:.4f} A, 1/4 I0 = {quarter_I0:.2f}")

# 3. 绘制Ua-Ic²图线并求斜率
# 提取电压数值（去掉'V'）
U_values = [float(voltage[:-1]) for voltage in critical_points.keys()]
Ic_squared = [Ic ** 2 for Ic in [point[0] for point in critical_points.values()]]


# 线性拟合 U = K * Ic²
def linear_func(x, K):
    return K * x


params, covariance = curve_fit(linear_func, Ic_squared, U_values)
K = params[0]
K_error = np.sqrt(np.diag(covariance))[0]

# 绘制Ua-Ic²图
plt.figure(figsize=(10, 6))
plt.scatter(Ic_squared, U_values, color='blue', label='实验数据')
plt.plot(Ic_squared, linear_func(np.array(Ic_squared), K), 'r--',
         label=f'线性拟合: U = {K:.4f} × Ic²')
plt.xlabel('临界电流平方 Ic² (A²)')
plt.ylabel('阳极加速电压 Ua (V)')
plt.title('Ua-Ic²关系图及线性拟合')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("result2.png")


# 4. 计算电子质荷比 e/m
k = 1.445e-2  # 给定常数

# 假设a为电子束路径的半径相关参数，这里假设a=1(实际实验中需要测量)
# 注意：实际计算时需要使用实验中测量的a值
a = 4.0
e_over_m = ((8 * K) / (a ** 2 * k ** 2))*10**6

print(f"\n拟合斜率 K = {K:.4f} ± {K_error:.4f} V·A⁻²")
print(f"电子质荷比 e/m = {e_over_m:.4e} C/kg")


# 与标准值比较 (标准值约为1.76×10^11 C/kg)
standard_value = 1.76e11
error_percent = abs(e_over_m - standard_value) / standard_value * 100
print(f"与标准值({standard_value:.2e} C/kg)的偏差: {error_percent:.2f}%")
