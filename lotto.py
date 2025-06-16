import random

list=[]
good=[1,1,1,1,1,1,1,1,1,1]
str='false'
repeat=0

while str:
    for i in range(10):
        k = random.randrange(0,2)
        list.append(k)
    repeat+=1
    
    print('반복횟수:',repeat,'결과:',list)
    if list==good:
        
        print('당첨')
        print('확률',(1/repeat)*100,'%')
        break
    list.clear()

