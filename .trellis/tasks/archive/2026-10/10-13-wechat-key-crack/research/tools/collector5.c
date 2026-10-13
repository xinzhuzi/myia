/* v6 collector5:阶段1.5「macOS 堆存根重绘」(10-13-wechat-key-crack)
 * 前提(本机 Darwin 25.4.0 arm64 layout_probe.cpp 实测):
 *   - macOS nano allocator 32B 块本体无内联元数据 → Windows tailA/B 存根不存在(collector4 tried=0 根因)
 *   - 「引用 32B 块的结构」三形态(存根在本体之外):
 *     S1 libc++ std::string(32B 载荷,>22B 必长形):
 *        [+0]=data指针 [+8]=size==0x20 [+16]=cap(0x8000...旗标|cap值,实测 0x8000000000000028)
 *     V1 std::vector<uint8_t>(32 元素):
 *        [+0]=begin [+8]=end==begin+0x20 [+16]=cap_end>=end(实测 ==end)
 *     C1 CFData/NSData(32B,不可变小载荷内联):
 *        [+16]=length==0x20 [+24]==0x20 [+32..47]=0 → 字节内联于 [+48](免解引用)
 * 打法:两遍扫描——①收区域映射(可写=堆域判定) ②逐 8B 对齐窗口匹配三模式
 *      →解引用 32B(S1/V1)或直取内联(C1)→去重→内联 chatlog darwin/v4 协议验证
 *      (PBKDF2-SHA512 256000 + XOR-0x3a macSalt + 2 迭代 macKey + 页1 HMAC,同 collector4/verify3)
 * 自验:--selftest 免 root(扫自身进程:植入已知 32B 钥匙于三种容器,验三模式召回+FP 密度)
 * 铁律:只读 mach 四调用(task_for_pid/mach_vm_region/mach_vm_read/mach_vm_deallocate);
 *      命中 KEY <64hex> 走 stdout;候选不落盘(形状级证据走 stderr 统计);零 exec/零 ptrace。
 * 用法:collector5 <message_0.db> [pid]      # 实战(需 root:task_for_pid)
 *      collector5 --selftest                # 免 root 自验(不需要 db)
 *
 * v7 +A1 锚邻域模式(C 计划,零干预):锚串 USER_KEYINFO / com.Tencent.WCDB.Config.Cipher /
 *      WCDB.Config.Cipher / setCipherKey(UTF-8+UTF-16LE 双编码,依据=Windows MindGraph
 *      probe_passphrase_41 锚邻域法+wx_info_v4 注释态预过滤器;macOS 侧同源词实证=
 *      key_info.db 唯一索引名 LoginKeyInfoTable_USER_KEYINFO)。锚实例 ±128B 窗内:
 *      8B 步进取裸 32B 候选 + 窗内 RW 指针解引用 32B 候选,共用 consider/去重/验证器。
 *      仅 RW 区生效(RO 区锚=静态常量,邻域无运行时钥匙;兼防 rodata 锚窗垃圾吃验证预算)。
 *      注意:锚实例跨 8MB 块边界(≤58B/8MB≈7e-6/边界)不续扫,窗钳制在本块内。
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <mach/mach.h>
#include <mach/mach_vm.h>
#include <CommonCrypto/CommonCrypto.h>

#ifdef __has_include
#if __has_include(<CoreFoundation/CoreFoundation.h>)
#define HAVE_CF 1
#include <CoreFoundation/CoreFoundation.h>
#endif
#endif

#ifndef HAVE_CF
#define HAVE_CF 0
#endif

/* ---------- 区域映射(升序,二分判定指针落点) ---------- */
typedef struct { mach_vm_address_t a; mach_vm_size_t s; int rw; } rg;
static rg *regions; static int nr_regions;

static int ptr_in_rw(uint64_t p) {
    int lo = 0, hi = nr_regions - 1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        if (p < regions[mid].a) hi = mid - 1;
        else if (p >= regions[mid].a + regions[mid].s) lo = mid + 1;
        else return regions[mid].rw;
    }
    return 0;
}

/* ---------- 验证(chatlog darwin/v4,与 collector4/verify3.py 同参) ---------- */
#define PAGE 4096
static unsigned char g_salt[16], g_prefix[PAGE], g_stored[64];
static size_t g_prefix_len = 0;
static int g_hits = 0;

