# @Version : 1.0
# @Author  : 亥子曜
# @File    : calculator.py.py
# @Time    : 2025/9/22 12:34
# 从calculator.py中导入需要公开的函数
import  math
def calculate_angle_difference(angle_pair):
    # 从元组中获取两个角度的度和分
    (deg1, min1), (deg2, min2) = angle_pair[0], angle_pair[1]

    # 先转换为总分数
    total_min1 = deg1 * 60 + min1
    total_min2 = deg2 * 60 + min2

    # 计算差值（分）
    diff_min = total_min2 - total_min1

    # 转换回度分格式
    deg_diff = diff_min // 60
    min_diff = diff_min % 60

    return (deg_diff, min_diff)


def cal_angle_avg(diff1, diff2):
    # 提取两组差值的度和分
    (deg1, min1), (deg2, min2) = diff1, diff2

    # 转换为总分数
    total_min1 = deg1 * 60 + min1
    total_min2 = deg2 * 60 + min2

    # 按照原有逻辑计算平均值（除以4）
    avg_total_min = (total_min1 + total_min2) / 4

    # 转换回度分格式
    avg_deg = int(avg_total_min // 60)
    avg_min = avg_total_min % 60

    return (avg_deg, avg_min)


def cal_three_angle_avg(diff1, diff2, diff3):
    # 计算三个差值的平均值
    (deg1, min1) = diff1
    (deg2, min2) = diff2
    (deg3, min3) = diff3

    # 转换为总分数
    total_min1 = deg1 * 60 + min1
    total_min2 = deg2 * 60 + min2
    total_min3 = deg3 * 60 + min3

    # 计算三个值的平均值（总和除以3）
    avg_total_min = (total_min1 + total_min2 + total_min3) / 3

    # 转换回度分格式
    avg_deg = int(avg_total_min // 60)
    avg_min = avg_total_min % 60

    return (avg_deg, avg_min)
def dms_to_degrees(degrees, minutes):
    return degrees + minutes / 60

def calculate_percent_error(measured, standard):
    return abs(measured - standard) / standard * 100


def calculate_wavelength_error(lamda, d, theta_deg, delta_d, delta_theta_deg):
    """
    根据误差传递公式计算波长的绝对误差
    公式：Δλ = λ · √[ (Δd/d)² + (cotθ · Δθ)² ]

    参数：
    lamda: 波长测量值（单位：nm）
    d: 光栅常数（单位：m）
    theta_deg: 衍射角（单位：度）
    delta_d: 光栅常数的绝对误差（单位：m）
    delta_theta_deg: 衍射角的绝对误差（单位：度）

    返回：
    delta_lamda: 波长的绝对误差（单位：nm）
    """
    # 将角度转换为弧度
    theta_rad = math.radians(theta_deg)
    delta_theta_rad = math.radians(delta_theta_deg)

    # 计算各误差项
    relative_d_error = delta_d / d  # Δd/d
    cot_theta = 1 / math.tan(theta_rad)  # cotθ
    angle_error_term = cot_theta * delta_theta_rad  # cotθ·Δθ

    # 计算波长相对误差
    relative_lamda_error = math.sqrt(relative_d_error ** 2 + angle_error_term ** 2)

    # 计算波长绝对误差
    delta_lamda = lamda  * relative_lamda_error

    return delta_lamda