# @Version : 1.0
# @Author  : 亥子曜
# @File    : main.py.py
# @Time    : 2025/10/23 12:23

from pyc.form1 import form1_cal
from pyc.form2 import form2_cal
from pyc.form3 import form3_cal

if __name__ == '__main__':
     k = form1_cal()
     form2_cal()
     KH,n =form3_cal(k)
     print(f"KH = {int(KH)} V/(A*T)  注意：这个的有效数字保留位置来源于你的原始数据只有三位有效数字，所以这里只能是三位有效数字")
     print(f"n = {n:.2f} m^(-3)")
     print(f"科学计数法： n = {n:.2e} m^(-3)")


