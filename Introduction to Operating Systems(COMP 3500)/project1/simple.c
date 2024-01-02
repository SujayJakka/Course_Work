#include <stdio.h>
#include <math.h>

int main() {

    int input[10];
    int i;

    for (i = 0; i < 10; i++) {
        printf("Enter a number. ");
        scanf("%d", &input[i]);
    }

    double sum, sqrtNum = 0;

    for (i = 0; i < 10; i++){
        sqrtNum = sqrt(input[i]);
        sum += sqrtNum;
    }

    double avg = sum / 10;

    printf("%lf", avg);
    
    return 0;

}