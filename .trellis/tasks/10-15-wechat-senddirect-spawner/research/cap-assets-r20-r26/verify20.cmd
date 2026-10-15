process attach --pid 20632
command script import /tmp/wxsend3/r20/verify20.py
script verify20.run(lldb.debugger, "baseline")
detach
quit
