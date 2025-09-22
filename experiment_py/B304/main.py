# @Version : 1.0
# @Author  : 亥子曜
# @File    : main.py
# @Time    : 2025/9/22 11:50
# 用光栅测量光波波长
import math

# 光栅常数 (单位：米，这里假设300线/毫米，转换为米)
d = 1 / 300 * 1e-3  # 1/300 mm转换为米
k = 1  # 谱线级数
#实验所用为汞灯，可在书最后一页查询
angles_std = {
    "黄色1":576.96 ,
    "黄色2": 579.07,
    "绿色": 546.07,
    "蓝色1": 435.83
}
# 从自定义包中导入所需函数
from angle_cal import (
    calculate_angle_difference,
    cal_angle_avg,
    cal_three_angle_avg,
    dms_to_degrees,
    calculate_percent_error,
    calculate_wavelength_error
)
#数据格式（度，分）
# 原始数据 - 黄色
yellow1_A = [(186,20), (206,14)]
yellow1_B = [(6,20), (26,37)]
yellow2_A = [(186,18), (206,20)]
yellow2_B = [(6,18), (26,20)]

# 原始数据 - 绿色
green1_A = [(186,57), (205,45)]
green2_A = [(186,50), (205,40)]
green3_A = [(186,55), (205,33)]
green1_B = [(6,57), (25,45)]
green2_B = [(6,50), (25,40)]
green3_B = [(6,55), (25,33)]

# 原始数据 - 蓝色
blue1_A = [(188,45), (203,45)]
blue1_B = [(8,45), (23,45)]

# 处理黄色数据
yellow1_A_diff = calculate_angle_difference(yellow1_A)
yellow1_B_diff = calculate_angle_difference(yellow1_B)
yellow2_A_diff = calculate_angle_difference(yellow2_A)
yellow2_B_diff = calculate_angle_difference(yellow2_B)
yellow1_avg_angle = cal_angle_avg(yellow1_A_diff, yellow1_B_diff)
yellow2_avg_angle = cal_angle_avg(yellow2_A_diff, yellow2_B_diff)

# 处理绿色数据
green1_A_diff = calculate_angle_difference(green1_A)
green1_B_diff = calculate_angle_difference(green1_B)
green1_avg = cal_angle_avg(green1_A_diff, green1_B_diff)

green2_A_diff = calculate_angle_difference(green2_A)
green2_B_diff = calculate_angle_difference(green2_B)
green2_avg = cal_angle_avg(green2_A_diff, green2_B_diff)

green3_A_diff = calculate_angle_difference(green3_A)
green3_B_diff = calculate_angle_difference(green3_B)
green3_avg = cal_angle_avg(green3_A_diff, green3_B_diff)

green_overall_avg = cal_three_angle_avg(green1_avg, green2_avg, green3_avg)

# 处理蓝色数据
blue1_A_diff = calculate_angle_difference(blue1_A)
blue1_B_diff = calculate_angle_difference(blue1_B)
blue1_avg_angle = cal_angle_avg(blue1_A_diff, blue1_B_diff)

# 打印结果
print("黄色1平均角度:", f"{yellow1_avg_angle[0]}度{yellow1_avg_angle[1]:.2f}分")
print("黄色2平均角度:", f"{yellow2_avg_angle[0]}度{yellow2_avg_angle[1]:.2f}分")
print("绿色总平均值:", f"{green_overall_avg[0]}度{green_overall_avg[1]:.2f}分")
print("蓝色1平均角度:", f"{blue1_avg_angle[0]}度{blue1_avg_angle[1]:.2f}分")

# 转换所有角度为度数
angles = {
    "黄色1": dms_to_degrees(*yellow1_avg_angle),
    "黄色2": dms_to_degrees(*yellow2_avg_angle),
    "绿色": dms_to_degrees(*green_overall_avg),
    "蓝色1": dms_to_degrees(*blue1_avg_angle)
}

# 计算各颜色的波长
wavelengths = {}
for color, angle in angles.items():
    # 将角度转换为弧度
    angle_rad = math.radians(angle)
    # 应用光栅方程：d*sinθ = k*λ，求解λ
    wavelength = (d * math.sin(angle_rad)) / k
    # 转换为纳米（1米 = 1e9纳米）
    wavelength_nm = wavelength * 1e9
    wavelengths[color] = wavelength_nm

# 打印测量角度和计算结果
print("各颜色平均角度测量值：")
for color in angles:
    print(f"{color}平均角度: {angles[color]:.4f}度")

print("\n计算得到的各颜色波长：")
for color in wavelengths:
    print(f"{color}波长: {wavelengths[color]:.2f}纳米")

errors = {}
for color in wavelengths:
    errors[color] = calculate_percent_error(wavelengths[color], angles_std[color])

# 打印结果
print("波长测量结果与标准值对比：")
print(f"{'颜色':<6} {'测量值(nm)':<12} {'标准值(nm)':<12} {'百分误差(%)':<10}")
print("-" * 45)
for color in wavelengths:
    print(f"{color:<6} {wavelengths[color]:<12.2f} {angles_std[color]:<12} {errors[color]:<10.2f}")


#误差传递公式
# 因为光栅标注300+—1，所以
d = 1 / 300 * 1e-3  # 光栅常数（米）
delta_d = 1 / (300 ** 2) * 1e-3  # 光栅常数误差（假设±1线/毫米）

# 角度测量误差（0.5分，转换为度）
delta_theta_deg = 0.5 / 60  # 0.5分 = 0.5/60度
for color in angles:
        lamda = wavelengths[color]
        theta = angles[color]
        delta_lamda = calculate_wavelength_error(lamda, d, theta, delta_d, delta_theta_deg)
        print(f"{color:<6} {lamda:<14.1f} {theta:<10.1f} {delta_lamda:<12.2f}")
        print(f"  波长结果: {lamda:.1f}±{delta_lamda:.1f} nm")