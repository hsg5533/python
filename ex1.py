import re
s = input()

p = re.compile("[^0-9]")
print("문자 :"+ "".join(p.findall(s)))
print("숫자 :"+ ''.join(filter(str.isdigit, s)))
