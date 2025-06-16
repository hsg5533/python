import numpy as np
import matplotlib.pyplot as plt

delta = 1e-7 # 0이 되는 것을 방지

#cross entropy 오차를 구하는 기능
def cross_entropy_error(a,x):
    return -np.sum(a*np.log(x+delta))

#dx: x의 증분 구하기
dx=[]
for i in range(0,1010,1):
    dx.append(i*0.001+delta)
print(dx)

#dy: dx에 따른 y의 증분 구하기
dy1=[]
dy2=[]
dy4=[]

for i in dx:
    dy1.append(cross_entropy_error(1,i)) #계수 a가 1일때
    dy2.append(cross_entropy_error(2,i)) #계수 a가 2일때
    dy4.append(cross_entropy_error(4,i)) #계수 a가 4일때

plt.title("y= -alogx graph") #그래프 타이틀 출력
plt.xlabel('X') #x축 레이블 출력
plt.ylabel('Y') #y축 레이블 출력

plt.subplot(311)
plt.grid(True,color='gray',alpha=0.5,linestyle='--') #그리드 출력
plt.plot(dx,dy1,color='red',linewidth=1,label='a=1') #-alogx의 a가 1일때
plt.legend()

plt.subplot(312)
plt.grid(True,color='gray',alpha=0.5,linestyle='--') #그리드 출력
plt.plot(dx,dy2,color='green',linewidth=1,label='a=2') #-alogx의 a가 2일때
plt.legend()

plt.subplot(313)
plt.grid(True,color='gray',alpha=0.5,linestyle='--') #그리드 출력
plt.plot(dx,dy4,color='blue',linewidth=1,label='a=4') #-alogx의 a가 4일때
plt.legend() #레이블 보이기

plt.show()
