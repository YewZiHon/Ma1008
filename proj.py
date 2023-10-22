import turtle as t
from random import random

def setup():
    t.ht()#hide turtle
    t.speed(0)#max speed
    t.delay(0)
    t.setup(width=1.0, height=1.0, startx=None, starty=None)#full screen, set origin to center
    t.title("MA1008 mini project")#Change window title
setup()

def line(start, end, colour=(0,0,0), width=1):
    oldwidth=t.width()
    oldcol=t.pencolor()
    t.width(width)
    t.pencolor(colour)
    t.pu()
    t.goto(*start)
    t.pd()
    t.goto(*end)
    t.width(oldwidth)
    t.pencolor(oldcol)

#line((0,0),(100,100))

def datatable(size, headers, data=None):
    CELLWIDTH=100
    CELLHEIGHT=20
    columns,rows=size

t.tracer(0, 0)
for i in range (100):
    line((i,i),((i**2)%100,100))

t.update()










t.done()