from graphics import *



def main():
	win = GraphWin("My Window", 500, 500)
	win.setBackground(color_rgb(0, 0, 0))
	
	myText = Text(Point(250, 250), "This is some text.")
	myText.setTextColor(color_rgb(0, 255, 255))
	myText.setSize(20)
	myText.setFace('helvetica')
	myText.draw(win)
	
	win.getMouse()
	win.close()

main()