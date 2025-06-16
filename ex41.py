import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

#x에 무작위 좌표 10개를 저장
x=np.random.rand(10)
print(x)

#y에 무작위 좌표 10개를 저장
y=np.random.rand(10)
print(y)

#(x,y)에 대해 그래프를 출력
plt.subplot(311)
plt.plot(x, y, 'x')

#x의 최소값과 최대값을 사이를 100 등분한 후 출력
dx=np.linspace(x.min(), x.max(), 100)

#x,y를 선형보간 후 출력
fL = interp1d(x, y, kind = 'linear')
Ldy = fL(dx)
plt.subplot(312)
plt.plot(Ldy)

#x,y를 부드러운 보간 후 출력
fQ = interp1d(x, y, kind = 'quadratic')
Qdy = fQ(dx)
plt.subplot(313)
plt.plot(Qdy)

#최종 그래프 출력
plt.show()


