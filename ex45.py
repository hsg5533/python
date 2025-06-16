import numpy as np
import matplotlib.pyplot as plt

delta = 1e-7 # 0이 되는 것을 방지

#cross entropy 오차를 구하는 기능
def cross_entropy_error(a,x):
    return -np.sum(a*np.log(x+delta))

#dx: x의 증분 구하기
dx=[]
for i in range(0,31,1):
    dx.append(i/30+delta)

#dy: dx에 따른 y의 증분 구하기
dy=[]
for i in dx:
    dy.append(cross_entropy_error(1,i)) #계수 a가 1일때

for i in range(len(dx)):
    print(format(dx[i], ".5f"), "=", format(dy[i], ".5f"))
