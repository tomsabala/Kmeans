#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

//constant
#define eps 0.0001

// defining input struct data type
struct vc {
    int K;
    int max_iter;
    int dim;
    int lines;
    char *input;
    char *output;
};

//functions
int valid_input(struct vc *);
int countDim(struct vc *);
void setMatrix(double **, struct vc *);
void k_means(double **, double **, struct vc *);
int isConv(double **, struct vc *);
double normCalc(double *, struct vc *);
void initCntr(double**, double**, int, int);
void assignVecToCluster(int *, double **, double **, struct vc *);
void calcCntrK(int *, double **, double **, struct vc *, int);
void writeBack(double**, struct vc *);


/*
 *next to do:
 * valid input + kind of errors
 * documentation
 * test for different inputs
 * accuracy
 * RUN ON NOVA!!!
 */


int main(int argc, char **argv) {
    /*

    */
    // creating input structure
    struct vc a;
    if(argc == 5) {
        a.max_iter= atoi(argv[2]);
    }else if (argc == 4){
        a.max_iter = 200;
    }else{
        printf("Invalid Input!\n");
        exit(1);
    }

    a.K = atoi(argv[1]);
    a.input = argv[argc-2];
    a.output = argv[argc-1];

    // finding lines of input && checking input validation
    a.lines = valid_input(&a);
    if(a.lines == 0){
        printf("Invalid Input!");
        exit(1);
    }

    // finding dimension of vectors
    a.dim = countDim(&a);

    // setting vector matrix from input
    double *d; // all data
    double **mat; // pointers for each line

    //allocating memory for d and mat
    d = calloc(a.lines*a.dim, sizeof (double));
    mat = calloc(a.lines, sizeof (double *));
    if(d == NULL || mat == NULL){
        printf("An Error Has Occurred\n");
        exit(1);
    }
    //attach each line of mat to the right cell in d
    int i;
    for(i=0; i<a.lines; i++){
        mat[i] = d + i*a.dim;
    }

    // vector matrix
    setMatrix(mat, &a);

    // cntr matrix
    double * v; // line of all data
    double ** cntr; // line of pointers

    v = calloc(a.K * a.dim, sizeof(double));
    cntr = calloc(a.K, sizeof(double *));
    if(v == NULL || cntr == NULL){
        printf("An Error Has Occurred\n");
        exit(1);
    }

    // attach each ine of vectors to the right cell in v
    for(i=0; i<a.K; i++){
        cntr[i] = v + i*a.dim;
    }

    // init vectors
    initCntr(cntr, mat, a.K, a.dim);

    // algorithm
    clock_t start, end;
    start = clock();
    k_means(mat, cntr, &a);
    end = clock()-start;
    double time_taken = ((double)end)/CLOCKS_PER_SEC;
    printf("%f", time_taken);

    //writing back in document output
    writeBack(cntr, &a);

    // free memory
    free(mat);
    free(cntr);
    free(d);
    free(v);

    return 0;
}

// *** settings ***
int valid_input(struct vc *a){
    /*
        input:
            int K: expected clusters amount, expected to be 1 < K < N,
                    where N is amount of lines in inputfile
            int max_iter: maximum amount of iteration to be exceeded, expected to be positive
            char *inputfile: input file name, assume is valid
    */
    if (a->max_iter <= 0){// max_iter cant be non-positive
        return 0;
    }
    FILE * input = NULL; // input file
    input = fopen(a->input, "r");
    if(input == NULL){
        printf("Invalid Input!\n");
        exit(1);
    }

    // counting lines iterator
    int counter = 0;
    char * line;
    size_t size = 1024;
    while(getline(&line, &size, input) != EOF){
        counter ++;
    }
    fclose(input);
    // checking K validation
    if (1 < a->K && a->K < counter) { return counter;}
    return 0;
}

int countDim(struct vc *a){
    FILE * input = NULL;
    input = fopen(a->input, "r");
    if(input == NULL){
        printf("Invalid Input!\n");
        exit(1);
    }

    int counter;
    counter = 1;
    char c;
    c = fgetc(input);
    while(c != '\n'){
        if(c == ','){
            counter++;
        }
        c = fgetc(input);
    }
    fclose(input);
    return counter;
}

