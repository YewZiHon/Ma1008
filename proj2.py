"""
"""
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
CLOSE_TO_POINT=50#threshold to detect a click on a point
GRIDSIZE=50
DEFAULT_VERTICES=[(vertexMarker_line,0,0),(vertexMarker_curve0,100,0),(vertexMarker_curve1,100,100),(vertexMarker_curveEnd,0,100),(vertexMarker_line,-150,100),(vertexMarker_line,-150,0),(vertexMarker_End,)]
DEFAULT_TRANSFORM=[5, 0, 0, 60, 100, 100, 0, 0, "None","Blue","red"]

#globals
g_new_vertices=[]
g_new_selected_point=-1
g_draw_grid_flag=False
g_show_values_flag=True
g_help_menu_flag=False
g_edit_mode=editMode_point_edit
g_table_bounds=[]#x bound, y bound, y increment
g_new_transformation=[]
g_all_data=[]

def setup():
    global sc
    t.ht()#hide turtle
    t.speed(0)#max speed
    t.delay(0)
    #t.setup(width=1.0, height=1.0, startx=None, starty=None)#full screen, set origin to center
    t.title("MA1008 mini project |  Art with geometry and engineering maths")#Change window title
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
            t.pencolor(line)
            t.goto(*vertices[0][1:])

        if g_show_values_flag and g_edit_mode==editMode_point_edit and not vertex[0]==vertexMarker_End:
            t.write(vertex[1:3])
    if fill is not None:
        t.end_fill()
       
def newPolygon():
    """
    Prompts user to create a new polygon
    """
    global g_new_vertices, g_new_transformation
    #start with a polygon
    g_new_vertices=DEFAULT_VERTICES.copy()
    g_new_transformation=DEFAULT_TRANSFORM.copy()
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
                newrotate = sc.textinput("Rotate", "Enter new rotation. Use C to seperate center coordinates:")
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    try:
                        if newrotate is None:
                            break
                        newrotate=newrotate.upper()
                        #remove spcae char
                        newrotate=newrotate.replace(' ','')
                        if 'C' in newrotate and ',' in newrotate:
                            newrotate,coords=newrotate.split('C')
                            coords = coords.split(',')
                            print(coords)
                            if not -360<int(coords[0])<360 or not -1000<int(coords[1])<1000 or not -1000<int(coords[2])<1000:
                                raise ValueError
                        else:
                            coords=[]

                        newrotate=int(newrotate)  

                        if newrotate<-360 or newrotate>360:
                            raise ValueError
                        
                        break
                    except ValueError:
                        newrotate = sc.textinput("rotation", "Enter rotation, please enter an integer between -360 and 360.\n Enter offsets between -1000 and 1000.\nAngle without offset: 60\nAngle with offset center: 60C60,100,-100")
                        sc.listen()#reclaim listener after textinput claimed handler
                if newrotate is not None:
                    if coords==[]:
                        g_new_transformation[tableIndex]=newrotate
                    else:
                        g_new_transformation[tableIndex]=str(newrotate)+'C'+str(coords[0])+','+str(coords[1])+','+str(coords[2])

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
                        if newShear<-100 or newShear>100:
                            raise ValueError
                        break
                    except ValueError:
                        newShear = sc.textinput("Scale", "Enter new shear, please enter an integer between -100 and 100:")
                        sc.listen()#reclaim listener after textinput claimed handler
                if newShear is not None:
                    g_new_transformation[tableIndex]=newShear

            #if rotation
            elif tableIndex==8:
                newReflection = sc.textinput("Reflection", "Enter new reflection (X,Y,XY,None):")
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    if newReflection=='Y' or newReflection=='y':
                        newReflection='Y'
                        break
                    elif newReflection=='X' or newReflection=='x':
                        newReflection='X'
                        break
                    elif newReflection.upper()=="NONE":
                        newReflection='None'
                        break
                    elif newReflection.upper() == 'XY':
                        newReflection='XY'
                        break
                    elif newReflection == None:
                        break
                    newReflection = sc.textinput("Reflection", "Enter new reflection, please enter either X, Y, XY or None:")
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
                            break
                        
                        #if line colour
                        elif tableIndex==9:
                            t.pencolor(newcolour)        
                        else:
                            t.fillcolor(newcolour)
                        g_new_transformation[tableIndex]=newcolour
                        break
                    except:
                        newcolour = sc.textinput("Colour", "Enter new colour, close this prompt and see help(h) for valid colours:")
                        sc.listen()#reclaim listener after textinput claimed handler
                
            redraw()

