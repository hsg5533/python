import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity #코사인 유사도 함수 호출

x = pd.read_csv('./data/recommenduser.csv', encoding='utf-8', index_col='고객명')
print(x)

result = cosine_similarity(x, x)  #Data의 코사인 유사도 계산
print(result)


