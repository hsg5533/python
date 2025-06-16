#!/usr/bin/env python
# coding: utf-8

# In[6]:


import numpy as np
#numpy를 np로 축약 선언

mat1 = np.random.rand(10,3)
#mat1 선언후 실수난수를 10행 3열로 만듬
print('mat1:\n', mat1,'\n')
#mat1 출력

mat2 = np.random.rand(10,3)
#mat2 선언후 실수난수를 10행 3열로 만듬
print('mat2:\n', mat2,'\n')
#mat2 출력

mat3 = mat1 * mat2
#mat3선언후 mat1 과 mat2를 더함
print('mat3:\n',mat3,'\n')
#mat3 출력

print('전체 요소 평균 numpy.mean():\n',np.mean(mat3),'\n')
#mat3의 전체 요소 평균 출력

print('행축 평균 numpy.mean(axis=1):\n',np.mean(mat3,axis=1),'\n')
#mat3의 행축 평균 출력 

print('열축 평균 numpy.mean(axis=0):\n',np.mean(mat3,axis=0))
#mat3의 열출 평균 출력


# In[ ]:




