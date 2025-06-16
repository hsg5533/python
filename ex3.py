def avarage(list):
    v = 0
    for i in list:
        v= v+i
    return v/len(list)

v = list(map(int, input().split()))
result = sum(v)
print(format(v),end='의 평균은 ')
print(result/len(v),end ='입니다.')
