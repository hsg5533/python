import turtle
t =  turtle.Pen()
def regularpentagon(size, filled):
    if filled == True:
        t.begin_fill()

    for x in range(1,5):
        t.right(90)  # 정오각형 한 내각의 크기 90'
        t.forward(size)

    if filled == True:
        t.end_fill()


t.color('green')
regularpentagon(100, True)
