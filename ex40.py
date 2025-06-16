import pandas as pd
import numpy as np

#numpy.nan 값이 있는 dict1 생성
dict1 = {
    'case1': [101, 89, np.nan, 98],
    'case2': [45, 54, 60, np.nan],
    'case3': [np.nan, 39, 79, 97]
    }

#dict1의 pandas의 DataFrame으로 생성한 후 head 출력
df = pd.DataFrame(dict1)
print(df.head())

#결측치를 모두 35로 채운 결과
print(df.fillna(35))

#결측치를 바로 앞에 있는 값으로 채운 결과
print(df.fillna(method='pad'))

#결측치를 바로 뒤에 있는 값으로 채운 결과
print(df.fillna(method='bfill'))

#dict1에 있는 no.nan을 -30으로 대체한 결과
print(df.replace(to_replace=np.nan,value=-30))

#결측치를 선형으로 보간한 결과
print(df.interpolate(method='linear',limit_direction='forward'))

#결측치를 다항식으로 보간한 결과
print(df.interpolate(method='polynomial',order=2))
