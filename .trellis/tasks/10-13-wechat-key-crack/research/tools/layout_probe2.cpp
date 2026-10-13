#include <CoreFoundation/CoreFoundation.h>
#include <stdio.h>
static void dump(const char *tag, const void *p, size_t n) {
    printf("%s @%p:", tag, p);
    for (size_t i = 0; i < n; i++) { if (i % 8 == 0) printf(" |"); printf("%02x", ((const unsigned char*)p)[i]); }
    printf("\n");
}
int main(void) {
    unsigned char key[32]; for (int i = 0; i < 32; i++) key[i] = 0xA0 + i;
    CFDataRef d = CFDataCreate(kCFAllocatorDefault, key, 32);
    dump("CFData32 obj(64B)", (const void*)d, 64);
    const unsigned char *bp = CFDataGetBytePtr(d);
    printf("bytePtr=%p (obj%+ld) bytes[0]=%02x\n", bp, (long)((const char*)bp - (const char*)d), bp[0]);
    dump("bytePtr 前后", bp - 16, 64);
    CFRelease(d);
    CFDataRef d16 = CFDataCreate(kCFAllocatorDefault, key, 16);
    dump("CFData16 obj(48B)", (const void*)d16, 48);
    printf("bytePtr16=%p (obj%+ld)\n", CFDataGetBytePtr(d16), (long)((const char*)CFDataGetBytePtr(d16) - (const char*)d16));
    CFRelease(d16);
    return 0;
}
