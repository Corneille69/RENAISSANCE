# -*- coding: utf-8 -*-
import turtle
import math

t= turtle.Turtle()
t.speed(0)
t.color("yellow") 
t.write("💚")      
turtle.bgcolor("black")

def carazon(n):
     x=19* math.sin(n)**3
     y=14* math.cos(n) - 5 *\
       math.cos(2*n)- 2*math.cos(3*n) -\
       math.cos(4*n)
     return x,y
t.penup
for i in range(15):
    t.goto(0,0)
    t.pendown()
    for n in range(0, 100, 2):
        x, y = carazon(n/10)
        t.goto(x*i, y*i)
    t.penup()

t.hideturtle()
turtle.done
