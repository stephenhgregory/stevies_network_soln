# Machina Labs: Network Problem

This repository contains a solution to 2 simple problems, specified as follows.

## Problem 1
Create two processes, known as "Process A" and "Process B". Then, using some communication protocol, pass an .stl file (3D CAD design description) from Process A to Process B. Process B will then return the contents of that .stl file back to Process A. Success in solving this problem is incumbent on equivalence between the original .stl file and newly saved .stl file.

## Problem 2 (challenge problem)
Again, create two process, known as "Process A" and "Process B" that communicate via some protocol. However, when Process B receives the .stl file from Process A, we want to convert the contents of the STL file into a CSV file. Each row of this CSV file will represent the x, y, and z coordinates of each point in the STL mesh. Process B will then return the contents of this file back to Process A. Process A will then save the contents of this file to a new CSV file to be stored. 

## My Solution
I have created a simple TCP socket communication class in Python. This class, which makes extensive use of the [socket](https://docs.python.org/3/library/socket.html) Python library, can be used to connect and bind to network ports via TCP sockets, send the contents of files across those ports, and receive data in the same way. I have also created two subclasses of this TCP socket communication class which organize the functionality of "Process A" and "Process B" into manageable, decoupled, and easily maintainable chunks of functionality. I have also made the TCP socket communication class rather generalizable, so as not to over-specialize for this exact problem description.

I have also solved the challenge problem, making use of the very effective [numpy-stl](https://pypi.org/project/numpy-stl/) library for reading STL mesh files into numpy arrays.

