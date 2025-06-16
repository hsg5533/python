# 각 자리수를 더하는 함수생성
def Digitsum(x):
    result=0
    while True:
        r=x%10
        result=result+r
        x=x//10
        
        if x==0:
            break
    return result

# 정수 입력받기
num=int(input("정수를 입력하시오."))

# 결과값 출
print("%d의 각자리 수의 합은 %d입니다."%(num,Digitsum(num)))
