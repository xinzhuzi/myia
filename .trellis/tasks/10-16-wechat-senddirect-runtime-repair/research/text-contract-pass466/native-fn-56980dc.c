// Ghidra inferred pseudocode; requested=0x56980dc
// entry=056980dc end=056984f3

void FUN_056980dc(long param_1)

{
  undefined8 uVar1;
  code *pcVar2;
  undefined **ppuVar3;
  long lVar4;
  undefined **local_58;
  long lStack_50;
  undefined ***local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_58 = &PTR_FUN_09f1c8c0;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 8);
  lStack_50 = param_1;
  if ((code *)**(undefined8 **)(param_1 + 0x10) == (code *)0x0) {
LAB_05698158:
    *(long *)(lVar4 + 0x18) = lVar4;
    (*(code *)(*local_40)[3])(local_40,lVar4);
  }
  else {
    (*(code *)**(undefined8 **)(param_1 + 0x10))(lVar4);
    lVar4 = *(long *)(param_1 + 8);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      if (local_40 == &local_58) goto LAB_05698158;
      uVar1 = (*(code *)(*local_40)[2])();
    }
    *(undefined8 *)(lVar4 + 0x18) = uVar1;
  }
  **(undefined8 **)(param_1 + 0x10) = FUN_0567e4f0;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_056981a8:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_056981a8;
  }
  ppuVar3 = &PTR_FUN_09f1c940;
  local_58 = &PTR_FUN_09f1c940;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 8);
  pcVar2 = *(code **)(*(long *)(param_1 + 0x10) + 8);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_05698200:
    *(long *)(lVar4 + 0x38) = lVar4 + 0x20;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0x20);
    lVar4 = *(long *)(param_1 + 8);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_05698200;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0x38) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 8) = FUN_0567e608;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_05698248:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_05698248;
  }
  ppuVar3 = &PTR_FUN_09f1c9c0;
  local_58 = &PTR_FUN_09f1c9c0;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 8);
  pcVar2 = *(code **)(*(long *)(param_1 + 0x10) + 0x10);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_056982a0:
    *(long *)(lVar4 + 0x58) = lVar4 + 0x40;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0x40);
    lVar4 = *(long *)(param_1 + 8);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_056982a0;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0x58) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x10) = FUN_0564f264;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_056982e8:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_056982e8;
  }
  ppuVar3 = &PTR_FUN_09f1ca40;
  local_58 = &PTR_FUN_09f1ca40;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 8);
  pcVar2 = *(code **)(*(long *)(param_1 + 0x10) + 0x18);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_05698340:
    *(long *)(lVar4 + 0x78) = lVar4 + 0x60;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0x60);
    lVar4 = *(long *)(param_1 + 8);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_05698340;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0x78) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x18) = FUN_0564f3c4;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_05698388:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_05698388;
  }
  ppuVar3 = &PTR_FUN_09f1cac0;
  local_58 = &PTR_FUN_09f1cac0;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 8);
  pcVar2 = *(code **)(*(long *)(param_1 + 0x10) + 0x20);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_056983e0:
    *(long *)(lVar4 + 0x98) = lVar4 + 0x80;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0x80);
    lVar4 = *(long *)(param_1 + 8);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_056983e0;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0x98) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x20) = FUN_0564f14c;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_05698428:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_05698428;
  }
  ppuVar3 = &PTR_FUN_09f1cb40;
  local_58 = &PTR_FUN_09f1cb40;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 8);
  pcVar2 = *(code **)(*(long *)(param_1 + 0x10) + 0x28);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_05698480:
    *(long *)(lVar4 + 0xb8) = lVar4 + 0xa0;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0xa0);
    lVar4 = *(long *)(param_1 + 8);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_05698480;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0xb8) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x28) = FUN_0564f3c4;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
  }
  else {
    if (local_40 == (undefined ***)0x0) goto LAB_056984c4;
    pcVar2 = (code *)(*local_40)[5];
  }
  (*pcVar2)();
LAB_056984c4:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