def getClosestLine(x,y, includeSplines=False):
    global g_new_vertices
    #get a list of valid lines
    lines=[]
    prevlineType=None
    prevVertex=(0,0)
    indexcount=0

    if not includeSplines:
        for vertex in g_new_vertices:
            if vertex[0] ==vertexMarker_line:#if the current vertex is a line
                if prevlineType==vertexMarker_line or prevlineType==vertexMarker_curveEnd:#check if the previous vertex is also a line or a curve end
                    lines.append(prevVertex+vertex[1:]+(indexcount,))
            prevlineType=vertex[0]
            if vertex[0]!=vertexMarker_End:
                prevVertex=vertex[1:]
            elif g_new_vertices[0][0]==vertexMarker_line:
                lines.append(prevVertex+g_new_vertices[0][1:]+(len(g_new_vertices)-1,))
            indexcount+=1
    
    else:
        prevVertex=None
        for vertex in g_new_vertices:
            if prevVertex is not None and vertex[0]!=vertexMarker_End:
                lines.append(prevVertex+vertex[1:]+(indexcount,))
            if vertex[0]!=vertexMarker_End:#get the first point for the vertex
                prevVertex=vertex[1:]
            else:#add end vertex first point to last point
                lines.append(prevVertex+g_new_vertices[0][1:]+(indexcount,))
            indexcount+=1
    
    #print(lines)

    #find distance from point to line
    distances=[]
    for line in lines:
        x1,y1,x2,y2,_=line
        if x1==x2:
            grad=math.inf
        else:
            grad=(y2-y1)/(x2-x1)
        if x1>x2:
            x1,x2=x2,x1
        if y1>y2:
            y1,y2=y2,y1

        #print(f"{line} {grad=} {x1-CLOSE_TO_POINT<x<x2+CLOSE_TO_POINT} {y1-CLOSE_TO_POINT<y<y2+CLOSE_TO_POINT}")

        #check if point is in range of line
        if x1-CLOSE_TO_POINT<x<x2+CLOSE_TO_POINT and y1-CLOSE_TO_POINT<y<y2+CLOSE_TO_POINT:
            dist=abs((x2-x1)*(y1-y)-(x1-x)*(y2-y1))/math.sqrt((x2-x1)**2+(y2-y1)**2)
            distances.append(dist)

            #if out of range of line, calculate distance to point
        else:
            dist1=math.sqrt((x1-x)**2+(y1-y)**2)
            dist2=math.sqrt((x2-x)**2+(y2-y)**2)
            if dist2<dist1:
                distances.append(dist2)
            else:
                distances.append(dist1)
        print(distances[-1])
    closestLine = lines[distances.index(min(distances))]
        
    return distances, closestLine

