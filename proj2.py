import turtle as t
import enum
import math

#CONSTANTS
vertexMarker=enum.Enum("vertexMarker", ["line","curve0","curve1","curveEnd","End"])
CURVEPOINTS=100
CLOSE_TO_POINT=8#threshold to detect a click on a point
GRIDSIZE=50

#globals
g_new_vertices=[]
g_new_selected_point=-1
g_draw_grid_flag=False

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
        #t.write(vertex)
       
def newPolygon():
    """
    Prompts user to create a new polygon
    """
    global g_new_vertices
    #start with a simple square
    g_new_vertices=[(vertexMarker.line,0,0),(vertexMarker.curve0,100,0),(vertexMarker.curve1,100,100),(vertexMarker.curveEnd,0,100),(vertexMarker.line,-150,100),(vertexMarker.line,-150,0),(vertexMarker.End,)]
    plotPolygon(g_new_vertices)
    t.update() 

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

def getClosestLine(x,y):
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
    closestLine = lines[distances.index(min(distances))]

    return distances, closestLine

def clickhandler_addpoint(x,y):
    global g_new_vertices

    distances,closest_line=getClosestLine(x,y)

    #if clicked point is close to a line
    if min(distances)<CLOSE_TO_POINT:
        #print(closest_line)
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
        #print(x,y,lx,ly)
        g_new_vertices.insert(targetIndex, (vertexMarker.line,lx,ly))
        plotPolygon(g_new_vertices)
        clickhandler_movepoint(lx,ly)
        t.update()

def drawGrid():
    y=sc.window_height()
    x=sc.window_width()
    x/=2
    y/=2
    x_step=int(x//GRIDSIZE*GRIDSIZE)
    y_step=int(y//GRIDSIZE*GRIDSIZE)
    t.color("#cfcfcf")
    t.width(1)
    t.pu()
    for linex in range(-x_step, x_step+1, GRIDSIZE):
        t.goto(linex,-y)
        t.pd()
        t.goto(linex,y)
        t.pu()

    for liney in range(-y_step, y_step+1, GRIDSIZE):
        t.goto(-x,liney)
        t.pd()
        t.goto(x,liney)
        t.pu()  

def redraw():
    global g_new_vertices, g_draw_grid_flag
    t.reset()
    if g_draw_grid_flag:
        drawGrid()
    plotPolygon(g_new_vertices)
    t.ht()
    t.update()

def ondraghandler(*coords):
    global g_new_vertices, g_new_selected_point

    #snap to grid
    if g_draw_grid_flag:
        coords=int(round(coords[0]/GRIDSIZE)*GRIDSIZE),int(round(coords[1]/GRIDSIZE)*GRIDSIZE)

    if g_new_selected_point!=-1:
        g_new_vertices[g_new_selected_point]=(g_new_vertices[g_new_selected_point][0],)+coords
        t.pu()
        t.goto(*coords)
        redraw()

def delPointhandler():
    global g_new_vertices, g_new_selected_point

    if g_new_selected_point!=-1 and g_new_vertices[g_new_selected_point][0]==vertexMarker.line and g_new_vertices[g_new_selected_point+1][0]==vertexMarker.line or g_new_vertices[g_new_selected_point+1][0]==vertexMarker.End:#if point is selected
        g_new_vertices.pop(g_new_selected_point)#remove polygon
        #redraw
        t.ht()
        redraw()

def editPoint():
    global g_new_vertices, g_new_selected_point

    if g_new_selected_point!=-1:
        newCoords = sc.textinput("Edit Point", "Enter new coordinates X,y:")
        sc.listen()#reclaim listener after textinput claimed handler
        if newCoords:
            try:
                newx,newy = newCoords.split(',')
                g_new_vertices[g_new_selected_point]=(g_new_vertices[g_new_selected_point][0],int(newx),int(newy))
                print(g_new_vertices)
                redraw()
            except:
                t.ht()
                t.goto(-300,-300)
                t.write("Invalid coordinate entered, please enter coordinates in the format, x,y")
                t.update()

def lineToSpline():
    pass

def splineToLine():
    pass

def splineHandler(*coords):
    
    _, closestLine =  getClosestLine(*coords)
    print(closestLine)
    
def toggleGrid():
    global g_draw_grid_flag
    g_draw_grid_flag= not g_draw_grid_flag
    redraw()

setup()
newPolygon()

sc.onclick(clickhandler_movepoint,btn=1)
sc.onclick(clickhandler_addpoint,btn=3)
t.ondrag(ondraghandler)
sc.onkeypress(delPointhandler,'Delete')
sc.onkeypress(editPoint,'e')
sc.onclick(splineHandler,btn=2)
sc.onkeypress(toggleGrid,'g')

t.listen()
sc.listen()
t.mainloop()
sc.mainloop()