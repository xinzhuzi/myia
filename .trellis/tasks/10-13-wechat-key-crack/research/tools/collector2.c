/* v3:chatlog key/darwin/v4.go 模式搬运——裸 32B 锚定提取
 * 模式D1: " fts5(%\0"(20 66 74 73 35 28 25 00) 命中处取 [+16][-80][+64] 各 32B
 * 模式D2: 16 连零块 命中处取 [-32]
 * 模式B: 连续96hex(保留)
 * 输出 candidates2.txt;验证归 verify2(chatlog v4 协议) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <mach/mach.h>
#include <mach/mach_vm.h>

#define MAX_KEYS 500000
static char (*keys)[65] = NULL;
static int key_count = 0;
static void add_key(const unsigned char *p) {
    char h[65]; int ok=1;
    for (int i=0;i<32;i++){ if(!p[i]&&i<31){} sprintf(h+i*2,"%02x",p[i]); }
    /* 全零/低熵快剔:首个字节与末字节同且中间大量重复的粗筛留给验证器 */
    for (int j=0;j<key_count;j++) if(!strncmp(keys[j],h,64)) return;
    if(key_count<MAX_KEYS){ memcpy(keys[key_count],h,65); key_count++; }
}
int main(void){
    pid_t pid=-1; FILE*pg=popen("pgrep -x WeChat | head -1","r");
    if(pg){fscanf(pg,"%d",&pid);pclose(pg);}
    fprintf(stderr,"WeChat pid=%d\n",pid);
    mach_port_t task; kern_return_t kr=task_for_pid(mach_task_self(),pid,&task);
    if(kr!=KERN_SUCCESS){fprintf(stderr,"task_for_pid failed:%d\n",kr);return 1;}
    keys=malloc(sizeof(char[65])*MAX_KEYS);
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
                    /* D1: fts5 标记 */
                    for(size_t i=0;i+8<=dc;i++){
                        if(!memcmp(buf+i,fts,8)){
                            long offs[3]={16,-80,64};
                            for(int o=0;o<3;o++){ long j=(long)i+offs[o]; if(j>=0&&j+32<=(long)dc) add_key(buf+j); }
                        }
                    }
                    /* D2: 16 连零 → 前 32B */
                    int zrun=0;
                    for(size_t i=0;i<dc;i++){
                        if(buf[i]==0){ zrun++; if(zrun==16){ long j=(long)i-47; if(j>=0) add_key(buf+j); } }
                        else zrun=0;
                    }
                    /* B: 96 连 hex */
                    size_t run=0;
                    for(size_t i=0;i<dc;i++){
                        if(isxdigit(buf[i])){run++; if(run==96){ add_key(buf+i-95); }}
                        else run=0;
                    }
                    mach_vm_deallocate(mach_task_self(),data,dc);
                }
                ca+=cs;
            }
        }
        addr+=size;
    }
    fprintf(stderr,"scanned %zu MB, candidates %d\n",total/1024/1024,key_count);
    FILE*out=fopen("candidates2.txt","w");
    for(int i=0;i<key_count;i++)fprintf(out,"%s\n",keys[i]);
    fclose(out);
    fprintf(stderr,"saved candidates2.txt\n");
    return 0;
}
