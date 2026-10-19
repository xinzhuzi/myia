process attach --pid 20632
command script import /tmp/wx_media_key_sentinel/cap.py
breakpoint set -n CCCrypt
breakpoint command add -F cap.on_hit -s python 1
breakpoint set -n CCCryptorCreate
breakpoint command add -F cap.on_hit -s python 2
continue
detach
quit
