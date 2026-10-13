/* 阶段1.5 原料取证:本机 darwin 25.4.0 arm64 上钉死「引用 32B 块」的真实字节形态
 * std::string(32B) / std::vector<uint8_t>(32) / CFData(32B) 描述符 dump */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <vector>
#include <CoreFoundation/CoreFoundation.h>

static void dump(const char *tag, const void *p, size_t n) {
    printf("%s @%p:", tag, p);
    for (size_t i = 0; i < n; i++) printf(" %02x", ((const unsigned char*)p)[i]);
    printf("\n");
}
int main(void) {
    unsigned char key[32]; for (int i = 0; i < 32; i++) key[i] = 0xA0 + i;
    /* 1. std::string 32B(长串,堆) */
    {
        std::string s((const char*)key, 32);
        dump("std::string obj", &s, 32);
        printf("  c_str=%p\n", (void*)s.c_str());
    }
    /* 2. std::string 31B(SSO 边界对照) */
    {
        std::string s((const char*)key, 31);
        dump("std::string 31(SSO)", &s, 32);
    }
    /* 3. std::vector<uint8_t> 32 */
    {
        std::vector<unsigned char> v(key, key + 32);
        dump("std::vector obj", &v, 24);
        printf("  data=%p\n", (void*)v.data());
    }
    /* 4. CFData 32B */
    {
        CFDataRef d = CFDataCreate(kCFAllocatorDefault, key, 32);
        dump("CFData obj", (const void*)d, 48);
        CFRelease(d);
    }
    /* 5. CFMutableData 32B */
    {
        CFMutableDataRef m = CFDataCreateMutable(kCFAllocatorDefault, 32);
        CFDataAppendBytes(m, key, 32);
        dump("CFMutableData obj", (const void*)m, 48);
        CFRelease(m);
    }
    /* 6. 裸 malloc 32B */
    {
        void *p = malloc(32); memcpy(p, key, 32);
        printf("malloc32 @%p (mod16=%ld mod32=%ld)\n", p, (long)((uintptr_t)p % 16), (long)((uintptr_t)p % 32));
        dump("malloc32 前后", (unsigned char*)p - 16, 64);
        free(p);
    }
    return 0;
}
