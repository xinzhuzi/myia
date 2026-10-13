/* v2 宽模式候选收集器(10-13 档:4.1.15 x'hex' 形态失配后的破局)
 * 模式A: x'<64hex key><32hex salt>'(原版,保留)
 * 模式B: 连续 96 hex 无包裹
 * 模式C: 已知 salt 的 32B 二进制邻近(±512B,1B 步进)——key 常伴 salt 驻留
 * 输出 candidates.txt:每行一个 64hex 候选 key(去重);验证归桥侧 sqlcipher。
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <mach/mach.h>
#include <mach/mach_vm.h>

#define MAX_KEYS 200000
#define MAX_SALTS 64
#define SALT_HEX_LEN 32
#define NEAR 512

static char g_salt_hex[MAX_SALTS][SALT_HEX_LEN+1];
static unsigned char g_salt_bin[MAX_SALTS][16];
static int g_salt_count = 0;
static char (*keys)[65] = NULL;
static int key_count = 0;

static int is_hex(char c){ return isxdigit((unsigned char)c); }

static void add_key(const char *hex64) {
    for (int j = 0; j < key_count; j++)
        if (strncmp(keys[j], hex64, 64) == 0) return;
    if (key_count < MAX_KEYS) { memcpy(keys[key_count], hex64, 65); key_count++; }
}

static int read_salt(const char *path, char *out_hex) {
    FILE *f = fopen(path, "rb");
    if (!f) return -1;
    unsigned char page[4096];
    size_t n = fread(page, 1, sizeof(page), f);
    fclose(f);
    if (n < 4096) return -1;
    /* SQLCipher salt = 页首 16 字节 */
    for (int i = 0; i < 16; i++) sprintf(out_hex + i*2, "%02x", page[i]);
    return 0;
}

int main(int argc, char **argv) {
    const char *home = getenv("HOME");
    if (!home) home = "/Users/zhengbingjin";
    char base[1024];
    snprintf(base, sizeof(base), "%s/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files", home);
    /* 遍历所有账号目录的 db_storage 采 salt */
    char cmd[2048];
    snprintf(cmd, sizeof(cmd), "find \"%s\" -name '*.db' -path '*db_storage*' 2>/dev/null | head -200", base);
    FILE *p = popen(cmd, "r");
    char line[2048];
    while (fgets(line, sizeof(line), p)) {
        line[strcspn(line, "\n")] = 0;
        char hx[SALT_HEX_LEN+1];
        if (read_salt(line, hx) == 0 && g_salt_count < MAX_SALTS) {
            strcpy(g_salt_hex[g_salt_count], hx);
            for (int i = 0; i < 16; i++) {
                unsigned v; sscanf(hx + i*2, "%2x", &v);
                g_salt_bin[g_salt_count][i] = (unsigned char)v;
            }
            g_salt_count++;
        }
    }
    pclose(p);
    fprintf(stderr, "salts collected: %d\n", g_salt_count);

    pid_t pid = -1;
    if (argc > 1) pid = atoi(argv[1]);
    else { FILE *pg = popen("pgrep -x WeChat | head -1", "r"); if (pg) { fscanf(pg, "%d", &pid); pclose(pg); } }
    fprintf(stderr, "WeChat pid=%d\n", pid);
    mach_port_t task;
    kern_return_t kr = task_for_pid(mach_task_self(), pid, &task);
    if (kr != KERN_SUCCESS) { fprintf(stderr, "task_for_pid failed: %d\n", kr); return 1; }

    keys = malloc(sizeof(char[65]) * MAX_KEYS);
    mach_vm_address_t addr = 0;
    size_t total = 0;
    while (1) {
        mach_vm_size_t size = 0;
        vm_region_basic_info_data_64_t info;
        mach_msg_type_number_t cnt = VM_REGION_BASIC_INFO_COUNT_64;
        mach_port_t obj;
        if (mach_vm_region(task, &addr, &size, VM_REGION_BASIC_INFO_64, (vm_region_info_t)&info, &cnt, &obj) != KERN_SUCCESS) break;
        if (info.protection & VM_PROT_READ) {
            mach_vm_address_t ca = addr;
            while (ca < addr + size) {
                mach_vm_size_t cs = addr + size - ca; if (cs > 8*1024*1024) cs = 8*1024*1024;
                vm_offset_t data; mach_msg_type_number_t dc;
                if (mach_vm_read(task, ca, cs, &data, &dc) == KERN_SUCCESS) {
                    unsigned char *buf = (unsigned char *)data;
                    total += dc;
                    /* 模式B: 连续 96 hex */
                    size_t run = 0;
                    for (size_t i = 0; i < dc; i++) {
                        if (is_hex(buf[i])) run++;
                        else {
                            if (run >= 96) { char h[65]; memcpy(h, buf + i - 96, 64); h[64]=0; add_key(h); }
                            run = 0;
                        }
                    }
                    /* 模式C: salt 二进制邻近 32B(1B 步进) */
                    for (size_t i = 0; i + 16 <= dc; i++) {
                        for (int s = 0; s < g_salt_count; s++) {
                            if (memcmp(buf + i, g_salt_bin[s], 16) == 0) {
                                long lo = (long)i - NEAR; if (lo < 0) lo = 0;
                                long hi = (long)i + NEAR;
                                if (hi > (long)dc - 32) hi = (long)dc - 32;
                                for (long j = lo; j <= hi; j++) {
                                    char h[65];
                                    int ok = 1;
                                    for (int k = 0; k < 32; k++) {
                                        unsigned char c = buf[j+k];
                                        if (c == 0) { ok = 0; break; } /* 全零跳过 */
                                        sprintf(h + k*2, "%02x", c);
                                    }
                                    if (ok) add_key(h);
                                }
                            }
                        }
                    }
                    mach_vm_deallocate(mach_task_self(), data, dc);
                }
                ca += cs;
            }
        }
        addr += size;
    }
    fprintf(stderr, "scanned %zu MB, candidates %d\n", total/1024/1024, key_count);
    FILE *out = fopen("candidates.txt", "w");
    for (int i = 0; i < key_count; i++) fprintf(out, "%s\n", keys[i]);
    fclose(out);
    fprintf(stderr, "saved candidates.txt\n");
    return 0;
}
