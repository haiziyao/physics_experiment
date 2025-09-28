import math
import matplotlib.pyplot as plt  # 新增：导入绘图库

# 金属逸出功的测定
# 数据定义
light_c = {  # Ua= 16.0 25.0 36.0 49.0 64.0 81.0 100.0
    '0.600': [6, 6, 7, 7, 7, 8, 8],  # 灯丝电流=0.600时的各Ua对应的Ia值
    '0.625': [11, 12, 13, 14, 14, 15, 15],  # 灯丝电流=0.625时的各Ua对应的Ia值
    '0.650': [21, 24, 26, 26, 27, 28, 29],  # 灯丝电流=0.650时的各Ua对应的Ia值
    '0.675': [38, 41, 44, 46, 48, 51, 52],  # 灯丝电流=0.675时的各Ua对应的Ia值
    '0.700': [66, 72, 77, 82, 85, 89, 91],  # 灯丝电流=0.700时的各Ua对应的Ia值
    '0.725': [112, 122, 132, 139, 146, 152, 157],  # 灯丝电流=0.725时的各Ua对应的Ia值
    '0.750': [182, 199, 214, 226, 237, 246, 254]  # 灯丝电流=0.750时的各Ua对应的Ia值
}


# 阳极电压列表（与数据顺序对应）
ua_values = [16.0, 25.0, 36.0, 49.0, 64.0, 81.0, 100.0]

# 打印表头
print(f"{'灯丝电流(A)':<15}", end="")  # 第一列：灯丝电流
for ua in ua_values:
    print(f"Ua={ua}V", end="\t")  # 后续列：各阳极电压
print("\n" + "-" * 120)  # 分隔线

# 按灯丝电流从小到大排序并打印数据行
for current in sorted(light_c.keys(), key=lambda x: float(x)):
    print(f"{current:<15}", end="")  # 打印灯丝电流
    # 打印对应各阳极电压的发射电流值
    for ia in light_c[current]:
        print(f"{ia:<10}", end="")
    print()  # 换行
print()

# 常数数据，不可变
T = {
    '0.600': 1.88,
    '0.625': 1.92,
    '0.650': 1.96,
    '0.675': 2.00,
    '0.700': 2.04,
    '0.725': 2.08,
    '0.750': 2.12,
    '0.775': 2.16,
    '0.800': 2.20
}
W0 = 4.54  # 单位eV  金属钨的逸出功
k = 1.381e-23  # 单位J/K  常数玻尔兹曼常量
eta = 0.439  # 肖特基效应系数（计算零场电流必需）


# 新增：零场电流计算（基于肖特基效应公式）+ 存储拟合直线参数（用于绘图）
zero_field_data = {}
fit_lines = {}  # 新增：存储每条拟合直线的参数（斜率、截距），用于绘图
sorted_currents = sorted(light_c.keys(), key=lambda x: float(x))

for current in sorted_currents:
    t = T[current]  # 当前灯丝温度（10³K）
    ia_list = light_c[current]  # 当前电流下的各Ua对应的Ia
    sqrt_ua_list = [math.sqrt(ua) for ua in ua_values]  # 各Ua的平方根（x轴原始数据）
    lg_ia_list = [math.log10(ia) for ia in ia_list]  # 各Ia的lg值（y轴原始数据）

    # 最小二乘法拟合：lgIa = slope * sqrt(Ua) + intercept（其中intercept=lgI）
    n = len(ua_values)
    sum_x = sum(sqrt_ua_list)
    sum_y = sum(lg_ia_list)
    sum_xy = sum(x*y for x,y in zip(sqrt_ua_list, lg_ia_list))
    sum_x2 = sum(x**2 for x in sqrt_ua_list)

    # 计算拟合直线的斜率和截距
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
    intercept = (sum_y - slope * sum_x) / n  # 截距=lgI（零场电流对数）
    I_zero = 10 ** intercept  # 零场电流

    # 存储零场电流数据
    zero_field_data[current] = {
        'lgI': intercept,
        'I_zero': I_zero
    }

    # 新增：存储拟合直线参数（用于后续绘图）
    fit_lines[current] = {
        'slope': slope,
        'intercept': intercept,
        'x_raw': sqrt_ua_list,  # 原始x数据（sqrt(Ua)）
        'y_raw': lg_ia_list     # 原始y数据（lgIa）
    }


