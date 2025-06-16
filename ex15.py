import random

q = random.randint(0,9) #랜덤으로 0~9 사이의 변수 생성

while True: #while 문으로 무한루프문을 만듬
    a= int(input('정답을 맞히세요[0~9]: ')) #int로 문자열로 저장되는 숫자를 강제로 정수형으로 바꾸기.
    if a == q: #a가 q랑 같을때.
        print("정답입니다.")
        break #정답이면 break로 나가기.
    else:# 그 외에 나머지
        print("틀렸습니다.") #정답이 아니면 반복.