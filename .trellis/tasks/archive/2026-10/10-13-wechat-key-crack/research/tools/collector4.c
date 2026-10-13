/* v5:Windows WeChatMsg v4「指针跳转」法 macOS 移植
 * 机制:内存中存在 8B 指针 P(指向 32B 钥匙块),后随堆元数据
 *      (\x00*8 + 0x20 块长 + 0x2f 标志)——找到存根→解引用→读 32B→协议验证
 * 变体A=Windows 原版模式;变体B=去中段零适应 macOS allocator;命中即验(chatlog v4 协议) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mach/mach.h>
#include <mach/mach_vm.h>
#include <CommonCrypto/CommonCrypto.h>

#define PAGE 4096
static unsigned char g_page1[PAGE], g_salt[16], g_prefix[PAGE], g_stored[64];
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
int main(int argc, char **argv){
    if (argc < 2) { fprintf(stderr,"用法: %s <message_0.db>\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "rb"); if (!f) { perror("db"); return 2; }
    fread(g_page1, 1, PAGE, f); fclose(f);
    memcpy(g_salt, g_page1, 16);
    memcpy(g_prefix, g_page1+16, 4032-16);
    unsigned char pg[4] = {1,0,0,0};
    memcpy(g_prefix+4032-16, pg, 4); g_prefix_len = 4032-16+4;
    memcpy(g_stored, g_page1+4032, 64);

    pid_t pid=-1; FILE*pgp=popen("pgrep -x WeChat | head -1","r");
    if(pgp){fscanf(pgp,"%d",&pid);pclose(pgp);}
    fprintf(stderr,"WeChat pid=%d\n",pid);
    mach_port_t task; if(task_for_pid(mach_task_self(),pid,&task)!=KERN_SUCCESS){fprintf(stderr,"task_for_pid failed\n");return 1;}

    /* 第一遍:收集内存区映射表(用于指针有效性判定) */
    typedef struct { mach_vm_address_t a; mach_vm_size_t s; } rg;
    rg *regions = malloc(sizeof(rg)*200000); int nr=0;
    mach_vm_address_t addr=0;
    while(1){
        mach_vm_size_t size=0; vm_region_basic_info_data_64_t info; mach_msg_type_number_t cnt=VM_REGION_BASIC_INFO_COUNT_64; mach_port_t obj;
        if(mach_vm_region(task,&addr,&size,VM_REGION_BASIC_INFO_64,(vm_region_info_t)&info,&cnt,&obj)!=KERN_SUCCESS)break;
        if((info.protection & VM_PROT_READ) && nr<200000){ regions[nr].a=addr; regions[nr].s=size; nr++; }
        addr+=size;
    }
    fprintf(stderr,"可读区 %d 个\n", nr);

    size_t total=0; unsigned long long tried=0;
    static const unsigned char tailA[] = {0,0,0,0,0,0,0,0, 0x20,0,0,0,0,0,0,0, 0x2f,0,0,0,0,0,0,0};
    static const unsigned char tailB[] = {0x20,0,0,0,0,0,0,0, 0x2f,0,0,0,0,0,0,0};
    for(int r=0;r<nr;r++){
        mach_vm_address_t ca=regions[r].a;
        while(ca<regions[r].a+regions[r].s){
            mach_vm_size_t cs=regions[r].a+regions[r].s-ca; if(cs>8*1024*1024)cs=8*1024*1024;
            vm_offset_t data; mach_msg_type_number_t dc;
            if(mach_vm_read(task,ca,cs,&data,&dc)==KERN_SUCCESS){
                unsigned char*buf=(unsigned char*)data; total+=dc;
                for(size_t i=0;i+32<=dc;i+=8){ /* 8 对齐 */
                    /* 指针值:高 2B 零(用户态),低 6B 任意;后随 tailA 或 tailB */
                    unsigned long long p=0; memcpy(&p, buf+i, 8);
                    if(p<0x100000000ULL || p>0x800000000000ULL) continue; /* 粗指针域 */
                    int okA = (i+8+24<=dc) && !memcmp(buf+i+8, tailA, 24);
                    int okB = (i+8+16<=dc) && !memcmp(buf+i+8, tailB, 16);
                    if(!okA && !okB) continue;
                    tried++;
                    vm_offset_t kd; mach_msg_type_number_t kdc;
                    if(mach_vm_read(task,(mach_vm_address_t)p,32,&kd,&kdc)==KERN_SUCCESS && kdc==32){
                        unsigned char key[32]; memcpy(key,(void*)kd,32);
                        mach_vm_deallocate(mach_task_self(),kd,kdc);
                        if(verify_key(key)) report(key);
                    }
                }
                mach_vm_deallocate(mach_task_self(),data,dc);
            }
            ca+=cs;
        }
    }
    fprintf(stderr,"scanned %zu MB, deref tried %llu, HITS %d\n",total/1024/1024,tried,g_hits);
    return g_hits>0?0:1;
}
