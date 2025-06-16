r = open('data/서시(윤동주).txt','a', encoding='utf-8') #한글 읽기 위해 utf-8이용 텍스트 추가를 위해 a 사용

data = "\n\n윤동주"  #줄바꾸기 두번 후 윤동주 입력이라는 data 만들기
r.write(data)  #data를 기반으로 쓰기 명령어 수행

f = open('data/서시(윤동주).txt','r', encoding='utf-8') # 읽어 오기 위해서 새로 열기

s = f.read() # s에 읽은값 저장
print(s) #s 출력