static int verify_key(const unsigned char *key) {
    unsigned char enc[32], mac_salt[16], mk[32], mac[CC_SHA512_DIGEST_LENGTH];
    for (int i = 0; i < 16; i++) mac_salt[i] = g_salt[i] ^ 0x3a;
    if (CCKeyDerivationPBKDF(kCCPBKDF2, (const char*)key, 32, g_salt, 16,
                             kCCPRFHmacAlgSHA512, 256000, enc, 32) != kCCSuccess) return 0;
    if (CCKeyDerivationPBKDF(kCCPBKDF2, (const char*)enc, 32, mac_salt, 16,
                             kCCPRFHmacAlgSHA512, 2, mk, 32) != kCCSuccess) return 0;
    CCHmac(kCCHmacAlgSHA512, mk, 32, g_prefix, g_prefix_len, mac);
    return memcmp(mac, g_stored, 64) == 0;
}

static void report(const unsigned char *key) {
    printf("KEY ");
    for (int i = 0; i < 32; i++) printf("%02x", key[i]);
    printf("\n"); fflush(stdout); g_hits++;
}

/* ---------- 候选去重(FNV-1a 64 开放地址哈希) ---------- */
#define HCAP (1 << 17)
static uint64_t *hset; static size_t hcount;
static int seen_before(const unsigned char *k) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < 32; i++) { h ^= k[i]; h *= 1099511628211ULL; }
    if (!h) h = 1;
    size_t idx = (size_t)(h & (HCAP - 1));
    while (hset[idx]) {
        if (hset[idx] == h) return 1;
        idx = (idx + 1) & (HCAP - 1);
    }
    hset[idx] = h; hcount++;
    return 0;
}

/* ---------- S1h:64-char hex 字符串持有者(hex-decode 后验证) ----------
 * 背景:历史内容扫只覆盖 x'hex' 包裹/≥96 连续 hex/salt 邻近三种形态,
 * 裸 64hex std::string 是漏网形态;S1h = {data, size==0x40, cap} → 解引用 → hex 解码 → 验证 */
static int hexval(unsigned char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    return -1;
}

/* ---------- 统计 ---------- */
static unsigned long long n_s1, n_v1, n_c1, n_s1h, n_deref_fail, n_dup, n_verified;
static unsigned long long n_anchor, n_anchor_raw, n_anchor_deref;

/* ---------- A1 锚表(UTF-8 + UTF-16LE 双编码) ---------- */
#define ANCHOR_WIN 128
#define A1_RAW 0x10   /* selftest 位:窗内裸 32B 召回 */
#define A1_DEREF 0x20 /* selftest 位:窗内指针解引用召回 */
static unsigned char a_pat[8][128]; static size_t a_len[8]; static int a_n;
static void init_anchors(void) {
    static const char *txt[] = {"USER_KEYINFO", "com.Tencent.WCDB.Config.Cipher",
                                "WCDB.Config.Cipher", "setCipherKey"};
    a_n = 0;
    for (int t = 0; t < 4; t++) {
        size_t L = strlen(txt[t]);
        memcpy(a_pat[a_n], txt[t], L); a_len[a_n] = L; a_n++;            /* UTF-8 */
        for (size_t i = 0; i < L; i++) {                                  /* UTF-16LE */
            a_pat[a_n][i * 2] = (unsigned char)txt[t][i];
            a_pat[a_n][i * 2 + 1] = 0;
        }
        a_len[a_n] = L * 2; a_n++;
    }
}

/* 评估一个 32B 候选:去重 → (实战)verify / (自验)比对植入钥匙 */
static void consider(const unsigned char *cand, int is_selftest,
                     const unsigned char *planted, int *found_mask, int bit) {
    if (is_selftest) {
        if (planted && memcmp(cand, planted, 32) == 0) *found_mask |= bit;
        return; /* 自验:先比对后去重,三模式互不吞 */
    }
    if (seen_before(cand)) { n_dup++; return; }
    n_verified++;
    if (verify_key(cand)) report(cand);
}

static inline uint64_t rd64(const unsigned char *b) { uint64_t v; memcpy(&v, b, 8); return v; }

