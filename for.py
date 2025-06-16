data=[1,2,3,4,5]
n=len(data) #n은 data의 길이를 의미하므로 5의 값을 가진다
a=1

for i in range(n): #range(n)은 n=5이므로 range(5)와 같아서 범위는 0,1,2,3,4이다. 따라서 i가 가질 수 있는 수는 0,1,2,3,4이다
    print(data) #data의 수열을 출력한다. [1,2,3,4,5]
    del data[0] #data의 수열 중 제일 왼쪽의 데이터를 지움
    data.append(a) #append는 data의 수열 제일 오른쪽에 a의 값을 추가함
    a+=1 #a의 값은 1씩 증가함
