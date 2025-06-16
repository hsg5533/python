list1 = [1, 2, 3, 4, 5] #리스트1 선언

print('list1:',list1) # 리스트1 출력
print('list1[0]=',list1[0],'list1[4]=',list1[4]) #리스트 1의 인덱스 0, 4값 출력

list2 = [6, 7, 8, 9] #리스트2 선언
print('list2:',list2) #리스트2 출력
list3 = list1 + list2 #리스트1 리스트2 합친게 리스트3
print('list3:',list3) #리스트3 출력

list3.append(0) #리스트3의 마지막에 0 추가
print('list3:',list3) #리스트3 출력