def clickhandler_addpoint(x,y):
    global g_new_vertices, g_edit_mode

    if g_edit_mode==editMode_point_edit:
        distances,closest_line=getClosestLine(x,y)
        #print("call",(x,y),distances, closest_line)

        #if clicked point is close to a line
        if min(distances)<CLOSE_TO_POINT:
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
    CELL_DATA_WIDTH=200
    CELL_DATA2_WIDTH=50
    CELL_HEIGHT=30
    FONT=('Courier', 18, 'normal')
    ROW_DATA=["Pattern count", "Transform pattern X","Transform pattern Y", "Rotate pattern", "Scale pattern X", "Scale pattern Y", "Shear pattern X", "Shear pattern Y", "Reflection", "Line colour", "Fill colour"]
    UNITS_DATA=["", "px","px", "deg", "%", "%", "%", "%", "", "", ""]
    CELLS_Y=len(ROW_DATA)
    xpoint=int((CELL_NAME_WIDTH+CELL_DATA_WIDTH+CELL_DATA2_WIDTH)/2)
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
        elif i==1:
            totalOffset+=CELL_DATA_WIDTH
        else:
            totalOffset+=CELL_DATA2_WIDTH

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
        plotPattern(g_new_vertices, g_new_transformation)
        
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
    elif g_edit_mode!=editMode_point_edit:
        g_edit_mode=editMode_point_edit
        redraw()

def lineToSpline(vertexIndex):
    """
    find line, add 2 points at 1/3 and 2/3
    """

    global g_new_vertices
    vertexIndex-=1

    #line points 
    x1,y1=g_new_vertices[vertexIndex][1:3]

    #check if the next verted is the end marker, if yes second point is start vertex
    if g_new_vertices[vertexIndex+1][0] != vertexMarker_End:
        x2,y2=g_new_vertices[vertexIndex+1][1:3]
    else:
        x2,y2=g_new_vertices[0][1:3]

    if x2 != x1:
        grad=(y2-y1)/(x2-x1)

    #make x2 and y2 larger than x1 and y1
    if x1>x2:
        x1,x2=x2,x1
    if y1>y2:
        y1,y2=y2,y1

    #if vert line x1=x2
    if x1==x2:
        delta=y2-y1
        clickhandler_addpoint(x1,y1+delta*1/3)
        clickhandler_addpoint(x1,y1+delta*2/3)

    #if vert line, y1=y2
    elif y1==y2:
        delta=x2-x1
        clickhandler_addpoint(x1+delta*1/3,y1)
        clickhandler_addpoint(x1+delta*2/3,y1)

    #slant line
    else:
        deltaX=x2-x1
        deltaY=y2-y1
        
        #positive slope
        if grad>0:
            clickhandler_addpoint(x1+deltaX*1/3,y1+deltaY*1/3)
            clickhandler_addpoint(x1+deltaX*2/3,y1+deltaY*2/3)
        #negative slope 
        else:
            #print(x1,y1)
            #print(x1+deltaX*1/3,y1+deltaY*1/3)
            #print(x1+deltaX*2/3,y1+deltaY*2/3)
            #print(x2,y2)
            clickhandler_addpoint(x1+deltaX*1/3,y1+deltaY*1/3)
            clickhandler_addpoint(x1+deltaX*2/3,y1+deltaY*2/3)
    #update lines to splines
    
    g_new_vertices[vertexIndex+1]=(vertexMarker_curve0,)+g_new_vertices[vertexIndex+1][1:]
    g_new_vertices[vertexIndex+2]=(vertexMarker_curve1,)+g_new_vertices[vertexIndex+2][1:]
    g_new_vertices[vertexIndex+3]=(vertexMarker_curveEnd,)+g_new_vertices[vertexIndex+3][1:]

