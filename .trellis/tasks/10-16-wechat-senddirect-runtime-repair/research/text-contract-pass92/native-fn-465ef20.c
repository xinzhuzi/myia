// Ghidra inferred pseudocode; requested=0x465ef20
// entry=0465ef20 end=0465f29f

undefined8 FUN_0465ef20(long param_1,long param_2)

{
  uint uVar1;
  char cVar2;
  int iVar3;
  undefined8 uVar4;
  ulong uVar5;
  int iVar6;
  char *pcVar7;
  uint uVar8;
  char *pcVar9;
  long lVar10;
  undefined8 *puVar11;
  int local_48;
  int local_44;
  
LAB_0465ef4c:
  do {
    pcVar9 = *(char **)(param_2 + 8);
    if (pcVar9 < *(char **)(param_2 + 0x10)) {
      cVar2 = *pcVar9;
      uVar5 = (ulong)cVar2;
      if (cVar2 < 0) goto LAB_0465ef74;
      *(int *)(param_2 + 0x20) = (int)cVar2;
      *(char **)(param_2 + 8) = pcVar9 + 1;
      if (cVar2 == '\0') {
        return 1;
      }
    }
    else {
LAB_0465ef74:
      uVar5 = FUN_05ab303c(param_2);
      *(int *)(param_2 + 0x20) = (int)uVar5;
      if ((int)uVar5 == 0) {
        return 1;
      }
    }
    uVar8 = (uint)(uVar5 >> 3) & 0x1fffffff;
    uVar1 = (uint)uVar5 & 7;
    if (uVar8 == 3) {
      if (uVar1 == 2) goto LAB_0465f118;
LAB_0465f01c:
      if (uVar1 == 4) {
        return 1;
      }
      uVar5 = FUN_05ab4aac(param_2);
      if ((uVar5 & 1) == 0) {
        return 0;
      }
      goto LAB_0465ef4c;
    }
    if (uVar8 == 2) {
      if ((uVar5 & 7) == 0) {
        pcVar9 = *(char **)(param_2 + 8);
        pcVar7 = *(char **)(param_2 + 0x10);
        if (pcVar9 < pcVar7) goto LAB_0465f0c8;
        goto LAB_0465f0e0;
      }
      goto LAB_0465f01c;
    }
    if ((uVar8 != 1) || (uVar1 != 2)) goto LAB_0465f01c;
    *(uint *)(param_1 + 0x30) = *(uint *)(param_1 + 0x30) | 1;
    lVar10 = *(long *)(param_1 + 8);
    if (lVar10 == 0) {
      lVar10 = __Znwm(0x20);
      FUN_0465b0bc();
      *(long *)(param_1 + 8) = lVar10;
    }
    local_48 = -0x55555556;
    pcVar9 = *(char **)(param_2 + 8);
    if ((pcVar9 < *(char **)(param_2 + 0x10)) && (cVar2 = *pcVar9, -1 < cVar2)) {
      *(char **)(param_2 + 8) = pcVar9 + 1;
      local_48 = (int)cVar2;
    }
    else {
      iVar3 = FUN_05ab2ea0(param_2,&local_48);
      if (iVar3 == 0) {
        return 0;
      }
    }
    iVar3 = *(int *)(param_2 + 0x38);
    *(int *)(param_2 + 0x38) = iVar3 + 1;
    if (*(int *)(param_2 + 0x3c) <= iVar3) {
      return 0;
    }
    uVar4 = FUN_05ab26f0(param_2,local_48);
    iVar3 = FUN_0465b43c(lVar10,param_2);
    if (iVar3 == 0) {
      return 0;
    }
    if (*(char *)(param_2 + 0x24) != '\x01') {
      return 0;
    }
    FUN_05ab276c(param_2,uVar4);
    if (0 < *(int *)(param_2 + 0x38)) {
      *(int *)(param_2 + 0x38) = *(int *)(param_2 + 0x38) + -1;
    }
    pcVar9 = *(char **)(param_2 + 8);
    pcVar7 = *(char **)(param_2 + 0x10);
    if ((pcVar9 < pcVar7) && (*pcVar9 == '\x10')) {
      pcVar9 = pcVar9 + 1;
      *(char **)(param_2 + 8) = pcVar9;
      if (pcVar9 < pcVar7) {
LAB_0465f0c8:
        if (*pcVar9 < 0) goto LAB_0465f0e0;
        *(int *)(param_1 + 0x28) = (int)*pcVar9;
        pcVar9 = pcVar9 + 1;
        *(char **)(param_2 + 8) = pcVar9;
      }
      else {
LAB_0465f0e0:
        uVar4 = FUN_05ab2ea0(param_2,param_1 + 0x28);
        if ((int)uVar4 == 0) {
          return uVar4;
        }
        pcVar9 = *(char **)(param_2 + 8);
        pcVar7 = *(char **)(param_2 + 0x10);
      }
      *(uint *)(param_1 + 0x30) = *(uint *)(param_1 + 0x30) | 2;
      if ((pcVar9 < pcVar7) && (*pcVar9 == '\x1a')) {
        do {
          *(char **)(param_2 + 8) = pcVar9 + 1;
LAB_0465f118:
          iVar3 = *(int *)(param_1 + 0x18);
          iVar6 = *(int *)(param_1 + 0x1c);
          if (iVar3 < iVar6) {
            *(int *)(param_1 + 0x18) = iVar3 + 1;
            puVar11 = *(undefined8 **)(*(long *)(param_1 + 0x10) + (long)iVar3 * 8);
          }
          else {
            if (iVar6 == *(int *)(param_1 + 0x20)) {
              FUN_05ab4038(param_1 + 0x10,iVar6 + 1);
              iVar6 = *(int *)(param_1 + 0x1c);
            }
            *(int *)(param_1 + 0x1c) = iVar6 + 1;
            puVar11 = (undefined8 *)__Znwm(0x38);
            *puVar11 = &PTR_FUN_09e91e70;
            puVar11[2] = 0;
            puVar11[1] = 0;
            puVar11[4] = 0;
            puVar11[3] = 0;
            puVar11[6] = 0;
            puVar11[5] = 0;
            iVar3 = *(int *)(param_1 + 0x18);
            *(int *)(param_1 + 0x18) = iVar3 + 1;
            *(undefined8 **)(*(long *)(param_1 + 0x10) + (long)iVar3 * 8) = puVar11;
          }
          local_44 = -0x55555556;
          pcVar9 = *(char **)(param_2 + 8);
          if ((pcVar9 < *(char **)(param_2 + 0x10)) && (cVar2 = *pcVar9, -1 < cVar2)) {
            *(char **)(param_2 + 8) = pcVar9 + 1;
            local_44 = (int)cVar2;
          }
          else {
            iVar3 = FUN_05ab2ea0(param_2,&local_44);
            if (iVar3 == 0) {
              return 0;
            }
          }
          iVar3 = *(int *)(param_2 + 0x38);
          *(int *)(param_2 + 0x38) = iVar3 + 1;
          if (*(int *)(param_2 + 0x3c) <= iVar3) {
            return 0;
          }
          uVar4 = FUN_05ab26f0(param_2,local_44);
          iVar3 = FUN_0465e144(puVar11,param_2);
          if (iVar3 == 0) {
            return 0;
          }
          if (*(char *)(param_2 + 0x24) != '\x01') {
            return 0;
          }
          FUN_05ab276c(param_2,uVar4);
          if (0 < *(int *)(param_2 + 0x38)) {
            *(int *)(param_2 + 0x38) = *(int *)(param_2 + 0x38) + -1;
          }
          pcVar9 = *(char **)(param_2 + 8);
        } while ((pcVar9 < *(char **)(param_2 + 0x10)) && (*pcVar9 == '\x1a'));
        if ((pcVar9 == *(char **)(param_2 + 0x10)) &&
           ((*(int *)(param_2 + 0x2c) != 0 || (*(int *)(param_2 + 0x18) == *(int *)(param_2 + 0x28))
            ))) {
          *(undefined4 *)(param_2 + 0x20) = 0;
          *(undefined1 *)(param_2 + 0x24) = 1;
          return 1;
        }
      }
    }
  } while( true );
}


