command script import /Users/zhengbingjin/Downloads/微信反编译/sendmsg-勘察-1014/tools/cap.py
script cap.configure(hit_dir='/Users/zhengbingjin/Downloads/微信反编译/sendmsg-勘察-1014/hunt')
breakpoint set -a 0x12d034000+0x5e1d050
breakpoint set -a 0x12d034000+0x5e1d680
breakpoint command add -F cap.on_hit 1
breakpoint command add -F cap.on_hit 2
breakpoint disable
breakpoint list
detach
quit
