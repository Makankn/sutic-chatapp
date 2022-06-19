#using turtle draw a star

import turtle


turtle.speed(0)
turtle.penup()
turtle.goto(-200, 0)
turtle.pendown()
turtle.begin_fill()
turtle.color("red")
turtle.circle(100)
turtle.end_fill()
turtle.penup()
turtle.goto(-200, 0)
turtle.pendown()
turtle.begin_fill()
turtle.color("blue")
turtle.circle(100)

