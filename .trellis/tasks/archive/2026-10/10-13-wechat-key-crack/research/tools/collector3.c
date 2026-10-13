/* v4:hash 去重 + 内置 chatlog v4 协议验证,命中即打印(一段式)
 * 协议: encKey=PBKDF2(key32,salt,256000,32,SHA512); macSalt=salt^0x3a;
 *       macKey=PBKDF2(encKey,macSalt,2,32); HMAC-SHA512(macKey,page[16:4032]+le32(1))==page[4032:4096] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <mach/mach.h>
#include <mach/mach_vm.h>
#include <CommonCrypto/CommonCrypto.h>

#define PAGE 4096
static unsigned char g_page1[PAGE], g_salt[16], g_prefix[PAGE], g_stored[64];
static size_t g_prefix_len = 0;
static int g_hits = 0;

static int verify_key(const unsigned char *key) { /* 32B */
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
/* 简单开放寻址 hash set 去重 32B */
#define HB 22
static unsigned char *hset = NULL; static size_t hcap = 0, hused = 0;
static void hinit(void){ hcap = 1UL<<HB; hset = calloc(hcap, 32); }
static unsigned long long fnv(const unsigned char*p){unsigned long long h=1469598103934665603ULL;for(int i=0;i<32;i++){h^=p[i];h*=1099511628211ULL;}return h;}
static int hseen(const unsigned char*p){
    size_t i = fnv(p) & (hcap-1);
    while (hset[i*32]) {
        if (!memcmp(hset+i*32, p, 32)) return 1;
        i = (i+1) & (hcap-1);
    }
    memcpy(hset+i*32, p, 32); hused++;
    return 0;
}
int main(int argc, char **argv){
    const char *db = argv[1] ? argv[1] : NULL;
    char dbpath[2048];
    if (!db) { fprintf(stderr,"用法: %s <message_0.db 路径>\n", argv[0]); return 2; }
    snprintf(dbpath, sizeof(dbpath), "%s", db);
    FILE *f = fopen(dbpath, "rb"); if (!f) { perror("db"); return 2; }
    fread(g_page1, 1, PAGE, f); fclose(f);
    memcpy(g_salt, g_page1, 16);
    memcpy(g_prefix, g_page1+16, 4032-16);
    unsigned char pg[4] = {1,0,0,0};
    memcpy(g_prefix+4032-16, pg, 4);
    g_prefix_len = 4032-16+4;
    memcpy(g_stored, g_page1+4032, 64);
    fprintf(stderr,"salt ok, 验证器就绪\n");

    pid_t pid=-1; FILE*pgp=popen("pgrep -x WeChat | head -1","r");
    if(pgp){fscanf(pgp,"%d",&pid);pclose(pgp);}
    fprintf(stderr,"WeChat pid=%d\n",pid);
    mach_port_t task; if(task_for_pid(mach_task_self(),pid,&task)!=KERN_SUCCESS){fprintf(stderr,"task_for_pid failed\n");return 1;}
    hinit();
    static const unsigned char fts[] = {0x20,0x66,0x74,0x73,0x35,0x28,0x25,0x00};
    mach_vm_address_t addr=0; size_t total=0;
    while(1){
        mach_vm_size_t size=0; vm_region_basic_info_data_64_t info; mach_msg_type_number_t cnt=VM_REGION_BASIC_INFO_COUNT_64; mach_port_t obj;
        if(mach_vm_region(task,&addr,&size,VM_REGION_BASIC_INFO_64,(vm_region_info_t)&info,&cnt,&obj)!=KERN_SUCCESS)break;
        if(info.protection & VM_PROT_READ){
            mach_vm_address_t ca=addr;
            while(ca<addr+size){
                mach_vm_size_t cs=addr+size-ca; if(cs>8*1024*1024)cs=8*1024*1024;
                vm_offset_t data; mach_msg_type_number_t dc;
                if(mach_vm_read(task,ca,cs,&data,&dc)==KERN_SUCCESS){
                    unsigned char*buf=(unsigned char*)data; total+=dc;
                    for(size_t i=0;i+8<=dc;i++){
                        if(!memcmp(buf+i,fts,8)){
                            long offs[3]={16,-80,64};
                            for(int o=0;o<3;o++){ long j=(long)i+offs[o]; if(j>=0&&j+32<=(long)dc){ const unsigned char*k=buf+j; if(!hseen(k) && verify_key(k)) report(k);} }
                        }
                    }
                    int zrun=0;
                    for(size_t i=0;i<dc;i++){
                        if(buf[i]==0){ zrun++; if(zrun==16){ long j=(long)i-47; if(j>=0&&j+32<=(long)dc){ const unsigned char*k=buf+j; if(!hseen(k) && verify_key(k)) report(k);} } }
                        else zrun=0;
                    }
                    size_t run=0;
                    for(size_t i=0;i<dc;i++){
                        if(isxdigit(buf[i])){ run++; if(run==96){ const unsigned char*k=buf+i-63; if(k>=buf && k+32<=buf+dc){ if(!hseen(k)&&verify_key(k)) report(k);} run=0; } }
                        else run=0;
                    }
                    mach_vm_deallocate(mach_task_self(),data,dc);
                }
                ca+=cs;
            }
        }
        addr+=size;
    }
    fprintf(stderr,"scanned %zu MB, unique candidates %zu, HITS %d\n",total/1024/1024,hused,g_hits);
    return g_hits>0?0:1;
}
