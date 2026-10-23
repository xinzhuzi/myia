// Ghidra inferred pseudocode; requested=0x50e0fb0
// entry=050e0fb0 end=050e1657

undefined8 FUN_050e0fb0(long param_1,long param_2)

{
  char cVar1;
  int iVar2;
  undefined8 uVar3;
  ulong uVar4;
  char *pcVar5;
  uint uVar6;
  char *pcVar7;
  uint uVar8;
  long lVar9;
  undefined8 *puVar10;
  int local_64;
  
LAB_050e1004:
  pcVar7 = *(char **)(param_2 + 8);
  if (pcVar7 < *(char **)(param_2 + 0x10)) {
    cVar1 = *pcVar7;
    uVar4 = (ulong)cVar1;
    if (cVar1 < 0) goto LAB_050e102c;
    *(int *)(param_2 + 0x20) = (int)cVar1;
    *(char **)(param_2 + 8) = pcVar7 + 1;
    if (cVar1 == '\0') {
      return 1;
    }
  }
  else {
LAB_050e102c:
    uVar4 = FUN_05ab303c(param_2);
    *(int *)(param_2 + 0x20) = (int)uVar4;
    if ((int)uVar4 == 0) {
      return 1;
    }
  }
  uVar6 = (uint)(uVar4 >> 3) & 0x1fffffff;
  uVar8 = (uint)uVar4 & 7;
  if (uVar6 < 4) {
    if (uVar6 != 1) {
      if (uVar6 == 2) {
        if ((uVar4 & 7) == 0) {
          pcVar7 = *(char **)(param_2 + 8);
          pcVar5 = *(char **)(param_2 + 0x10);
          if (pcVar7 < pcVar5) goto LAB_050e11c8;
          goto LAB_050e11e0;
        }
      }
      else if ((uVar6 == 3) && (uVar8 == 2)) {
        uVar8 = *(uint *)(param_1 + 0x38);
        goto LAB_050e121c;
      }
LAB_050e111c:
      if (uVar8 == 4) {
        return 1;
      }
      uVar4 = FUN_05ab4aac(param_2);
      if ((uVar4 & 1) == 0) {
        return 0;
      }
      goto LAB_050e1004;
    }
    if (uVar8 != 2) goto LAB_050e111c;
    *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 1;
    lVar9 = *(long *)(param_1 + 8);
    if (lVar9 == 0) {
      lVar9 = __Znwm(0x20);
      FUN_0465b0bc();
      *(long *)(param_1 + 8) = lVar9;
    }
    local_64 = -0x55555556;
    pcVar7 = *(char **)(param_2 + 8);
    if ((pcVar7 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar7, -1 < cVar1)) {
      *(char **)(param_2 + 8) = pcVar7 + 1;
      local_64 = (int)cVar1;
    }
    else {
      iVar2 = FUN_05ab2ea0(param_2,&local_64);
      if (iVar2 == 0) {
        return 0;
      }
    }
    iVar2 = *(int *)(param_2 + 0x38);
    *(int *)(param_2 + 0x38) = iVar2 + 1;
    if (*(int *)(param_2 + 0x3c) <= iVar2) {
      return 0;
    }
    uVar3 = FUN_05ab26f0(param_2,local_64);
    iVar2 = FUN_0465b43c(lVar9,param_2);
    if (iVar2 == 0) {
      return 0;
    }
    if (*(char *)(param_2 + 0x24) != '\x01') {
      return 0;
    }
    FUN_05ab276c(param_2,uVar3);
    if (0 < *(int *)(param_2 + 0x38)) {
      *(int *)(param_2 + 0x38) = *(int *)(param_2 + 0x38) + -1;
    }
    pcVar7 = *(char **)(param_2 + 8);
    pcVar5 = *(char **)(param_2 + 0x10);
    if ((pcVar5 <= pcVar7) || (*pcVar7 != '\x10')) goto LAB_050e1004;
    pcVar7 = pcVar7 + 1;
    *(char **)(param_2 + 8) = pcVar7;
    if (pcVar7 < pcVar5) {
LAB_050e11c8:
      if (*pcVar7 < 0) goto LAB_050e11e0;
      *(int *)(param_1 + 0x30) = (int)*pcVar7;
      pcVar7 = pcVar7 + 1;
      *(char **)(param_2 + 8) = pcVar7;
    }
    else {
LAB_050e11e0:
      uVar3 = FUN_05ab2ea0(param_2,param_1 + 0x30);
      if ((int)uVar3 == 0) {
        return uVar3;
      }
      pcVar7 = *(char **)(param_2 + 8);
      pcVar5 = *(char **)(param_2 + 0x10);
    }
    uVar8 = *(uint *)(param_1 + 0x38) | 2;
    *(uint *)(param_1 + 0x38) = uVar8;
    if ((pcVar5 <= pcVar7) || (*pcVar7 != '\x1a')) goto LAB_050e1004;
    *(char **)(param_2 + 8) = pcVar7 + 1;
LAB_050e121c:
    *(uint *)(param_1 + 0x38) = uVar8 | 4;
    puVar10 = *(undefined8 **)(param_1 + 0x10);
    if (puVar10 == (undefined8 *)0x0) {
      puVar10 = (undefined8 *)__Znwm(200);
      *puVar10 = &PTR_FUN_09edc180;
      puVar10[2] = 0;
      puVar10[1] = 0;
      puVar10[4] = 0;
      puVar10[3] = 0;
      puVar10[6] = 0;
      puVar10[5] = 0;
      puVar10[8] = 0;
      puVar10[7] = 0;
      *(undefined8 *)((long)puVar10 + 0x4c) = 0;
      *(undefined8 *)((long)puVar10 + 0x44) = 0;
      puVar10[0xb] = &DAT_0a524ad0;
      puVar10[0xc] = 0;
      puVar10[0xd] = &DAT_0a524ad0;
      puVar10[0xe] = 0;
      puVar10[0xf] = &DAT_0a524ad0;
      *(undefined4 *)((long)puVar10 + 0x54) = 0;
      puVar10[0x10] = 0;
      puVar10[0x11] = &DAT_0a524ad0;
      *(undefined8 *)((long)puVar10 + 0xbc) = 0;
      puVar10[0x13] = 0;
      puVar10[0x12] = 0;
      puVar10[0x15] = 0;
      puVar10[0x14] = 0;
      *(undefined8 *)((long)puVar10 + 0xb4) = 0;
      *(undefined8 *)((long)puVar10 + 0xac) = 0;
      *(undefined8 **)(param_1 + 0x10) = puVar10;
    }
    local_64 = -0x55555556;
    pcVar7 = *(char **)(param_2 + 8);
    if ((pcVar7 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar7, -1 < cVar1)) {
      *(char **)(param_2 + 8) = pcVar7 + 1;
      local_64 = (int)cVar1;
    }
    else {
      iVar2 = FUN_05ab2ea0(param_2,&local_64);
      if (iVar2 == 0) {
        return 0;
      }
    }
    iVar2 = *(int *)(param_2 + 0x38);
    *(int *)(param_2 + 0x38) = iVar2 + 1;
    if (*(int *)(param_2 + 0x3c) <= iVar2) {
      return 0;
    }
    uVar3 = FUN_05ab26f0(param_2,local_64);
    iVar2 = FUN_050dab54(puVar10,param_2);
    if (iVar2 == 0) {
      return 0;
    }
    if (*(char *)(param_2 + 0x24) != '\x01') {
      return 0;
    }
    FUN_05ab276c(param_2,uVar3);
    if (0 < *(int *)(param_2 + 0x38)) {
      *(int *)(param_2 + 0x38) = *(int *)(param_2 + 0x38) + -1;
    }
    pcVar7 = *(char **)(param_2 + 8);
    if ((*(char **)(param_2 + 0x10) <= pcVar7) || (*pcVar7 != '\"')) goto LAB_050e1004;
    *(char **)(param_2 + 8) = pcVar7 + 1;
LAB_050e1330:
    *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 8;
    puVar10 = *(undefined8 **)(param_1 + 0x18);
    if (puVar10 == (undefined8 *)0x0) {
      puVar10 = (undefined8 *)__Znwm(0x90);
      *puVar10 = &PTR_FUN_09edc1f8;
      puVar10[1] = &DAT_0a524ad0;
      puVar10[2] = &DAT_0a524ad0;
      puVar10[3] = 0;
      puVar10[4] = &DAT_0a524ad0;
      puVar10[5] = &DAT_0a524ad0;
      puVar10[6] = &DAT_0a524ad0;
      puVar10[7] = 0;
      puVar10[8] = &DAT_0a524ad0;
      puVar10[9] = 0;
      puVar10[10] = &DAT_0a524ad0;
      puVar10[0xb] = &DAT_0a524ad0;
      puVar10[0xc] = &DAT_0a524ad0;
      puVar10[0xd] = 0;
      puVar10[0x10] = 0;
      puVar10[0x11] = 0;
      puVar10[0xe] = &DAT_0a524ad0;
      puVar10[0xf] = 0;
      *(undefined8 **)(param_1 + 0x18) = puVar10;
    }
    local_64 = -0x55555556;
    pcVar7 = *(char **)(param_2 + 8);
    if ((pcVar7 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar7, -1 < cVar1)) {
      *(char **)(param_2 + 8) = pcVar7 + 1;
      local_64 = (int)cVar1;
    }
    else {
      iVar2 = FUN_05ab2ea0(param_2,&local_64);
      if (iVar2 == 0) {
        return 0;
      }
    }
    iVar2 = *(int *)(param_2 + 0x38);
    *(int *)(param_2 + 0x38) = iVar2 + 1;
    if (*(int *)(param_2 + 0x3c) <= iVar2) {
      return 0;
    }
    uVar3 = FUN_05ab26f0(param_2,local_64);
    iVar2 = FUN_050ddaf4(puVar10,param_2);
    if (iVar2 == 0) {
      return 0;
    }
    if (*(char *)(param_2 + 0x24) != '\x01') {
      return 0;
    }
    FUN_05ab276c(param_2,uVar3);
    if (0 < *(int *)(param_2 + 0x38)) {
      *(int *)(param_2 + 0x38) = *(int *)(param_2 + 0x38) + -1;
    }
    pcVar7 = *(char **)(param_2 + 8);
    if ((*(char **)(param_2 + 0x10) <= pcVar7) || (*pcVar7 != '*')) goto LAB_050e1004;
    *(char **)(param_2 + 8) = pcVar7 + 1;
LAB_050e143c:
    *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 0x10;
    puVar10 = *(undefined8 **)(param_1 + 0x20);
    if (puVar10 == (undefined8 *)0x0) {
      puVar10 = (undefined8 *)__Znwm(0x40);
      *puVar10 = &PTR_FUN_09edc108;
      puVar10[2] = 0;
      puVar10[1] = 0;
      puVar10[4] = 0;
      puVar10[3] = 0;
      puVar10[6] = 0;
      puVar10[5] = 0;
      *(undefined4 *)(puVar10 + 7) = 0;
      *(undefined8 **)(param_1 + 0x20) = puVar10;
    }
    local_64 = -0x55555556;
    pcVar7 = *(char **)(param_2 + 8);
    if ((pcVar7 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar7, -1 < cVar1)) {
      *(char **)(param_2 + 8) = pcVar7 + 1;
      local_64 = (int)cVar1;
    }
    else {
      iVar2 = FUN_05ab2ea0(param_2,&local_64);
      if (iVar2 == 0) {
        return 0;
      }
    }
    iVar2 = *(int *)(param_2 + 0x38);
    *(int *)(param_2 + 0x38) = iVar2 + 1;
    if (*(int *)(param_2 + 0x3c) <= iVar2) {
      return 0;
    }
    uVar3 = FUN_05ab26f0(param_2,local_64);
    iVar2 = FUN_050d919c(puVar10,param_2);
    if (iVar2 == 0) {
      return 0;
    }
    if (*(char *)(param_2 + 0x24) != '\x01') {
      return 0;
    }
    FUN_05ab276c(param_2,uVar3);
    if (0 < *(int *)(param_2 + 0x38)) {
      *(int *)(param_2 + 0x38) = *(int *)(param_2 + 0x38) + -1;
    }
    pcVar7 = *(char **)(param_2 + 8);
    if ((*(char **)(param_2 + 0x10) <= pcVar7) || (*pcVar7 != '2')) goto LAB_050e1004;
    *(char **)(param_2 + 8) = pcVar7 + 1;
  }
  else {
    if (uVar6 == 4) {
      if (uVar8 != 2) goto LAB_050e111c;
      goto LAB_050e1330;
    }
    if (uVar6 == 5) {
      if (uVar8 != 2) goto LAB_050e111c;
      goto LAB_050e143c;
    }
    if ((uVar6 != 6) || (uVar8 != 2)) goto LAB_050e111c;
  }
  *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 0x20;
  puVar10 = *(undefined8 **)(param_1 + 0x28);
  if (puVar10 == (undefined8 *)0x0) {
    puVar10 = (undefined8 *)__Znwm(0x38);
    puVar10[1] = 0;
    puVar10[2] = 0;
    *puVar10 = &PTR_FUN_09edc270;
    *(undefined4 *)(puVar10 + 3) = 0;
    puVar10[4] = 0;
    puVar10[5] = 0;
    *(undefined4 *)(puVar10 + 6) = 0;
    *(undefined8 **)(param_1 + 0x28) = puVar10;
  }
  local_64 = -0x55555556;
  pcVar7 = *(char **)(param_2 + 8);
  if ((pcVar7 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar7, -1 < cVar1)) {
    *(char **)(param_2 + 8) = pcVar7 + 1;
    local_64 = (int)cVar1;
  }
  else {
    iVar2 = FUN_05ab2ea0(param_2,&local_64);
    if (iVar2 == 0) {
      return 0;
    }
  }
  iVar2 = *(int *)(param_2 + 0x38);
  *(int *)(param_2 + 0x38) = iVar2 + 1;
  if (*(int *)(param_2 + 0x3c) <= iVar2) {
    return 0;
  }
  uVar3 = FUN_05ab26f0(param_2,local_64);
  iVar2 = FUN_050df41c(puVar10,param_2);
  if (iVar2 == 0) {
    return 0;
  }
  if (*(char *)(param_2 + 0x24) != '\x01') {
    return 0;
  }
  FUN_05ab276c(param_2,uVar3);
  if (0 < *(int *)(param_2 + 0x38)) {
    *(int *)(param_2 + 0x38) = *(int *)(param_2 + 0x38) + -1;
  }
  if ((*(long *)(param_2 + 8) == *(long *)(param_2 + 0x10)) &&
     ((*(int *)(param_2 + 0x2c) != 0 || (*(int *)(param_2 + 0x18) == *(int *)(param_2 + 0x28))))) {
    *(undefined4 *)(param_2 + 0x20) = 0;
    *(undefined1 *)(param_2 + 0x24) = 1;
    return 1;
  }
  goto LAB_050e1004;
}


