

import numpy as np #numpy라이브러리 불러오고 명령어 np로 변경

mat1 = np.random.randint(1,5,size=2) #랜덤함수로 mat1에 1-5사이의 정수중 2개 지정
print(mat1) #mat1출력
print('type(mat1):',type(mat1)) #type 출력
print('mat1.dtype:',mat1.dtype) #dtype 출력
print('mat1.ndim:',mat1.ndim)   #차원 출력
print('mat1.shape',mat1.shape)  #shape 출력
print('mat1.size:',mat1.size)   #size 출력
 #문제3번 

print('\n')
mat2 = np.reshape(mat1,(2,1)) #mat2를 선언하고 내용을 mat1을 2행 1열로 변경한 값을 집어넣는다.
print(mat2) #mat2출력
print('type(mat2):',type(mat2))#type 출력
print('mat2.dtype:',mat2.dtype)#dtype 출력
print('mat2.ndim:',mat2.ndim)  #차원 출력
print('mat2.shape',mat2.shape) #shape 출력
print('mat2.size:',mat2.size)  #size 출력
#문제4

print('\n')
print('mat1*2=\n',mat1*2) #mat1에 2를 곱해서 출력
print('mat1*mat2=\n',mat1*mat2)#ma1과 mat2를 곱해서 출력

#문제5




