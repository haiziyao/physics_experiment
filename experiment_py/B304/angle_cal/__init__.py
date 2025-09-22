# @Version : 1.0
# @Author  : 亥子曜
# @File    : __init__.py.py
# @Time    : 2025/9/22 12:34
# 从calculator.py中导入需要公开的函数
from .calculator import (
    calculate_angle_difference,
    cal_angle_avg,
    cal_three_angle_avg,
    dms_to_degrees,
    calculate_percent_error,
    calculate_wavelength_error
)

# 定义__all__，指定通过from package import *时可导入的函数
__all__ = [
    'calculate_angle_difference',
    'cal_angle_avg',
    'cal_three_angle_avg',
    'dms_to_degrees',
    'calculate_percent_error',
    'calculate_wavelength_error'
]