/* ---------- 核心:一个 8MB 块内逐 8B 窗口匹配三模式 + RW 区锚邻域 ---------- */
static void scan_chunk(const unsigned char *buf, size_t dc, int is_selftest,
                       const unsigned char *planted, int *found_mask,
                       mach_port_t task, unsigned long long max_verify, int rw) {
    for (size_t i = 0; i + 48 <= dc; i += 8) {
        uint64_t w0 = rd64(buf + i), w1 = rd64(buf + i + 8), w2 = rd64(buf + i + 16);

        /* V1: vector {begin, end, cap} 三指针, end==begin+0x20 */
        if (w0 > 0x100000000ULL && w0 < 0x800000000000ULL && w1 == w0 + 0x20 &&
            w2 >= w1 && w2 < w1 + 0x100 && ptr_in_rw(w0)) {
            n_v1++;
            unsigned char cand[32];
            vm_offset_t kd; mach_msg_type_number_t kdc;
            if (mach_vm_read(task, (mach_vm_address_t)w0, 32, &kd, &kdc) == KERN_SUCCESS && kdc == 32) {
                memcpy(cand, (void *)kd, 32);
                mach_vm_deallocate(mach_task_self(), kd, kdc);
                if (n_verified < max_verify || is_selftest) consider(cand, is_selftest, planted, found_mask, 1);
            } else n_deref_fail++;
        }

        /* S1: std::string {data, size==0x20, cap|long-flag(bit63)} */
        if (w0 > 0x100000000ULL && w0 < 0x800000000000ULL && w1 == 0x20 &&
            ((w2 >> 63) == 1 ? ((w2 & 0xFFFFFFFFFFULL) >= 0x1F && (w2 & 0xFFFFFFFFFFULL) <= 0x400)
                             : (w2 >= 0x1F && w2 <= 0x400)) && ptr_in_rw(w0)) {
            n_s1++;
            unsigned char cand[32];
            vm_offset_t kd; mach_msg_type_number_t kdc;
            if (mach_vm_read(task, (mach_vm_address_t)w0, 32, &kd, &kdc) == KERN_SUCCESS && kdc == 32) {
                memcpy(cand, (void *)kd, 32);
                mach_vm_deallocate(mach_task_self(), kd, kdc);
                if (n_verified < max_verify || is_selftest) consider(cand, is_selftest, planted, found_mask, 2);
            } else n_deref_fail++;
        }

        /* S1h: std::string {data, size==0x40, cap} 持 64-char hex → 解码后验证 */
        if (w0 > 0x100000000ULL && w0 < 0x800000000000ULL && w1 == 0x40 &&
            ((w2 >> 63) == 1 ? ((w2 & 0xFFFFFFFFFFULL) >= 0x3F && (w2 & 0xFFFFFFFFFFULL) <= 0x800)
                             : (w2 >= 0x3F && w2 <= 0x800)) && ptr_in_rw(w0)) {
            n_s1h++;
            unsigned char hexraw[64], cand[32];
            vm_offset_t kd; mach_msg_type_number_t kdc;
            if (mach_vm_read(task, (mach_vm_address_t)w0, 64, &kd, &kdc) == KERN_SUCCESS && kdc == 64) {
                memcpy(hexraw, (void *)kd, 64);
                mach_vm_deallocate(mach_task_self(), kd, kdc);
                int ok = 1;
                for (int j = 0; j < 32; j++) {
                    int hi = hexval(hexraw[j*2]), lo = hexval(hexraw[j*2+1]);
                    if (hi < 0 || lo < 0) { ok = 0; break; }
                    cand[j] = (unsigned char)((hi << 4) | lo);
                }
                if (ok && (n_verified < max_verify || is_selftest))
                    consider(cand, is_selftest, planted, found_mask, 8);
            } else n_deref_fail++;
        }

        /* C1: CFData/NSData {isa,rc,len==0x20@+16,cap==0x20@+24,0@+32,0@+40,inline[32]@+48} */
        if (w2 == 0x20 && rd64(buf + i + 24) == 0x20 &&
            rd64(buf + i + 32) == 0 && rd64(buf + i + 40) == 0) {
            n_c1++;
            const unsigned char *cand = buf + i + 48;
            if (n_verified < max_verify || is_selftest) consider(cand, is_selftest, planted, found_mask, 4);
        }
    }

    /* A1 锚邻域(仅 RW 区):锚实例 ±128B 窗内 8B 步进裸 32B + 窗内 RW 指针解引用 */
    if (!rw) return;
    for (int ap = 0; ap < a_n; ap++) {
        if (a_len[ap] > dc) continue;
        size_t pos = 0;
        while (pos + a_len[ap] <= dc) {
            const unsigned char *hit = memmem(buf + pos, dc - pos, a_pat[ap], a_len[ap]);
            if (!hit) break;
            size_t j = (size_t)(hit - buf);
            n_anchor++;
            size_t wlo = j >= ANCHOR_WIN ? (j - ANCHOR_WIN) & ~(size_t)7 : 0;
            size_t whi = (dc - j >= a_len[ap] + ANCHOR_WIN) ? j + a_len[ap] + ANCHOR_WIN : dc;
            for (size_t k = wlo; k + 8 <= whi; k += 8) {
                if (k + 32 <= whi && (n_verified < max_verify || is_selftest)) {
                    consider(buf + k, is_selftest, planted, found_mask, A1_RAW);
                    n_anchor_raw++;
                }
                uint64_t pv = rd64(buf + k);
                if (pv > 0x100000000ULL && pv < 0x800000000000ULL && ptr_in_rw(pv)) {
                    unsigned char cand[32];
                    vm_offset_t kd; mach_msg_type_number_t kdc;
                    if (mach_vm_read(task, (mach_vm_address_t)pv, 32, &kd, &kdc) == KERN_SUCCESS && kdc == 32) {
                        memcpy(cand, (void *)kd, 32);
                        mach_vm_deallocate(mach_task_self(), kd, kdc);
                        if (n_verified < max_verify || is_selftest) {
                            consider(cand, is_selftest, planted, found_mask, A1_DEREF);
                            n_anchor_deref++;
                        }
                    }
                }
            }
            pos = j + a_len[ap];
        }
    }
}

