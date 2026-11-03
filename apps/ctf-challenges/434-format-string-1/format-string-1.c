#include <stdio.h>

int main() {
    char buf[1024];
    char secret1[64] = "secret_chef_special_crabby_patty\n";
    char flag[64] = "CTF{fmt_str1ng_st4ck_l34k_64b1t_7d8e2c}\n";
    char secret2[64] = "secret_recipe_seasoning_0x99\n";

    printf("Give me your order and I'll read it back to you:\n");
    fflush(stdout);

    if (scanf("%1023s", buf) == 1) {
        printf("Here's your order: ");
        printf(buf);
        printf("\nBye!\n");
        fflush(stdout);
    }
    return 0;
}
