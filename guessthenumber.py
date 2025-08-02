# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import PySimpleGUI as simplegui

import random
import math
num_range=100
# helper function to start and restart the game
def new_game():
    global num_range
    if num_range==100:
        range100()
    elif num_range==1000:
        range1000()
    # initialize global variables used in your code here
    # remove this when you add your code

# define event handlers for control panel
def range100():
    global x
    global count
    global num_range
    num_range=100
    # button that changes the range to [0,100) and starts a new game 
    x = random.randrange(0, 100)
    count=7
    print ("")
    print ("New game.Range is from 0 to 100.")
    print ("Number of remaining guesses 7.")
    return x
    # remove this when you add your code

def range1000():
    global x
    global num_range
    global count
    num_range=1000
    # button that changes the range to [0,1000) and starts a new game     
    x = random.randrange(0, 1000)
    count=10
    print ("")
    print ("New game.Range is from 0 to 1000.")
    print ("Number of remaining guesses 10.")
    return x
    
def input_guess(guess):
    global x
    global count
    global num_range
    count-=1
    gues=int(guess)
    print("")
    print ("Guess was"),guess
    print ("Number of remaining guesses"),count
    # main game logic goes here	
    if x>guess:
        print ("Higher!")
    elif x<guess:
        print ("Lower!")
    else:
        print ("Correct!")
    if (count<=0):
        new_game()
    # remove this when you add your code

    
# create frame
frame=simplegui.create_frame("Guess the number",200,300)

# register event handlers for control elements and start frame
frame.add_button("Range is [0,100]",range100,200)
frame.add_button("Range is [0,1000]",range1000,200)
frame.add_input("Enter the guess",input_guess,200)
# call new_game 
new_game()

frame.start()
# always remember to check your completed program against the grading rubric
