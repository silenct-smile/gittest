#-*-coding:utf-8 -*-
import time

intNum,longNum,floatNum=19,123,12.232
#complexNum=2+4i
listType=["java","python","C++","Ruby"]
strType="中文的汉字"
tupleType=(1,2,3,6)
dictType={"name":"张三","age":18,"sec":"男"}

for i in listType:
    print(i)
username="admin"
password="123456"
#inputUsername=raw_input("请输入你的名字：")
#inputPassword=raw_input("请输入你的密码：")
#str=input("please input a string:")
print("I\'m OK")
print("I\'m \"OK\"")
print(r"C:\Users\Administrator\Desktop\脚本\nginx配置.xlsx")
print("""这是很多的字符串，不能放在一行
      放法法阿帆违法法法法法 发发发我
      faffagwgwggggwgwgwgwgwggwgg""")
print(3<2 or 2>1)
print(not 1>2)
print(chr(65))
print(ord('A'))

birth=input("please input your birth:")
if int(birth)<2000:
    print("00前")
else:
    print("00后")