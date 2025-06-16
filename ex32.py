#!/usr/bin/env python
# coding: utf-8

# In[8]:


import numpy as np
#numpy를 np로 축약 선언

mat1 = np.random.rand(2,2)
#mat1에 실수난수를 2X2모양으로 저장
print('mat1:\n',mat1,'\n')
#ma1 출력

mat2 = np.random.rand(2,2)
#mat2에 실수난수를 2X2모양으로 저장
print('mat2:\n',mat2,'\n')
#mat2 출력

mat3 = mat1 + mat2
#mat3에 mat1 과 mat2를 더한 결과를 저장
print('mat3=mat1+mat2:\n',mat3,'\n')
#mat3 출력

print('mean1:\n',np.mean(mat3))
#mat3의 평균결과 출력

