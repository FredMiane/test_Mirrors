# Mirrors

This project Mirrors simulate a safe with mirrors:


#  Features
When the laser is activated, a beam enters the top row of the grid horizontally from the
left. The beam is reflected by every mirror that it hits. Each mirror has a 45 degree diagonal
orientation, either / or \. If the beam exits the bottom row of the grid horizontally to the
right, it is detected and the safe opens (see the left side of the figure above). Otherwise the
safe remains closed and an alarm is raised.
Then according to the distance to an obstacles, we switch from lidar to sonars to lidar,
as we put them to Run state or Stop state

Command: Python Mirrors.py input1

>  Tested with Python 3.4.3 

