# @Version : 1.0
# @Author  : 亥子曜
# @File    : main.py.py
# @Time    : 2025/10/30 9:10
from  pyc.form3 import form3_cal
from  pyc.form2 import form2_cal
from  pyc.form1 import form1_cal

k,b,h,error= form3_cal()
print(f"k = {k}  b = {b}")
print(f"普朗克常量测定为:{h}×10^-34")
print(f"百分误差为{error}%")
form1_cal()
form2_cal()