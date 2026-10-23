/* Read-only process identity/tracer status from the macOS SDK. */
#include <errno.h>
#include <libproc.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/proc.h>
#include <sys/sysctl.h>

int main(int argc, char **argv) {
    char *end = NULL;
    if (argc != 2) return 2;
    long value = strtol(argv[1], &end, 10);
    if (!end || *end || value < 1 || value > 2147483647) return 2;
    pid_t pid = (pid_t)value;
    int mib[] = {CTL_KERN, KERN_PROC, KERN_PROC_PID, pid};
    struct kinfo_proc info = {0};
    size_t size = sizeof(info);
    if (sysctl(mib, 4, &info, &size, NULL, 0) || size != sizeof(info)) return 3;
    char path[PROC_PIDPATHINFO_MAXSIZE] = {0};
    if (proc_pidpath(pid, path, sizeof(path)) <= 0) return 4;
    printf("%d\t%u\t%d\t%lld\t%d\t%s\n", info.kp_proc.p_pid,
           (unsigned)info.kp_proc.p_flag, info.kp_proc.p_stat,
           (long long)info.kp_proc.p_starttime.tv_sec,
           info.kp_proc.p_starttime.tv_usec, path);
    return 0;
}
