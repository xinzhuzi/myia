/* collector.c — 微信进程密钥候选收集器(task 10-13-wechat-key-subsystem)
 *
 * 2026-10-13 主人令「把获取这些密钥的方式全部固化成代码」:/tmp/wxkey-c
 * 临时件(当日真跑验证)工程化为组件 native 件。扫描逻辑照搬已验证的
 * /tmp/wxkey-c/collector.c(模式 B/C)+ find_all_keys.c(模式 A),三模式
 * 宽收集,验真归桥侧(sqlcipher 试开 + page1 离线 HMAC)。
 *
 * 三模式(候选 = 64-hex key 形态,去重):
 *   A: x'<64hex key><32hex salt>' 包裹字符串(find_all_keys 血统;
 *      4.1.15 实测失配——保留是因为代价为零,其他版本形态可命中);
 *   B: 连续 ≥96 个 hex 字符的裸串(取前 64;A 是 B 的子集,B 阈值若漂移
 *      A 仍独立兜底);
 *   C: 已知 salt(各库 page1 前 16B,由桥侧采集经 stdin 传入)二进制
 *      邻域 ±512B 内的 32B 窗(1B 步进,含零字节窗弃)。
 *
 * 安全红线(固化时硬化,threat model 详见组件 native/README 与
 * install-keyscanner.sh 头注):
 *   - 只读 mach API,与已审计的 /tmp 件同集:task_for_pid /
 *     mach_vm_region / mach_vm_read / mach_vm_deallocate——零写、零注入、
 *     零 exec(setuid 件审计焦点:不 popen/system/fork/exec*,salt 采集与
 *     pid 发现移到桥侧 Python,salt 走 stdin、pid 走 argv);
 *   - argv 白名单:恰好一个参数 = 目标 pid,纯数字,否则 exit 2;
 *   - 输出路径固定:候选(每行一个 64-hex)恒走 stdout,诊断形状
 *     (salt 数/区数/扫描字节/候选数)恒走 stderr,零文件落盘;
 *   - 预算上界为编译期常量(MAX_KEYS/MAX_SALTS/段长),单遍批处理,
 *     扫完即退,零常驻零轮询。
 *
 * 构建:cc -O2 -o collector collector.c(桥侧首用时自动编译;无 cc 时
 * 结构化报错带 Xcode CLT 指引)。
 * 用法:collector <pid>  (salt 清单经 stdin:每行 32-hex,EOF 结束)
 * 退出:0 收集完成(候选数可为 0);1 task_for_pid 被拒(如实,不规避);
 *      2 用法错(argv 形状不符)。
 */

#include <ctype.h>
#include <mach/mach.h>
#include <mach/mach_vm.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_KEYS 200000
#define MAX_SALTS 64
#define SALT_BIN_LEN 16
#define SALT_HEX_LEN 32
#define KEY_HEX_LEN 64
#define NEAR 512                 /* 模式 C:salt 邻域半径(字节) */
#define CHUNK_MAX (8 * 1024 * 1024) /* 单段 mach_vm_read 上限 */

static unsigned char g_salt_bin[MAX_SALTS][SALT_BIN_LEN];
static int g_salt_count = 0;
static char (*g_keys)[KEY_HEX_LEN + 1] = NULL;
static int g_key_count = 0;

static int is_hex(unsigned char c) { return isxdigit(c); }

/* 顺序去重入库(候选库上界 MAX_KEYS,超界弃——单遍批处理的预算边界) */
static void add_key(const char *hex64) {
    int j;
    for (j = 0; j < g_key_count; j++)
        if (strncmp(g_keys[j], hex64, KEY_HEX_LEN) == 0) return;
    if (g_key_count < MAX_KEYS) {
        memcpy(g_keys[g_key_count], hex64, KEY_HEX_LEN + 1);
        g_key_count++;
    }
}

/* salt 清单经 stdin 读入(桥侧已从各库 page1 前 16B 采集;每行 32-hex,
 * 形状不符行弃,EOF 结束)——替代 /tmp 件的 popen(find) 采集:setuid 件
 * 零 exec,材料采集留在非提权的桥侧。 */
static void read_salts_stdin(void) {
    char line[SALT_HEX_LEN + 8];
    while (fgets(line, sizeof(line), stdin)) {
        int i, ok = 1;
        line[strcspn(line, "\r\n")] = '\0';
        if (line[0] == '\0') continue;
        if (strlen(line) != SALT_HEX_LEN) continue;
        for (i = 0; i < SALT_HEX_LEN; i++)
            if (!is_hex((unsigned char)line[i])) { ok = 0; break; }
        if (!ok) continue;
        if (g_salt_count >= MAX_SALTS) break;
        for (i = 0; i < SALT_BIN_LEN; i++) {
            unsigned v = 0;
            if (sscanf(line + i * 2, "%2x", &v) != 1) { ok = 0; break; }
            g_salt_bin[g_salt_count][i] = (unsigned char)v;
        }
        if (!ok) continue;
        g_salt_count++;
    }
}

