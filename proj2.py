"""
MA1008 mini project |  Art with geometry and engineering maths

This program allows a user to generate polygons. 
Polygons are inputed by mouse inputs. Points can be moved and edited.
Points can be added, removed and edited with a prescise text input.
Lines can be changed to splines and splines can be changed to lines.
Precise values of each vertex can be shown.
Points can be moved by left clicking and draging.
Snap to grid can be enabled the grid is set to 50px.
The whole working polygon can be moved and rotated relative to its current 
position and rotation.

The transformations can be controlled by the user. The transformations 
avaliable are translation in the X and Y direction, rotation, scale, shear, 
and reflection. The line color and fill color can be controled. The 
transformations can be patterned. All transformations can be applied 
at the same time. The transformations can be previewed before adding 
the polygon to the final pattern.

The final pattern can be seen. All transformations can be used at the same time.
The number of patterns and the number of vertices of each pattern is unlimited.

Controls

MOUSE

left click - Select vertex
click and drag - Move vertex
right click - Add vertex at point
middle mouse click - Change line to spline or change spline to line

KEYBOARD
e - Edit mode, Edit vertex location
Del - Delete vertex, vertex must not be part of a spline
v - Show/hide values
g - Toggle grid, Snap to grid
x - Offset, moves the entire working polygon by a relative ammount
t - Edit transformations for working polygon
p - Preview working polygon with transformations
a - Add polygon to final polygon and transformations cannot be edited after this
f - Show final polygon
s - Save final polygon
o - Open a save file
n - Create a new polygon, resets to starting polygon and resets transformations of working polygon
h - Show help

"""

import turtle as t
import math

#CONSTANTS
#constant vertexMarker_line
vertexMarker_line = "line"
vertexMarker_curve0 = "curve0"
vertexMarker_curve1 = "curve1"
vertexMarker_curveEnd = "curveEnd"
vertexMarker_End = "End"

#constant editMode
editMode_point_edit = "point_edit"
editMode_transformations = "transformations"
editMode_preview_transformations = "preview_transformations"
editMode_show_result="show_result"

CURVEPOINTS=100#number of lines in a spline
CLOSE_TO_POINT=50#threshold to detect a click on a point
GRIDSIZE=50#snap to grid size

#Below are polygon defaults
DEFAULT_VERTICES=[(vertexMarker_line,0,0),(vertexMarker_curve0,100,0),(vertexMarker_curve1,100,100),(vertexMarker_curveEnd,0,100),(vertexMarker_line,-150,100),(vertexMarker_line,-150,0),(vertexMarker_End,)]
DEFAULT_TRANSFORM=[5, 0, 0, 60, 100, 100, 0, 0, "None","Blue","red"]

#globals
g_new_selected_point=-1
g_draw_grid_flag=False
g_show_values_flag=False
g_help_menu_flag=False
g_edit_mode=editMode_point_edit#the current edit mode
g_table_bounds=[]#x bound, y bound, y increment
g_new_vertices=[]
g_new_transformation=[]
g_all_data=[]

def setup():
    """
    Sets the speed of the turtle, aquire a handle on the turtleScreen object and setup the screen draw buffer.
    """
    global sc#turtlescreen object
    t.ht()#hide turtle
    t.speed(0)#max speed
    t.delay(0)#no delay
    t.setup(width=1.0, height=1.0, startx=None, starty=None)#full screen, set origin to center
    t.title("MA1008 mini project |  Art with geometry and engineering maths")#Change window title
    sc=t.getscreen()#get a handler for the screen
    t.tracer(0, 0)#setup screen buffer

def plotPolygon(vertices, line="blue", fill=None):  
    """
    Plots polygon, takes in a list of vertices.
    
    For lines:
    -goto first vertex
    -pen down
    -go to last vertex

    For curves:
    -find the 3 curve segments
    -pen down
    -go to the first point
    -for each curve segment, calculate position
    -go to curve point until target curve segments are reached

    -if fill is selected
    -begin fill and end fill before and after plotting the polygon

    @param vertices - a list of vertices of a polygon to plot
    @param line - line colour of the polygon to plot, defailts to "blue"
    @param fill - defaults to no fill for edit mode
    """
    #pen up, go to first down then pen down to start drawing
    t.pu()
    t.goto(*vertices[0][1:])
    t.pd()

    #data for splines
    sx,sy=0,0#start point for splines
    points=[]#vertices for the curve points

    #Set fill colour if needed. No fill for edit mode
    if fill is not None:
        t.fillcolor(fill)
        t.begin_fill()
    else:#else set 
        t.color("blue")

    #go through each vertex
    for vertex in vertices:
        #if line vertex
        if vertex[0]==vertexMarker_line:
            t.pencolor(line)#set pen colour
            t.goto(*vertex[1:])#go to next vertex
            if fill is None:
                t.dot("black")#if in edit mode, add a dot.
                

        #if curve line
        elif vertex[0]==vertexMarker_curve0:
            #get start point
            sx,sy=t.position()

            #plot control vertex if in edit mode
            if fill is None:
                t.pencolor("red")#plot control point in red
                t.goto(*vertex[1:])
                t.dot("red")
            points=[*vertex[1:]]#add vertex to spline point array

        elif vertex[0]==vertexMarker_curve1:
            #second control vertex
            if fill is None:
                t.pencolor("red")
                t.goto(*vertex[1:])
                t.dot("red")
            points.extend(vertex[1:])#add vertex to spline point array

        elif vertex[0]==vertexMarker_curveEnd:
            #third control vertex
            if fill is None:
                t.pencolor("red")
                t.goto(*vertex[1:])
                t.dot("black")  
            points.extend(vertex[1:])#add vertex to spline point array

            #plot curve
            t.pu()#Lift pen and move to start point of curve
            t.goto(sx,sy)
            t.pencolor(line)#set line color for spline
            t.pd()#start drawing the curve

            #start calculating the curve segments and plotting curve segment
            for i in range(CURVEPOINTS+1):
                #p will be in range 0.0 to 1.0
                p = i/CURVEPOINTS
                #calculate x and y of each curve point
                x = sx*(1-p)**3 + 3*points[0]*p*(1-p)**2 + 3*points[2]*p**2*(1-p) + points[4]*p**3
                y = sy*(1-p)**3 + 3*points[1]*p*(1-p)**2 + 3*points[3]*p**2*(1-p) + points[5]*p**3
                #move to curve point
                t.goto(x, y)

        # if return to start
        elif vertex[0]==vertexMarker_End:
            t.pencolor(line)
            #goto first vertex to close the polygon
            t.goto(*vertices[0][1:])

        #if vrite values and in edit mode, draw vertex values
        if g_show_values_flag and g_edit_mode==editMode_point_edit and not vertex[0]==vertexMarker_End:
            #get values for x and y coordinates, round to integer and display
            x,y=vertex[1:3]
            x=round(x)
            y=round(y)
            t.write(str(x)+','+str(y))

    #end fill if fill is enabled
    if fill is not None:
        t.end_fill()
       