# 计算lg(Ia/T²)（原有代码不变）
lgI_Tsqar = {}
for key in light_c:
    lg_values = [math.log10(ia / (T[key] ** 2)) for ia in light_c[key]]
    lgI_Tsqar[key] = lg_values

# 定义阳极电压列表并计算其平方根（原有代码不变）
ua_values = [16.0, 25.0, 36.0, 49.0, 64.0, 81.0, 100.0]
sqrt_ua = [math.sqrt(ua) for ua in ua_values]  # 计算各电压的平方根

# 打印表头（原有代码不变）
print("不同T下的lgIa值")
print(f"{'温度 ':<10}", end="")  # 第一列：温度
for s in sqrt_ua:
    print(f"Ua平方根 :{s:.2f}", end="\t")  # 后续列：电压平方根（保留2位小数）
print()  # 换行

# 打印分隔线（原有代码不变）
print("-" * 80)

# 按温度顺序打印数据行（原有代码不变）
for filament_current in sorted(lgI_Tsqar.keys(), key=lambda x: float(x)):
    temp = T[filament_current]
    print(f"{temp:<10.3f}", end="")  # 打印温度（保留3位小数）
    # 打印对应各电压平方根的计算值
    for value in lgI_Tsqar[filament_current]:
        print(f"{value:.4f}", end="\t")  # 保留4位小数
    print()  # 换行

# 计算每组电压下的lg(I/T²)与1/T的斜率（原有代码不变）
print("\n各组电压下lg(I/T^2)--1/T的斜率：")
k_lg = {}
# 提取1/T值列表（x轴数据）
x_values = [1 / T[key] for key in sorted(lgI_Tsqar.keys(), key=lambda x: float(x))]
W_cal = {}
for ua_idx, ua in enumerate(ua_values):
    # 提取对应电压下的lg(I/T²)值（y轴数据）
    y_values = [lgI_Tsqar[key][ua_idx] for key in sorted(lgI_Tsqar.keys(), key=lambda x: float(x))]

    # 使用最小二乘法计算斜率
    n = len(x_values)
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))
    sum_x2 = sum(x ** 2 for x in x_values)

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    k_lg[ua] = slope
    w = -slope * k * 2.303 * 6.24e18 * 1000
    # 1J = 6.24e18 eV
    W_cal[ua] = w
    print(f"Ua={ua}V时的斜率: {slope:.4f}  逸出功测量值:{w:.2f}eV")


# 新增：按要求格式打印表格（灯丝温度→lgIa→lg(I/T²)→1/T）
print("\n" + "="*80)
print("热电子发射关键参数汇总表（按灯丝电流顺序）")
print("="*80)

# 1. 第一行：灯丝温度（对应所有灯丝电流）
print(f"{'灯丝温度(T/10^3K)':<20}", end="")  # 第一列标题
for current in sorted_currents:
    print(f"{T[current]:<10.3f}", end="")  # 每个电流对应的温度（保留3位小数）
print()  # 换行·

# 2. 第二行：lgI（零场电流的对数，与温度一一对应）
print(f"{'lgI(零场电流对数)':<20}", end="")  # 第一列标题
for current in sorted_currents:
    print(f"{zero_field_data[current]['lgI']:<10.4f}", end="")  # lgI保留4位小数
print()  # 换行

