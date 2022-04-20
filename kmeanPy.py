import sys

global eps, max_iter, K, input_file, output_file, lines, dim


def __main__():
    """
    finding k-means clusters to the given input data
    :return:
    """
    # setting eps, k, max_iter, input/output file, lines and dim for the requested given variables
    setVariables()
    # creating a vector matrix from size lines*dim
    vectors = [[0.0 for x in range(dim)] for y in range(lines)]
    setMatrix(vectors)
    # init centroids vectors
    centroids = [[0.0 for x in range(dim)] for y in range(K)]
    initCntr(centroids, vectors)
    # algorithm
    k_means(vectors, centroids)
    # write back to output file
    writeToFile(centroids)


def setVariables():
    """
    setting all the global variables needed for the algorithm for the requested input
    error:
        if len(sys.argv)!=4-5 then one of the requested variables is missing
        if valid_input() == -1, then input is in-valid, and we have an error
    :return: None
    """
    eps = 0.0001
    K = int(sys.argv[1])
    if len(sys.argv) == 5:
        max_iter = int(sys.argv[2])
    elif len(sys.argv) == 4:
        max_iter = 200
    else:
        exit()
    input_file = sys.argv[-2]
    output_file = sys.argv[-1]
    lines = valid_input()
    if lines == -1:  # file not found
        print("Invalid input")
        exit()
    dim = countDim()


def valid_input():
    """
    open input file and checks for valid input file
    also, check for valid K clusters input vs total vectors given
    :return: integer
    -1 -> invalid input. other -> valid input
    """
    if max_iter <= 0:
        return -1
    try:
        # open file
        file = open(input_file, 'r')
        lines = len(file.readlines())  # lines array
        file.close()  # close file
        if 1 < K < lines:  # check 1<k<#vectors
            return lines
        return -1
    except IOError:  # file not found
        print("Invalid Input!")
        exit()


def countDim():
    """
    finding vector dimension
    :return: integer
    vector dim
    """
    try:
        # open file
        file = open(input_file, 'r')
        lines = file.readlines()  # lines array
        file.close()  # close file
        dim = len(lines[0].split(","))
        return dim
    except IOError:  # file not found
        print("Invalid Input!")
        exit()
    except IndexError:  # if en empty vector is received
        print("An Error Has Occurred")
        exit()


def setMatrix(vectors):
    """
    receive an empty matrix from size #vectors*dim,
    setting values in the cells according to the input file
    :param vectors: #vectors*dim matrix
    :return: None
    """
    try:
        # open file
        file = open(input_file, 'r')
        lines = file.readlines()  # lines array
        file.close()  # close file
        for i in range(len(lines)):  # for each vector
            line = lines[i].split(",")  # make vector array
            for j in range(len(line)):
                vectors[i][j] = float(line[j])  # set mat[i][j] = vector[j]
    except IOError:  # file not found
        print("Invalid Input!")
        exit()


def initCntr(centroids, vectors):
    """
    receive an empty centroids array and all vectors matrix
    set centroids to the first K vectors in vectors matrix
    :param centroids: matrix from size K*dim
    :param vectors: vectors matrix
    :return: None
    """
    for i in range(len(centroids)):  # for the first K vectors
        for j in range(len(centroids[i])):  # for each entry in the vector
            centroids[i][j] = vectors[i][j]  # set entry etc.


def normCalc(centroid):
    """
    calculate norm of a vector
    :param centroid: receive a vector, float array
    :return: float - vector norm
    X = (x1, x2, ... , xn) -> ||X|| = sqrt(x1^2 + ... xn^2)
    """
    norm = 0  # set for zero
    # sum all powers of two
    for i in range(len(centroid)):
        norm += pow(centroid[i], 2)
    return pow(norm, 0.5)  # sqrt(sum of powers)


def isConv(centroids):
    """
    checking all centroids are convergences
    :param centroids: array of centroids
    :return: true if centroids are convergences, else false
    a centroid is converging iff his norm is less than eps
    """
    for centroid in centroids:
        if normCalc(centroid) >= eps:
            return False
    return True


def assignVecToCluster(clusters, vectors, centroids):
    """
    assign each vector in vectors matrix to a specific cluster
    find the closest cluster by the minimum destination from a centroid
    :param clusters: an array of all clusters
    :param vectors: an array of all vectors
    :param centroids: an array of all centroids
    :return: None
    """
    # tmp variables
    minInd = 0
    minVal = -1
    currVal = 0.0
    for i in range(lines):  # for each vector
        for j in range(K):  # for each centroid
            for p in range(dim):  # for each vector entry
                currVal += pow((vectors[i][p] - centroids[j][p]), 2)  # calc current vector dest. from current centroid
            # check for min
            if minVal == -1 or minVal > currVal:
                minVal = currVal
                minInd = j
            currVal = 0
        clusters[i] = minInd
        minVal = -1


def calcCntrK(clusters, vectors, centroids, k):
    """
    calculate the K-th new centroid
    :param clusters: all clusters
    :param vectors: all vectors matrix
    :param centroids: all centroids array
    :param k: the k-th centroid we interested in
    :return: None
    a new centroid is calculated by the following formula
    Uk = (sum of v in Sk)/|Sk|
    where|: Uk-> k-th centroid, Sk-> k-th cluster, v-> a vector in Sk
    """
    # tmp variables
    sum = [0.0 for _ in range(dim)]
    cnt = 0
    for i in range(lines):  # for each vector
        if clusters[i] == k:  # if a vector is referenced for the k-th cluster
            # add to sum
            for j in range(dim):
                sum[j] += vectors[i][j]
            cnt += 1
    for j in range(dim):
        try:
            centroids[k][j] = sum[j] / cnt  # calc centroid
        except ZeroDivisionError:  # division by zero
            print("An Error Has Occurred")
            exit()


def k_means(vectors, centroids):
    """
    k means algorithm, receive all vectors and an init centroids array
    :param vectors: all vectors matrix
    :param centroids: all centroids array
    :return: None
    """
    iter = 0
    while not isConv(centroids) and iter < max_iter:  # if we passed max iteration number or all centroids are converged
        iter += 1
        clusters = [0 for _ in range(lines)]
        # find new cluster
        assignVecToCluster(clusters, vectors, centroids)
        # calc new centroids
        for i in range(K):
            calcCntrK(clusters, vectors, centroids, i)


def writeToFile(centroids):
    """
    write cluster/centroids to an output file
    :param centroids: centroids array
    :return: None
    """
    try:
        # open file
        file = open(output_file, 'w')
        for i in range(len(centroids)):
            for j in range(dim):
                if j != dim - 1:  # not the last entry
                    file.write("%.4f" % centroids[i][j] + ",")
                else:  # last entry
                    file.write("%.4f" % centroids[i][j] + "\n")
        file.close()
    except FileNotFoundError:  # file not found
        print("Invalid Input!")
        exit()

