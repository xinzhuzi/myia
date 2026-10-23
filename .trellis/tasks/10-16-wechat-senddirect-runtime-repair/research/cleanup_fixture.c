/* A new disposable test program; it never contacts WeChat or any service. */
#include <stdio.h>
#include <unistd.h>

__attribute__((noinline)) void fixture_tick(void) {
    __asm__ volatile("" ::: "memory");
}

int main(void) {
    printf("fixture_pid=%d\n", getpid());
    fflush(stdout);
    for (int index = 0; index < 80; index++) {
        fixture_tick();
        usleep(100000);
    }
    return 0;
}
