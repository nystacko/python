from graphics import *



def main():
	win = GraphWin("My Window", 500, 500)
	win.setBackground(color_rgb(0, 0, 0))
	
	myCirc = Circle(Point(250, 250), 100)
	myCirc.setOutline(color_rgb(0, 255, 255))
	myCirc.setFill(color_rgb(255, 100, 50))
	myCirc.setWidth(5)
	myCirc.draw(win)
	
	win.getMouse()
	win.close()

main()