/* ---------- 区域枚举 ---------- */
static int build_region_map(mach_port_t task) {
    regions = malloc(sizeof(rg) * 400000);
    if (!regions) return -1;
    nr_regions = 0;
    mach_vm_address_t addr = 0;
    while (1) {
        mach_vm_size_t size = 0;
        vm_region_basic_info_data_64_t info;
        mach_msg_type_number_t cnt = VM_REGION_BASIC_INFO_COUNT_64;
        mach_port_t obj;
        if (mach_vm_region(task, &addr, &size, VM_REGION_BASIC_INFO_64,
                           (vm_region_info_t)&info, &cnt, &obj) != KERN_SUCCESS) break;
        if (info.protection & VM_PROT_READ) {
            if (nr_regions >= 400000) { fprintf(stderr, "区域表溢出\n"); break; }
            regions[nr_regions].a = addr;
            regions[nr_regions].s = size;
            regions[nr_regions].rw = ((info.protection & VM_PROT_WRITE) != 0);
            nr_regions++;
        }
        addr += size;
    }
    return nr_regions;
}

/* ---------- 自验模式:植入三种容器持有同一把已知钥匙 ---------- */
#if HAVE_CF
static CFDataRef g_planted_cf;
#endif
/* 保险栓:防编译器把死数据优化掉 */
static volatile int g_keep = 1;

