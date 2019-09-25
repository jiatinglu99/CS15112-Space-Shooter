# 15-122 Foundamentals of Programming and Computer Science
# Full Name: Terry Lu
# Andrew ID: jiatingl
# Section: A
# Date: 08/09/2017
# Homework: Term Project -- Alien Strike
# Title: ReadMe.txt

Please open 'Main.py' to run the program

My project is a space shooter game, simply relax and enjoy the gameplay

# the following can be ignored
In my program, class UserInterface(UI) draws the menu and chooses what classes to run and what to draw. Class SpecialEffectCollection contains all types of special effect, and runs every effect added, and write over it when the index counter loops through the collection list(fixed size). This mechanism is also applied to other classes: EnemyLaserCollection, EnemyShipCollection, UserLaserCollection. I have my own class of transitioning color that can be called as a hex value, which can transit to another color and switch back and forth if set so. The explosion trials are generated recursively following an indicated direction.