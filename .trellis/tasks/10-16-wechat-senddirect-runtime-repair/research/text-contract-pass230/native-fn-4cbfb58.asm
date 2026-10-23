0x4cbfb58	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x4cbfb5c	fd7b01a9	stp x29,x30,[sp, #0x10]
0x4cbfb60	fd430091	add x29,sp,#0x10
0x4cbfb64	f30300aa	mov x19,x0
0x4cbfb68	00400691	add x0,x0,#0x190
0x4cbfb6c	abc00794	bl 0x04eafe18
0x4cbfb70	097c4093	sxtw x9,w0
0x4cbfb74	61a257a9	ldp x1,x8,[x19, #0x178]
0x4cbfb78	080101cb	sub x8,x8,x1
0x4cbfb7c	280108eb	subs x8,x9,x8
0x4cbfb80	c9000054	b.ls 0x04cbfb98
0x4cbfb84	60e20591	add x0,x19,#0x178
0x4cbfb88	e10308aa	mov x1,x8
0x4cbfb8c	d466cd96	bl 0x000196dc
0x4cbfb90	61be40f9	ldr x1,[x19, #0x178]
0x4cbfb94	04000014	b 0x04cbfba4
0x4cbfb98	62000054	b.cs 0x04cbfba4
0x4cbfb9c	2800098b	add x8,x1,x9
0x4cbfba0	68c200f9	str x8,[x19, #0x180]
0x4cbfba4	688a41b9	ldr w8,[x19, #0x188]
0x4cbfba8	0201014b	sub w2,w8,w1
0x4cbfbac	60420691	add x0,x19,#0x190
0x4cbfbb0	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x4cbfbb4	f44fc2a8	ldp x20,x19,[sp], #0x20
0x4cbfbb8	f8d03714	b 0x05ab3f98
