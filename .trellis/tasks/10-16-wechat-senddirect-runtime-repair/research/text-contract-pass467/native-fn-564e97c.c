// Ghidra inferred pseudocode; requested=0x564e97c
// entry=0564e97c end=0564ed23

void FUN_0564e97c(long param_1,long param_2)

{
  long *plVar1;
  undefined8 uVar2;
  code *pcVar3;
  undefined **ppuVar4;
  long lVar5;
  long lVar6;
  undefined **local_58;
  long lStack_50;
  undefined ***local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  *(long *)(param_1 + 0x18) = param_2;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_1 + 0x10) + 0x20);
  if (pcVar3 != (code *)0x0) {
    (*pcVar3)(*(long *)(param_1 + 8) + 0x80);
  }
  lVar6 = *(long *)(param_1 + 8);
  plVar1 = *(long **)(lVar5 + 0x98);
  if (plVar1 == (long *)0x0) {
    *(undefined8 *)(lVar6 + 0x98) = 0;
  }
  else if (plVar1 == (long *)(lVar5 + 0x80)) {
    *(long *)(lVar6 + 0x98) = lVar6 + 0x80;
    (**(code **)(**(long **)(lVar5 + 0x98) + 0x18))();
  }
  else {
    uVar2 = (**(code **)(*plVar1 + 0x10))();
    *(undefined8 *)(lVar6 + 0x98) = uVar2;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x20) = FUN_0564f14c;
  local_58 = &PTR_FUN_09f19508;
  lStack_50 = param_1;
  local_40 = &local_58;
  lVar6 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x20);
  lVar5 = lVar6 + 0x80;
  if (pcVar3 == (code *)0x0) {
LAB_0564ea90:
    *(long *)(lVar6 + 0x98) = lVar5;
    (*(code *)(*local_40)[3])();
LAB_0564eaa0:
    *(code **)(*(long *)(param_2 + 0x10) + 0x20) = FUN_0564f14c;
    if (local_40 == &local_58) {
      pcVar3 = (code *)(*local_40)[4];
    }
    else {
      if (local_40 == (undefined ***)0x0) goto LAB_0564ead4;
      pcVar3 = (code *)(*local_40)[5];
    }
    (*pcVar3)();
  }
  else {
    (*pcVar3)(lVar5);
    lVar6 = *(long *)(param_2 + 8);
    if (local_40 != (undefined ***)0x0) {
      if (local_40 == &local_58) {
        lVar5 = lVar6 + 0x80;
        goto LAB_0564ea90;
      }
      uVar2 = (*(code *)(*local_40)[2])();
      *(undefined8 *)(lVar6 + 0x98) = uVar2;
      goto LAB_0564eaa0;
    }
    *(undefined8 *)(lVar6 + 0x98) = 0;
    *(code **)(*(long *)(param_2 + 0x10) + 0x20) = FUN_0564f14c;
  }
LAB_0564ead4:
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_1 + 0x10) + 0x10);
  if (pcVar3 != (code *)0x0) {
    (*pcVar3)(*(long *)(param_1 + 8) + 0x40);
  }
  lVar6 = *(long *)(param_1 + 8);
  plVar1 = *(long **)(lVar5 + 0x58);
  if (plVar1 == (long *)0x0) {
    *(undefined8 *)(lVar6 + 0x58) = 0;
  }
  else if (plVar1 == (long *)(lVar5 + 0x40)) {
    *(long *)(lVar6 + 0x58) = lVar6 + 0x40;
    (**(code **)(**(long **)(lVar5 + 0x58) + 0x18))();
  }
  else {
    uVar2 = (**(code **)(*plVar1 + 0x10))();
    *(undefined8 *)(lVar6 + 0x58) = uVar2;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x10) = FUN_0564f264;
  ppuVar4 = &PTR_FUN_09f19598;
  local_58 = &PTR_FUN_09f19598;
  local_40 = &local_58;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x10);
  lStack_50 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0564eba0:
    *(long *)(lVar5 + 0x58) = lVar5 + 0x40;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x40);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar4 = *local_40;
      if (local_40 == &local_58) goto LAB_0564eba0;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x58) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x10) = FUN_0564f264;
  if (local_40 == &local_58) {
    pcVar3 = (code *)(*local_40)[4];
LAB_0564ebe0:
    (*pcVar3)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_40)[5];
    goto LAB_0564ebe0;
  }
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_1 + 0x10) + 0x18);
  if (pcVar3 != (code *)0x0) {
    (*pcVar3)(*(long *)(param_1 + 8) + 0x60);
  }
  lVar6 = *(long *)(param_1 + 8);
  plVar1 = *(long **)(lVar5 + 0x78);
  if (plVar1 == (long *)0x0) {
    *(undefined8 *)(lVar6 + 0x78) = 0;
  }
  else if (plVar1 == (long *)(lVar5 + 0x60)) {
    *(long *)(lVar6 + 0x78) = lVar6 + 0x60;
    (**(code **)(**(long **)(lVar5 + 0x78) + 0x18))();
  }
  else {
    uVar2 = (**(code **)(*plVar1 + 0x10))();
    *(undefined8 *)(lVar6 + 0x78) = uVar2;
  }
  *(code **)(*(long *)(param_1 + 0x10) + 0x18) = FUN_0564f3c4;
  ppuVar4 = &PTR_FUN_09f19618;
  local_58 = &PTR_FUN_09f19618;
  local_40 = &local_58;
  lVar5 = *(long *)(param_2 + 8);
  pcVar3 = *(code **)(*(long *)(param_2 + 0x10) + 0x18);
  lStack_50 = param_1;
  if (pcVar3 == (code *)0x0) {
LAB_0564ecb0:
    *(long *)(lVar5 + 0x78) = lVar5 + 0x60;
    (*(code *)ppuVar4[3])();
  }
  else {
    (*pcVar3)(lVar5 + 0x60);
    lVar5 = *(long *)(param_2 + 8);
    uVar2 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar4 = *local_40;
      if (local_40 == &local_58) goto LAB_0564ecb0;
      uVar2 = (*(code *)ppuVar4[2])();
    }
    *(undefined8 *)(lVar5 + 0x78) = uVar2;
  }
  *(code **)(*(long *)(param_2 + 0x10) + 0x18) = FUN_0564f3c4;
  if (local_40 == &local_58) {
    pcVar3 = (code *)(*local_40)[4];
  }
  else {
    if (local_40 == (undefined ***)0x0) goto LAB_0564ecf4;
    pcVar3 = (code *)(*local_40)[5];
  }
  (*pcVar3)();
LAB_0564ecf4:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


