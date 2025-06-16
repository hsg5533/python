myList = [] #myList 선언

f = open('data/score.txt','r') # 읽기 모드로 열기

myList = str.split(f.readline()) #리스트 형태로 읽어오기, 문자형태로 변환시켜서

myList = list(map(int, myList)) #문자형태로 불러온 값 다시 숫자형태로 변환


print('myList: ',myList) #출력