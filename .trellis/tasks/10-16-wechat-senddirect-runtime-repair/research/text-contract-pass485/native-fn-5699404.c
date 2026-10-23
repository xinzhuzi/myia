// Ghidra inferred pseudocode; requested=0x5699404
// entry=05699404 end=05699bd3

void FUN_05699404(long param_1)

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
  local_58 = &PTR_FUN_09f1cd10;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 0x188);
  lStack_50 = param_1;
  if ((code *)**(undefined8 **)(param_1 + 400) == (code *)0x0) {
LAB_05699480:
    *(long *)(lVar4 + 0x18) = lVar4;
    (*(code *)(*local_40)[3])(local_40,lVar4);
  }
  else {
    (*(code *)**(undefined8 **)(param_1 + 400))(lVar4);
    lVar4 = *(long *)(param_1 + 0x188);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      if (local_40 == &local_58) goto LAB_05699480;
      uVar1 = (*(code *)(*local_40)[2])();
    }
    *(undefined8 *)(lVar4 + 0x18) = uVar1;
  }
  **(undefined8 **)(param_1 + 400) = FUN_05655e10;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_056994d0:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_056994d0;
  }
  ppuVar3 = &PTR_FUN_09f1cd90;
  local_58 = &PTR_FUN_09f1cd90;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 0x188);
  pcVar2 = *(code **)(*(long *)(param_1 + 400) + 8);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_05699528:
    *(long *)(lVar4 + 0x38) = lVar4 + 0x20;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0x20);
    lVar4 = *(long *)(param_1 + 0x188);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_05699528;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0x38) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 400) + 8) = FUN_0564f3c4;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_05699570:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_05699570;
  }
  ppuVar3 = &PTR_FUN_09f1ce10;
  local_58 = &PTR_FUN_09f1ce10;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 0x188);
  pcVar2 = *(code **)(*(long *)(param_1 + 400) + 0x10);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_056995c8:
    *(long *)(lVar4 + 0x58) = lVar4 + 0x40;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0x40);
    lVar4 = *(long *)(param_1 + 0x188);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_056995c8;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0x58) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 400) + 0x10) = FUN_0564f264;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_05699610:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_05699610;
  }
  ppuVar3 = &PTR_FUN_09f1ce90;
  local_58 = &PTR_FUN_09f1ce90;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 0x188);
  pcVar2 = *(code **)(*(long *)(param_1 + 400) + 0x18);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_05699668:
    *(long *)(lVar4 + 0x78) = lVar4 + 0x60;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0x60);
    lVar4 = *(long *)(param_1 + 0x188);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_05699668;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0x78) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 400) + 0x18) = FUN_0564f3c4;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_056996a8:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_056996a8;
  }
  ppuVar3 = &PTR_FUN_09f1cf10;
  local_58 = &PTR_FUN_09f1cf10;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 0x188);
  pcVar2 = *(code **)(*(long *)(param_1 + 400) + 0x20);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_05699700:
    *(long *)(lVar4 + 0x98) = lVar4 + 0x80;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0x80);
    lVar4 = *(long *)(param_1 + 0x188);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_05699700;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0x98) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 400) + 0x20) = FUN_0564f3c4;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_05699740:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_05699740;
  }
  ppuVar3 = &PTR_FUN_09f1cf90;
  local_58 = &PTR_FUN_09f1cf90;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 0x188);
  pcVar2 = *(code **)(*(long *)(param_1 + 400) + 0x28);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_05699798:
    *(long *)(lVar4 + 0xb8) = lVar4 + 0xa0;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0xa0);
    lVar4 = *(long *)(param_1 + 0x188);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_05699798;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0xb8) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 400) + 0x28) = FUN_05656418;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_056997e0:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_056997e0;
  }
  ppuVar3 = &PTR_FUN_09f1d010;
  local_58 = &PTR_FUN_09f1d010;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 0x188);
  pcVar2 = *(code **)(*(long *)(param_1 + 400) + 0x30);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_05699838:
    *(long *)(lVar4 + 0xd8) = lVar4 + 0xc0;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0xc0);
    lVar4 = *(long *)(param_1 + 0x188);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_05699838;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0xd8) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 400) + 0x30) = FUN_05656534;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_05699880:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_05699880;
  }
  ppuVar3 = &PTR_FUN_09f1d090;
  local_58 = &PTR_FUN_09f1d090;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 0x188);
  pcVar2 = *(code **)(*(long *)(param_1 + 400) + 0x38);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_056998d8:
    *(long *)(lVar4 + 0xf8) = lVar4 + 0xe0;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0xe0);
    lVar4 = *(long *)(param_1 + 0x188);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_056998d8;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0xf8) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 400) + 0x38) = FUN_05656650;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_05699920:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_05699920;
  }
  ppuVar3 = &PTR_FUN_09f1d110;
  local_58 = &PTR_FUN_09f1d110;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 0x188);
  pcVar2 = *(code **)(*(long *)(param_1 + 400) + 0x40);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_05699978:
    *(long *)(lVar4 + 0x118) = lVar4 + 0x100;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0x100);
    lVar4 = *(long *)(param_1 + 0x188);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_05699978;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0x118) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 400) + 0x40) = FUN_0565676c;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_056999c0:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_056999c0;
  }
  ppuVar3 = &PTR_FUN_09f1d190;
  local_58 = &PTR_FUN_09f1d190;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 0x188);
  pcVar2 = *(code **)(*(long *)(param_1 + 400) + 0x48);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_05699a18:
    *(long *)(lVar4 + 0x138) = lVar4 + 0x120;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0x120);
    lVar4 = *(long *)(param_1 + 0x188);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_05699a18;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0x138) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 400) + 0x48) = FUN_05656890;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_05699a60:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_05699a60;
  }
  ppuVar3 = &PTR_FUN_09f1d210;
  local_58 = &PTR_FUN_09f1d210;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 0x188);
  pcVar2 = *(code **)(*(long *)(param_1 + 400) + 0x50);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_05699ab8:
    *(long *)(lVar4 + 0x158) = lVar4 + 0x140;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0x140);
    lVar4 = *(long *)(param_1 + 0x188);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_05699ab8;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0x158) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 400) + 0x50) = FUN_056569ac;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
LAB_05699b00:
    (*pcVar2)();
  }
  else if (local_40 != (undefined ***)0x0) {
    pcVar2 = (code *)(*local_40)[5];
    goto LAB_05699b00;
  }
  ppuVar3 = &PTR_FUN_09f1d290;
  local_58 = &PTR_FUN_09f1d290;
  local_40 = &local_58;
  lVar4 = *(long *)(param_1 + 0x188);
  pcVar2 = *(code **)(*(long *)(param_1 + 400) + 0x58);
  lStack_50 = param_1;
  if (pcVar2 == (code *)0x0) {
LAB_05699b58:
    *(long *)(lVar4 + 0x178) = lVar4 + 0x160;
    (*(code *)ppuVar3[3])();
  }
  else {
    (*pcVar2)(lVar4 + 0x160);
    lVar4 = *(long *)(param_1 + 0x188);
    uVar1 = 0;
    if (local_40 != (undefined ***)0x0) {
      ppuVar3 = *local_40;
      if (local_40 == &local_58) goto LAB_05699b58;
      uVar1 = (*(code *)ppuVar3[2])();
    }
    *(undefined8 *)(lVar4 + 0x178) = uVar1;
  }
  *(code **)(*(long *)(param_1 + 400) + 0x58) = FUN_05656ac8;
  if (local_40 == &local_58) {
    pcVar2 = (code *)(*local_40)[4];
  }
  else {
    if (local_40 == (undefined ***)0x0) goto LAB_05699ba4;
    pcVar2 = (code *)(*local_40)[5];
  }
  (*pcVar2)();
LAB_05699ba4:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


