// Ghidra inferred pseudocode; requested=0x567f2a8
// entry=0567f2a8 end=0567ffbf

void FUN_0567f2a8(long param_1,long param_2)

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
  local_68 = &PTR_FUN_09f1b748;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  lStack_60 = param_1;
  if ((code *)**(undefined8 **)(param_2 + 0x10) == (code *)0x0) {
LAB_0567f3a0:
    *(long *)(lVar5 + 0x18) = lVar5;
    (*(code *)(*local_50)[3])(local_50,lVar5);
  }
  else {
    (*(code *)**(undefined8 **)(param_2 + 0x10))(lVar5);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      if (local_50 == &local_68) goto LAB_0567f3a0;
      uVar2 = (*(code *)(*local_50)[2])();
    }
    *(undefined8 *)(lVar5 + 0x18) = uVar2;
  }
  **(undefined8 **)(param_2 + 0x10) = FUN_05655e10;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567f3e8:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567f3e8;
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
  ppuVar4 = &PTR_FUN_09f1b7c8;
  local_68 = &PTR_FUN_09f1b7c8;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 8);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567f4b8:
    *(long *)(lVar5 + 0x38) = lVar5 + 0x20;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x20);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567f4b8;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x38) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 8) = FUN_0564f3c4;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567f4f8:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567f4f8;
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
  ppuVar4 = &PTR_FUN_09f1b848;
  local_68 = &PTR_FUN_09f1b848;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x10);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567f5c8:
    *(long *)(lVar5 + 0x58) = lVar5 + 0x40;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x40);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567f5c8;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x58) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x10) = FUN_0564f264;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567f608:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567f608;
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
  ppuVar4 = &PTR_FUN_09f1b8c8;
  local_68 = &PTR_FUN_09f1b8c8;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x18);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567f6d0:
    *(long *)(lVar5 + 0x78) = lVar5 + 0x60;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x60);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567f6d0;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x78) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x18) = FUN_0564f3c4;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567f710:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567f710;
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
  ppuVar4 = &PTR_FUN_09f1b948;
  local_68 = &PTR_FUN_09f1b948;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x20);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567f7d8:
    *(long *)(lVar5 + 0x98) = lVar5 + 0x80;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x80);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567f7d8;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x98) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x20) = FUN_0564f3c4;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567f818:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567f818;
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
  ppuVar4 = &PTR_FUN_09f1b9c8;
  local_68 = &PTR_FUN_09f1b9c8;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x28);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567f8e8:
    *(long *)(lVar5 + 0xb8) = lVar5 + 0xa0;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0xa0);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567f8e8;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0xb8) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x28) = FUN_05656418;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567f928:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567f928;
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
  ppuVar4 = &PTR_FUN_09f1ba48;
  local_68 = &PTR_FUN_09f1ba48;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x30);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567f9f8:
    *(long *)(lVar5 + 0xd8) = lVar5 + 0xc0;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0xc0);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567f9f8;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0xd8) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x30) = FUN_05656534;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567fa38:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567fa38;
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
  ppuVar4 = &PTR_FUN_09f1bac8;
  local_68 = &PTR_FUN_09f1bac8;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x38);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567fb08:
    *(long *)(lVar5 + 0xf8) = lVar5 + 0xe0;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0xe0);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567fb08;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0xf8) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x38) = FUN_05656650;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567fb48:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567fb48;
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
  ppuVar4 = &PTR_FUN_09f1bb48;
  local_68 = &PTR_FUN_09f1bb48;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x40);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567fc18:
    *(long *)(lVar5 + 0x118) = lVar5 + 0x100;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x100);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567fc18;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x118) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x40) = FUN_0565676c;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567fc58:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567fc58;
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
  ppuVar4 = &PTR_FUN_09f1bbc8;
  local_68 = &PTR_FUN_09f1bbc8;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x48);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567fd28:
    *(long *)(lVar5 + 0x138) = lVar5 + 0x120;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x120);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567fd28;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x138) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x48) = FUN_05656890;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567fd68:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567fd68;
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
  ppuVar4 = &PTR_FUN_09f1bc48;
  local_68 = &PTR_FUN_09f1bc48;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x50);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567fe38:
    *(long *)(lVar5 + 0x158) = lVar5 + 0x140;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x140);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567fe38;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x158) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x50) = FUN_056569ac;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567fe78:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567fe78;
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
  ppuVar4 = &PTR_FUN_09f1bcc8;
  local_68 = &PTR_FUN_09f1bcc8;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x58);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567ff48:
    *(long *)(lVar5 + 0x178) = lVar5 + 0x160;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x160);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567ff48;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x178) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x58) = FUN_05656ac8;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
  }
  else {
    if (local_50 == (undefined ***)0x0) goto LAB_0567ff8c;
    pcVar3 = (code *)(*local_50)[5];
  }
  (*pcVar3)();
LAB_0567ff8c:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


