// Ghidra inferred pseudocode; requested=0x564f98c
// entry=0564f98c end=056506a3

void FUN_0564f98c(long param_1,long param_2)

{
  long *plVar1;
  undefined8 uVar2;
  code *pcVar3;
  undefined **ppuVar4;
  long lVar5;
  long *plVar6;
  long lVar7;
  undefined **local_68;
  long lStack_60;
  undefined ***local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  *(long *)(param_1 + 0x18) = param_2;
  plVar6 = *(long **)(param_2 + 8);
  if ((code *)**(undefined8 **)(param_1 + 0x10) != (code *)0x0) {
    (*(code *)**(undefined8 **)(param_1 + 0x10))(*(undefined8 *)(param_1 + 8));
  }
  lVar5 = *(long *)(param_1 + 8);
  plVar1 = (long *)plVar6[3];
  if (plVar1 == (long *)0x0) {
    *(undefined8 *)(lVar5 + 0x18) = 0;
  }
  else if (plVar1 == plVar6) {
    *(long *)(lVar5 + 0x18) = lVar5;
    (**(code **)(*(long *)plVar6[3] + 0x18))((long *)plVar6[3],lVar5);
  }
  else {
    uVar2 = (**(code **)(*plVar1 + 0x10))();
    *(undefined8 *)(lVar5 + 0x18) = uVar2;
  }
  **(undefined8 **)(param_1 + 0x10) = FUN_05655e10;
  local_68 = &PTR_FUN_09f197e0;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  lStack_60 = param_1;
  if ((code *)**(undefined8 **)(param_2 + 0x10) == (code *)0x0) {
LAB_0564fa84:
    *(long *)(lVar5 + 0x18) = lVar5;
    (*(code *)(*local_50)[3])(local_50,lVar5);
  }
  else {
    (*(code *)**(undefined8 **)(param_2 + 0x10))(lVar5);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      if (local_50 == &local_68) goto LAB_0564fa84;
      uVar2 = (*(code *)(*local_50)[2])();
    }
    *(undefined8 *)(lVar5 + 0x18) = uVar2;
  }
  **(undefined8 **)(param_2 + 0x10) = FUN_05655e10;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0564facc:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0564facc;
  }
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_1 + 0x10) + 8);
  if (pcVar3 != (code *)0x0) {
    (*pcVar3)(*(long *)(param_1 + 8) + 0x20);
  }
  lVar7 = *(long *)(param_1 + 8);
  plVar6 = *(long **)(lVar5 + 0x38);
  if (plVar6 == (long *)0x0) {
    *(undefined8 *)(lVar7 + 0x38) = 0;
  }
  else if (plVar6 == (long *)(lVar5 + 0x20)) {
    *(long *)(lVar7 + 0x38) = lVar7 + 0x20;
    (**(code **)(**(long **)(lVar5 + 0x38) + 0x18))();
  }
  else {
    uVar2 = (**(code **)(*plVar6 + 0x10))();
    *(undefined8 *)(lVar7 + 0x38) = uVar2;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 8) = FUN_0564f3c4;
  ppuVar4 = &PTR_FUN_09f19870;
  local_68 = &PTR_FUN_09f19870;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 8);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0564fb9c:
    *(long *)(lVar5 + 0x38) = lVar5 + 0x20;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x20);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0564fb9c;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x38) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 8) = FUN_0564f3c4;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0564fbdc:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0564fbdc;
  }
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_1 + 0x10) + 0x10);
  if (pcVar3 != (code *)0x0) {
    (*pcVar3)(*(long *)(param_1 + 8) + 0x40);
  }
  lVar7 = *(long *)(param_1 + 8);
  plVar6 = *(long **)(lVar5 + 0x58);
  if (plVar6 == (long *)0x0) {
    *(undefined8 *)(lVar7 + 0x58) = 0;
  }
  else if (plVar6 == (long *)(lVar5 + 0x40)) {
    *(long *)(lVar7 + 0x58) = lVar7 + 0x40;
    (**(code **)(**(long **)(lVar5 + 0x58) + 0x18))();
  }
  else {
    uVar2 = (**(code **)(*plVar6 + 0x10))();
    *(undefined8 *)(lVar7 + 0x58) = uVar2;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x10) = FUN_0564f264;
  ppuVar4 = &PTR_FUN_09f198f0;
  local_68 = &PTR_FUN_09f198f0;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x10);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0564fcac:
    *(long *)(lVar5 + 0x58) = lVar5 + 0x40;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x40);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0564fcac;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x58) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x10) = FUN_0564f264;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0564fcec:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0564fcec;
  }
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_1 + 0x10) + 0x18);
  if (pcVar3 != (code *)0x0) {
    (*pcVar3)(*(long *)(param_1 + 8) + 0x60);
  }
  lVar7 = *(long *)(param_1 + 8);
  plVar6 = *(long **)(lVar5 + 0x78);
  if (plVar6 == (long *)0x0) {
    *(undefined8 *)(lVar7 + 0x78) = 0;
  }
  else if (plVar6 == (long *)(lVar5 + 0x60)) {
    *(long *)(lVar7 + 0x78) = lVar7 + 0x60;
    (**(code **)(**(long **)(lVar5 + 0x78) + 0x18))();
  }
  else {
    uVar2 = (**(code **)(*plVar6 + 0x10))();
    *(undefined8 *)(lVar7 + 0x78) = uVar2;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x18) = FUN_0564f3c4;
  ppuVar4 = &PTR_FUN_09f19970;
  local_68 = &PTR_FUN_09f19970;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x18);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0564fdb4:
    *(long *)(lVar5 + 0x78) = lVar5 + 0x60;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x60);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0564fdb4;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x78) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x18) = FUN_0564f3c4;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0564fdf4:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0564fdf4;
  }
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_1 + 0x10) + 0x20);
  if (pcVar3 != (code *)0x0) {
    (*pcVar3)(*(long *)(param_1 + 8) + 0x80);
  }
  lVar7 = *(long *)(param_1 + 8);
  plVar6 = *(long **)(lVar5 + 0x98);
  if (plVar6 == (long *)0x0) {
    *(undefined8 *)(lVar7 + 0x98) = 0;
  }
  else if (plVar6 == (long *)(lVar5 + 0x80)) {
    *(long *)(lVar7 + 0x98) = lVar7 + 0x80;
    (**(code **)(**(long **)(lVar5 + 0x98) + 0x18))();
  }
  else {
    uVar2 = (**(code **)(*plVar6 + 0x10))();
    *(undefined8 *)(lVar7 + 0x98) = uVar2;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x20) = FUN_0564f3c4;
  ppuVar4 = &PTR_FUN_09f199f0;
  local_68 = &PTR_FUN_09f199f0;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x20);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0564febc:
    *(long *)(lVar5 + 0x98) = lVar5 + 0x80;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x80);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0564febc;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x98) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x20) = FUN_0564f3c4;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0564fefc:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0564fefc;
  }
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_1 + 0x10) + 0x28);
  if (pcVar3 != (code *)0x0) {
    (*pcVar3)(*(long *)(param_1 + 8) + 0xa0);
  }
  lVar7 = *(long *)(param_1 + 8);
  plVar6 = *(long **)(lVar5 + 0xb8);
  if (plVar6 == (long *)0x0) {
    *(undefined8 *)(lVar7 + 0xb8) = 0;
  }
  else if (plVar6 == (long *)(lVar5 + 0xa0)) {
    *(long *)(lVar7 + 0xb8) = lVar7 + 0xa0;
    (**(code **)(**(long **)(lVar5 + 0xb8) + 0x18))();
  }
  else {
    uVar2 = (**(code **)(*plVar6 + 0x10))();
    *(undefined8 *)(lVar7 + 0xb8) = uVar2;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x28) = FUN_05656418;
  ppuVar4 = &PTR_FUN_09f19a70;
  local_68 = &PTR_FUN_09f19a70;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x28);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0564ffcc:
    *(long *)(lVar5 + 0xb8) = lVar5 + 0xa0;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0xa0);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0564ffcc;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0xb8) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x28) = FUN_05656418;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0565000c:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0565000c;
  }
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_1 + 0x10) + 0x30);
  if (pcVar3 != (code *)0x0) {
    (*pcVar3)(*(long *)(param_1 + 8) + 0xc0);
  }
  lVar7 = *(long *)(param_1 + 8);
  plVar6 = *(long **)(lVar5 + 0xd8);
  if (plVar6 == (long *)0x0) {
    *(undefined8 *)(lVar7 + 0xd8) = 0;
  }
  else if (plVar6 == (long *)(lVar5 + 0xc0)) {
    *(long *)(lVar7 + 0xd8) = lVar7 + 0xc0;
    (**(code **)(**(long **)(lVar5 + 0xd8) + 0x18))();
  }
  else {
    uVar2 = (**(code **)(*plVar6 + 0x10))();
    *(undefined8 *)(lVar7 + 0xd8) = uVar2;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x30) = FUN_05656534;
  ppuVar4 = &PTR_FUN_09f19b00;
  local_68 = &PTR_FUN_09f19b00;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x30);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_056500dc:
    *(long *)(lVar5 + 0xd8) = lVar5 + 0xc0;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0xc0);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_056500dc;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0xd8) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x30) = FUN_05656534;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0565011c:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0565011c;
  }
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_1 + 0x10) + 0x38);
  if (pcVar3 != (code *)0x0) {
    (*pcVar3)(*(long *)(param_1 + 8) + 0xe0);
  }
  lVar7 = *(long *)(param_1 + 8);
  plVar6 = *(long **)(lVar5 + 0xf8);
  if (plVar6 == (long *)0x0) {
    *(undefined8 *)(lVar7 + 0xf8) = 0;
  }
  else if (plVar6 == (long *)(lVar5 + 0xe0)) {
    *(long *)(lVar7 + 0xf8) = lVar7 + 0xe0;
    (**(code **)(**(long **)(lVar5 + 0xf8) + 0x18))();
  }
  else {
    uVar2 = (**(code **)(*plVar6 + 0x10))();
    *(undefined8 *)(lVar7 + 0xf8) = uVar2;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x38) = FUN_05656650;
  ppuVar4 = &PTR_FUN_09f19b90;
  local_68 = &PTR_FUN_09f19b90;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x38);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_056501ec:
    *(long *)(lVar5 + 0xf8) = lVar5 + 0xe0;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0xe0);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_056501ec;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0xf8) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x38) = FUN_05656650;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0565022c:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0565022c;
  }
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_1 + 0x10) + 0x40);
  if (pcVar3 != (code *)0x0) {
    (*pcVar3)(*(long *)(param_1 + 8) + 0x100);
  }
  lVar7 = *(long *)(param_1 + 8);
  plVar6 = *(long **)(lVar5 + 0x118);
  if (plVar6 == (long *)0x0) {
    *(undefined8 *)(lVar7 + 0x118) = 0;
  }
  else if (plVar6 == (long *)(lVar5 + 0x100)) {
    *(long *)(lVar7 + 0x118) = lVar7 + 0x100;
    (**(code **)(**(long **)(lVar5 + 0x118) + 0x18))();
  }
  else {
    uVar2 = (**(code **)(*plVar6 + 0x10))();
    *(undefined8 *)(lVar7 + 0x118) = uVar2;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x40) = FUN_0565676c;
  ppuVar4 = &PTR_FUN_09f19c20;
  local_68 = &PTR_FUN_09f19c20;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x40);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_056502fc:
    *(long *)(lVar5 + 0x118) = lVar5 + 0x100;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x100);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_056502fc;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x118) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x40) = FUN_0565676c;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0565033c:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0565033c;
  }
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_1 + 0x10) + 0x48);
  if (pcVar3 != (code *)0x0) {
    (*pcVar3)(*(long *)(param_1 + 8) + 0x120);
  }
  lVar7 = *(long *)(param_1 + 8);
  plVar6 = *(long **)(lVar5 + 0x138);
  if (plVar6 == (long *)0x0) {
    *(undefined8 *)(lVar7 + 0x138) = 0;
  }
  else if (plVar6 == (long *)(lVar5 + 0x120)) {
    *(long *)(lVar7 + 0x138) = lVar7 + 0x120;
    (**(code **)(**(long **)(lVar5 + 0x138) + 0x18))();
  }
  else {
    uVar2 = (**(code **)(*plVar6 + 0x10))();
    *(undefined8 *)(lVar7 + 0x138) = uVar2;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x48) = FUN_05656890;
  ppuVar4 = &PTR_FUN_09f19cb0;
  local_68 = &PTR_FUN_09f19cb0;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x48);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0565040c:
    *(long *)(lVar5 + 0x138) = lVar5 + 0x120;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x120);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0565040c;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x138) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x48) = FUN_05656890;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0565044c:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0565044c;
  }
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_1 + 0x10) + 0x50);
  if (pcVar3 != (code *)0x0) {
    (*pcVar3)(*(long *)(param_1 + 8) + 0x140);
  }
  lVar7 = *(long *)(param_1 + 8);
  plVar6 = *(long **)(lVar5 + 0x158);
  if (plVar6 == (long *)0x0) {
    *(undefined8 *)(lVar7 + 0x158) = 0;
  }
  else if (plVar6 == (long *)(lVar5 + 0x140)) {
    *(long *)(lVar7 + 0x158) = lVar7 + 0x140;
    (**(code **)(**(long **)(lVar5 + 0x158) + 0x18))();
  }
  else {
    uVar2 = (**(code **)(*plVar6 + 0x10))();
    *(undefined8 *)(lVar7 + 0x158) = uVar2;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x50) = FUN_056569ac;
  ppuVar4 = &PTR_FUN_09f19d40;
  local_68 = &PTR_FUN_09f19d40;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x50);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0565051c:
    *(long *)(lVar5 + 0x158) = lVar5 + 0x140;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x140);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0565051c;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x158) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x50) = FUN_056569ac;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0565055c:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0565055c;
  }
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_1 + 0x10) + 0x58);
  if (pcVar3 != (code *)0x0) {
    (*pcVar3)(*(long *)(param_1 + 8) + 0x160);
  }
  lVar7 = *(long *)(param_1 + 8);
  plVar6 = *(long **)(lVar5 + 0x178);
  if (plVar6 == (long *)0x0) {
    *(undefined8 *)(lVar7 + 0x178) = 0;
  }
  else if (plVar6 == (long *)(lVar5 + 0x160)) {
    *(long *)(lVar7 + 0x178) = lVar7 + 0x160;
    (**(code **)(**(long **)(lVar5 + 0x178) + 0x18))();
  }
  else {
    uVar2 = (**(code **)(*plVar6 + 0x10))();
    *(undefined8 *)(lVar7 + 0x178) = uVar2;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x58) = FUN_05656ac8;
  ppuVar4 = &PTR_FUN_09f19dc0;
  local_68 = &PTR_FUN_09f19dc0;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x58);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0565062c:
    *(long *)(lVar5 + 0x178) = lVar5 + 0x160;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x160);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0565062c;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x178) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x58) = FUN_05656ac8;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
  }
  else {
    if (local_50 == (undefined ***)0x0) goto LAB_05650670;
    pcVar3 = (code *)(*local_50)[5];
  }
  (*pcVar3)();
LAB_05650670:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


