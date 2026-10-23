0x4cbebac	ff4301d1	sub sp,sp,#0x50
0x4cbebb0	f65702a9	stp x22,x21,[sp, #0x20]
0x4cbebb4	f44f03a9	stp x20,x19,[sp, #0x30]
0x4cbebb8	fd7b04a9	stp x29,x30,[sp, #0x40]
0x4cbebbc	fd030191	add x29,sp,#0x40
0x4cbebc0	081041f9	ldr x8,[x0, #0x220]
0x4cbebc4	c80000b4	cbz x8,0x04cbebdc
0x4cbebc8	fd7b44a9	ldp x29,x30,[sp, #0x40]
0x4cbebcc	f44f43a9	ldp x20,x19,[sp, #0x30]
0x4cbebd0	f65742a9	ldp x22,x21,[sp, #0x20]
0x4cbebd4	ff430191	add sp,sp,#0x50
0x4cbebd8	c0035fd6	ret
0x4cbebdc	f30300aa	mov x19,x0
0x4cbebe0	39a9f597	bl 0x04a290c4
0x4cbebe4	e0010034	cbz w0,0x04cbec20
0x4cbebe8	005e8052	mov w0,#0x2f0
0x4cbebec	11059294	bl 0x07140030
0x4cbebf0	f40300aa	mov x20,x0
0x4cbebf4	1ffc00a9	stp xzr,xzr,[x0, #0x8]
0x4cbebf8	888f02d0	adrp x8,0x9eb0000
0x4cbebfc	08012391	add x8,x8,#0x8c0
0x4cbec00	080000f9	str x8,[x0]
0x4cbec04	15600091	add x21,x0,#0x18
0x4cbec08	e00315aa	mov x0,x21
0x4cbec0c	015b8052	mov w1,#0x2d8
0x4cbec10	e0059294	bl 0x07140390
0x4cbec14	e00315aa	mov x0,x21
0x4cbec18	df100094	bl 0x04cc2f94
0x4cbec1c	11000014	b 0x04cbec60
0x4cbec20	e00313aa	mov x0,x19
0x4cbec24	58acf597	bl 0x04a29d84
0x4cbec28	00040034	cbz w0,0x04cbeca8
0x4cbec2c	00018152	mov w0,#0x808
0x4cbec30	00059294	bl 0x07140030
0x4cbec34	f40300aa	mov x20,x0
0x4cbec38	1ffc00a9	stp xzr,xzr,[x0, #0x8]
0x4cbec3c	487d02f0	adrp x8,0x9c69000
0x4cbec40	08012491	add x8,x8,#0x900
0x4cbec44	080000f9	str x8,[x0]
0x4cbec48	15600091	add x21,x0,#0x18
0x4cbec4c	e00315aa	mov x0,x21
0x4cbec50	01fe8052	mov w1,#0x7f0
0x4cbec54	cf059294	bl 0x07140390
0x4cbec58	e00315aa	mov x0,x21
0x4cbec5c	9a60f896	bl 0x00ad6ec4
0x4cbec60	751201f9	str x21,[x19, #0x220]
0x4cbec64	751641f9	ldr x21,[x19, #0x228]
0x4cbec68	741601f9	str x20,[x19, #0x228]
0x4cbec6c	f5faffb4	cbz x21,0x04cbebc8
0x4cbec70	a8220091	add x8,x21,#0x8
0x4cbec74	09008092	mov x9,#-0x1
0x4cbec78	0801e9f8	ldaddal x9,x8,[x8]
0x4cbec7c	68faffb5	cbnz x8,0x04cbebc8
0x4cbec80	a80240f9	ldr x8,[x21]
0x4cbec84	080940f9	ldr x8,[x8, #0x10]
0x4cbec88	e00315aa	mov x0,x21
0x4cbec8c	00013fd6	blr x8
0x4cbec90	e00315aa	mov x0,x21
0x4cbec94	fd7b44a9	ldp x29,x30,[sp, #0x40]
0x4cbec98	f44f43a9	ldp x20,x19,[sp, #0x30]
0x4cbec9c	f65742a9	ldp x22,x21,[sp, #0x20]
0x4cbeca0	ff430191	add sp,sp,#0x50
0x4cbeca4	de039214	b 0x0713fc1c
0x4cbeca8	e00313aa	mov x0,x19
0x4cbecac	88a8f597	bl 0x04a28ecc
0x4cbecb0	a0000034	cbz w0,0x04cbecc4
0x4cbecb4	e8030091	mov x8,sp
0x4cbecb8	e07f0091	add x0,sp,#0x1f
0x4cbecbc	2d110094	bl 0x04cc3170
0x4cbecc0	0a000014	b 0x04cbece8
0x4cbecc4	e00313aa	mov x0,x19
0x4cbecc8	88a7f597	bl 0x04a28ae8
0x4cbeccc	80000037	tbnz w0,#0x0,0x04cbecdc
0x4cbecd0	e00313aa	mov x0,x19
0x4cbecd4	1eb4f597	bl 0x04a2bd4c
0x4cbecd8	00040034	cbz w0,0x04cbed58
0x4cbecdc	e8030091	mov x8,sp
0x4cbece0	e07f0091	add x0,sp,#0x1f
0x4cbece4	7e110094	bl 0x04cc32dc
0x4cbece8	e003c03d	ldr q0,[sp]
0x4cbecec	ff7f00a9	stp xzr,xzr,[sp]
0x4cbecf0	741641f9	ldr x20,[x19, #0x228]
0x4cbecf4	608a803d	str q0,[x19, #0x220]
0x4cbecf8	740100b4	cbz x20,0x04cbed24
0x4cbecfc	88220091	add x8,x20,#0x8
0x4cbed00	09008092	mov x9,#-0x1
0x4cbed04	0801e9f8	ldaddal x9,x8,[x8]
0x4cbed08	e80000b5	cbnz x8,0x04cbed24
0x4cbed0c	880240f9	ldr x8,[x20]
0x4cbed10	080940f9	ldr x8,[x8, #0x10]
0x4cbed14	e00314aa	mov x0,x20
0x4cbed18	00013fd6	blr x8
0x4cbed1c	e00314aa	mov x0,x20
0x4cbed20	bf039294	bl 0x0713fc1c
0x4cbed24	f30740f9	ldr x19,[sp, #0x8]
0x4cbed28	13f5ffb4	cbz x19,0x04cbebc8
0x4cbed2c	68220091	add x8,x19,#0x8
0x4cbed30	09008092	mov x9,#-0x1
0x4cbed34	0801e9f8	ldaddal x9,x8,[x8]
0x4cbed38	88f4ffb5	cbnz x8,0x04cbebc8
0x4cbed3c	680240f9	ldr x8,[x19]
0x4cbed40	080940f9	ldr x8,[x8, #0x10]
0x4cbed44	e00313aa	mov x0,x19
0x4cbed48	00013fd6	blr x8
0x4cbed4c	e00313aa	mov x0,x19
0x4cbed50	b3039294	bl 0x0713fc1c
0x4cbed54	9dffff17	b 0x04cbebc8
0x4cbed58	e00313aa	mov x0,x19
0x4cbed5c	72a8f597	bl 0x04a28f24
0x4cbed60	40010034	cbz w0,0x04cbed88
0x4cbed64	e8030091	mov x8,sp
0x4cbed68	e07f0091	add x0,sp,#0x1f
0x4cbed6c	c0110094	bl 0x04cc346c
0x4cbed70	60820891	add x0,x19,#0x220
0x4cbed74	e1030091	mov x1,sp
0x4cbed78	5599d696	bl 0x002652cc
0x4cbed7c	e0030091	mov x0,sp
0x4cbed80	7aacd196	bl 0x00129f68
0x4cbed84	91ffff17	b 0x04cbebc8
0x4cbed88	e00313aa	mov x0,x19
0x4cbed8c	47a8f597	bl 0x04a28ea8
0x4cbed90	20010034	cbz w0,0x04cbedb4
0x4cbed94	e8030091	mov x8,sp
0x4cbed98	56000094	bl 0x04cbeef0
0x4cbed9c	60820891	add x0,x19,#0x220
0x4cbeda0	e1030091	mov x1,sp
0x4cbeda4	4a99d696	bl 0x002652cc
0x4cbeda8	e0030091	mov x0,sp
0x4cbedac	6facd196	bl 0x00129f68
0x4cbedb0	86ffff17	b 0x04cbebc8
0x4cbedb4	e00313aa	mov x0,x19
0x4cbedb8	47a9f597	bl 0x04a292d4
0x4cbedbc	40010034	cbz w0,0x04cbede4
0x4cbedc0	e8030091	mov x8,sp
0x4cbedc4	e07f0091	add x0,sp,#0x1f
0x4cbedc8	410d0094	bl 0x04cc22cc
0x4cbedcc	60820891	add x0,x19,#0x220
0x4cbedd0	e1030091	mov x1,sp
0x4cbedd4	3e99d696	bl 0x002652cc
0x4cbedd8	e0030091	mov x0,sp
0x4cbeddc	63acd196	bl 0x00129f68
0x4cbede0	7affff17	b 0x04cbebc8
0x4cbede4	e00313aa	mov x0,x19
0x4cbede8	37a9f597	bl 0x04a292c4
0x4cbedec	20010034	cbz w0,0x04cbee10
0x4cbedf0	e8030091	mov x8,sp
0x4cbedf4	53000094	bl 0x04cbef40
0x4cbedf8	60820891	add x0,x19,#0x220
0x4cbedfc	e1030091	mov x1,sp
0x4cbee00	3399d696	bl 0x002652cc
0x4cbee04	e0030091	mov x0,sp
0x4cbee08	58acd196	bl 0x00129f68
0x4cbee0c	6fffff17	b 0x04cbebc8
0x4cbee10	e00313aa	mov x0,x19
0x4cbee14	12aaf597	bl 0x04a2965c
0x4cbee18	20010034	cbz w0,0x04cbee3c
0x4cbee1c	e8030091	mov x8,sp
0x4cbee20	8a000094	bl 0x04cbf048
0x4cbee24	60820891	add x0,x19,#0x220
0x4cbee28	e1030091	mov x1,sp
0x4cbee2c	2899d696	bl 0x002652cc
0x4cbee30	e0030091	mov x0,sp
0x4cbee34	4dacd196	bl 0x00129f68
0x4cbee38	64ffff17	b 0x04cbebc8
0x4cbee3c	e00313aa	mov x0,x19
0x4cbee40	29a9f597	bl 0x04a292e4
0x4cbee44	20010034	cbz w0,0x04cbee68
0x4cbee48	e8030091	mov x8,sp
0x4cbee4c	c9000094	bl 0x04cbf170
0x4cbee50	60820891	add x0,x19,#0x220
0x4cbee54	e1030091	mov x1,sp
0x4cbee58	1d99d696	bl 0x002652cc
0x4cbee5c	e0030091	mov x0,sp
0x4cbee60	42acd196	bl 0x00129f68
0x4cbee64	59ffff17	b 0x04cbebc8
0x4cbee68	e00313aa	mov x0,x19
0x4cbee6c	f8a9f597	bl 0x04a2964c
0x4cbee70	e8030091	mov x8,sp
0x4cbee74	00010034	cbz w0,0x04cbee94
0x4cbee78	08010094	bl 0x04cbf298
0x4cbee7c	60820891	add x0,x19,#0x220
0x4cbee80	e1030091	mov x1,sp
0x4cbee84	1299d696	bl 0x002652cc
0x4cbee88	e0030091	mov x0,sp
0x4cbee8c	37acd196	bl 0x00129f68
0x4cbee90	4effff17	b 0x04cbebc8
0x4cbee94	4b010094	bl 0x04cbf3c0
0x4cbee98	60820891	add x0,x19,#0x220
0x4cbee9c	e1030091	mov x1,sp
0x4cbeea0	0b99d696	bl 0x002652cc
0x4cbeea4	e0030091	mov x0,sp
0x4cbeea8	30acd196	bl 0x00129f68
0x4cbeeac	47ffff17	b 0x04cbebc8
