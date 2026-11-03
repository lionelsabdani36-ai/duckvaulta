#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>

void segfault_handler() {
  printf("Segfault Occurred, incorrect address.\n");
  exit(0);
}

static unsigned char ENC[] = {0x27, 0x21, 0x25, 0x10, 0x10, 0x51, 0x44, 0x0f, 0x47, 0x56, 0x49, 0x12, 0x58, 0x00, 0x49, 0x51, 0x03, 0x00, 0x02, 0x53, 0x16, 0x07, 0x0a, 0x15, 0x02, 0x13, 0x58, 0x41, 0x03, 0x4b, 0x40, 0x50, 0x51, 0x1a, 0x06, 0x52, 0x05, 0x00, 0x57, 0x44, 0x1e};
static const char *KEY = "duckvaulta-pie-2026";

__attribute__((noinline, noclone)) int win() {
  char flag[128];
  size_t klen = strlen(KEY), n = sizeof(ENC), i;
  for (i = 0; i < n && i < sizeof(flag) - 1; i++) flag[i] = ENC[i] ^ KEY[i % klen];
  flag[i] = '\0';
  printf("You won!\n%s\n", flag);
}

int main() {
  signal(SIGSEGV, segfault_handler);
  setvbuf(stdout, NULL, _IONBF, 0);
  printf("Address of main: %p\n", &main);
  unsigned long val;
  printf("Enter the address to jump to, ex => 0x12345: ");
  scanf("%lx", &val);
  printf("Your input: %lx\n", val);
  void (*foo)(void) = (void (*)())val;
  foo();
}
