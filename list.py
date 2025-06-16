fruits=['orange','apple','pear','banana','kiwi','apple','mango','watermelon','grape']
print(len(fruits)) #fruits 배열의 길이를 출력

fruits.append('apple') #fruits 배열 끝자리에 apple 원소를 추가
print(fruits)

apple=fruits.count('apple') #apple 원소의 갯수 세기
print(apple)

mango=fruits.index('mango') 
print(mango)

fruits.sort()
print(fruits)

fruits.remove('kiwi')
print(fruits)

fruits.insert(5,'melon')
print(fruits)

print(fruits[-1])
print(fruits.pop())

      
                
