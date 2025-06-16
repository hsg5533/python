import random

for i in range(10001):#10000까지 범위 지정
    if i%3==0: #3으로 나눴을때 나머지가 0이면
        continue #계속
    elif i%7==0: #7로 나눴을때 나머지가 0이면
        continue #계속
    else: #그 외에 다른경우
        print(i,'',end='') #출력 end=''는 바로뒤에 이어서 하는 문장