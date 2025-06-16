#!/usr/bin/env python
# coding: utf-8

# In[11]:


import numpy as np
#numpy를 np로 축약 선언
import random
#random함수 선언

mat1 = np.random.rand(10)
#mat1에 실수 난수 10개 선언
print('mat1\n',mat1)
#mat1 출력
print('최댓값 numpy.max():', np.max(mat1))
#최댓값 출력
print('최솟값 numpy.min():', np.min(mat1))
#최솟값 출력
print('평균 numpy.mean():', np.mean(mat1))
#평균 출력
print('분산 numpy.var():', np.var(mat1))
#분산 출력
print('표준편차 numpy.std():', np.std(mat1))
#표준편차 출력


# In[ ]:




