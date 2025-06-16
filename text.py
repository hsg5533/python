infile = open("a.txt", "r") #이름 a의 텍스트 파일을 읽는다.

for line in infile:
    print( "[" +line.rstrip() + "]" ) #대괄호를 추가하고 계행문자 (\n)을 지운다
infile.close()
