#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
#numpy를 np로 축약 선언

mat1 = np.random.randn(10)
#실수 난수(-1.0~1.0) 10개를 mat1에 저장
print('mat1:\n',mat1)
#mat1 출력
print('최댓값 numpy.max():',np.max(mat1))
#mat1의 최댓값 출력
print('최솟값 numpy.max():',np.min(mat1))
#mat1의 최솟값 출력
print('Min-Max 정규화:', (mat1-np.min(mat1))/(np.max(mat1)-np.min(mat1)))
#mat1의 최대 최소 정규화 출력

