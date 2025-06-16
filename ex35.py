#!/usr/bin/env python
# coding: utf-8

# In[13]:


import numpy as np
#numpy를 np로 축약 선언

mat1 = np.random.randn(10)
#실수 난수(-1.0~1.0) 10개를 mat1에 저장
print('mat1:\n',mat1)
#mat1 출력
print('평균 numpy.mean():',np.mean(mat1))
#mat1의 평균 출력
print('표준편차 numpy.std():',np.std(mat1))
#mat1의 표준편차 출력
normZScore = (mat1-np.mean(mat1))/np.std(mat1) 
#Z-점수 정규화 수식을 normZScore라는 변수에 입력
print('Z-점수 정규화:\n', normZScore)
#mat1 Z-점수 정규화 normZScore 출력


# In[ ]:




