# ConvertUnit.py

# 평→제곱미터
def Pyung2msq(value):
    Msq=value*3.3
    return Msq

# 제곱미터→평
def Msq2pyung(value):
    Pyung=value/3.3
    return Pyung

# 센티미터→인치
def Cm2inch(value):
    inch=value*0.394
    return inch

# 인치→센티미터
def Inch2cm(value):
    cm=value/0.394
    return cm

#화씨온도→섭씨온도
def TempF2C(value):
    TempC=(value-32.0)*5.0/9.0
    return TempC

# 섭씨온도→화씨온도
def TempC2F(value):
    TempF=(value*9.0/5.0)+32
    return TempF


