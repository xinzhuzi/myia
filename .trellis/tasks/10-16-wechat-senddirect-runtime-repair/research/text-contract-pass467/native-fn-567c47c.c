// Ghidra inferred pseudocode; requested=0x567c47c
// entry=0567c47c end=0567cb3b

void FUN_0567c47c(long param_1,long param_2)

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
  **(undefined8 **)(param_1 + 0x10) = FUN_0567e4f0;
  local_68 = &PTR_FUN_09f1b2b8;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  lStack_60 = param_1;
  if ((code *)**(undefined8 **)(param_2 + 0x10) == (code *)0x0) {
LAB_0567c574:
    *(long *)(lVar5 + 0x18) = lVar5;
    (*(code *)(*local_50)[3])(local_50,lVar5);
  }
  else {
    (*(code *)**(undefined8 **)(param_2 + 0x10))(lVar5);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      if (local_50 == &local_68) goto LAB_0567c574;
      uVar2 = (*(code *)(*local_50)[2])();
    }
    *(undefined8 *)(lVar5 + 0x18) = uVar2;
  }
  **(undefined8 **)(param_2 + 0x10) = FUN_0567e4f0;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567c5bc:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567c5bc;
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
  *(code **)(*(long *)(param_1 + 0x10) + 8) = FUN_0567e608;
  ppuVar4 = &PTR_FUN_09f1b348;
  local_68 = &PTR_FUN_09f1b348;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 8);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567c68c:
    *(long *)(lVar5 + 0x38) = lVar5 + 0x20;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x20);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567c68c;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x38) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 8) = FUN_0567e608;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567c6cc:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567c6cc;
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
  ppuVar4 = &PTR_FUN_09f1b3d8;
  local_68 = &PTR_FUN_09f1b3d8;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x10);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567c79c:
    *(long *)(lVar5 + 0x58) = lVar5 + 0x40;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x40);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567c79c;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x58) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x10) = FUN_0564f264;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567c7dc:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567c7dc;
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
  ppuVar4 = &PTR_FUN_09f1b458;
  local_68 = &PTR_FUN_09f1b458;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x18);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567c8ac:
    *(long *)(lVar5 + 0x78) = lVar5 + 0x60;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x60);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567c8ac;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x78) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x18) = FUN_0564f3c4;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567c8ec:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567c8ec;
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
  *(code **)(*(long *)(param_1 + 0x10) + 0x20) = FUN_0564f14c;
  ppuVar4 = &PTR_FUN_09f1b4d8;
  local_68 = &PTR_FUN_09f1b4d8;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x20);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567c9bc:
    *(long *)(lVar5 + 0x98) = lVar5 + 0x80;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x80);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567c9bc;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x98) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x20) = FUN_0564f14c;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
LAB_0567c9fc:
    (*pcVar3)();
  }
  else if (local_50 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_50)[5];
    goto LAB_0567c9fc;
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
  *(code **)(*(long *)(param_1 + 0x10) + 0x28) = FUN_0564f3c4;
  ppuVar4 = &PTR_FUN_09f1b558;
  local_68 = &PTR_FUN_09f1b558;
  local_50 = &local_68;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x28);
  lStack_60 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0567cac4:
    *(long *)(lVar5 + 0xb8) = lVar5 + 0xa0;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0xa0);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_50 != (undefined ***)0x0) {
      ppuVar4 = *local_50;
      if (local_50 == &local_68) goto LAB_0567cac4;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0xb8) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x28) = FUN_0564f3c4;
  if (local_50 == &local_68) {
    pcVar3 = (code *)(*local_50)[4];
  }
  else {
    if (local_50 == (undefined ***)0x0) goto LAB_0567cb08;
    pcVar3 = (code *)(*local_50)[5];
  }
  (*pcVar3)();
LAB_0567cb08:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


