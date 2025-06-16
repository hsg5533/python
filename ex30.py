#!/usr/bin/env python
# coding: utf-8

# In[27]:


import numpy as np
#numpy 선언 후 np로 축약
import random
#random함수를 쓰기위해 선언

iList = [random.randint(1,100) for i in range(6)]
# random함수로 1~100사이의 수를 지정후 6개만 선언
print('iList:',iList)
#iList출력
print('type(iList):',type(iList),'\n')
#iList타입 출력

mat1 = np.array(iList)
#mat1을 선언후 iList의 값을 np.array형으로 변환
print('mat1:',mat1)
#mat1 출력
print('type(mat1):',type(mat1))
#mat1의 타입 출력
print('mat1.dtype:', mat1.dtype)
#mat1의 데이터타입 출력
print("np.min(mat1):",min(mat1))
#mat1의 최솟값 출력
print("np.max(mat1):",max(mat1),'\n')
#mat1의 최댓값 출력

mat2 = mat1/100 
#mat2를 선언후 mat1을 100으로 나눈값을 집어넣기
print('mat2:',mat2)
#mat2 출력
print('type(mat2):',type(mat2))
#mat2의 타입출력
print('mat2.dtype:', mat2.dtype,'\n')
#mat2의 데이터타입 출력

mat3 = np.random.random(6)
#mat3을 선언 후 랜덤으로 6개의 실수 생성
print('mat3:',mat3)
#mat3 출력
print('type(mat3):',type(mat3))
#mat3의 타입 출력
print('mat3.dtype:', mat3.dtype)
#mat3의 데이터타입 출력


# In[ ]:




