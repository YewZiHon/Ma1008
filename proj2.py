import turtle as t
import math

#CONSTANTS
vertexMarker_line = "line"
vertexMarker_curve0 = "curve0"
vertexMarker_curve1 = "curve1"
vertexMarker_curveEnd = "curveEnd"
vertexMarker_End = "End"

editMode_point_edit = "point_edit"
editMode_transformations = "transformations"
editMode_preview_transformations = "preview_transformations"
editMode_show_result="show_result"

CURVEPOINTS=100
CLOSE_TO_POINT=8#threshold to detect a click on a point
GRIDSIZE=50

#globals
g_new_vertices=[]
g_new_selected_point=-1
g_draw_grid_flag=False
g_edit_mode=editMode_point_edit
g_table_bounds=[]#x bound, y bound, y increment
g_new_transformation=[]
g_all_data=[]

def setup():
    global sc
    t.ht()#hide turtle
    t.speed(0)#max speed
    t.delay(0)
    t.setup(width=1.0, height=1.0, startx=None, starty=None)#full screen, set origin to center
    t.title("MA1008 mini project")#Change window title
    sc=t.getscreen()
    t.tracer(0, 0)

def plotPolygon(vertices, line="blue", fill=None):
    """
    plots polygon, takes in a list of vertices
    """
    t.pu()
    t.goto(*vertices[0][1:])
    t.pd()
    sx,sy=0,0
    points=[]
    if fill is not None:
        t.fillcolor(fill)
        t.begin_fill()
    else:
        t.color("blue")
    for vertex in vertices:
        #if line vertex
        if vertex[0]==vertexMarker_line:
            t.pencolor(line)
            t.goto(*vertex[1:])
            if fill is None:
                t.dot("black")

        #if curve line
        elif vertex[0]==vertexMarker_curve0:
            #get start point
            sx,sy=t.position()
            if fill is None:
                t.pencolor("red")
                t.goto(*vertex[1:])
                t.dot("red")
            points=[*vertex[1:]]

        elif vertex[0]==vertexMarker_curve1:
            if fill is None:
                t.pencolor("red")
                t.goto(*vertex[1:])
                t.dot("red")
            points.extend(vertex[1:])

        elif vertex[0]==vertexMarker_curveEnd:
            if fill is None:
                t.pencolor("red")
                t.goto(*vertex[1:])
                t.dot("black")  
            points.extend(vertex[1:]) 
            #plot curve
            t.pu()
            t.pencolor(line)
            t.goto(sx,sy)
            t.pd()
            for i in range(CURVEPOINTS+1):
                p = i/CURVEPOINTS
                x = sx*(1-p)**3 + 3*points[0]*p*(1-p)**2 + 3*points[2]*p**2*(1-p) + points[4]*p**3
                y = sy*(1-p)**3 + 3*points[1]*p*(1-p)**2 + 3*points[3]*p**2*(1-p) + points[5]*p**3
                t.goto(x, y)

        # if return to start
        elif vertex[0]==vertexMarker_End:
            t.pencolor("blue")
            t.goto(*vertices[0][1:])
        #t.write(vertex)
    if fill is not None:
        t.end_fill()
       
def newPolygon():
    """
    Prompts user to create a new polygon
    """
    global g_new_vertices, g_new_transformation
    #start with a simple square
    g_new_vertices=[(vertexMarker_line,0,0),(vertexMarker_curve0,100,0),(vertexMarker_curve1,100,100),(vertexMarker_curveEnd,0,100),(vertexMarker_line,-150,100),(vertexMarker_line,-150,0),(vertexMarker_End,)]
    g_new_transformation=[5, 0,0, 60, 100, 100, 0, 0, "None","Blue","red"]
    plotPolygon(g_new_vertices)
    t.update() 