# 3. 第三行：lg(I/T²)（取Ua=100V时的值，与温度一一对应）
print(f"{'lg(I/T²)(Ua=100V)':<20}", end="")  # 第一列标题
for current in sorted_currents:
    print(f"{lgI_Tsqar[current][-1]:<10.4f}", end="")  # 保留4位小数
print()  # 换行

# 4. 第四行：1/T（温度的倒数，与温度一一对应）
print(f"{'1/T(10^-3K^-1)':<20}", end="")  # 第一列标题
for current in sorted_currents:
    one_over_T = 1 / T[current]  # 1/T（单位：10⁻³K⁻¹）
    print(f"{one_over_T:<10.6f}", end="")  # 保留6位小数
print()  # 换行
print("="*80)


# -------------------------- 新增：用matplotlib绘制7条“lgIa - sqrt(Ua)”拟合直线 --------------------------
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 解决中文显示问题
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 创建画布（设置大小，方便查看）
fig, ax = plt.subplots(figsize=(10, 6))

# 定义颜色列表（区分7条直线，颜色依次变化）
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
color_idx = 0  # 颜色索引

# 遍历每个灯丝电流，绘制原始数据点和拟合直线
for current in sorted_currents:
    # 获取当前电流的拟合参数和原始数据
    slope = fit_lines[current]['slope']
    intercept = fit_lines[current]['intercept']
    x_raw = fit_lines[current]['x_raw']  # 原始sqrt(Ua)
    y_raw = fit_lines[current]['y_raw']  # 原始lgIa

    # 1. 绘制原始数据点（用圆形标记，颜色与直线一致）
    ax.scatter(x_raw, y_raw, color=colors[color_idx], s=50, label=f'灯丝电流 {current}A（原始数据）')

    # 2. 绘制拟合直线（扩展x范围，使直线更完整）
    x_fit = [min(x_raw) - 0.5, max(x_raw) + 0.5]  # 拟合直线的x范围（比原始数据宽0.5）
    y_fit = [slope * x + intercept for x in x_fit]  # 拟合直线的y值
    ax.plot(x_fit, y_fit, color=colors[color_idx], linewidth=2, linestyle='--')

    # 颜色索引递增（循环使用颜色）
    color_idx = (color_idx + 1) % len(colors)

# 设置图表标题和坐标轴标签
ax.set_title('不同灯丝电流下 lgIa - √Ua 拟合直线', fontsize=14, pad=20)
ax.set_xlabel('√Ua (V^0.5)', fontsize=12)
ax.set_ylabel('lgIa (lg(μA))', fontsize=12)

# 添加网格（便于读取数据）
ax.grid(True, alpha=0.3, linestyle='-')

# 添加图例（放在右上角，避免遮挡数据）
ax.legend(loc='upper right', fontsize=10, bbox_to_anchor=(1, 1))

# 调整布局（防止标签被截断）
plt.tight_layout()

# 显示图像（运行代码后会弹出窗口）
plt.savefig("result.png")

# -------------------------- 新增：绘制各组电压下 lg(I/T²)-1/T 拟合直线 + 计算逸出功平均值与误差 --------------------------
# 1. 准备数据
# 提取x轴数据：1/T（单位：10⁻³K⁻¹），按灯丝电流排序
x_1T = [1 / T[key] for key in sorted(lgI_Tsqar.keys(), key=lambda x: float(x))]
# 存储每条拟合直线的参数（用于计算R²，评估拟合效果）
fit_params = {}
# 存储所有电压下的逸出功测量值（用于后续计算平均值和误差）
W_measurements = []

# 2. 创建新画布
fig2, ax2 = plt.subplots(figsize=(12, 7))
# 定义新的颜色列表（区分7组电压）
volt_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF']
volt_color_idx = 0