static int selftest(void) {
    static unsigned char planted[32];
    for (int i = 0; i < 32; i++) planted[i] = (unsigned char)(0xC0 + i);
    int found_mask = 0;

    /* S1 容器:std::string 形态手工构造(C 里没有 libc++,按实测布局写描述符) */
    static unsigned char keybuf[64];
    memcpy(keybuf, planted, 32);
    struct { char *data; unsigned long size; unsigned long cap; } s1desc = {
        (char *)keybuf, 32, 0x8000000000000028UL };
    /* S1h 容器:同 key 的 64-char hex 字符串 */
    static unsigned char hexbuf[65];
    for (int i = 0; i < 32; i++) sprintf((char *)hexbuf + i*2, "%02x", planted[i]);
    struct { char *data; unsigned long size; unsigned long cap; } s1hdesc = {
        (char *)hexbuf, 64, 0x8000000000000048UL };
    /* V1 容器:vector 三指针 */
    struct { unsigned char *b, *e, *c; } v1desc = { keybuf, keybuf + 32, keybuf + 32 };
    /* A1 容器:锚串 + 锚邻域内裸 32B 钥匙(+192) + 锚邻域内指针→钥匙(+256);
     * 锚在 zone+128,窗=[zone+0, zone+128+12+128=zone+268),两候选均落窗内 */
    static unsigned char zone[1024] __attribute__((aligned(16)));
    arc4random_buf(zone, sizeof zone);
    memcpy(zone + 128, "USER_KEYINFO", 12);
    memcpy(zone + 192, planted, 32);
    uint64_t kp = (uint64_t)(uintptr_t)keybuf;
    memcpy(zone + 256, &kp, 8);
#if HAVE_CF
    g_planted_cf = CFDataCreate(kCFAllocatorDefault, planted, 32);
    if (!g_planted_cf) { fprintf(stderr, "CFDataCreate 失败\n"); return 2; }
#endif
    /* 128MB 随机垃圾堆:估 FP 密度(外推 7.8GB) */
    size_t junk_n = 128u * 1024 * 1024;
    unsigned char *junk = malloc(junk_n);
    if (!junk) { fprintf(stderr, "垃圾堆分配失败\n"); return 2; }
    arc4random_buf(junk, junk_n);

    mach_port_t self = mach_task_self();
    init_anchors();
    if (build_region_map(self) <= 0) { fprintf(stderr, "自进程区域枚举失败\n"); return 2; }
    fprintf(stderr, "selftest: 可读区 %d 个\n", nr_regions);
    unsigned long long maxv = ~0ULL;
    size_t total = 0;
    for (int r = 0; r < nr_regions; r++) {
        mach_vm_address_t ca = regions[r].a;
        while (ca < regions[r].a + regions[r].s) {
            mach_vm_size_t cs = regions[r].a + regions[r].s - ca;
            if (cs > 8 * 1024 * 1024) cs = 8 * 1024 * 1024;
            vm_offset_t data; mach_msg_type_number_t dc;
            if (mach_vm_read(self, ca, cs, &data, &dc) == KERN_SUCCESS) {
                total += dc;
                scan_chunk((unsigned char *)data, dc, 1, planted, &found_mask, self, maxv,
                           regions[r].rw);
                mach_vm_deallocate(mach_task_self(), data, dc);
            }
            ca += cs;
        }
    }
    fprintf(stderr, "selftest: 扫 %.1f MB | S1=%llu V1=%llu C1=%llu S1h=%llu 锚实例=%llu 锚裸=%llu 锚解引用=%llu deref失败=%llu 去重跳过=%llu\n",
            total / 1048576.0, n_s1, n_v1, n_c1, n_s1h, n_anchor, n_anchor_raw, n_anchor_deref, n_deref_fail, n_dup);
    int pass = 1;
    fprintf(stderr, "  S1(std::string 32B)  召回: %s\n", (found_mask & 2) ? "命中" : "未命中");
    fprintf(stderr, "  S1h(std::string 64hex)召回: %s\n", (found_mask & 8) ? "命中" : "未命中");
    fprintf(stderr, "  V1(vector)     召回: %s\n", (found_mask & 1) ? "命中" : "未命中");
    fprintf(stderr, "  A1(锚邻域裸32B)召回: %s\n", (found_mask & A1_RAW) ? "命中" : "未命中");
    fprintf(stderr, "  A1(锚邻域指针)  召回: %s\n", (found_mask & A1_DEREF) ? "命中" : "未命中");
#if HAVE_CF
    fprintf(stderr, "  C1(CFData)     召回: %s\n", (found_mask & 4) ? "命中" : "未命中");
    if (!(found_mask & 4)) pass = 0;
    CFRelease(g_planted_cf);
#else
    fprintf(stderr, "  C1(CFData): 本编译无 CoreFoundation,未测\n");
#endif
    if (!(found_mask & 2)) pass = 0;
    if (!(found_mask & 8)) pass = 0;
    if (!(found_mask & 1)) pass = 0;
    if (!(found_mask & A1_RAW)) pass = 0;
    if (!(found_mask & A1_DEREF)) pass = 0;
    if (g_keep == 0) { fprintf(stderr, "%p%p%p%p\n", (void *)&s1desc, (void *)&s1hdesc, (void *)&v1desc, (void *)zone); } /* 保险栓引用 */
    fprintf(stderr, "selftest %s\n", pass ? "PASS" : "FAIL");
    return pass ? 0 : 1;
}

