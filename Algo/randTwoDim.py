import sys
import random as rand
"""
This program responsible for creating a two dimension data points
after running this program you will have a new .txt file named 'randTwoDim.txt'
in 'Kmeans/Files/' path, 
* you can also add a seed argument to the program
"""


def __main__():
    if len(sys.argv) > 1:
        rand.seed(sys.argv[1])
    with open("./Files/randTwoDim.txt", "x") as f:
        for i in range(1000):
            f.write(str(rand.uniform(-10, 10)) + ", " + str(rand.uniform(-10, 10)) + "\n")
    f.close()


if "__name__" == __main__():
    __main__()




