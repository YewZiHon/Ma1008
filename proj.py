import turtle as t
import enum

#CONSTANTS
vertexMarker=enum.Enum("vertexMarker", ["End"])
CURVEPOINTS=100


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

def plotPolygon(vertices):
    """
    plots polygon, takes in a list of vertices
    """
    t.pu()
    t.goto(*vertices[0])
    t.pd()
    for vertex in vertices:
        #if line vertex
        if len(vertex)==2:
            t.color("blue")
            t.goto(*vertex)
            t.dot("black")

        #if curve line
        elif len(vertex)==6:
            #get start point
            sx,sy=t.position()

            #plot guidelines
            for i in range(3):
                t.color("red")
                t.goto(*vertex[i*2:i*2+2])
                #plot the dots, only red for spline guidelines
                if i!=2:
                    t.dot("red")
                else:
                    t.dot("black")
            
            #plot curve
            t.pu()
            t.color("light green")
            t.goto(sx,sy)
            t.pd()
            for i in range(CURVEPOINTS+1):
                p = i/CURVEPOINTS
                x = sx*(1-p)**3 + 3*vertex[0]*p*(1-p)**2 + 3*vertex[2]*p**2*(1-p) + vertex[4]*p**3
                y = sy*(1-p)**3 + 3*vertex[1]*p*(1-p)**2 + 3*vertex[3]*p**2*(1-p) + vertex[5]*p**3
                t.goto(x, y)

        # if return to start
        elif len(vertex)==1:
            if vertex[0]==vertexMarker.End:
                t.color("blue")
                t.goto(*vertices[0])

def newPolygon():
    """
    Prompts user to create a new polygon
    """
    #start with a simple square
    vertices=[(0,0),(100,0,100,100,0,100),(vertexMarker.End,)]
    plotPolygon(vertices)

#t.tracer(0, 0)
newPolygon()
#t.update()

def clickhandler(x,y):
    print(x,y)

t.onscreenclick(clickhandler)

def clickhandler():
    print("cick")

t.onclick(clickhandler,1)




t.mainloop()