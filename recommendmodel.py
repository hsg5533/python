"""
[ 연관규칙 실습 ]
mlxtend 라이브러리 활용 (pip install mlxtend)
mlxtend.apriori 파라미터
df : padnas DataFrame
min_support : 최소 지지도
use_colnames : 컬럼이름 사용 여부 (default = False)
max_len : 최대 길이
"""


import pandas as pd

from mlxtend.preprocessing import TransactionEncoder    # Transaction Sparse Matrix 생성
from mlxtend.frequent_patterns import apriori           # min_support를 통해 itemset 
from mlxtend.frequent_patterns import association_rules # itemset -> Confidence, lift 확인

dataset = [
	['아메리카노', '카페라떼'],
	['카페라떼', '아메리카노', '카푸치노'],
	['바닐라라떼', '아메리카노'],
	['녹차라떼', '카페라떼', '아메리카노'],
	['카페모카', '아메리카노'],
	['아메리카노', '카페라떼', '바닐라라떼'],
	['초콜릿', '아메리카노'],
	['아메리카노'],
	['카페모카', '카페라떼', '카푸치노']
]

encoder = TransactionEncoder()

transaction_matrix = encoder.fit(dataset).transform(dataset)

print(transaction_matrix)

"""
([[False, False,  True, False,  True, False, False],
       [False, False,  True, False,  True, False,  True],
       [False,  True,  True, False, False, False, False],
       [ True, False,  True, False,  True, False, False],
       [False, False,  True, False, False,  True, False],
       [False,  True,  True, False,  True, False, False],
       [False, False,  True,  True, False, False, False],
       [False, False,  True, False, False, False, False],
       [False, False, False, False,  True,  True,  True]])
"""

item_list = set([j for i in dataset for j in i ])
print(item_list)

transaction_df = pd.DataFrame(transaction_matrix)
transaction_df.columns = ['녹차라떼', '바닐라라떼', '아메리카노', '초콜릿', '카페라떼', '카페모카', '카푸치노']
print(transaction_df)

itemset = apriori(transaction_df, min_support=0.2, use_colnames=True)
print(itemset)
# 카푸치노가 포함된 transaction 0.222
# 녹차라떼, 카페라떼가 포함된 transction 0.444

from mlxtend.frequent_patterns import association_rules

print(association_rules(itemset, metric='confidence', min_threshold=0.3))
# antecedents : 선행사건
# consequents : 결과

# 아메리카노와 카페라떼의 confidence 0.5 / lift 0.9
#  아메키라노와 카페라떼는 향상도는 크게 의미 없음 (상호 대체 느낌)

# 카푸치노와 카페라떼의 confidecne 0.4 / lift 1.8
# 카푸치노와 카페라떼의 향상도는 1.8로 각각 구매할 확률보다 같이 구매할 확률 높음

# 카페라떼를 구매할 때
# 아메리카노, 카푸치노를 같이 구매하는 경우 있음
# confidence(카페라떼 -> 아메리카노) : 0.8
# confidence(카페라떼 -> 카푸치노) : 0.4
# 아메리카노와 함께 구매할 경우가 더 많음