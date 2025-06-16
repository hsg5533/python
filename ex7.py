import random

score = random.randint(1,100)
if score>= 60 :  
    print("score =",score,"합격입니다.")#여기에서 여러가지 시도를 해봤으나 프로그램을 종료합니다가 나올때까지 무한반복하는 방법은 찾기가 어려움. while문을 넣어봤으나 같은 점수만 반복됨. score에 들어가는 함수를 계속 지속적으로 바꾸는 방법이 필요...
else:
    print("score =",score,"프로그램을 종료합니다.")
print("\n")#문제1

score = random.randint(1,100)# 숫자를 랜덤으로 1-100까지 지정
if score <=60:
    print("score =",score,"불합격")
else:
    print("score =",score,"합격")
print("\n")#문제2

score = random.randint(1,100)# 숫자를 랜덤으로 1-100까지 지정
if score <=60:#스코어가 60이하면 불합격
    print("score =",score,"\n불합격입니다.\n조금만 더 힘내세요.")#문제와 줄을 맞추기위해서 \n을 씀
else:#그 외에 나머지는 합격
    print("score =",score,"\n합격입니다.\n축하합니다.")

print("\n")#문제3

score = random.randint(1,100)# 숫자를 랜덤으로 1-100까지 지정
if score >= 96:
    print("score =",score,"A+") #4점 단위로 등급 지정.. 
elif score >= 92:
    print("score =",score,"A0")
elif score >= 88:
    print("score =",score,"B+")
elif score >= 84:
    print("score =",score,"B0")
elif score >= 80:
    print("score =",score,"C+")
elif score >= 76:
    print("score =",score,"C0")
elif score >= 72:
    print("score =",score,"D+")
elif score >= 68:
    print("score =",score,"D0")
elif score >= 64:
    print("score =",score,"E+")
elif score >= 60:
    print("score =",score,"E0")
else:print("score =",score,"F")
print("\n")#문제4

num = random.randint(1,100)
if num%2==0: #num을 2로 나눴을때 나머지가 0이면 짝수
    print("num=",num,"은(는) 짝수")
else:#그 나머지는 홀수
    print("num=",num,"은(는) 홀수")
    #문제5

    



    