int main(int argc, char **argv) {
    const char *p;
    char h[KEY_HEX_LEN + 1];
    pid_t pid;
    long regions = 0;
    size_t total = 0;
    mach_port_t task;
    kern_return_t kr;
    mach_vm_address_t addr = 0;

    /* argv 白名单:恰好 1 个参数,pid 纯数字(其余一律拒) */
    if (argc != 2) {
        fprintf(stderr, "usage: collector <pid>(salt 清单走 stdin)\n");
        return 2;
    }
    for (p = argv[1]; *p; p++)
        if (!isdigit((unsigned char)*p)) {
            fprintf(stderr, "pid 须为纯数字,拒: 形状不符\n");
            return 2;
        }
    pid = (pid_t)strtol(argv[1], NULL, 10);

    read_salts_stdin();
    fprintf(stderr, "salts: %d\n", g_salt_count);
    fprintf(stderr, "pid: %d\n", (int)pid);

    kr = task_for_pid(mach_task_self(), pid, &task);
    if (kr != KERN_SUCCESS) {
        fprintf(stderr, "task_for_pid failed: %d\n", (int)kr);
        return 1; /* hardened runtime 目标对无调试 entitlement 的调用方
                     root 亦可能被拒(KERN_FAILURE)——如实上报,不规避 */
    }

    g_keys = malloc(sizeof(char[KEY_HEX_LEN + 1]) * MAX_KEYS);
    if (g_keys == NULL) {
        fprintf(stderr, "oom\n");
        mach_port_deallocate(mach_task_self(), task);
        return 1;
    }

    while (1) {
        mach_vm_size_t size = 0;
        vm_region_basic_info_data_64_t info;
        mach_msg_type_number_t cnt = VM_REGION_BASIC_INFO_COUNT_64;
        mach_port_t obj;
        mach_vm_address_t ca;
        if (mach_vm_region(task, &addr, &size, VM_REGION_BASIC_INFO_64,
                           (vm_region_info_t)&info, &cnt, &obj) != KERN_SUCCESS)
            break; /* 地址空间走完,单遍正常终止 */
        if (size == 0) { addr++; continue; }
        regions++;
        if (info.protection & VM_PROT_READ) {
            for (ca = addr; ca < addr + size;) {
                mach_vm_size_t cs = addr + size - ca;
                vm_offset_t data;
                mach_msg_type_number_t dc;
                size_t i, run;
                if (cs > CHUNK_MAX) cs = CHUNK_MAX;
                if (mach_vm_read(task, ca, cs, &data, &dc) != KERN_SUCCESS)
                    break; /* 区中途失读:弃该区剩余,继续下一区 */
                {
                    unsigned char *buf = (unsigned char *)data;
                    total += dc;

                    /* 模式 A:x'<96hex>' 包裹(find_all_keys 血统) */
                    for (i = 0; i + KEY_HEX_LEN + SALT_HEX_LEN + 3 <= dc; i++) {
                        size_t j;
                        if (buf[i] != 'x' || buf[i + 1] != '\'') continue;
                        for (j = 0; j < KEY_HEX_LEN + SALT_HEX_LEN; j++)
                            if (!is_hex(buf[i + 2 + j])) break;
                        if (j < KEY_HEX_LEN + SALT_HEX_LEN) continue;
                        if (buf[i + 2 + KEY_HEX_LEN + SALT_HEX_LEN] != '\'') continue;
                        memcpy(h, buf + i + 2, KEY_HEX_LEN);
                        h[KEY_HEX_LEN] = '\0';
                        add_key(h);
                    }

                    /* 模式 B:连续 ≥96 hex 裸串(取前 64) */
                    run = 0;
                    for (i = 0; i <= dc; i++) {
                        if (i < dc && is_hex(buf[i])) { run++; continue; }
                        if (run >= KEY_HEX_LEN + SALT_HEX_LEN) {
                            memcpy(h, buf + i - (KEY_HEX_LEN + SALT_HEX_LEN), KEY_HEX_LEN);
                            h[KEY_HEX_LEN] = '\0';
                            add_key(h);
                        }
                        run = 0;
                    }

                    /* 模式 C:已知 salt 二进制邻域 ±512B 的 32B 窗(1B 步进) */
                    for (i = 0; i + SALT_BIN_LEN <= dc; i++) {
                        int s;
                        for (s = 0; s < g_salt_count; s++) {
                            if (memcmp(buf + i, g_salt_bin[s], SALT_BIN_LEN) == 0) {
                                long lo = (long)i - NEAR;
                                long hi = (long)i + NEAR;
                                long j;
                                if (lo < 0) lo = 0;
                                if (hi > (long)dc - 32) hi = (long)dc - 32;
                                for (j = lo; j <= hi; j++) {
                                    int k, ok = 1;
                                    for (k = 0; k < 32; k++) {
                                        unsigned char c = buf[j + k];
                                        if (c == 0) { ok = 0; break; } /* 含零字节窗弃 */
                                        sprintf(h + k * 2, "%02x", c);
                                    }
                                    if (ok) add_key(h);
                                }
                            }
                        }
                    }
                }
                mach_vm_deallocate(mach_task_self(), data, dc);
                ca += cs;
            }
        }
        addr += size;
    }
    fprintf(stderr, "regions: %ld\n", regions);
    fprintf(stderr, "scanned_mb: %zu\n", total / 1024 / 1024);
    fprintf(stderr, "candidates: %d\n", g_key_count);

    /* 输出路径固定:候选恒走 stdout(桥侧落数据根私有区临时文件),
     * 本件自身零文件写。 */
    {
        int i;
        for (i = 0; i < g_key_count; i++) printf("%s\n", g_keys[i]);
    }
    fflush(stdout);

    free(g_keys);
    mach_port_deallocate(mach_task_self(), task);
    return 0;
}
