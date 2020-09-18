from graphics import *



def main():
	win = GraphWin("My Window", 500, 500)
	win.setBackground(color_rgb(255, 255, 255))
	
	# Create our objects
	myInputBox = Entry(Point(250, 250), 10)
	myInputBox.draw(win)
	outputtedText = Text(Point(250, 280), "")
	outputtedText.draw(win)
	
	# Wait to do stuff with our objects
	# This creates infinite loop -- NOT GOOD PRACTICE
	while True:
		outputtedText.setText(myInputBox.getText())
	
	win.getMouse()
	win.close()

main()