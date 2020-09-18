from graphics import *



def main():
	win = GraphWin("My Window", 500, 500)
	win.setBackground(color_rgb(0, 0, 0))
	
	bballPic = Image(Point(250, 250), "basketball.gif")
	bballPic.draw(win)
	
	win.getMouse()
	win.close()

main()