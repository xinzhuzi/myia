// FUN_05a6c374 05a6c374
05a6c374	stp x20,x19,[sp, #-0x20]!
05a6c378	stp x29,x30,[sp, #0x10]
05a6c37c	add x29,sp,#0x10
05a6c380	mov x19,x0
05a6c384	adrp x8,0xa524000
05a6c388	add x8,x8,#0xad0
05a6c38c	adrp x9,0x9f35000
05a6c390	add x9,x9,#0x488
05a6c394	stp x9,x8,[x0]
05a6c398	stp x8,xzr,[x0, #0x10]
05a6c39c	str xzr,[x0, #0x20]
05a6c3a0	bl 0x05a6c22c
05a6c3a4	mov x0,x19
05a6c3a8	ldp x29,x30,[sp, #0x10]
05a6c3ac	ldp x20,x19,[sp], #0x20
05a6c3b0	ret
