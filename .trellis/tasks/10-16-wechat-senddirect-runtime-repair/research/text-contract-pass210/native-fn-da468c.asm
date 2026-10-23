0xda468c	ff8301d1	sub sp,sp,#0x60
0xda4690	fa6701a9	stp x26,x25,[sp, #0x10]
0xda4694	f85f02a9	stp x24,x23,[sp, #0x20]
0xda4698	f65703a9	stp x22,x21,[sp, #0x30]
0xda469c	f44f04a9	stp x20,x19,[sp, #0x40]
0xda46a0	fd7b05a9	stp x29,x30,[sp, #0x50]
0xda46a4	fd430191	add x29,sp,#0x50
0xda46a8	f40301aa	mov x20,x1
0xda46ac	f30300aa	mov x19,x0
0xda46b0	285c4039	ldrb w8,[x1, #0x17]
0xda46b4	091d0013	sxtb w9,w8
0xda46b8	2a2c40a9	ldp x10,x11,[x1]
0xda46bc	3f010071	cmp w9,#0x0
0xda46c0	41b1819a	csel x1,x10,x1,lt
0xda46c4	62b1889a	csel x2,x11,x8,lt
0xda46c8	e03f0091	add x0,sp,#0xf
0xda46cc	c9bfca97	bl 0x000545f0
0xda46d0	750640f9	ldr x21,[x19, #0x8]
0xda46d4	150900b4	cbz x21,0x00da47f4
0xda46d8	a002679e	fmov d0,x21
0xda46dc	0058200e	cnt v0.8B,v0.8B
0xda46e0	0038302e	uaddlv h0,v0.8B
0xda46e4	1600261e	fmov w22,s0
0xda46e8	df0600f1	cmp x22,#0x1
0xda46ec	88000054	b.hi 0x00da46fc
0xda46f0	a80600d1	sub x8,x21,#0x1
0xda46f4	1701008a	and x23,x8,x0
0xda46f8	06000014	b 0x00da4710
0xda46fc	f70300aa	mov x23,x0
0xda4700	1f0015eb	cmp x0,x21
0xda4704	63000054	b.cc 0x00da4710
0xda4708	0808d59a	udiv x8,x0,x21
0xda470c	1781159b	msub x23,x8,x21,x0
0xda4710	680240f9	ldr x8,[x19]
0xda4714	087977f8	ldr x8,[x8, x23, LSL #0x3]
0xda4718	e80600b4	cbz x8,0x00da47f4
0xda471c	130140f9	ldr x19,[x8]
0xda4720	d30600b4	cbz x19,0x00da47f8
0xda4724	b80600d1	sub x24,x21,#0x1
0xda4728	885e4039	ldrb w8,[x20, #0x17]
0xda472c	091d0013	sxtb w9,w8
0xda4730	3f010071	cmp w9,#0x0
0xda4734	8a2640a9	ldp x10,x9,[x20]
0xda4738	39b1889a	csel x25,x9,x8,lt
0xda473c	54b1949a	csel x20,x10,x20,lt
0xda4740	06000014	b 0x00da4758
0xda4744	0801188a	and x8,x8,x24
0xda4748	1f0117eb	cmp x8,x23
0xda474c	41050054	b.ne 0x00da47f4
0xda4750	730240f9	ldr x19,[x19]
0xda4754	330500b4	cbz x19,0x00da47f8
0xda4758	680640f9	ldr x8,[x19, #0x8]
0xda475c	1f0100eb	cmp x8,x0
0xda4760	a1020054	b.ne 0x00da47b4
0xda4764	689e4039	ldrb w8,[x19, #0x27]
0xda4768	091d0013	sxtb w9,w8
0xda476c	620e40f9	ldr x2,[x19, #0x18]
0xda4770	3f010071	cmp w9,#0x0
0xda4774	49b0889a	csel x9,x2,x8,lt
0xda4778	3f0119eb	cmp x9,x25
0xda477c	a1feff54	b.ne 0x00da4750
0xda4780	69420091	add x9,x19,#0x10
0xda4784	68023837	tbnz w8,#0x7,0x00da47d0
0xda4788	88030034	cbz w8,0x00da47f8
0xda478c	ea0314aa	mov x10,x20
0xda4790	2b014039	ldrb w11,[x9]
0xda4794	4c014039	ldrb w12,[x10]
0xda4798	7f010c6b	cmp w11,w12
0xda479c	a1fdff54	b.ne 0x00da4750
0xda47a0	29050091	add x9,x9,#0x1
0xda47a4	4a050091	add x10,x10,#0x1
0xda47a8	080500f1	subs x8,x8,#0x1
0xda47ac	21ffff54	b.ne 0x00da4790
0xda47b0	12000014	b 0x00da47f8
0xda47b4	df0600f1	cmp x22,#0x1
0xda47b8	69fcff54	b.ls 0x00da4744
0xda47bc	1f0115eb	cmp x8,x21
0xda47c0	43fcff54	b.cc 0x00da4748
0xda47c4	0909d59a	udiv x9,x8,x21
0xda47c8	28a1159b	msub x8,x9,x21,x8
0xda47cc	dfffff17	b 0x00da4748
0xda47d0	280140f9	ldr x8,[x9]
0xda47d4	fa0300aa	mov x26,x0
0xda47d8	e00308aa	mov x0,x8
0xda47dc	e10314aa	mov x1,x20
0xda47e0	a7718e95	bl 0x07140e7c
0xda47e4	e80300aa	mov x8,x0
0xda47e8	e0031aaa	mov x0,x26
0xda47ec	28fbff35	cbnz w8,0x00da4750
0xda47f0	02000014	b 0x00da47f8
0xda47f4	130080d2	mov x19,#0x0
0xda47f8	e00313aa	mov x0,x19
0xda47fc	fd7b45a9	ldp x29,x30,[sp, #0x50]
0xda4800	f44f44a9	ldp x20,x19,[sp, #0x40]
0xda4804	f65743a9	ldp x22,x21,[sp, #0x30]
0xda4808	f85f42a9	ldp x24,x23,[sp, #0x20]
0xda480c	fa6741a9	ldp x26,x25,[sp, #0x10]
0xda4810	ff830191	add sp,sp,#0x60
0xda4814	c0035fd6	ret
