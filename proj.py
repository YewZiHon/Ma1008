import turtle as t
import enum
import math

#CONSTANTS
vertexMarker=enum.Enum("vertexMarker", ["End"])
CURVEPOINTS=100
CLOSE_TO_POINT=8#threshold to detect a click on a point

#globals
g_new_vertices=[]
g_new_handle_vertices=[]
g_new_selected_point=-1


def setup():
    global sc
    t.ht()#hide turtle
    t.speed(0)#max speed
    t.delay(0)
    t.setup(width=1.0, height=1.0, startx=None, starty=None)#full screen, set origin to center
    t.title("MA1008 mini project")#Change window title
    sc=t.getscreen()
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
    global g_new_vertices
    #start with a simple square
    g_new_vertices=[(0,0),(100,0,100,100,0,100),(-100,100),(-100,0),(vertexMarker.End,)]

    plotPolygon(g_new_vertices)

t.tracer(0, 0)
newPolygon()
t.update()

def clickhandler(x,y):
    global g_new_vertices, g_new_selected_point,g_new_handle_vertices
    g_new_handle_vertices=g_new_vertices.copy()
    distances=[]

    #add control points
    for i in range(len(g_new_vertices)):
        #if vertex
        if len(g_new_vertices[i])==6:
            g_new_handle_vertices.append(g_new_vertices[i][0:2]+(i,))
            g_new_handle_vertices.append(g_new_vertices[i][2:4]+(i,))

    #find closest vertex
    for vertex in g_new_handle_vertices:
        #find distance
        #for line point
        if len(vertex)==2:
            distances.append(math.sqrt((x-vertex[0])**2+(y-vertex[1])**2))
        #for curve points
        elif len(vertex)==6:
            distances.append(math.sqrt((x-vertex[4])**2+(y-vertex[5])**2))
        elif len(vertex)==3:
            distances.append(math.sqrt((x-vertex[1])**2+(y-vertex[2])**2))
    #if clicked point is close to a point
    if min(distances)<CLOSE_TO_POINT:
        t.pu()
        t.st()
        t.shape("circle")
        t.goto(*g_new_handle_vertices[distances.index(min(distances))][0:2])
        t.update()
        g_new_selected_point=distances.index(min(distances))
    #if not close escape
    else:
        g_new_selected_point=-1
        t.ht()
        t.update()

sc.onclick(clickhandler)

def handler(*coords):
    global g_new_vertices, g_new_selected_point
    print("handler", g_new_selected_point,g_new_selected_point!=-1)
    if g_new_selected_point!=-1:
        g_new_vertices[g_new_selected_point]=coords
        print(*coords,g_new_vertices,(coords,))
        t.reset()
        plotPolygon(g_new_vertices)
        t.pu()
        t.goto(*coords)
        t.update()

t.ondrag(handler)








t.listen()
sc.listen()
t.mainloop()
sc.mainloop()