#include <stdio.h>
#include <stdlib.h>

static int addIntOvf(int result, int a, int b) {
    result = a + b;
    if(a > 0 && b > 0 && result < 0)
        return -1;
    if(a < 0 && b < 0 && result > 0)
        return -1;
    return 0;
}

int main() {
    int num1, num2, sum;
    FILE *flag;

    printf("Condition: n1 > n1 + n2 OR n2 > n1 + n2 \n");
    printf("What two positive numbers can make this possible: \n");
    fflush(stdout);

    if (scanf("%d %d", &num1, &num2) == 2) {
        printf("You entered %d and %d\n", num1, num2);
        sum = num1 + num2;
        if (addIntOvf(sum, num1, num2) == 0) {
            printf("No overflow detected. Exiting.\n");
            exit(0);
        } else if (addIntOvf(sum, num1, num2) == -1) {
            printf("You triggered signed integer overflow!\n");
        }

        if (num1 > 0 && num2 > 0) {
            flag = fopen("flag.txt", "r");
            if (flag == NULL) {
                printf("Error opening flag file.\n");
                exit(1);
            }
            char buf[64];
            if (fgets(buf, sizeof(buf), flag)) {
                printf("YOUR FLAG IS: %s\n", buf);
            }
            fclose(flag);
            exit(0);
        }
    }
    return 0;
}
