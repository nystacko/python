from graphics import *



def main():
	win = GraphWin("My Window", 500, 500)
	win.setBackground(color_rgb(0, 0, 0))
	
	pt1 = Point(250,250)
	pt2 = Point(250, 350)
	myLine = Line(pt1, pt2)
	myLine.setOutline(color_rgb(0, 255, 255))
	myLine.setWidth(8)
	myLine.draw(win)
	
	win.getMouse()
	win.close()

main()