def splineToLine(vertexIndex):
    global g_new_vertices
    #find points and convert to line
    vertextype= g_new_vertices[vertexIndex][0]
    if vertextype == vertexMarker_curve0:
        g_new_vertices[vertexIndex]=(vertexMarker_line,)+g_new_vertices[vertexIndex][1:]
        g_new_vertices[vertexIndex+1]=(vertexMarker_line,)+g_new_vertices[vertexIndex+1][1:]
        g_new_vertices[vertexIndex+2]=(vertexMarker_line,)+g_new_vertices[vertexIndex+2][1:]
    elif vertextype == vertexMarker_curve1:
        g_new_vertices[vertexIndex-1]=(vertexMarker_line,)+g_new_vertices[vertexIndex-1][1:]
        g_new_vertices[vertexIndex]=(vertexMarker_line,)+g_new_vertices[vertexIndex][1:]
        g_new_vertices[vertexIndex+1]=(vertexMarker_line,)+g_new_vertices[vertexIndex+1][1:]
    elif vertextype == vertexMarker_curveEnd:
        g_new_vertices[vertexIndex-2]=(vertexMarker_line,)+g_new_vertices[vertexIndex-2][1:]
        g_new_vertices[vertexIndex-1]=(vertexMarker_line,)+g_new_vertices[vertexIndex-1][1:]
        g_new_vertices[vertexIndex]=(vertexMarker_line,)+g_new_vertices[vertexIndex][1:]
    redraw()

def splineHandler(*coords):
    global g_edit_mode, g_new_vertices
    if g_edit_mode == editMode_point_edit:
        dist, closestLine =  getClosestLine(*coords, True)
        dist=min(dist)
        if dist < CLOSE_TO_POINT:
            vertexIndex=closestLine[-1]
            vertextype= g_new_vertices[vertexIndex][0]
            if vertextype==vertexMarker_End or vertextype== vertexMarker_line:
                lineToSpline(vertexIndex)
                print(vertexIndex)
            elif vertextype==vertexMarker_curve0 or vertextype==vertexMarker_curve1 or vertextype==vertexMarker_curveEnd:
                splineToLine(vertexIndex)
                
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

def matmul(*mat):
    def mat3x3(mat1,mat2):
        retVal=[]

        #calculate each row
        for i in range(3):
            #for each row in result
            row = []
            #for each colloum in row, in result
            for j in range(3):
                product = 0
                #calculate products
                for k in range(3):
                    product += mat1[i][k]*mat2[k][j]
                #add int to row
                row.append(product)
            #add row to result matrix
            retVal.append(row)
        return retVal
    
    #identity matrix multiplied by any matrix gives back the same matrix
    # I = identity matrix
    # A = matrix
    # AI = A
    IDENTITY=[
        [1,0,0],
        [0,1,0],
        [0,0,1]
    ]
    res=[]

    for matrix in mat:
        #for first matrix
        if not res:
            res=mat3x3(IDENTITY,matrix)
        else:
            res=mat3x3(res,matrix)
    return res

def transMat(a,b):
    return [
        [1,0,a],
        [0,1,b],
        [0,0,1]
    ]

def rotMat(angle):
    angle=math.radians(angle)
    return [
        [math.cos(angle),-math.sin(angle),0],
        [math.sin(angle),math.cos(angle),0],
        [0,0,1]
    ]

def scaleMat(sx,sy):
    #normalise values
    sx=sx/100
    sy=sy/100

    return [
        [sx,0,0],
        [0,sy,0],
        [0,0,1]
    ]

def shearMat(tx,ty):
    tx=tx/100
    ty=ty/100
    return [
        [1,tx,0],
        [ty,1,0],
        [0,0,1]
    ]

def reflectMat(reflection):

    if reflection=="X"or reflection=='x':
        rx=-1
        ry=1
    
    elif reflection=="Y"or reflection=="y":
        rx=1
        ry=-1
    
    elif reflection.upper()=="XY":
        rx=-1
        ry=-1

    else:
        rx=1
        ry=1

    return [
        [rx,0,0],
        [0,ry,0],
        [0,0,1]
    ]

def vertexTransformer(Matrix, vertices=g_new_vertices):
    """
    Takes in a 3x3 matrix and a list of vertices.

    For each vertex in vetices
        Get X and Y coordinates
        Perform matrix multiplication to get the transformed coordinates
    Returns a list of transformed vertices

    @param Matrix 3x3 homogeneous matrix
    @param vertices, a list of vertices, defaults to g_new_vertices
    @return resultVertices, a list of vertices similar to param vertices
    
    """
    rowx,rowy,_=Matrix

    resultVertices=[]
    #do for every point
    for vertex in vertices:
        if vertex[0]==vertexMarker_End:
            resultVertices.append(vertex)
            continue
        #Get x y coords
        pointx,pointy=vertex[1:3]

        #transform with homo coords
        newx=rowx[0]*pointx+rowx[1]*pointy+rowx[2]
        newy=rowy[0]*pointx+rowy[1]*pointy+rowy[2]

        #add to result list
        resultVertices.append((vertex[0],newx,newy))

    return resultVertices

