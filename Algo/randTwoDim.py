import sys
import random as rand
import os
"""
This program responsible for creating a two dimension data points
after running this program you will have a new .txt file named 'randTwoDim.txt'
in 'Kmeans/Files/' path, 
* you can also add a seed argument to the program
"""


def __main__():
    size = 100
    try:
        rand.seed(sys.argv[2])
        size = eval(sys.argv[1])
    except IndexError:
        if len(sys.argv) == 2:
            size = eval(sys.argv[1])
    finally:
        if os.path.exists("./Files/randTwoDim.txt"):
            os.remove("./Files/randTwoDim.txt")
        with open("./Files/randTwoDim.txt", "x") as f:
            for i in range(size):
                f.write("%.4f" % rand.uniform(-10, 10) + ", " + "%.4f" % rand.uniform(-10, 10) + "\n")
        f.close()


if "__name__" == __main__():
    __main__()




