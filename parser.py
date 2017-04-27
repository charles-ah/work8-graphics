from display import *
from matrix import *
from draw import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         sphere: add a sphere to the edge matrix - 
	    takes 4 arguemnts (cx, cy, cz, r)
         torus: add a torus to the edge matrix - 
	    takes 5 arguemnts (cx, cy, cz, r1, r2)
         box: add a rectangular prism to the edge matrix - 
	    takes 6 arguemnts (x, y, z, width, height, depth)	    

	 circle: add a circle to the edge matrix - 
	    takes 3 arguments (cx, cy, r)
	 hermite: add a hermite curve to the edge matrix -
	    takes 8 arguments (x0, y0, x1, y1, rx0, ry0, rx1, ry1)
	 bezier: add a bezier curve to the edge matrix -
	    takes 8 arguments (x0, y0, x1, y1, x2, y2, x3, y3)
         line: add a line to the edge matrix - 
	    takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
	 ident: set the transform matrix to the identity matrix - 
	 scale: create a scale matrix, 
	    then multiply the transform matrix by the scale matrix - 
	    takes 3 arguments (sx, sy, sz)
	 move: create a translation matrix, 
	    then multiply the transform matrix by the translation matrix - 
	    takes 3 arguments (tx, ty, tz)
	 rotate: create a rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 2 arguments (axis, theta) axis should be x, y or z
         clear: clear the edge matrix of points
	 apply: apply the current transformation matrix to the 
	    edge matrix
	 display: draw the lines of the edge matrix to the screen
	    display the screen
	 save: draw the lines of the edge matrix to the screen
	    save the screen to a file -
	    takes 1 argument (file name)
	 quit: end parsing

See the file script for an example of the file format
"""
ARG_COMMANDS = [ 'line', 'scale', 'move', 'rotate', 'save', 'circle', 'bezier', 'hermite', 'box', 'sphere', 'torus','color' ]

def parse_file( fname, edges, transform, screen, color ):

    f = open(fname)
    lines = f.readlines()

    lol = new_matrix()
    ident(lol)
    stack = [lol]

    step = 0.05
    c = 0
    while c < len(lines):
        line = lines[c].strip()
#        print ':' + line + ':'

        #print str(stack[-1])

        if line in ARG_COMMANDS:            
            c+= 1
            args = lines[c].strip().split(' ')
            #print 'args\t' + str(args)
        
        if line == 'push':
            print "push"
            top = stack[len(stack)-1]
 #           print "old: " + str(top)
            #print str(top)
            m = new_matrix()
            ident(m)
            matrix_mult(top ,m)
#            print "new: " + str(m)
            stack.append(m)

        elif line == 'pop':
            print "pop"
#            print "old: " + str(stack[-2])
 #           print "new: " + str(stack[-1])            

            stack.pop()

        if line == 'sphere':
            print 'SPHERE\t' + str(args)
            temp_poly = []
            add_sphere(temp_poly,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step, color)
            #print str(temp_poly)
            matrix_mult(stack[len(stack)-1] ,temp_poly)
            draw_polygons(temp_poly, screen, color)
            
        elif line == 'torus':
            print 'TORUS\t' + str(args)
            temp_poly = []
            add_torus(temp_poly,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step, color)
            matrix_mult(stack[len(stack)-1] ,temp_poly)
            draw_polygons(temp_poly, screen, color)

        elif line == 'box':
            print 'BOX\t' + str(args)
            temp_poly = []
            add_box(temp_poly,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            #print str(temp_poly)
            matrix_mult(stack[-1] ,temp_poly)
            draw_polygons(temp_poly, screen, color)

        elif line == 'circle':
            #print 'CIRCLE\t' + str(args)
            temp_edge = []
            add_circle(temp_edge,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult(stack[-1] ,temp_edge)
            draw_lines(temp_edge.screen,color)

        elif line == 'hermite' or line == 'bezier':
            #print 'curve\t' + line + ": " + str(args)
            temp_edge = []
            add_curve(temp_edge,
                      float(args[0]), float(args[1]),
                      float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]),
                      float(args[6]), float(args[7]),
                      step, line)            
            matrix_mult(stack[-1] ,temp_edge)          
            draw_lines(temp_edge.screen,color)

        elif line == 'line':            
            #print 'LINE\t' + str(args)
            temp_edge = []
            add_edge( temp_edge,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult(stack[-1] ,temp_edge)
            draw_lines(temp_edge.screen,color)

        elif line == 'scale':
            print 'SCALE\t' + str(args)
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(stack[len(stack)-1], t)
            stack[-1] = t

        elif line == 'move':
            print 'MOVE\t' + str(args)
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            #print str(t)
            matrix_mult(stack[len(stack)-1], t)
            stack[-1] = t

        elif line == 'rotate':
            print 'ROTATE\t' + str(args)
            theta = float(args[1]) * (math.pi / 180)
            
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(stack[len(stack)-1], t)
            stack[-1] = t
                            
        elif line == 'clear':
            edges = []
        elif line == "color":
            color = [args[0],args[1],args[2]]
        elif line == 'ident':
            ident(transform)

        elif line == 'apply':
            matrix_mult( transform, edges )

        elif line == 'display' or line == 'save':
         #   clear_screen(screen)
            #draw_polygons(edges, screen, color)

            if line == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
            
        c+= 1