def plotPattern(new_vertices, new_transformations):
    global g_new_transformation, g_new_vertices

    patternCount = new_transformations[0]
    transformX = new_transformations[1]
    transformY = new_transformations[2]
    rotation = new_transformations[3]
    scaleX = new_transformations[4]
    scaleY = new_transformations[5]
    shearX = new_transformations[6]
    shearY = new_transformations[7]
    reflection = new_transformations[8]
    lineCol = new_transformations[9]
    fillCol = new_transformations[10]

    if type(rotation)==str:
        rotation,coords=rotation.split('C')
        rotation=int(rotation)

        rotc, coordx, coordy=coords.split(',')
        rotc, coordx, coordy=int(rotc), int(coordx), int(coordy)
        rotonC=True
        print(rotc, coordx, coordy)
    else:
        rotonC=False

    
    deltaScaleX=scaleX-100
    deltaScaleY=scaleY-100
    if deltaScaleX<0:
        scaleXMult=-1
    else:
        scaleXMult=1
    if deltaScaleY<0:
        scaleYMult=-1
    else:
        scaleYMult=1

    reflection=reflection.upper()

    if reflection=='NONE':
        reflectionpatterns=['NONE']
    elif reflection=='X':
        reflectionpatterns=['NONE','X']
    elif reflection=='Y':
        reflectionpatterns=['NONE','Y']
    elif reflection=='XY':
        reflectionpatterns=['NONE','X','Y','XY']
    for reflect in reflectionpatterns:
        #plot first polygon
        firstVertex=vertexTransformer(reflectMat(reflect), new_vertices)
        plotPolygon(firstVertex,line=lineCol,fill=fillCol)
        for i in range(patternCount-1):
            j=(i+1)/(patternCount-1)

            if scaleXMult==-1:
                jX=1-j
            else:
                jX=j

            if scaleXMult==-1:
                jY=1-j
            else:
                jY=j
            if rotonC:
                new_vertices=vertexTransformer(transMat(-coordx,-coordy),new_vertices)
                new_vertices=vertexTransformer(rotMat(rotc*j),new_vertices)
                new_vertices=vertexTransformer(transMat(coordx,coordy),new_vertices)

            homoCoords=matmul(transMat(transformX*j,transformY*j), rotMat(rotation*j), scaleMat(scaleX+deltaScaleX*jX*scaleXMult,scaleY+deltaScaleY*jY*scaleYMult), shearMat(shearX*j, shearY *j), reflectMat(reflect))
            #homoCoords=matmul(transMat(transformX*j,transformY*j), scaleMat(10,10))
            transformed_vectors = vertexTransformer(homoCoords,new_vertices)
            plotPolygon(transformed_vectors,line=lineCol,fill=fillCol)

