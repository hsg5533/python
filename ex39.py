import numpy as np
#numpy를 np로 축약선언

mat1 = np.random.randn(10,3)
#mat1에 10x3모양으로 랜덤 실수 행렬 생성
print("mat1(10x3)=\n",mat1)
#mat1출력
print("\n")

mat2 = np.random.randn(10,1)
#mat2에 10x1모양으로 랜덤 실수 행렬 생성
print("mat2(10x1)=\n",mat2)
#mat2출력
print("\n")

mat3 = mat1*mat2
#mat3에 mat1 과 mat2를 곱한 행렬 입력
print("mat3(10x3)*(10x1)=\n",mat3)
#mat3출력





