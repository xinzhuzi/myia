attach -p 40379
command script import /tmp/wxsend3/cap2.py
script cap2.install(lldb.debugger)
continue
script cap2.shutdown()
detach
quit
