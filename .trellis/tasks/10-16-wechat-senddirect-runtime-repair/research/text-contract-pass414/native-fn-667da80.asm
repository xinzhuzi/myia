0x667da80	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x667da84	fd7b01a9	stp x29,x30,[sp, #0x10]
0x667da88	fd430091	add x29,sp,#0x10
0x667da8c	130840f9	ldr x19,[x0, #0x10]
0x667da90	b30000b4	cbz x19,0x0667daa4
0x667da94	68220091	add x8,x19,#0x8
0x667da98	09008092	mov x9,#-0x1
0x667da9c	0801e9f8	ldaddal x9,x8,[x8]
0x667daa0	880000b4	cbz x8,0x0667dab0
0x667daa4	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x667daa8	f44fc2a8	ldp x20,x19,[sp], #0x20
0x667daac	c0035fd6	ret
0x667dab0	680240f9	ldr x8,[x19]
0x667dab4	080940f9	ldr x8,[x8, #0x10]
0x667dab8	e00313aa	mov x0,x19
0x667dabc	00013fd6	blr x8
0x667dac0	e00313aa	mov x0,x19
0x667dac4	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x667dac8	f44fc2a8	ldp x20,x19,[sp], #0x20
0x667dacc	54082b14	b 0x0713fc1c