def newPolygon():
    """
    Prompts user to create a new polygon

    Sets g_new_vertice and g_new_transformation to default values
    Plots a new polygon
    And updates the screen

    """
    global g_new_vertices, g_new_transformation
    #copy default values to g_new_vertice and g_new_transformation
    g_new_vertices=DEFAULT_VERTICES.copy()
    g_new_transformation=DEFAULT_TRANSFORM.copy()
    plotPolygon(g_new_vertices)#plot polygon
    t.update()#push screen buffer to screen

def leftclickhandler(x,y):
    """
    Call back function for left mouse button.
    Left mouse button is used in edit mode and when editing transformation table.

    EDIT MODE

    Select vertex points. 
    Find distance to all points from the clicked point.
    If distance is less than set constant CLOSE_TO_POINT,
    point is the one that the user has intended to click.
    Select the point by moving the turtle to it making the turtle visible.
    
    EDIT TRANSFORM
    Get table boundaries of the transformation table to make sure that clicks 
    are within table bounds. And to check which index the table is clicked.


    @param x, y - x, and y coordinates that the user clicked on.
    """
    global g_new_vertices, g_new_selected_point, g_edit_mode, g_table_bounds, g_new_transformation
    
    #left click handler for edit mode
    if g_edit_mode==editMode_point_edit:
        distances=[]#array for storing distances to vertices
        #find closest vertex
        for vertex in g_new_vertices:
            #find distance
            if len(vertex)==3:#only for vertices with x, y coords. And not end marker.
                #use pythagorean distance for finding the distance between the vertex and point clicked
                #dist^2=deltaX^2+deltaY^2
                distances.append(math.sqrt((x-vertex[1])**2+(y-vertex[2])**2))
        
        #if clicked point is close to a point
        if min(distances)<CLOSE_TO_POINT:
            #stop drawing, pen up and show turtle.
            t.pu()
            t.st()
            t.shape("circle")#set turtle to circle shape
            t.goto(*g_new_vertices[distances.index(min(distances))][1:])#go to closest point
            t.update()#push turtle to screen
            g_new_selected_point=distances.index(min(distances))#update the index of the closest vertex
        
        #if not close, user lcicked on empty space, escape selected point state.
        else:
            g_new_selected_point=-1#no selected point
            t.ht()#hide turtle and update screen
            t.update()
    
    #left click handler for transformation table
    if g_edit_mode==editMode_transformations:
        xmax,ymax,inc = g_table_bounds#get pre calculated table bounds.
        if -xmax<=x<=xmax and -ymax<=y<=ymax-1:#-1 is to prevent clicking on the line to result in an out of range index
            tableIndex=int((y+ymax)//inc-ymax*2/inc)*-1-1#calculate cell clicked, flip, invert and offset range to be within 0 to 10

            #if pattern count
            if tableIndex==0:
                newPatternCount = sc.textinput("Pattern count", "Enter new pattern count:")#ask for new pattern count
                sc.listen()#reclaim listener after textinput claimed handler

                #check if given number is valid
                while True:
                    try:
                        #check if the user cancled the prompt.
                        if newPatternCount is None:
                            break
                        
                        newPatternCount=int(newPatternCount)#attempt to convert to integer
                        if newPatternCount<1 or newPatternCount>100:#check if value is in range
                            raise ValueError
                        break

                    #error handler, prompt user again
                    except ValueError:
                        newPatternCount = sc.textinput("Pattern count", "Enter new pattern count, please enter an integer between 1 and 10:")#ask for new pattern count with limits
                        sc.listen()#reclaim listener after textinput claimed handler
                
                #if the user gave a valid value, save to list
                if newPatternCount is not None:
                    g_new_transformation[tableIndex]=newPatternCount

            #if transform
            elif tableIndex==1 or tableIndex==2:
                newTransform = sc.textinput("Transform", "Enter new transformation:")#ask for new transform value
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    try:
                        #check if the user cancled the prompt.
                        if newTransform is None:
                            break
                        newTransform=int(newTransform)#attempt to convert to integer
                        if newTransform<-1000 or newTransform>1000:
                            raise ValueError
                        break
                    except ValueError:
                        newTransform = sc.textinput("Transform", "Enter new transformation, please enter an integer between -1000 and 1000:")#ask for new transform value with limits
                        sc.listen()#reclaim listener after textinput claimed handler

                #if the user gave a valid value, save to list
                if newTransform is not None:
                    g_new_transformation[tableIndex]=newTransform

            #if rotate
            elif tableIndex==3:
                newrotate = sc.textinput("Rotate", "Enter new rotation. Use C to seperate center coordinates:")#ask for new rotation
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    try:
                        #check if the user cancled the prompt.
                        if newrotate is None:
                            break

                        #convert to upper case
                        newrotate=newrotate.upper()
                        #remove spcae char
                        newrotate=newrotate.replace(' ','')
                        #check the required chars are in the return value
                        if 'C' in newrotate and ',' in newrotate:
                            #split to new rotation and coordinates
                            newrotate,coords=newrotate.split('C')
                            #split x,y coordinates
                            coords = coords.split(',')
                            #check rotation and coords are in range
                            if not -360<int(coords[0])<360 or not -1000<int(coords[1])<1000 or not -1000<int(coords[2])<1000:
                                raise ValueError
                        else:
                            #else no center coords
                            coords=[]

                        #attempt to convert to integer
                        newrotate=int(newrotate)

                        #check rotation is in range
                        if newrotate<-360 or newrotate>360:
                            raise ValueError
                        
                        break
                    except ValueError:#ask for new rotation with help on how
                        newrotate = sc.textinput("rotation", "Enter rotation, please enter an integer between -360 and 360.\n Enter offsets between -1000 and 1000.\nAngle without offset: 60\nAngle with offset center: 60C60,100,-100")
                        sc.listen()#reclaim listener after textinput claimed handler
                
                #if the user gave a valid value, save to list
                if newrotate is not None:
                    if coords==[]:
                        g_new_transformation[tableIndex]=newrotate#copy to transform list as integer
                    else:
                        g_new_transformation[tableIndex]=str(newrotate)+'C'+str(coords[0])+','+str(coords[1])+','+str(coords[2])#convert to string and save to array

            #if scale
            elif tableIndex==4 or tableIndex==5:
                newScale = sc.textinput("Scale", "Enter new scale:")#ask user for scale
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    try:
                        #check if the user cancled the prompt.
                        if newScale is None:
                            break

                        newScale=int(newScale)#attempt to convert to integer
                        #check if scale is in range
                        if newScale<1 or newScale>1000:
                            raise ValueError
                        break

                    except ValueError:
                        newScale = sc.textinput("Scale", "Enter new scale, please enter an integer between 1 and 1000:")#ask user for scale with range
                        sc.listen()#reclaim listener after textinput claimed handler
                
                #if the user gave a valid value, save to list
                if newScale is not None:
                    g_new_transformation[tableIndex]=newScale
            
            #if shear
            elif tableIndex==6 or tableIndex==7:
                newShear = sc.textinput("Shear", "Enter new shear:")#ask user for new shear value
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    try:
                        #check if the user cancled the prompt.
                        if newShear is None:
                            break

                        newShear=int(newShear)#attempt to convert to integer
                        #check if new shear is in range
                        if newShear<-100 or newShear>100:
                            raise ValueError
                        break

                    except ValueError:
                        newShear = sc.textinput("Scale", "Enter new shear, please enter an integer between -100 and 100:")#ask for new shear value, prompt provides valid range
                        sc.listen()#reclaim listener after textinput claimed handler
                
                #if the user gave a valid value, save to list
                if newShear is not None:
                    g_new_transformation[tableIndex]=newShear

            #if rotation
            elif tableIndex==8:
                newReflection = sc.textinput("Reflection", "Enter new reflection (X,Y,XY,None):")#ask the user for a reflection
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    
                    #If else to check if there is a valid reflection
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

                    #check if the user cancled the prompt.
                    elif newReflection == None:
                        break

                    newReflection = sc.textinput("Reflection", "Enter new reflection, please enter either X, Y, XY or None:")#ask the user for a reflection
                    sc.listen()#reclaim listener after textinput claimed handler
                
                #if the user gave a valid value, save to list
                if newReflection is not None:
                    g_new_transformation[tableIndex]=newReflection

            #if colour change
            elif tableIndex==9 or tableIndex==10:
                newcolour = sc.textinput("Colour", "Enter new colour:")#ask the user for a new colour
                sc.listen()#reclaim listener after textinput claimed handler
                while True:
                    try:
                        #check if the user cancled the prompt.
                        if newcolour==None:
                            break
                        
                        #attempt to set the colour, if successful, no errors, else error will be handled by except.
                        #if line colour
                        elif tableIndex==9:
                            t.pencolor(newcolour)        
                        else:#else fill colour
                            t.fillcolor(newcolour)
                        
                        #if the user gave a valid value, save to list
                        g_new_transformation[tableIndex]=newcolour
                        break
                    except:
                        newcolour = sc.textinput("Colour", "Enter new colour, close this prompt and see help(h) for valid colours:")
                        sc.listen()#reclaim listener after textinput claimed handler
           
            #finally, update the transform table
            redraw()

def getClosestLine(x,y, includeSplines=False):
    """
    Finds the closest line to a point

    First, finds a list of valid lines from the list of vertices in the globals, then,
    finds the distance by calculating the perpendicular distance of the line vector to a 
    vector fromed by the clicked point and a point on the line. When the clicked point is 
    out of range, but still near the projected line, the line will be detected as closer, 
    but in reality it is not. There is another check to make sure the line is within range 
    of the clicked point. The pythogoran distane from the clicked point to the line's point 
    is checked and the shortest is selected as the closest distance to the line. The 
    distances and the closest line is returned.

    @see Referenced: https://wikimedia.org/api/rest_v1/media/math/render/svg/aad3f60fa75c4e1dcbe3c1d3a3792803b6e78bf6

    @params x,y - x, y coordinates fow which to find the closest line
    @param includeSplines - Wheather to include the control points of splines, deafults to false
    @return distances, closestLine - tuple
        distances - An array of distances for all indexes
        closestline - The x1,y1,x2,y2,index of a line, a list

    """
    global g_new_vertices

    #initilise array to store lines
    lines=[]
    
    prevlineType=None#variable for storing the vertex type
    prevVertex=(0,0)#stores the previous vertex
    indexcount=0#stores the current index accessed

    #First, find a list of valid lines
    #if spline control lines are not included in the search
    if not includeSplines:
        for vertex in g_new_vertices:#loop through each vertex
            if vertex[0] ==vertexMarker_line:#if the current vertex is a line
                if prevlineType==vertexMarker_line or prevlineType==vertexMarker_curveEnd:#check if the previous vertex is also a line or a curve end
                    lines.append(prevVertex+vertex[1:]+(indexcount,))#add to the line list
            prevlineType=vertex[0]#update the line type
            if vertex[0]!=vertexMarker_End:#if endmarker, add the end point to the start vertex as it is also a line that the user might click on.
                prevVertex=vertex[1:]#update x, y coords of vertex
            elif g_new_vertices[0][0]==vertexMarker_line:
                lines.append(prevVertex+g_new_vertices[0][1:]+(len(g_new_vertices)-1,))
            indexcount+=1
    
    #if spline control lines are included
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

        #unpack line to coordinates
        x1,y1,x2,y2,_=line

        #normalise points so that x2 and y2 will be larger
        if x1>x2:
            x1,x2=x2,x1
        if y1>y2:
            y1,y2=y2,y1

        #print(f"{line} {grad=} {x1-CLOSE_TO_POINT<x<x2+CLOSE_TO_POINT} {y1-CLOSE_TO_POINT<y<y2+CLOSE_TO_POINT}")

        #check if point is in range of line
        if x1-CLOSE_TO_POINT<x<x2+CLOSE_TO_POINT and y1-CLOSE_TO_POINT<y<y2+CLOSE_TO_POINT:#if point clicked is close to the line, use vectors to find distance
            dist=abs((x2-x1)*(y1-y)-(x1-x)*(y2-y1))/math.sqrt((x2-x1)**2+(y2-y1)**2)
            distances.append(dist)

        #if out of range of line, calculate distance to point
        else:
            dist1=math.sqrt((x1-x)**2+(y1-y)**2)#pythagorean distance
            dist2=math.sqrt((x2-x)**2+(y2-y)**2)

            #choose the shoprter distance as it is the one closer to the line
            if dist2<dist1:
                distances.append(dist2)
            else:
                distances.append(dist1)
    #find the closest line by using the index of the minimum distance
    closestLine = lines[distances.index(min(distances))]
    
    #return the distances and the data for the closest line
    return distances, closestLine

def clickhandler_addpoint(x,y):
    """
    Adds a vertex into the polygon with a right click.


    First, uses previously defined function getClosestLine to find the closest line.
    Then, finds the gradient of the line.
    Find the gradient of the perpendicular line, whick would be the negative reciprocial of the graqdient of the line.
    Solve for x and y intercepts.
    Add vertex to array of vertices.
    Redraw polygon.
    Set cursor on point.

    @param x,y - x,y coordiante of the clicked point

    """
    global g_new_vertices, g_edit_mode

    #only able to add points in edit mode, ignore right clicks in other modes
    if g_edit_mode==editMode_point_edit:
        #use getClosestLine to get the closest line
        distances,closest_line=getClosestLine(x,y)

        #if clicked point is close to a line
        if min(distances)<CLOSE_TO_POINT:
            #calculate closest point on the line
            x1,y1,x2,y2,targetIndex=closest_line
            
            #special case for horizontal and verticle line, gradient is infinite and 0
            #if horizontal line
            if y1==y2:
                ly=y1
                lx=x
            #if verticle line
            elif x1==x2:
                lx=x1
                ly=y
                
            else:#calculate the gradients
                m1=(y1-y2)/(x1-x2)#gradient of line
                m2=-1/m1#grad of perpendicular line
                lx=(m1*x1-m2*x-y1+y)/(m1-m2)#Solve for x intercept
                ly=m2*(lx-x)+y#solve for y intercept

            #insert new vertex into array
            g_new_vertices.insert(targetIndex, (vertexMarker_line,lx,ly))
            #redraw opolygon
            plotPolygon(g_new_vertices)
            #set cursor on newly created point
            leftclickhandler(lx,ly)
            t.update()

def drawGrid():
    """
    Graw the grid.
    Only availiable in edit mode. 
    Draws lines in the x and y direction. 
    Centered at 0,0
    Gets the size of the screen and draws lines within the screen bounds.

    """

    #get window width and height
    y=sc.window_height()
    x=sc.window_width()

    #distance from center to edge will be half the height and width
    x/=2
    y/=2

    #floor divide the values to find the number of lines and find the start and coordinates
    x_step=int(x//GRIDSIZE*GRIDSIZE)
    y_step=int(y//GRIDSIZE*GRIDSIZE)

    #set color and width of the line
    t.color("#cfcfcf")
    t.width(1)
    #pen up
    t.pu()

    #plot all lines on the x axis, plot from negative bound, through 0 and to the positive bound
    for linex in range(-x_step, x_step+1, GRIDSIZE):
        t.goto(linex,-y)
        t.pd()
        t.goto(linex,y)
        t.pu()

    #plot all lines on the y axis, plot from negative bound, through 0 and to the positive bound
    for liney in range(-y_step, y_step+1, GRIDSIZE):
        t.goto(-x,liney)
        t.pd()
        t.goto(x,liney)
        t.pu()  

def drawTransformationTable(tabledata):
    """
    Draws table lines first,
    Then writes table names, data and units

    Transformations availiable are:
    pattern count
    shear xy , 
    transform xy, 
    rotate, 
    scale xy, 
    reflection xy

    @param tabledata - list of transformations to plot on the table
    
    """
    global g_table_bounds

    #CONSTANTS
    #for table
    CELL_NAME_WIDTH=300
    CELL_DATA_WIDTH=200
    CELL_DATA2_WIDTH=50
    CELL_HEIGHT=30
    FONT=('Courier', 18, 'normal')

    #constant row data
    ROW_DATA=["Pattern count", "Transform pattern X","Transform pattern Y", "Rotate pattern", "Scale pattern X", "Scale pattern Y", "Shear pattern X", "Shear pattern Y", "Reflection", "Line colour", "Fill colour"]
    UNITS_DATA=["", "px","px", "deg", "%", "%", "%", "%", "", "", ""]
    CELLS_Y=len(ROW_DATA)
    xpoint=int((CELL_NAME_WIDTH+CELL_DATA_WIDTH+CELL_DATA2_WIDTH)/2)
    ypoint=int(CELL_HEIGHT*CELLS_Y/2)

    #draw x grid lines
    t.pu()
    for yline in range(-ypoint,ypoint+1,CELL_HEIGHT):
        #draw from left side to right side
        t.goto(-xpoint,yline)#left side
        t.pd()
        t.goto(xpoint,yline)#right side
        t.pu()
        t.goto(-xpoint+10,yline+5)

    #draw y lines
    totalOffset=0#draws 4 lines, first one at the extreem left and last on extreem right.
    for i in range(4):
        t.pu()
        t.goto(-xpoint+totalOffset,-yline)#bottom of table
        t.pd()
        t.goto(-xpoint+totalOffset,yline)#top of table
        if i==0:
            totalOffset+=CELL_NAME_WIDTH
        elif i==1:
            totalOffset+=CELL_DATA_WIDTH
        else:
            totalOffset+=CELL_DATA2_WIDTH

    #write names and data and units
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

    #set table boundries for editing transformation values later
    g_table_bounds=[xpoint, ypoint, CELL_HEIGHT]

def redraw():
    """
    Clears the screen, redraws polygons in edit mode and preview mode, draws and redraws transformation table

    Checks the state of the current edit mode

    """
    global g_new_vertices, g_draw_grid_flag, g_edit_mode, g_new_transformation

    #clear the screen
    t.reset()

    #if edit mode
    if g_edit_mode==editMode_point_edit:
        if g_draw_grid_flag:#check if the grid is needed
            drawGrid()
        plotPolygon(g_new_vertices)#redraw polygon and hide turtle and update screen
        t.ht()

    #if edit transformations mode
    if g_edit_mode==editMode_transformations:
        drawTransformationTable(g_new_transformation)#redraw transform table with new values
        t.ht()

    if g_edit_mode==editMode_preview_transformations:
        plotPattern(g_new_vertices, g_new_transformation)#plot polygon with patterns
        t.ht()

    #update screen
    t.update()

def ondraghandler(*coords):
    """
    Moves the selected point if any.
    Checks if snap to grid is anabled, if yes, finds nearest x and y point on the grid and snaps to it.


    @params coords - the x and y coordinates that the turtle currently is draged to.
    """
    global g_new_vertices, g_new_selected_point

    #snap to grid
    if g_draw_grid_flag:
        coords=int(round(coords[0]/GRIDSIZE)*GRIDSIZE),int(round(coords[1]/GRIDSIZE)*GRIDSIZE)#find the nearest x and y point 

    if g_new_selected_point!=-1:
        g_new_vertices[g_new_selected_point]=(g_new_vertices[g_new_selected_point][0],)+coords#update the vertices information
        t.pu()
        t.goto(*coords)#goto the selected point
        redraw()#draw the polygon

def delPointhandler():
    """
    Delets a selected point if avaliable and able.
    Only points that are not part of curves can be deleted, 
    control points cannot be deleted and must be converted to line before it can be deleted.

    """
    global g_new_vertices, g_new_selected_point, g_edit_mode

    #check if there is a selected line   
    #makes sure the selected point can be deleted by checking if the point is a line type and the next point is also a line type
    if g_new_selected_point!=-1 and g_new_vertices[g_new_selected_point][0]==vertexMarker_line and g_new_vertices[g_new_selected_point+1][0]==vertexMarker_line or g_new_vertices[g_new_selected_point+1][0]==vertexMarker_End and g_edit_mode==editMode_point_edit:#if point is selected
        g_new_vertices.pop(g_new_selected_point)#remove polygon from array
        #redraw tghe polygon
        t.ht()
        redraw()

def editPoint():
    """
    Handler for the 'e' key being pressed.

    When in edit mode, the user can press 'e' to edit the coordiates of the selected vertex.
    if there is a vertex selected, a prompt would show to ask the user for the new coordinates. 
    A sanity check is performed on those requested coordinates and updated if valid. 

    In Preview mode and transformation table mode, It switches to edit mode.
    """
    global g_new_vertices, g_new_selected_point,g_edit_mode

    #check that there is a selected point and in edit mode
    if g_new_selected_point!=-1 and g_edit_mode==editMode_point_edit:
        showHelp(1)#hide help
        newCoords = sc.textinput("Edit Point", "Enter new coordinates X,Y:")#request for new coordinartes
        sc.listen()#reclaim listener after textinput claimed handler
        if newCoords:
            try:
                newx,newy = newCoords.split(',')#split the coordinates for into x and y coordinates
                g_new_vertices[g_new_selected_point]=(g_new_vertices[g_new_selected_point][0],int(newx),int(newy))#update vertex, attempt to convert to integer
                redraw()#redraw polygojn with new coordinate
            except:
                t.ht()#hide turtle
                t.goto(-300,-300)
                t.write("Invalid coordinate entered, please enter coordinates in the format, x,y")#tell user coordinates are invalid
                t.update()
    
    #else switch to edit mode
    elif g_edit_mode!=editMode_point_edit:
        g_edit_mode=editMode_point_edit
        redraw()#redraw editing mode

def lineToSpline(vertexIndex):
    """
    Find line, add 2 points at 1/3 and 2/3
    First gets the line data.
    Then finds the 1/3 and 2/3 coordinates of the line.
    Adds points to those lines
    Convert to spline points

    @param vertexIndex - index of vertex in g_new_vertices to convert into spline
    """

    global g_new_vertices

    #decrement by 1
    vertexIndex-=1

    #find the line start and end point
    #line points 
    x1,y1=g_new_vertices[vertexIndex][1:3]

    #check if the next verted is the end marker, if yes second point is start vertex
    if g_new_vertices[vertexIndex+1][0] != vertexMarker_End:
        x2,y2=g_new_vertices[vertexIndex+1][1:3]
    else:
        x2,y2=g_new_vertices[0][1:3]

    #calculate gradient of not infinity, check that the line is not a verticle line
    if x2 != x1:
        grad=(y2-y1)/(x2-x1)

    #make x2 and y2 larger than x1 and y1
    if x1>x2:
        x1,x2=x2,x1
    if y1>y2:
        y1,y2=y2,y1

    #if vert line x1=x2
    if x1==x2:
        delta=y2-y1#chnage in y values
        clickhandler_addpoint(x1,y1+delta*1/3)#add two vertices
        clickhandler_addpoint(x1,y1+delta*2/3)

    #if vert line, y1=y2
    elif y1==y2:
        delta=x2-x1#change in x values
        clickhandler_addpoint(x1+delta*1/3,y1)#add two vertices
        clickhandler_addpoint(x1+delta*2/3,y1)

    #slant line
    else:
        #find change in x and y
        deltaX=x2-x1
        deltaY=y2-y1
        
        #positive slope
        if grad>0:
            clickhandler_addpoint(x1+deltaX*1/3,y1+deltaY*1/3)#add two vertices
            clickhandler_addpoint(x1+deltaX*2/3,y1+deltaY*2/3)
        #negative slope 
        else:
            clickhandler_addpoint(x1+deltaX*1/3,y1+deltaY*1/3)#add two vertices
            clickhandler_addpoint(x1+deltaX*2/3,y1+deltaY*2/3)
    
    #update lines to splines, also update the two new created vertices
    g_new_vertices[vertexIndex+1]=(vertexMarker_curve0,)+g_new_vertices[vertexIndex+1][1:]
    g_new_vertices[vertexIndex+2]=(vertexMarker_curve1,)+g_new_vertices[vertexIndex+2][1:]
    g_new_vertices[vertexIndex+3]=(vertexMarker_curveEnd,)+g_new_vertices[vertexIndex+3][1:]

def splineToLine(vertexIndex):
    """
    Convert spline to line

    Get the index of line that is clicked.
    User can click on start, middle and end of the spline. 
    Turn all spline segments into lines.

    @param vertexIndex - index of vertex in g_new_vertices to convert into line
    """


    global g_new_vertices
    #find points and convert to line
    vertextype= g_new_vertices[vertexIndex][0]
    #check whick type of line the user clicked on.
    if vertextype == vertexMarker_curve0:#change current and next two into line
        g_new_vertices[vertexIndex]=(vertexMarker_line,)+g_new_vertices[vertexIndex][1:]
        g_new_vertices[vertexIndex+1]=(vertexMarker_line,)+g_new_vertices[vertexIndex+1][1:]
        g_new_vertices[vertexIndex+2]=(vertexMarker_line,)+g_new_vertices[vertexIndex+2][1:]
    elif vertextype == vertexMarker_curve1:#chnage current, next one and before one onto line
        g_new_vertices[vertexIndex-1]=(vertexMarker_line,)+g_new_vertices[vertexIndex-1][1:]
        g_new_vertices[vertexIndex]=(vertexMarker_line,)+g_new_vertices[vertexIndex][1:]
        g_new_vertices[vertexIndex+1]=(vertexMarker_line,)+g_new_vertices[vertexIndex+1][1:]
    elif vertextype == vertexMarker_curveEnd:#change current and before 2 into line
        g_new_vertices[vertexIndex-2]=(vertexMarker_line,)+g_new_vertices[vertexIndex-2][1:]
        g_new_vertices[vertexIndex-1]=(vertexMarker_line,)+g_new_vertices[vertexIndex-1][1:]
        g_new_vertices[vertexIndex]=(vertexMarker_line,)+g_new_vertices[vertexIndex][1:]
    redraw()#update and redraw polygon

def splineHandler(*coords):
    """
    Call back function for center mouse button.

    Check if in edit mode. 
    Find the closest line.
    If line close enough, check line type.
    If line, turn into spline.
    If curve, turn into line.

    @param coords - x and y coordinate that is clicked
    """
    global g_edit_mode, g_new_vertices

    #check if currently in edit mode
    if g_edit_mode == editMode_point_edit:

        #find the closest line
        dist, closestLine =  getClosestLine(*coords, True)
        dist=min(dist)

        #check if line is closer to line. 
        if dist < CLOSE_TO_POINT:

            #get index and line type
            vertexIndex=closestLine[-1]
            vertextype= g_new_vertices[vertexIndex][0]

            #if line
            if vertextype==vertexMarker_End or vertextype== vertexMarker_line:
                lineToSpline(vertexIndex)
            
            #if curve segment
            elif vertextype==vertexMarker_curve0 or vertextype==vertexMarker_curve1 or vertextype==vertexMarker_curveEnd:
                splineToLine(vertexIndex)
                
def toggleGrid():
    """
    Callback function for "g" key.
    Toggles grid on and off
    Updates polygon
    """

    global g_draw_grid_flag, g_edit_mode

    if g_edit_mode==editMode_point_edit:
        g_draw_grid_flag= not g_draw_grid_flag

    redraw()

def editTransformations():
    """
    Callback for 't' key.
    If currently in transformation table editing, chage to edit mode
    If currently in edit mode or preview mode, change to trable mode
    Redraw table or polygon
    """

    global g_edit_mode, g_new_selected_point

    #check if in table mode
    if g_edit_mode==editMode_transformations:
        g_edit_mode=editMode_point_edit#change to edit mode

    #else in edit mode or preview mode
    else:
        g_edit_mode=editMode_transformations#change to table mode

    #redraw table or polygon
    redraw()

def previewPolygons(): 
    """
    Callback function for polygon editing. 
    Checks if in preview mode
    If in preview mode, change to edit mode.
    Redraw the correct mode
    """
    global g_edit_mode, g_new_selected_point

    #if in previiew mode
    if g_edit_mode==editMode_preview_transformations:
        g_edit_mode=editMode_point_edit#change to edit mode

    #else in edit mode or transform table mode
    else:
        g_edit_mode=editMode_preview_transformations#chnage to preview polygon mode
    
    #update the polygon preview
    redraw()

def matmul(*mat):
    """
    Matrix multiplication for only 3x3 matrices.
    For each matrix, multiply with IDENTITY matricx for the first operation
    Multiply with each succesive matrix to get result.
    Multiplies 2 matrices each time using mat3x3 function.
    Return result

    @param mat - An array of 3x3 matrices, 
    @return res - result of the multiplication.
    """
    def mat3x3(mat1,mat2):
        """
        Multiplies two matrices.

        @param mat1 - 3x3 matrix
        @param mat2 - 3x3 matrix
        @return retVal - the result of the matrix multiplication
        """

        #initilise the returnn value array
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
                    product += mat1[i][k]*mat2[k][j]#sum each constituent of the products
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

    #init array to store resylt matrix
    res=[]

    for matrix in mat:
        #for first matrix
        if not res:
            res=mat3x3(IDENTITY,matrix)
        else:
            res=mat3x3(res,matrix)#for subsequent matrrices, multiply result by anothe matrix

    #return result matrix
    return res

def transMat(a,b):
    """
    Takes in x and y translation.
    Returns a translation matrix

    @param a - X coordinate to translate
    @param b - Y coordinate to translate
    @return translation matrix
    """
    return [
        [1,0,a],
        [0,1,b],
        [0,0,1]
    ]

def rotMat(angle):
    """
    Takes in an angle to rotate
    Convert angle from degrees to radian
    Calculates rotation matrix and returns rotation matrix

    @param angle - ratation angle in degrees
    @return rotation matrix
    """
    angle=math.radians(angle)
    return [
        [math.cos(angle),-math.sin(angle),0],
        [math.sin(angle),math.cos(angle),0],
        [0,0,1]
    ]

def scaleMat(sx,sy):
    """
    Takes in x and y scale.
    Normalises scale values, 1 for 100%.
    Returns a scale matrix.

    @param a - X ammount to scale
    @param b - Y ammount to scale
    @return scale matrix
    """

    #normalise values
    sx=sx/100
    sy=sy/100

    return [
        [sx,0,0],
        [0,sy,0],
        [0,0,1]
    ]

def shearMat(tx,ty):
    """
    Takes in x and y shear.
    Normalises shear values, 0% for no scale.
    Returns a shear matrix.

    @param a - X ammount to shear
    @param b - Y ammount to shear
    @return shear matrix
    """

    tx=tx/100
    ty=ty/100
    return [
        [1,tx,0],
        [ty,1,0],
        [0,0,1]
    ]

def reflectMat(reflection):
    """
    Takes in reflection.
    Reflection can be 'X', 'Y', 'XY' or 'None'

    @param reflection - desired reflection
    @return shear matrix
    """
    #if x axis reflection
    if reflection=="X"or reflection=='x':
        rx=-1
        ry=1
    #y axis reflection
    elif reflection=="Y"or reflection=="y":
        rx=1
        ry=-1
    #xy axis reflection
    elif reflection.upper()=="XY":
        rx=-1
        ry=-1
    #No rellection, return identity matrix
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

    #return transformed vertex
    return resultVertices

def plotPattern(new_vertices, new_transformations):
    """
    Plots polygons in a pattern. 
    Finds the number of patterns.
    FInds the percentage influence on each pattern, then applies it to the transformations.
    Translation starts from 0
    Rotation starts from 0
    Rotation offset set to 0,0, by default
    Scale starts at 1.0
    Shear starts from 0.0
    Rotation is repeted for each rotation pattern
    
    @param new_vertices - polygon vertices to plot
    @param new_transformation - transformations for the polygon
    """
    global g_new_transformation, g_new_vertices

    #copy values for transformation
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

    #if rotation offset is not 0, find the offset, rotation and main rotation
    if type(rotation)==str:
        rotation,coords=rotation.split('C')#seperate offset from main rotation
        rotation=int(rotation)#get main rotation

        rotc, coordx, coordy=coords.split(',')#seperate x,y offsets and sub rotation
        rotc, coordx, coordy=int(rotc), int(coordx), int(coordy)#convert to int
        rotonC=True

    else:
        rotonC=False

    #find the difference in scale
    deltaScaleX=scaleX-100
    deltaScaleY=scaleY-100

    #set scale factors
    if deltaScaleX<0:
        scaleXMult=-1
    else:
        scaleXMult=1
    if deltaScaleY<0:
        scaleYMult=-1
    else:
        scaleYMult=1

    #convert reflections to upper
    reflection=reflection.upper()

    #rotation planes to replace
    if reflection=='NONE':
        reflectionpatterns=['NONE']
    elif reflection=='X':
        reflectionpatterns=['NONE','X']
    elif reflection=='Y':
        reflectionpatterns=['NONE','Y']
    elif reflection=='XY':
        reflectionpatterns=['NONE','X','Y','XY']

    #for each reflection
    for reflect in reflectionpatterns:
        #plot first polygon
        firstVertex=vertexTransformer(reflectMat(reflect), new_vertices)
        plotPolygon(firstVertex,line=lineCol,fill=fillCol)#plot first shape
        for i in range(patternCount-1):#for subsequent shapes
            j=(i+1)/(patternCount-1)#find the influence of each pattern

            #calculate with scale factor
            if scaleXMult==-1:
                jX=1-j
            else:
                jX=j

            if scaleXMult==-1:
                jY=1-j
            else:
                jY=j
            
            #if rotation offset
            if rotonC:
                new_vertices=vertexTransformer(transMat(-coordx,-coordy),new_vertices)#transform to offset
                new_vertices=vertexTransformer(rotMat(rotc*j),new_vertices)#rotate
                new_vertices=vertexTransformer(transMat(coordx,coordy),new_vertices)#transform back to origin

            #calculate homofeneous coordiantes
            homoCoords=matmul(transMat(transformX*j,transformY*j), rotMat(rotation*j), scaleMat(scaleX+deltaScaleX*jX*scaleXMult,scaleY+deltaScaleY*jY*scaleYMult), shearMat(shearX*j, shearY *j), reflectMat(reflect))
            #convert vertices to use include homogeneous coordinates
            transformed_vectors = vertexTransformer(homoCoords,new_vertices)
            #plot the polygon in the pattern
            plotPolygon(transformed_vectors,line=lineCol,fill=fillCol)

def offsetPolygon():
    """
    Move the current working polygon
    Callback function to the 'o' key

    Check if in edit mode
    Prompts user for offset to use.
    If x axis offset, transform x axis and update vertex information.
    If y axis offset, transform y axis and update vertex information.
    If rotation, rotate polygon and update vertex information.

    """
    global g_edit_mode, g_new_vertices

    #check to make sure in edit mode
    if g_edit_mode==editMode_point_edit:
        axisToOffset = sc.textinput("Relative offset", "Enter Axis(X)(Y) or rotation(R) to offset:")
        sc.listen()#reclaim listener after textinput claimed handler

        while True:
            #if cancled prompt
            if axisToOffset==None:
                return
            axisToOffset=axisToOffset.upper()
            #check that the user input is valid
            if axisToOffset=='X' or axisToOffset=='Y' or axisToOffset=='R':
                break

            else:#if invalid, ask again
                axisToOffset = sc.textinput("Relative offset", "Enter Axis(X)(Y) or rotation(R) to offset:")
                sc.listen()#reclaim listener after textinput claimed handler
        if axisToOffset =='X':
            xAxisOffset = sc.textinput("X relative offset", "Enter X axis offset:")
            sc.listen()#reclaim listener after textinput claimed handler
            while True:
                #if user cancled prompt
                if xAxisOffset==None:
                    return
                try:
                    #check that the user input is valid
                    xAxisOffset=int(xAxisOffset)
                    #check if transform in range
                    if not -1000<=xAxisOffset<=1000:
                        raise ValueError
                    break
                except (ValueError,TypeError):#if invalid, ask again
                    xAxisOffset = sc.textinput("X relative offset", "Enter X axis offset(An integer between -1000 and 1000):")
                sc.listen()#reclaim listener after textinput claimed handler

            #update vertices and redraw
            g_new_vertices=vertexTransformer(transMat(xAxisOffset,0),g_new_vertices)
            redraw()

        elif axisToOffset =='Y':
            yAxisOffset = sc.textinput("Y relative offset", "Enter Y axis offset:")
            sc.listen()#reclaim listener after textinput claimed handler
            while True:
                #if user cancled prompt
                if yAxisOffset==None:
                    return
                try:#check that the user input is valid
                    yAxisOffset=int(yAxisOffset)
                    #check if transform in range
                    if not -1000<=yAxisOffset<=1000:
                        raise ValueError
                    break
                except (ValueError,TypeError):#if invalid, ask again
                    yAxisOffset = sc.textinput("Y relative offset", "Enter Y axis offset(An integer between -1000 and 1000):")
                sc.listen()#reclaim listener after textinput claimed handler

            #update vertices and redraw
            g_new_vertices=vertexTransformer(transMat(0,yAxisOffset),g_new_vertices)
            redraw()

        elif axisToOffset =='R':
            rotOffset = sc.textinput("Rotation offset", "Enter rotation offset:")
            sc.listen()#reclaim listener after textinput claimed handler
            while True:
                #if user cancled prompt
                if rotOffset==None:
                    return
                try:#check that the user input is valid
                    rotOffset=int(rotOffset)
                    #check if rotation in range
                    if not -360<=rotOffset<=360:
                        raise ValueError
                    break
                except (ValueError,TypeError):#if invalid, ask again
                    rotOffset = sc.textinput("Rotationoffset", "Enter rotation offset(An integer between -1000 and 1000):")
                sc.listen()#reclaim listener after textinput claimed handler

            #update vertices and redraw
            g_new_vertices=vertexTransformer(rotMat(rotOffset),g_new_vertices)
            redraw()

def showHideCoordinates():
    """
    Callback function for the 'v' key
    Shows and hides the values of the vertices.

    Update the flag and update the screen
    """
    global g_show_values_flag
    g_show_values_flag = not g_show_values_flag
    if g_edit_mode==editMode_point_edit:
        redraw()

def addPolygon():
    """
    Add polygon to list of verteicec to plot in the final drawing.
    Copy the vertex information and the transformation data into the final data list.
    Ask user to confirm if they want to add polygon
    """
    global g_all_data, g_new_vertices, g_new_transformation
    axisToOffset = sc.textinput("Confirm add polygon", "Enter (Y) to confirm:")
    sc.listen()#reclaim listener after textinput claimed handler
    if axisToOffset.upper() =='Y':
        g_all_data.append([g_new_vertices.copy(),g_new_transformation.copy()])
        sc.textinput("Polygon added", "Polygon added!\nClose to continue")
        sc.listen()#reclaim listener after textinput claimed handler

def showAll():
    """
    Show all from the final polygon.
    Reset screen
    For each polygon,
    Get their vertices and transformations
    Plot their pattern

    """
    global g_all_data, g_edit_mode

    showHelp(1)#hide help
    g_edit_mode=editMode_show_result#upate edit mode to show result

    t.reset()#reset all

    #for each polygon pattern, plot the pattern
    for vertices_data, transformation_data in g_all_data:
        plotPattern(vertices_data,transformation_data)
        t.ht()
    #push to screen
    t.update()        

def saveFile():
    """
    Saves a file to drive
    Checks if there is any data to save to
    Ask user for file name to save to
    Parse polygon vertex data and transformation data, 
    Endode and write to file
    """
    global g_all_data

    #check if there is data to write
    if g_all_data==[]:
        sc.textinput("Error", "No data to save, add polygons first!")
        sc.listen()#reclaim listener after textinput claimed handler
        return

    #Prompt user for a file name
    saveFileName = sc.textinput("Save File", "Enter save file name:")
    sc.listen()#reclaim listener after textinput claimed handler

    #cjheck if the file name is valid
    while True:
        #if user closed the prompt
        if saveFileName==None:
            return
        
        try:#try to create file
            saveFileHandle = open(saveFileName,'w')
            break
        
        except OSError:#if the user gave an ivalid file name
            saveFileName = sc.textinput("Save File", "Error creating file.\nEnter save file name:")
            sc.listen()#reclaim listener after textinput claimed handler

    #go through each polygon pattern
    for vertices_data, transformation_data in g_all_data:
        #accumulator for vertex information
        vertexDataString=''
        #go through each vertex in the data
        for vertex in vertices_data:
            #convert to string and add a delimiter
            vertexString=''
            #for each data point in the vertex
            for i in vertex:
                i=str(i)
                vertexString+=i+','
            vertexString=vertexString[:-1]
            vertexDataString+=vertexString+'|'
        #write to file
        saveFileHandle.write('@'+vertexDataString[:-1]+'\n')

        #initilize the transformation data string
        transDataString=''
        #go through each data point int the string
        for transform in transformation_data:
            transform=str(transform)
            transDataString+=transform+','
        #writte to file
        saveFileHandle.write('#'+transDataString[:-1]+'\n')
        saveFileHandle.write('\n')

def openFile():
    """
    Ask user for an input file name
    Check if the file name exists
    Parse the file data
    For vertex data, extract data parse into a list of tuples
    For transformation data parse, into a list
    For items that can be converted to ont, convert to int, else tray as string

    """
    global g_all_data

    #ask user for the file to input
    openFileName = sc.textinput("Open File", "Enter input file name:")
    sc.listen()#reclaim listener after textinput claimed handler

    #check if the filename is valid
    while True:
        if openFileName==None:#if user cancled the prompt
            return
        
        try:#try to open the file
            openFileHandle = open(openFileName,'r')
            break
        
        except FileNotFoundError:#if the file is not found
            openFileName = sc.textinput("Open File", "Error opening file, check file name.\nEnter input file name:")
            sc.listen()#reclaim listener after textinput claimed handler

    #clear array
    g_all_data=[]
    while True:
        #read the vertex data and the transformation data
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
            vertexRaw= vertex.split(',')#split each data point in the vertex
            vertex=()
            for i in vertexRaw:
                try:#check if the value is a number
                    i=float(i)
                    i=int(i)
                except ValueError:#else leave as string
                    pass
                vertex=vertex+(i,)#add to tuple for vertex
            vertexList.append(vertex)#add to list of vertices

        #split up the data
        transData=transData[1:-1].split(',')
        transList=[]
        for trans in transData:#if number, convert to int
            if trans.replace('-','').isnumeric():
                trans=int(trans)
            transList.append(trans)
        #add to transform list
        g_all_data.append([vertexList,transList])
    #redraw and show all transformations
    showAll()

def createNew():
    """
    Callback fuction for the 'n' key
    Allows the user to create a new polygon
    CLears the existing polygon and reload
    """
    showHelp(1)
    confirmNew = sc.textinput("Confirm new polygon", "Enter (Y) to confirm:")
    sc.listen()#reclaim listener after textinput claimed handler
    if confirmNew.upper() =='Y':
        t.reset()#clear screen
        t.ht()
        newPolygon()#copy vertex and transform data

def showHelp(hide=False):
    """
    Shows the help for the program
    Toggles help on and off
    Callback for the 'h' hey
    """
    global g_help_menu_flag
    #if show help
    if g_help_menu_flag==False and not hide:
        g_help_menu_flag=True
        t.reset()#clear screen
        sc.bgpic("help.gif")#show help image

    #else, hide help
    else:
        g_help_menu_flag=False
        sc.bgpic('nopic')#hide image

        #return to mode
        if g_edit_mode!=editMode_show_result:
            redraw()
        else:
            showAll()

#run setup to setup the window and turtle drawing parameters
setup()

#Setup callbacks for the mouse
sc.onclick(leftclickhandler,btn=1)#left click
sc.onclick(clickhandler_addpoint,btn=3)#right clcik
sc.onclick(splineHandler,btn=2)#middle click
t.ondrag(ondraghandler)#left click and drag

#Setup callbacks for keybaord input
sc.onkeypress(delPointhandler,'Delete')
#switch to edit mode, if not in edit mode. If in edit mode, edit selected point coordinates
sc.onkeypress(editPoint,'e')
sc.onkeypress(editPoint,'E')
#toggle snap to grid
sc.onkeypress(toggleGrid,'g')
sc.onkeypress(toggleGrid,'G')
#toggle transformation table
sc.onkeypress(editTransformations,'t')
sc.onkeypress(editTransformations,'T')
#Toggle preview polygons
sc.onkeypress(previewPolygons,'p')
sc.onkeypress(previewPolygons,'P')
#offset working polygon
sc.onkeypress(offsetPolygon,'x')
sc.onkeypress(offsetPolygon,'X')
#add polygon to the final pattern 
sc.onkeypress(addPolygon,'a')
sc.onkeypress(addPolygon,'A')
#show hide coordinates
sc.onkeypress(showHideCoordinates,'v')
sc.onkeypress(showHideCoordinates,'V')
#show final polygon patterns
sc.onkeypress(showAll,'f')
sc.onkeypress(showAll,'F')
#save file
sc.onkeypress(saveFile,'s')
sc.onkeypress(saveFile,'S')
#open file
sc.onkeypress(openFile,'o')
sc.onkeypress(openFile,'O')
#new polygon, resets working polygon
sc.onkeypress(createNew,'n')
sc.onkeypress(createNew,'N')
#shows help
sc.onkeypress(showHelp,'h')
sc.onkeypress(showHelp,'H')

#show starting polygon
newPolygon()

#start the listeners and loops to run the program
t.listen()
sc.listen()
t.mainloop()
sc.mainloop()