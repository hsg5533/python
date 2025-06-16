import random

myList = []
for i in range(100): #100까지 범위 지정
    a = random.randint(1,100) #1부터 100까지 랜덤으로 숫자 뽑기
    myList.append(a) #리스트 100까지의 숫자 랜덤으로 안에 집어넣기
print("myList:",myList) #myList 출력

for index, value in enumerate(myList):  #열거함수 이용
    print("myList[",index,"]=",value)# 인덱스와 리스트 내의 숫자 출력