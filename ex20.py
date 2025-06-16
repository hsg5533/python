import random

f = open('data/score.txt','w') #score.txt 만들고 쓰기모드로 열기
scoreList =[] #스코어 리스트 선언
for i in range(30): #30까지 범위 지정
    a = random.randint(1,100) #1부터 100까지 랜덤으로 숫자 뽑기
    scoreList.append(a) #리스트 100까지의 숫자 랜덤으로 안에 집어넣기
print("scoreList:",scoreList) #scoreList 출력

# print(' '.join(map(str, scoreList))) 테스트

data = ' '.join(map(str, scoreList)) #map과 join을 이용하여 대괄호와 쉼표 제거
f.write(data) #data값 score파일에 쓰기
f.close() #for문을 이용해서 닫기...