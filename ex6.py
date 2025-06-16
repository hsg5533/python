print(3>7) #3이 7보다 크다. 거짓
print(3<7) #3이 7보다 작다. 진실
print(3==3) #3과 3은 같다. 진실
print(3<=3) #3은 3보다 작거나 같다. 진실
print(3>=7) #3은 7보다 크거나 같다. 거짓
print(3!=7) #3은 7과 같지 않다. 진실
print("\n")#문제1

x = 1 #x에 1을 할당
print(x) #x 출력
x+=3 # 1이 할당된 x에 3을 증가시킴
print(x) #3이 증가된 x 출력
x+=-2 #3이 증가된 x에 2를 감소시킴
print(x) #감소된 x 출력
print("\n")#문제2

x = -2<=x<7

print("x=3\n" "-2<x<7 :",-2<x<7)# 모르겠어요.....문제가 이해 안되네요
print("\n")#문제3

x= 10
y= 3

print("x+y =", x+y)#덧셈
print("x-y =", x-y)#뺄셈
print("x*y =",x*y)#곱하기
print("x/y =",x/y)#나누기
print("x//y =",x//y)#나누기 후 소수점이하 버리기
print("x%y =", x%y)#나누기후 몫이 아닌 나머지 구하기
print("x**y =", x**y)#거듭 제곱
print("\n")#문제4

year = 2020#연도 입력
 
if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0): #4의 배수이면서 100의 배수가 아닐때 또는 400의 배수일때
    print("True")
else:
    print("False")#문제5
 
