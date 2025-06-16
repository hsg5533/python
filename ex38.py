def mySum(x):
    #mySum(x)이라는 함수 선언 
    ret = 0
    for n in range(1,x+1):
        ret += n
    return ret
    #반복문을 이용해서 단순하게 1부터 x까지 더하는 문장이다.

print("1~100까지 합 =", mySum(100))
# 1~100까지의 합 출력
print("1~1000까지 합 =", mySum(1000))
# 1~1000까지의 합 출력
print("1~10000까지 합 =", mySum(10000))
# 1~10000까지의 합 출력
print("1~100000까지 합 =", mySum(100000))
# 1~100000까지의 합 출력






