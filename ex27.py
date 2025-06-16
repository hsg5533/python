import numpy as np

mat1 = np.array([[1, 2, 3], [4, 5, 6]]) #mat1선언 후 데이터값 입력
print('mat1\n',mat1) #mat1 출력
print('mat1 data type',mat1.dtype) #mat1의 type출력
print('\n')
mat2 = mat1.astype('float') #mat2를 선언하여 mat1의 데이터를 float으로 변환
print('mat2\n',mat2) #mat2출력
print('mat2 data type',mat2.dtype) #mat2의 type출력
print('\n')
mat3 = mat2.astype('float32') #mat3을 선언하여 mat2의 데이터를 float32로 변환하여 복사
print('mat3\n',mat3) #mat3 출력
print('mat3 data type',mat3.dtype) #mat3의 type출력