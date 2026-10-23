0x667ddf8	ff0301d1	sub sp,sp,#0x40
0x667ddfc	f44f02a9	stp x20,x19,[sp, #0x20]
0x667de00	fd7b03a9	stp x29,x30,[sp, #0x30]
0x667de04	fdc30091	add x29,sp,#0x30
0x667de08	e30302aa	mov x3,x2
0x667de0c	e20301aa	mov x2,x1
0x667de10	e10300aa	mov x1,x0
0x667de14	f30308aa	mov x19,x8
0x667de18	e8030091	mov x8,sp
0x667de1c	a04700d1	sub x0,x29,#0x11
0x667de20	490e0094	bl 0x06681744
0x667de24	e003c03d	ldr q0,[sp]
0x667de28	6002803d	str q0,[x19]
0x667de2c	fd7b43a9	ldp x29,x30,[sp, #0x30]
0x667de30	f44f42a9	ldp x20,x19,[sp, #0x20]
0x667de34	ff030191	add sp,sp,#0x40
0x667de38	c0035fd6	ret