void setMatrix(double ** mat, struct vc *a){
    /*
     * receiving size of rows - n, and size of columns - m,
     * and creates matrix of size n*m (double type) from input file data
     */
    //access to file
    FILE * input = NULL;
    input = fopen(a->input, "r");
    if(input==NULL){
        printf("Invalid Input!\n");
        exit(1);
    }

    //mat
    // building int matrix of n*m size, for saving each cell size
    int *r;
    int **sizeOfCell;

    //allocating memory for r and sizeOfCell
    r = calloc(a->lines*a->dim, sizeof (int));
    sizeOfCell = calloc(a->lines, sizeof(int *));
    if(r == NULL || sizeOfCell == NULL){
        printf("An Error Has Occurred\n");
        exit(1);
    }

    //attaching sizeOfCell to r
    int i;
    for(i = 0; i<a->lines; i++){
        sizeOfCell[i] = r + i*a->dim;
    }

    // building size of each entry matrix
    int size;
    int j;
    char c;
    i = 0;
    c = fgetc(input);
    while(i < a->lines){
        size = 0;
        j = 0;
        while(j < a->dim){
            while(c != ',' && c != '\n'){
                size ++;
                c = fgetc(input);
            }
            sizeOfCell[i][j] = size;
            j ++;
            size=0;
            c = fgetc(input);
        }
        i ++;
    }

    //close file and re-open
    fclose(input);
    input = fopen(a->input, "r");
    if(input==NULL){
        printf("Invalid Input!\n");
        exit(1);
    }

    //building the matrix itself
    char * curr;
    int currInd;
    i = 0;
    c = fgetc(input);
    while(i < a->lines){
        j = 0;
        while(j < a->dim){
            curr = calloc(sizeOfCell[i][j], sizeof(char));
            currInd = 0;
            while(c != ',' && c != '\n'){
                curr[currInd++] = c;
                c = fgetc(input);
            }
            mat[i][j] = atof(curr);
            free(curr);
            j++;
            c = fgetc(input);
        }
        i++;
    }
    fclose(input);
}

void initCntr(double ** cntr, double** vectors, int k, int dim){
    int i; int j;
    for(i=0; i<k; i++){
        for(j=0; j<dim; j++){
            cntr[i][j] = vectors[i][j];
        }
    }
}

// *** algorithm ***
void k_means(double ** vectors, double ** cntr, struct vc *a){
    int * clusters;
    clusters = calloc(a->lines, sizeof(int));
    if(clusters == NULL){
        printf("An Error Has Occurred\n");
        exit(1);
    }

    int iter; int i;
    iter = 0;

    while(!isConv(cntr, a) && iter < a->max_iter){
        iter ++;
        // update cntr
        assignVecToCluster(clusters, vectors, cntr, a);

        for(i=0; i<a->K; i++){
            calcCntrK(clusters, cntr, vectors, a, i);
        }
    }
    free(clusters);
}

int isConv(double ** cntr,struct vc * a){
    int i;
    for(i = 0; i < a->K; i++){
        if(normCalc(cntr[i], a) >= eps){ return 0; }
    }
    return 1;
}

double normCalc(double * cntr, struct vc * a){
    // calculating euclidean norm on a certain centroid
    double norm;
    int i;
    for(i = 0; i < a->dim; i++){
        norm += pow(cntr[i], 2);
    }
    return pow(norm, 0.5);
}

void assignVecToCluster(int * clusters, double ** vectors, double ** cntr, struct vc * a){
    int minInd; double minVal; int i; int j; int p;
    minInd = 0; minVal = -1;

    double currVal;
    currVal = 0;

    for(i=0; i<a->lines; i++){
        for(j=0; j<a->K; j++){
            for(p=0; p<a->dim; p++){
                currVal += pow((vectors[i][p] - cntr[j][p]), 2);
            }
            if (minVal == -1 || minVal > currVal){
                minVal = currVal;
                minInd = j;
            }
            currVal = 0;

        }
        clusters[i] = minInd;
        minVal = -1;
    }
}

void calcCntrK(int * clusters, double ** cntr, double ** vectors,struct vc * a, int ind){
    double * sum;
    sum = calloc(a->dim, sizeof(double));
    if (sum == NULL){
        printf("An Error Has Occurred\n");
        exit(1);
    }

    int i; int j; int count;
    count = 0;
    for (i=0; i<a->lines; i++){
        if(clusters[i] == ind){
            for (j=0; j<a->dim; j++){
                sum[j] += vectors[i][j];
            }
            count ++;
        }
    }
    for (j = 0; j < a->dim; j++) {
        if(count == 0){
            printf("An Error Has Occurred\n");
            exit(1);
        }
        cntr[ind][j] = sum[j] / count;
    }
    free(sum);
}

void writeBack(double** cntr, struct vc *a){
    FILE * output = NULL; // output file
    output = fopen(a->output, "w");
    if(output == NULL){
        printf("Invalid Input!\n");
        exit(1);
    }

    int i; int j;
    for (i=0; i<a->K; i++){
        for(j=0; j<a->dim; j++){
            if(j != a->dim-1){
                fprintf(output, "%.4f,", cntr[i][j]);
            } else {
                fprintf(output, "%.4f\n", cntr[i][j]);
            }
        }
    }
}