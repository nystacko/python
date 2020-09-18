from graphics import *



def main():
	win = GraphWin("My Window", 500, 500)
	win.setBackground(color_rgb(0, 0, 0))
	
	myRect = Rectangle(Point(250, 250), Point(350, 350))
	myRect.setOutline(color_rgb(0, 255, 255))
	myRect.setFill(color_rgb(255, 100, 50))
	myRect.draw(win)
	
	win.getMouse()
	win.close()

main()