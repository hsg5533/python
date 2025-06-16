list1 = [1, 2, 3, 4, 5]
list2 = [6, 7, 8, 9]
list3 = list1 + list2
list3.append(0)
print('list3:',list3) #Q1 복붙

print('list3 length:',len(list3)) #리스트 길이 출력

del list3[9] #리스트3에서 인덱스 9 지우기 (0이 지워짐)
print('list3:',list3)# 리스트3 출력

list3.insert(0,0) #리스트3 인덱스0 자리에 0넣기
print('list3:',list3) #리스트3 출력
print('list3 앞에서 3개의 요소 값:',list3[0:3]) #리스트3에서 인덱스 0-2까지 출력
print('list3 뒤에서 3개의 요소 값:', list3[-3:]) #리스트3에서 뒤에서 세번째까지 출력