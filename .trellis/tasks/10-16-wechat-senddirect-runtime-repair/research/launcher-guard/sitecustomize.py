import os, sys

def reject_runtime(event, args):
    if event in {'subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn'}:
        with open(os.environ['WX_REPAIR_AUDIT_FILE'], 'a') as log:
            log.write(event + '\n')
        raise RuntimeError('Runtime subprocess forbidden in passive launcher check')

sys.addaudithook(reject_runtime)
