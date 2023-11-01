import turtle as t
import enum
import math

#CONSTANTS
vertexMarker=enum.Enum("vertexMarker", ["line","curve0","curve1","curveEnd","End"])
CURVEPOINTS=100
CLOSE_TO_POINT=8#threshold to detect a click on a point

#globals
g_new_vertices=[]
g_new_selected_point=-1

def setup():
    global sc
    t.ht()#hide turtle
    t.speed(0)#max speed
    t.delay(0)
    t.setup(width=1.0, height=1.0, startx=None, starty=None)#full screen, set origin to center
    t.title("MA1008 mini project")#Change window title
    sc=t.getscreen()
    t.tracer(0, 0)

def plotPolygon(vertices):
    """
    plots polygon, takes in a list of vertices
    """
    t.pu()
    t.goto(*vertices[0][1:])
    t.pd()
    sx,sy=0,0
    points=[]
    for vertex in vertices:
        #if line vertex
        if vertex[0]==vertexMarker.line:
            t.color("blue")
            t.goto(*vertex[1:])
            t.dot("black")

        #if curve line
        elif vertex[0]==vertexMarker.curve0:
            #get start point
            sx,sy=t.position()
            t.color("red")
            t.goto(*vertex[1:])
            t.dot("red")
            points=[*vertex[1:]]

        elif vertex[0]==vertexMarker.curve1:
            t.color("red")
            t.goto(*vertex[1:])
            t.dot("red")
            points.extend(vertex[1:])

        elif vertex[0]==vertexMarker.curveEnd:
            t.color("red")
            t.goto(*vertex[1:])
            t.dot("black")  
            points.extend(vertex[1:]) 
            #plot curve
            t.pu()
            t.color("light green")
            t.goto(sx,sy)
            t.pd()
            for i in range(CURVEPOINTS+1):
                p = i/CURVEPOINTS
                x = sx*(1-p)**3 + 3*points[0]*p*(1-p)**2 + 3*points[2]*p**2*(1-p) + points[4]*p**3
                y = sy*(1-p)**3 + 3*points[1]*p*(1-p)**2 + 3*points[3]*p**2*(1-p) + points[5]*p**3
                t.goto(x, y)

        # if return to start
        elif vertex[0]==vertexMarker.End:
            t.color("blue")
            t.goto(*vertices[0][1:])
       

def newPolygon():
    """
    Prompts user to create a new polygon
    """
    global g_new_vertices
    #start with a simple square
    g_new_vertices=[(vertexMarker.line,0,0),(vertexMarker.curve0,100,0),(vertexMarker.curve1,100,100),(vertexMarker.curveEnd,0,100),(vertexMarker.line,-150,100),(vertexMarker.line,-150,0),(vertexMarker.End,)]
    plotPolygon(g_new_vertices)
    t.update() 


#rewrite chunk below
def clickhandler_movepoint(x,y):
    global g_new_vertices, g_new_selected_point
    distances=[]
    #find closest vertex
    for vertex in g_new_vertices:
        #find distance
        if len(vertex)==3:
            distances.append(math.sqrt((x-vertex[1])**2+(y-vertex[2])**2))
    #if clicked point is close to a point
    if min(distances)<CLOSE_TO_POINT:
        t.pu()
        t.st()
        t.shape("circle")
        t.goto(*g_new_vertices[distances.index(min(distances))][1:])
        t.update()
        g_new_selected_point=distances.index(min(distances))
    #if not close escape
    else:
        g_new_selected_point=-1
        t.ht()
        t.update()

def clickhandler_addpoint(x,y):
    global g_new_vertices

    #get a list of valid lines
    lines=[]
    prevlineType=None
    prevVertex=(0,0)
    indexcount=0
    for vertex in g_new_vertices:
        if vertex[0] ==vertexMarker.line:
            if prevlineType==vertexMarker.line or prevlineType==vertexMarker.curveEnd:
                lines.append(prevVertex+vertex[1:]+(indexcount,))
        prevlineType=vertex[0]
        if vertex[0]!=vertexMarker.End:
            prevVertex=vertex[1:]
        elif g_new_vertices[0][0]==vertexMarker.line:
            lines.append(prevVertex+g_new_vertices[0][1:]+(len(g_new_vertices)-1,))
        indexcount+=1
    
    #find distance from point to line
    distances=[]
    for line in lines:
        x1,y1,x2,y2,_=line
        distances.append(abs((x2-x1)*(y1-y)-(x1-x)*(y2-y1))/math.sqrt((x2-x1)**2+(y2-y1)**2))
    print(distances)

    #if clicked point is close to a line
    if min(distances)<CLOSE_TO_POINT:
        closest_line=lines[distances.index(min(distances))]
        print(closest_line)
        #calculate closest point on the line
        x1,y1,x2,y2,targetIndex=closest_line
        
        #if horizontal line
        if y1==y2:
            ly=y1
            lx=x
        #if verticle line
        elif x1==x2:
            lx=x1
            ly=y
            
        else:
            m1=(y1-y2)/(x1-x2)
            m2=-1/m1
            lx=(m1*x1-m2*x-y1+y)/(m1-m2)
            ly=m2*(lx-x)+y
        print(x,y,lx,ly)
        g_new_vertices.insert(targetIndex, (vertexMarker.line,lx,ly))
        plotPolygon(g_new_vertices)
        clickhandler_movepoint(lx,ly)
        t.update()

def handler(*coords):
    global g_new_vertices, g_new_selected_point
    print("handler", g_new_selected_point,g_new_selected_point!=-1)
    if g_new_selected_point!=-1:
        print(g_new_vertices[g_new_selected_point][0],coords)
        g_new_vertices[g_new_selected_point]=(g_new_vertices[g_new_selected_point][0],)+coords
        print(*coords,g_new_vertices,(coords,))
        t.reset()
        plotPolygon(g_new_vertices)
        t.pu()
        t.goto(*coords)
        t.update()

setup()
newPolygon()
sc.onclick(clickhandler_movepoint,btn=1)
sc.onclick(clickhandler_addpoint,btn=3)
t.ondrag(handler)

t.listen()
sc.listen()
t.mainloop()
sc.mainloop()