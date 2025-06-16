
import numpy as np
#numpy를 np로 축약 선언

a = np.loadtxt("diabetes.csv",dtype=np.float32, delimiter=",")
#numpy.loadtxt명령어로 diabetes.csv파일을 float32 형으로 불러와서 a에 저장시키기.


x_data = a[0:,:-1]
#x_data에 1행부터8행까지만 표시기위하여 9행을 뺀다는 의미로 -1사용

y_data = a[0:,8:]
#y_data에 9행만 저장

print(x_data.shape, y_data.shape)
#x_data와 y_data의 shape 출력
print(x_data)
#x_data 출력

print(y_data)
#y_data 출력

print(x_data[:5])
#x_data에서 1-5행까지 출력
print(y_data[:5])
#y_data에서 1-5행까지 출력





