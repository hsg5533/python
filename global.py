def func(one,two):
    global sum
    value = one + two
    sum += one + two
    print(value,sum)
    return value
# main
value = 0
sum = 0
ret1 = func(2,3) #def함수내에 계산된 value와 sum의 값 출력
print(value,sum) #def함수 밖의 vaule의 값과 def함수내에 계산된 sum의 값 출력 
ret2 = func(3,3) #def함수내에 계산된 value와 sum의 값 출력
print(value,sum) #def함수 밖의 vaule의 값과 def함수내에 계산된 sum의 값 출력 
print(ret1,ret2) #계산된 ret1과 ret2의 값을 출력. 이 값은 def함수 내의 return의 값이다.


