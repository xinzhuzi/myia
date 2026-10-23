0x4cbf820	08c040f8	ldur x8,[x0, #0xc]
0x4cbf824	088400f9	str x8,[x0, #0x108]
0x4cbf828	08004939	ldrb w8,[x0, #0x240]
0x4cbf82c	1f050071	cmp w8,#0x1
0x4cbf830	01020054	b.ne 0x04cbf870
0x4cbf834	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x4cbf838	fd7b01a9	stp x29,x30,[sp, #0x10]
0x4cbf83c	fd430091	add x29,sp,#0x10
0x4cbf840	f30300aa	mov x19,x0
0x4cbf844	dafcff97	bl 0x04cbebac
0x4cbf848	601241f9	ldr x0,[x19, #0x220]
0x4cbf84c	a00000b4	cbz x0,0x04cbf860
0x4cbf850	080040f9	ldr x8,[x0]
0x4cbf854	080940f9	ldr x8,[x8, #0x10]
0x4cbf858	e10313aa	mov x1,x19
0x4cbf85c	00013fd6	blr x8
0x4cbf860	e00313aa	mov x0,x19
0x4cbf864	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x4cbf868	f44fc2a8	ldp x20,x19,[sp], #0x20
0x4cbf86c	4a000014	b 0x04cbf994
0x4cbf870	c0035fd6	ret