# 3. 遍历每组电压，计算拟合直线、绘制图像并收集逸出功
for ua_idx, ua in enumerate(ua_values):
    # 提取当前电压下的y轴数据：lg(I/T²)
    y_lgIT2 = [lgI_Tsqar[key][ua_idx] for key in sorted(lgI_Tsqar.keys(), key=lambda x: float(x))]

    # 最小二乘法拟合：lg(I/T^2) = slope * (1/T) + intercept
    n = len(x_1T)
    sum_x = sum(x_1T)
    sum_y = sum(y_lgIT2)
    sum_xy = sum(x * y for x, y in zip(x_1T, y_lgIT2))
    sum_x2 = sum(x ** 2 for x in x_1T)
    sum_y2 = sum(y ** 2 for y in y_lgIT2)

    # 计算拟合参数
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n
    # 计算R²（拟合优度，越接近1越好）
    y_pred = [slope * x + intercept for x in x_1T]
    ss_total = sum((y - sum_y / n) ** 2 for y in y_lgIT2)
    ss_residual = sum((y - yp) ** 2 for y, yp in zip(y_lgIT2, y_pred))
    r_squared = 1 - (ss_residual / ss_total)

    # 计算当前电压下的逸出功（单位：eV）
    # 公式：W = -slope * k * 2.303 * 1e3 / e （e=1.602e-19J/eV，k=1.381e-23J/K）
    e = 1.602e-19
    W = -slope * k * 2.303 * 1000 / e
    W_measurements.append(W)
    fit_params[ua] = {'slope': slope, 'intercept': intercept, 'R²': r_squared, 'W': W}

    # 绘制原始数据点
    ax2.scatter(x_1T, y_lgIT2, color=volt_colors[volt_color_idx], s=60,
                label=f'Ua={ua}V | W={W:.2f}eV | R²={r_squared:.4f}')

    # 绘制拟合直线（扩展x范围，使直线更完整）
    x_fit_1T = [min(x_1T) - 0.02, max(x_1T) + 0.02]
    y_fit_1T = [slope * x + intercept for x in x_fit_1T]
    ax2.plot(x_fit_1T, y_fit_1T, color=volt_colors[volt_color_idx],
             linewidth=2, linestyle='-', alpha=0.8)

    volt_color_idx = (volt_color_idx + 1) % len(volt_colors)

# 4. 计算逸出功的平均值和误差
import numpy as np

W_mean = np.mean(W_measurements)  # 平均值
W_std = np.std(W_measurements, ddof=1)  # 样本标准差（实验误差用样本标准差）
W_relative_error = (W_std / W_mean) * 100  # 相对误差（百分比）

# 5. 设置图像格式
ax2.set_title(
    f'各组电压下 lg(I/T^2)-1/T 拟合直线\n逸出功平均值：{W_mean:.2f}eV | 标准差：{W_std:.2f}eV | 相对误差：{W_relative_error:.2f}%',
    fontsize=14, pad=25)
ax2.set_xlabel('1/T (10^-3 K^-1)', fontsize=12)
ax2.set_ylabel('lg(I/T^2) (lg(μA·K^-2))', fontsize=12)
ax2.grid(True, alpha=0.3, linestyle='-')
# 图例放在图像右侧，避免遮挡
ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
plt.savefig("lgIT2_1T_fit.png")  # 保存图像

# 6. 打印逸出功统计结果
print("\n" + "=" * 80)
print("逸出功测量结果统计")
print("=" * 80)
print(f"{'电压Ua(V)':<12} {'逸出功W(eV)':<15} {'拟合R^2':<10}")
print("-" * 80)
for ua in sorted(ua_values):
    print(f"{ua:<12.1f} {fit_params[ua]['W']:<15.2f} {fit_params[ua]['R²']:<10.4f}")
print("-" * 80)
print(f"逸出功平均值：{W_mean:.2f} eV")
print(f"样本标准差（误差）：{W_std:.2f} eV")
print(f"相对误差：{W_relative_error:.2f}%")
print(f"理论值（钨）：{W0:.2f} eV")
print("=" * 80)