def clickhandler_movepoint(x,y):
    global g_new_vertices, g_new_selected_point, g_edit_mode, g_table_bounds, g_new_transformation
    
    if g_edit_mode==editMode_point_edit:
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
    if g_edit_mode==editMode_transformations:
        xmax,ymax,inc = g_table_bounds
        if -xmax<=x<=xmax and -ymax<=y<=ymax-1:#-1 is to prevent clicking on the line to result in an out of range index
            tableIndex=int((y+ymax)//inc-ymax*2/inc)*-1-1#calculate cell clicked, flip, invert and offset range to be within 0 to 10

            #edit table value

            #if pattern count
            if tableIndex==0:
                newPatternCount = sc.textinput("Pattern count", "Enter new pattern count:")
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    try:
                        if newPatternCount is None:
                            break
                        newPatternCount=int(newPatternCount)
                        if newPatternCount<1 or newPatternCount>10:
                            raise ValueError
                        break
                    except ValueError:
                        newPatternCount = sc.textinput("Pattern count", "Enter new pattern count, please enter an integer between 1 and 10:")
                        sc.listen()#reclaim listener after textinput claimed handler
                if newPatternCount is not None:
                    g_new_transformation[tableIndex]=newPatternCount

            #if transform
            elif tableIndex==1 or tableIndex==2:
                newTransform = sc.textinput("Transform", "Enter new transformation:")
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    try:
                        if newTransform is None:
                            break
                        newTransform=int(newTransform)
                        if newTransform<-1000 or newTransform>1000:
                            raise ValueError
                        break
                    except ValueError:
                        newTransform = sc.textinput("Transform", "Enter new transformation, please enter an integer between -1000 and 1000:")
                        sc.listen()#reclaim listener after textinput claimed handler
                if newTransform is not None:
                    g_new_transformation[tableIndex]=newTransform

            #if rotate
            elif tableIndex==3:
                newrotate = sc.textinput("Rotate", "Enter new rotation:")
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    try:
                        if newrotate is None:
                            break
                        newrotate=int(newrotate)
                        if newrotate<-360 or newrotate>360:
                            raise ValueError
                        break
                    except ValueError:
                        newrotate = sc.textinput("rotation", "Enter rotation, please enter an integer between -360 and 360:")
                        sc.listen()#reclaim listener after textinput claimed handler
                if newrotate is not None:
                    g_new_transformation[tableIndex]=newrotate

            #if scale
            elif tableIndex==4 or tableIndex==5:
                newScale = sc.textinput("Scale", "Enter new scale:")
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    try:
                        if newScale is None:
                            break
                        newScale=int(newScale)
                        if newScale<1 or newScale>1000:
                            raise ValueError
                        break
                    except ValueError:
                        newScale = sc.textinput("Scale", "Enter new scale, please enter an integer between 1 and 1000:")
                        sc.listen()#reclaim listener after textinput claimed handler
                if newScale is not None:
                    g_new_transformation[tableIndex]=newScale
            
            #if shear
            elif tableIndex==6 or tableIndex==7:
                newShear = sc.textinput("Shear", "Enter new shear:")
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    try:
                        if newShear is None:
                            break
                        newShear=int(newShear)
                        if newShear<-200 or newShear>200:
                            raise ValueError
                        break
                    except ValueError:
                        newShear = sc.textinput("Scale", "Enter new shear, please enter an integer between -200 and 200:")
                        sc.listen()#reclaim listener after textinput claimed handler
                if newShear is not None:
                    g_new_transformation[tableIndex]=newShear

            #if rotation
            elif tableIndex==8:
                newReflection = sc.textinput("Reflection", "Enter new reflection (X,Y,None):")
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    if newReflection=='Y' or 'y':
                        newReflection='Y'
                        break
                    elif newReflection=='X' or 'x':
                        newReflection='X'
                        break
                    elif newReflection.upper()=="NONE":
                        newReflection='None'
                        break
                    elif newReflection == None:
                        break
                    newReflection = sc.textinput("Reflection", "Enter new reflection, please enter either X, Y or None:")
                    sc.listen()#reclaim listener after textinput claimed handler
                if newReflection is not None:
                    g_new_transformation[tableIndex]=newReflection
            #if colour change
            elif tableIndex==9 or tableIndex==10:
                newcolour = sc.textinput("Colour", "Enter new colour:")
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    try:
                        if newcolour==None:
                            pass
                        #if line colour
                        elif tableIndex==9:
                            t.pencolor(newcolour)        
                        else:
                            t.fillcolor(newcolour)
                        break
                    except:
                        newcolour = sc.textinput("Colour", "Enter new colour, close this prompt and see help(h) for valid colours:")
                        sc.listen()#reclaim listener after textinput claimed handler
                if newcolour is not None:
                    g_new_transformation[tableIndex]=newcolour
            redraw()

def getClosestLine(x,y):
    global g_new_vertices
    #get a list of valid lines
    lines=[]
    prevlineType=None
    prevVertex=(0,0)
    indexcount=0
    for vertex in g_new_vertices:
        if vertex[0] ==vertexMarker_line:
            if prevlineType==vertexMarker_line or prevlineType==vertexMarker_curveEnd:
                lines.append(prevVertex+vertex[1:]+(indexcount,))
        prevlineType=vertex[0]
        if vertex[0]!=vertexMarker_End:
            prevVertex=vertex[1:]
        elif g_new_vertices[0][0]==vertexMarker_line:
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
    global g_new_vertices, g_edit_mode

    if g_edit_mode==editMode_point_edit:
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
            g_new_vertices.insert(targetIndex, (vertexMarker_line,lx,ly))
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

def drawTransformationTable(tabledata):
    """
    x,y offset
    angle offset
    pattern type
    shear xy , transform xy, rotate, scale xy, reflection xy
    pattern count
    """
    global g_table_bounds
    CELL_NAME_WIDTH=300
    CELL_DATA_WIDTH=100
    CELL_HEIGHT=30
    FONT=('Courier', 18, 'normal')
    ROW_DATA=["Pattern count", "Transform X","Transform Y", "Rotate", "Scale X", "Scale Y", "Shear X", "Shear Y", "Reflection", "Line colour", "Fill colour"]
    UNITS_DATA=["", "px","px", "deg", "%", "%", "%", "%", "", "", ""]
    CELLS_Y=len(ROW_DATA)
    xpoint=int((CELL_NAME_WIDTH+2*CELL_DATA_WIDTH)/2)
    ypoint=int(CELL_HEIGHT*CELLS_Y/2)

    #draw x grid lines
    t.pu()
    for yline in range(-ypoint,ypoint+1,CELL_HEIGHT):
        
        t.goto(-xpoint,yline)
        t.pd()
        t.goto(xpoint,yline)
        t.pu()
        t.goto(-xpoint+10,yline+5)

    #draw y lines
    totalOffset=0
    for i in range(4):
        t.pu()
        t.goto(-xpoint+totalOffset,-yline)
        t.pd()
        t.goto(-xpoint+totalOffset,yline)
        if i==0:
            totalOffset+=CELL_NAME_WIDTH
        else:
            totalOffset+=CELL_DATA_WIDTH

    #write names and data
    t.pu()
    starty=ypoint
    for i in range(CELLS_Y):
        starty-=CELL_HEIGHT
        #print name
        t.goto(-xpoint+5,starty)
        t.write(ROW_DATA[i], font=FONT)
        #print data
        t.goto(-xpoint+CELL_NAME_WIDTH+5,starty)
        t.write(tabledata[i], font=FONT)
        #print units
        t.goto(-xpoint+CELL_NAME_WIDTH+CELL_DATA_WIDTH+5,starty)
        t.write(UNITS_DATA[i], font=FONT)
    g_table_bounds=[xpoint, ypoint, CELL_HEIGHT]

def redraw():
    global g_new_vertices, g_draw_grid_flag, g_edit_mode, g_new_transformation
    t.reset()
    if g_edit_mode==editMode_point_edit:
        if g_draw_grid_flag:
            drawGrid()
        plotPolygon(g_new_vertices)
        t.ht()
    
    if g_edit_mode==editMode_transformations:
        drawTransformationTable(g_new_transformation)
        t.ht()

    if g_edit_mode==editMode_preview_transformations:
        plotPolygon(g_new_vertices,line="blue",fill="red")
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
    global g_new_vertices, g_new_selected_point, g_edit_mode

    if g_new_selected_point!=-1 and g_new_vertices[g_new_selected_point][0]==vertexMarker_line and g_new_vertices[g_new_selected_point+1][0]==vertexMarker_line or g_new_vertices[g_new_selected_point+1][0]==vertexMarker_End and g_edit_mode==editMode_point_edit:#if point is selected
        g_new_vertices.pop(g_new_selected_point)#remove polygon
        #redraw
        t.ht()
        redraw()

def editPoint():
    global g_new_vertices, g_new_selected_point,g_edit_mode

    if g_new_selected_point!=-1 and g_edit_mode==editMode_point_edit:
        newCoords = sc.textinput("Edit Point", "Enter new coordinates X,Y:")
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
    global g_draw_grid_flag, g_edit_mode

    if g_edit_mode==editMode_point_edit:
        g_draw_grid_flag= not g_draw_grid_flag

    redraw()

def editTransformations():
    global g_edit_mode, g_new_selected_point
    if g_edit_mode==editMode_transformations:
        g_edit_mode=editMode_point_edit
    else:
        g_edit_mode=editMode_transformations
    redraw()

def previewPolygons():
    global g_edit_mode, g_new_selected_point
    if g_edit_mode==editMode_preview_transformations:
        g_edit_mode=editMode_point_edit
    else:
        g_edit_mode=editMode_preview_transformations
    redraw()

def addPolygon():
    return
    #g_all_data.append()

setup()

sc.onclick(clickhandler_movepoint,btn=1)
sc.onclick(clickhandler_addpoint,btn=3)
t.ondrag(ondraghandler)
sc.onkeypress(delPointhandler,'Delete')
sc.onkeypress(editPoint,'e')
sc.onclick(splineHandler,btn=2)
sc.onkeypress(toggleGrid,'g')
sc.onkeypress(editTransformations,'t')
sc.onkeypress(previewPolygons,'p')
sc.onkeypress(addPolygon,'a')




#show starting polygon
newPolygon()

t.listen()
sc.listen()
t.mainloop()
sc.mainloop()