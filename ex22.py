import copy 
myList = [] #선언

f = open('data/score.txt','r') #읽기 모드로 열기

myList = str.split(f.readline()) # 4번문제 복사

myList = list(map(int, myList))

sortList = copy.deepcopy(myList) #sortList에 myList 복사

sortList.sort() #sortList 내림차순 정렬

print('sortList:',sortList) #출력
print('myList: ',myList)    #출력

