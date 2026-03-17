import os, subprocess, sys
 
def read_cgroup_info():
    info={}
    try:
        with open('/sys/fs/cgroup/cgroup.controllers') as f:
            info['controllers']=f.read().strip().split()
    except: info['controllers']=['cpu','memory','io','pids']
    return info
 
def list_namespaces(pid=None):
    pid=pid or os.getpid()
    try: return os.listdir(f'/proc/{pid}/ns')
    except: return ['mnt','uts','ipc','net','pid','user','cgroup','time']
 
def get_proc_memory(pid=None):
    pid=pid or os.getpid()
    try:
        with open(f'/proc/{pid}/status') as f:
            return {l.split(':')[0]:l.split(':')[1].strip()
                    for l in f if ':' in l}.get('VmRSS','N/A')
    except: return 'N/A'
 
def simulate_cgroup_limit(memory_mb=128):
    print(f"\n[SIMULATION] Setting memory limit: {memory_mb}MB")
    print(f"  cgroup path: /sys/fs/cgroup/memory/mycontainer/")
    print(f"  echo {memory_mb*1024*1024} > memory.limit_in_bytes")
    print(f"  echo {os.getpid()} > cgroup.procs")
 
print("cgroup controllers:", read_cgroup_info())
print("Namespaces:", list_namespaces())
print("Memory RSS:", get_proc_memory())
simulate_cgroup_limit(256)
