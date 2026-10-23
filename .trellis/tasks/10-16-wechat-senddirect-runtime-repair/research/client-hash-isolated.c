#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
extern uint32_t wx_hash_leaf(const unsigned char *, uint32_t);
int main(void) {
    uint32_t length;
    while (fread(&length, sizeof(length), 1, stdin) == 1) {
        if (length > 1048576) return 2;
        unsigned char *data = malloc(length ? length : 1);
        if (!data) return 3;
        if (fread(data, 1, length, stdin) != length) { free(data); return 4; }
        printf("%08x\n", wx_hash_leaf(data, length));
        free(data);
    }
    return ferror(stdin) ? 5 : 0;
}
