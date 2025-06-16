f = open("data/Gettysburg Address.txt",'r') #텍스트 파일 열어서 읽기
while True:
    line = f.readline() #파일의 텍스트를 한줄씩 불러오기, 자동으로 다음줄의 텍스트 부르기
    if not line: break #다음줄에 텍스트가 없으면 종료
    print(line) #텍스트 출력
f.close() #닫기