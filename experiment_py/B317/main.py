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
     print(f"KH = {KH.round(2)} V/(A*T)")
     print(f"n = {n:.2f} m^(-3)")
     print(f"科学计数法： n = {n:.2e} m^(-3)")