def offsetPolygon():
    global g_edit_mode, g_new_vertices

    if g_edit_mode==editMode_point_edit:
        axisToOffset = sc.textinput("Relative offset", "Enter Axis(X)(Y) or rotation(R) to offset:")
        sc.listen()#reclaim listener after textinput claimed handler

        while True:
            if axisToOffset==None:
                return
            axisToOffset=axisToOffset.upper()
            if axisToOffset=='X' or axisToOffset=='Y' or axisToOffset=='R':
                break
            elif axisToOffset==None:
                return
            else:
                axisToOffset = sc.textinput("Relative offset", "Enter Axis(X)(Y) or rotation(R) to offset:")
                sc.listen()#reclaim listener after textinput claimed handler
        if axisToOffset =='X':
            xAxisOffset = sc.textinput("X relative offset", "Enter X axis offset:")
            sc.listen()#reclaim listener after textinput claimed handler
            while True:
                if xAxisOffset==None:
                    return
                try:
                    xAxisOffset=int(xAxisOffset)
                    if not -1000<=xAxisOffset<=1000:
                        raise ValueError
                    break
                except (ValueError,TypeError):
                    xAxisOffset = sc.textinput("X relative offset", "Enter X axis offset(An integer between -1000 and 1000):")
                sc.listen()#reclaim listener after textinput claimed handler

            g_new_vertices=vertexTransformer(transMat(xAxisOffset,0),g_new_vertices)
            redraw()

        elif axisToOffset =='Y':
            yAxisOffset = sc.textinput("Y relative offset", "Enter Y axis offset:")
            sc.listen()#reclaim listener after textinput claimed handler
            while True:
                try:
                    yAxisOffset=int(yAxisOffset)
                    if not -1000<=yAxisOffset<=1000:
                        raise ValueError
                    break
                except (ValueError,TypeError):
                    yAxisOffset = sc.textinput("Y relative offset", "Enter Y axis offset(An integer between -1000 and 1000):")
                sc.listen()#reclaim listener after textinput claimed handler

            g_new_vertices=vertexTransformer(transMat(0,yAxisOffset),g_new_vertices)
            redraw()

        elif axisToOffset =='R':
            rotOffset = sc.textinput("Rotation offset", "Enter rotation offset:")
            sc.listen()#reclaim listener after textinput claimed handler
            while True:
                try:
                    rotOffset=int(rotOffset)
                    if not -360<=rotOffset<=360:
                        raise ValueError
                    break
                except (ValueError,TypeError):
                    rotOffset = sc.textinput("Rotationoffset", "Enter rotation offset(An integer between -1000 and 1000):")
                sc.listen()#reclaim listener after textinput claimed handler

            g_new_vertices=vertexTransformer(rotMat(rotOffset),g_new_vertices)
            redraw()

def showHideCoordinates():
    global g_show_values_flag
    g_show_values_flag = not g_show_values_flag
    if g_edit_mode==editMode_point_edit:
        redraw()

def addPolygon():
    global g_all_data, g_new_vertices, g_new_transformation
    axisToOffset = sc.textinput("Confirm add polygon", "Enter (Y) to confirm:")
    sc.listen()#reclaim listener after textinput claimed handler
    if axisToOffset.upper() =='Y':
        g_all_data.append([g_new_vertices.copy(),g_new_transformation.copy()])
        sc.textinput("Polygon added", "Polygon added!\nClose to continue")
        sc.listen()#reclaim listener after textinput claimed handler

def showAll():
    global g_all_data, g_edit_mode

    g_edit_mode=editMode_show_result

    print(g_all_data)
    t.reset()
    for vertices_data, transformation_data in g_all_data:
        plotPattern(vertices_data,transformation_data)
        t.ht()
    t.update()        

def saveFile():
    global g_all_data

    if g_all_data==[]:
        sc.textinput("Error", "No data to save, add polygons first!")
        sc.listen()#reclaim listener after textinput claimed handler
        return

    saveFileName = sc.textinput("Save File", "Enter save file name:")
    sc.listen()#reclaim listener after textinput claimed handler

    while True:
        if saveFileName==None:
            return
        
        try:
            saveFileHandle = open(saveFileName,'w')
            break
        
        except OSError:
            saveFileName = sc.textinput("Save File", "Error creating file.\nEnter save file name:")
            sc.listen()#reclaim listener after textinput claimed handler

    for vertices_data, transformation_data in g_all_data:
        vertexDataString=''
        for vertex in vertices_data:
            vertexString=''
            for i in vertex:
                i=str(i)
                vertexString+=i+','
            vertexString=vertexString[:-1]
            vertexDataString+=vertexString+'|'
        saveFileHandle.write('@'+vertexDataString[:-1]+'\n')

        transDataString=''
        for transform in transformation_data:
            transform=str(transform)
            transDataString+=transform+','
        saveFileHandle.write('#'+transDataString[:-1]+'\n')
        saveFileHandle.write('\n')

