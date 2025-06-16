from sympy import Derivative, symbols

a = symbols('a') #a를 기호변수화
b = symbols('b') #b를 기호변수화
x = symbols('x') #x를 기호변수화
a = int(input('a: '))
b = int(input('b: '))

fx = a*x**2+b*x #fx 함수 선언
fprime = Derivative(fx, x).doit() #x에 대해서 미분

x1 = int(input('x: ')) #x1 값 입력받기

n = fprime.subs({x: x1}) #x에 x1 값 대입
print(fx,"에서의 x = ",x1," 에서의 미분값은 ", n , "입니다")