int main(int argc, char **argv) {
    setlinebuf(stderr);
    hset = calloc(HCAP, sizeof(uint64_t));
    if (!hset) return 2;

    if (argc >= 2 && strcmp(argv[1], "--selftest") == 0) return selftest();
    if (argc < 2) { fprintf(stderr, "用法: %s <message_0.db> [pid] | --selftest\n", argv[0]); return 2; }

    FILE *f = fopen(argv[1], "rb");
    if (!f) { perror("db"); return 2; }
    unsigned char page1[PAGE];
    if (fread(page1, 1, PAGE, f) != PAGE) { fprintf(stderr, "db 读不足 4096B\n"); fclose(f); return 2; }
    fclose(f);
    memcpy(g_salt, page1, 16);
    memcpy(g_prefix, page1 + 16, 4032 - 16);
    unsigned char pg[4] = {1, 0, 0, 0};
    memcpy(g_prefix + 4032 - 16, pg, 4);
    g_prefix_len = 4032 - 16 + 4;
    memcpy(g_stored, page1 + 4032, 64);
    fprintf(stderr, "salt+页1 HMAC 就绪(验证器=chatlog darwin/v4)\n");

    pid_t pid = -1;
    if (argc > 2) pid = atoi(argv[2]);
    else {
        FILE *pgp = popen("pgrep -x WeChat | head -1", "r");
        if (pgp) { if (fscanf(pgp, "%d", &pid) != 1) pid = -1; pclose(pgp); }
    }
    fprintf(stderr, "WeChat pid=%d\n", pid);
    if (pid <= 0) return 1;
    mach_port_t task;
    if (task_for_pid(mach_task_self(), pid, &task) != KERN_SUCCESS) {
        fprintf(stderr, "task_for_pid 失败(需 root:sudo ./collector5 <db> [pid])\n");
        return 1;
    }

    if (build_region_map(task) <= 0) { fprintf(stderr, "区域枚举失败\n"); return 1; }
    init_anchors();
    fprintf(stderr, "可读区 %d 个(可写 %d 个)\n", nr_regions,
            ({ int w = 0; for (int i = 0; i < nr_regions; i++) w += regions[i].rw; w; }));

    unsigned long long max_verify = 5000;
    const char *mv = getenv("COLLECTOR5_MAXVERIFY");
    if (mv) max_verify = strtoull(mv, NULL, 10);

    size_t total = 0;
    for (int r = 0; r < nr_regions; r++) {
        mach_vm_address_t ca = regions[r].a;
        while (ca < regions[r].a + regions[r].s) {
            mach_vm_size_t cs = regions[r].a + regions[r].s - ca;
            if (cs > 8 * 1024 * 1024) cs = 8 * 1024 * 1024;
            vm_offset_t data; mach_msg_type_number_t dc;
            if (mach_vm_read(task, ca, cs, &data, &dc) == KERN_SUCCESS) {
                total += dc;
                scan_chunk((unsigned char *)data, dc, 0, NULL, NULL, task, max_verify,
                           regions[r].rw);
                mach_vm_deallocate(mach_task_self(), data, dc);
            }
            ca += cs;
        }
    }
    fprintf(stderr, "scanned %zu MB | S1=%llu V1=%llu C1=%llu S1h=%llu 锚实例=%llu 锚裸=%llu 锚解引用=%llu deref失败=%llu 去重跳过=%llu 已验证=%llu HITS %d\n",
            total / 1024 / 1024, n_s1, n_v1, n_c1, n_s1h, n_anchor, n_anchor_raw, n_anchor_deref, n_deref_fail, n_dup, n_verified, g_hits);
    return g_hits > 0 ? 0 : 1;
}
