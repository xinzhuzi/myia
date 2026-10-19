// FUN_05a6c868 05a6c868
05a6c868	stp x22,x21,[sp, #-0x30]!
05a6c86c	stp x20,x19,[sp, #0x10]
05a6c870	stp x29,x30,[sp, #0x20]
05a6c874	add x29,sp,#0x20
05a6c878	mov x19,x0
05a6c87c	ldrb w8,[x0, #0x24]
05a6c880	cbz w8,0x05a6c894
05a6c884	tbnz w8,#0x0,0x05a6c89c
05a6c888	mov w20,#0x0
05a6c88c	tbnz w8,#0x1,0x05a6c8f0
05a6c890	b 0x05a6c914
05a6c894	mov w20,#0x0
05a6c898	b 0x05a6c9a4
05a6c89c	ldr x20,[x19, #0x8]
05a6c8a0	ldrb w9,[x20, #0x17]
05a6c8a4	sxtb w12,w9
05a6c8a8	ldr x10,[x20, #0x8]
05a6c8ac	cmp w12,#0x0
05a6c8b0	csel w0,w10,w9,lt
05a6c8b4	cmp w0,#0x80
05a6c8b8	b.cs 0x05a6c8c4
05a6c8bc	mov w11,#0x2
05a6c8c0	b 0x05a6c8dc
05a6c8c4	bl 0x0571a3d8
05a6c8c8	ldrb w9,[x20, #0x17]
05a6c8cc	ldr x10,[x20, #0x8]
05a6c8d0	add w11,w0,#0x1
05a6c8d4	ldr w8,[x19, #0x24]
05a6c8d8	mov x12,x9
05a6c8dc	sxtb w12,w12
05a6c8e0	cmp w12,#0x0
05a6c8e4	csel w9,w10,w9,lt
05a6c8e8	add w20,w11,w9
05a6c8ec	tbz w8,#0x1,0x05a6c914
05a6c8f0	ldr w0,[x19, #0x18]
05a6c8f4	cmp w0,#0x80
05a6c8f8	b.cs 0x05a6c904
05a6c8fc	mov w9,#0x2
05a6c900	b 0x05a6c910
05a6c904	bl 0x0571a3d8
05a6c908	add w9,w0,#0x1
05a6c90c	ldr w8,[x19, #0x24]
05a6c910	add w20,w9,w20
05a6c914	tbnz w8,#0x2,0x05a6c920
05a6c918	tbnz w8,#0x3,0x05a6c978
05a6c91c	b 0x05a6c9a4
05a6c920	ldr x21,[x19, #0x10]
05a6c924	ldrb w9,[x21, #0x17]
05a6c928	sxtb w11,w9
05a6c92c	ldr x10,[x21, #0x8]
05a6c930	cmp w11,#0x0
05a6c934	csel w0,w10,w9,lt
05a6c938	cmp w0,#0x80
05a6c93c	b.cs 0x05a6c948
05a6c940	mov w0,#0x1
05a6c944	b 0x05a6c95c
05a6c948	bl 0x0571a3d8
05a6c94c	ldrb w9,[x21, #0x17]
05a6c950	ldr x10,[x21, #0x8]
05a6c954	ldr w8,[x19, #0x24]
05a6c958	mov x11,x9
05a6c95c	sxtb w11,w11
05a6c960	cmp w11,#0x0
05a6c964	csel w9,w10,w9,lt
05a6c968	add w10,w20,w0
05a6c96c	add w9,w10,w9
05a6c970	add w20,w9,#0x1
05a6c974	tbz w8,#0x3,0x05a6c9a4
05a6c978	ldr w0,[x19, #0x1c]
05a6c97c	tbnz w0,#0x1f,0x05a6c990
05a6c980	cmp w0,#0x80
05a6c984	b.cs 0x05a6c998
05a6c988	mov w8,#0x2
05a6c98c	b 0x05a6c9a0
05a6c990	mov w8,#0xb
05a6c994	b 0x05a6c9a0
05a6c998	bl 0x0571a3d8
05a6c99c	add w8,w0,#0x1
05a6c9a0	add w20,w8,w20
05a6c9a4	str w20,[x19, #0x20]
05a6c9a8	mov x0,x20
05a6c9ac	ldp x29,x30,[sp, #0x20]
05a6c9b0	ldp x20,x19,[sp, #0x10]
05a6c9b4	ldp x22,x21,[sp], #0x30
05a6c9b8	ret