def openFile():
    global g_all_data
    openFileName = sc.textinput("Open File", "Enter input file name:")
    sc.listen()#reclaim listener after textinput claimed handler

    while True:
        if openFileName==None:
            return
        
        try:
            openFileHandle = open(openFileName,'r')
            break
        
        except FileNotFoundError:
            openFileName = sc.textinput("Open File", "Error opening file, check file name.\nEnter input file name:")
            sc.listen()#reclaim listener after textinput claimed handler


    g_all_data=[]
    while True:
        vertexData = openFileHandle.readline()
        transData = openFileHandle.readline()
        openFileHandle.readline()#clear newline char

        #if end of file
        if vertexData=='' or transData =='':
            break
        
        #convert vertex list to list of tuples
        vertexData=vertexData[1:-1].split('|')
        vertexList=[]
        for vertex in vertexData:
            vertexRaw= vertex.split(',')
            vertex=()
            for i in vertexRaw:
                try:
                    i=float(i)
                    i=int(i)
                except ValueError:
                    pass
                vertex=vertex+(i,)
            vertexList.append(vertex)
        print(vertexList)

        transData=transData[1:-1].split(',')
        transList=[]
        for trans in transData:
            if trans.replace('-','').isnumeric():
                trans=int(trans)
            transList.append(trans)
        print(transList)
        g_all_data.append([vertexList,transList])
    redraw()
    showAll()

def createNew():
    confirmNew = sc.textinput("Confirm new polygon", "Enter (Y) to confirm:")
    sc.listen()#reclaim listener after textinput claimed handler
    if confirmNew.upper() =='Y':
        t.reset()
        t.ht()
        newPolygon()

def showHelp():
    global g_help_menu_flag
    if g_help_menu_flag==False:
        g_help_menu_flag=True
        t.reset()
        sc.bgpic("help.gif")
    else:
        g_help_menu_flag=False
        sc.bgpic('nopic')
        if g_edit_mode!=editMode_show_result:
            redraw()
        else:
            showAll()

setup()

sc.onclick(clickhandler_movepoint,btn=1)
sc.onclick(clickhandler_addpoint,btn=3)
t.ondrag(ondraghandler)
sc.onkeypress(delPointhandler,'Delete')
sc.onkeypress(editPoint,'e')
sc.onkeypress(editPoint,'E')
sc.onclick(splineHandler,btn=2)
sc.onkeypress(toggleGrid,'g')
sc.onkeypress(toggleGrid,'G')
sc.onkeypress(editTransformations,'t')
sc.onkeypress(editTransformations,'T')
sc.onkeypress(previewPolygons,'p')
sc.onkeypress(previewPolygons,'P')
sc.onkeypress(offsetPolygon,'x')
sc.onkeypress(offsetPolygon,'X')
sc.onkeypress(addPolygon,'a')
sc.onkeypress(addPolygon,'A')
sc.onkeypress(showHideCoordinates,'v')
sc.onkeypress(showHideCoordinates,'V')
sc.onkeypress(showAll,'g')
sc.onkeypress(showAll,'G')
sc.onkeypress(saveFile,'s')
sc.onkeypress(saveFile,'S')
sc.onkeypress(openFile,'o')
sc.onkeypress(openFile,'O')
sc.onkeypress(createNew,'n')
sc.onkeypress(createNew,'N')
sc.onkeypress(showHelp,'h')
sc.onkeypress(showHelp,'H')

#show starting polygon
newPolygon()

t.listen()
sc.listen()
t.mainloop()
sc.mainloop()


#todo
#help menu