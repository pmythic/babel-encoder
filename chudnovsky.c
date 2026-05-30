#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define DIGITS_PER_ITER  14.1816474627254776555

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: ./chudnovsky <digits>\n");
        return 1;
    }

    int digits = atoi(argv[1]);

    if (digits < 0) {
        fprintf(stderr, "Error - digits must be > 0\n");
        return 1;
    }

    printf("Digits: %d\n", digits);
    printf("Iterations required: %i\n", (int)ceil(digits / DIGITS_PER_ITER));

}
