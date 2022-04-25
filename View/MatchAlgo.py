import pandas as pd
import csv
from matplotlib import pyplot as plt
import sys
import os

"""
    after running both algorithms,
    run this program to view results and compare
"""


def __main__():
    try:
        dataTxt = sys.argv[1]
        outputFileName = sys.argv[2]
        dim, absPath = createCSV(dataTxt)
        if dim != 3:
            print("Cannot execute plot from with dimension != 3")
            exit()
        plotData(outputFileName, absPath)
    except IndexError:
        print("one of the two is missing: data file, output file name")
        exit()


def plotData(fileName, absPath):
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    columns = ["v[0]", "v[1]", "v[2]"]
    df = pd.read_csv(absPath, usecols=columns)

    Xlist = df["v[0]"].tolist()
    Ylist = df["v[1]"].tolist()
    Clist = df["v[2]"].tolist()

    clustrs = len(list(set(Clist)))

    def mapIntToColor(clusters_list):
        import random
        n = len(list(set(clusters_list)))
        unique_colors = [["#" + ''.join([random.choice('ABCDEF0123456789') for _ in range(6)])] for i in range(n)]
        colors_list = [unique_colors[g][0] for g in clusters_list]
        return colors_list

    Clist = [int(c) for c in Clist]
    Clist = mapIntToColor(Clist)

    plt.suptitle(str(len(Xlist)) + " vectors and " + str(clustrs) + " clusters")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.scatter(Xlist, Ylist, c=Clist, edgecolors='black', alpha=0.75)
    plt.savefig(fileName)


def createCSV(txtFile):
    dataMatrix = []
    try:
        with open(txtFile, "r") as f:
            for line in f:
                dataMatrix.append(line.split(","))
                for i, dot in enumerate(dataMatrix[-1]):
                    dataMatrix[-1][i] = eval(dot)
    except IOError:
        print("File is missing")
        exit()
    if os.path.exists("../csvData.txt"):
        os.remove("../csvData.txt")
    with open("csvData", 'w') as csvFile:
        absPath = os.path.abspath("csvData")
        wr = csv.writer(csvFile)
        headLine = ["v[" + str(_) + "]" for _ in range(len(dataMatrix[0]))]
        wr.writerow(headLine)
        for vector in dataMatrix:
            wr.writerow([float(vector[i]) for i in range(len(vector))])
    return len(dataMatrix[0]), absPath


if "__name__" == __main__():
    __main__()
