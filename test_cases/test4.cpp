
// expected to replace: 1

#include "stdio.h"
#include "time.h"
#include "stdlib.h"
#include <iostream>
#include <chrono>
using namespace std;

// From https://stackoverflow.com/questions/33058848/generate-a-random-double-between-1-and-1
/* generate a random floating point number from min to max */
double randfrom(double min, double max) 
{
    double range = (max - min); 
    double div = RAND_MAX / range;
    return min + (rand() / div);
}

double op_function(double d, double k, double g, double b) {
  // Start optimization range
    d = k + g; 
    b = k + g;
    // End optimization range
    return d+k+g+b;
}

int main() {
    srand (0);
    double d,k,b,g;  
    b = randfrom(-100.0, 100.0);
    d = randfrom(-100.0, 100.0);
    g = randfrom(-100.0, 100.0);
    k = randfrom(-100.0, 100.0);
    // Timer code from https://www.techiedelight.com/measure-elapsed-time-program-chrono-library/
    auto start = chrono::steady_clock::now();
    double res;
    for (int i = 0; i < 2000000; i++) {
        res = op_function(d,k,g,b);
    }
    auto end = chrono::steady_clock::now();
    cout << "Elapsed time in milliseconds: "
        << chrono::duration_cast<chrono::milliseconds>(end - start).count()
        << " ms" << endl;
    printf("hash: %f\n", res);
    return 0;
}

