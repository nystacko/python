from graphics import *



def main():
	win = GraphWin("My Window", 500, 500)
	win.setBackground(color_rgb(0, 0, 0))
	
	myPoly = Polygon(Point(40, 40),
					Point(100, 100),
					Point(40, 100),
					Point(0, 60),
					Point(450, 400),
					Point(300, 100))
	myPoly.setOutline(color_rgb(0, 255, 255))
	myPoly.setFill(color_rgb(255, 100, 50))
	myPoly.setWidth(5)
	myPoly.draw(win)
	
	win.getMouse()
	win.close()

main()