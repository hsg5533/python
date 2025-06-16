from sympy import Derivative, symbols

x = symbols('x') #x를 기호변수화

fx = (x**2+2*x)**3 #fx 함수 선언
fprime = Derivative(fx, x).doit() #x에 대해서 미분

x1 = int(input('x: ')) #x1 값 입력받기

n = fprime.subs({x: x1}) #x에 x1 값 대입
print("y' = 3(x^2 + 2x)^2 * (2x+2) = %d"%n)
