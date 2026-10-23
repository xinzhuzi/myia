// Ghidra inferred pseudocode; requested=0x465d7c4
// entry=0465d7c4 end=0465da57

undefined8 FUN_0465d7c4(long param_1,long param_2)

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
  undefined8 *puVar10;
  int local_54;
  
LAB_0465d7fc:
  do {
    pcVar7 = *(char **)(param_2 + 8);
    if (pcVar7 < *(char **)(param_2 + 0x10)) {
      cVar2 = *pcVar7;
      uVar5 = (ulong)cVar2;
      if (cVar2 < 0) goto LAB_0465d824;
      *(int *)(param_2 + 0x20) = (int)cVar2;
      *(char **)(param_2 + 8) = pcVar7 + 1;
      if (cVar2 == '\0') {
        return 1;
      }
    }
    else {
LAB_0465d824:
      uVar5 = FUN_05ab303c(param_2);
      *(int *)(param_2 + 0x20) = (int)uVar5;
      if ((int)uVar5 == 0) {
        return 1;
      }
    }
    uVar8 = (uint)(uVar5 >> 3) & 0x1fffffff;
    uVar1 = (uint)uVar5 & 7;
    if (uVar8 == 2) {
      if (uVar1 == 2) goto LAB_0465d8d0;
LAB_0465d880:
      if (uVar1 == 4) {
        return 1;
      }
      uVar5 = FUN_05ab4aac(param_2);
      if ((uVar5 & 1) == 0) {
        return 0;
      }
      goto LAB_0465d7fc;
    }
    if ((uVar8 != 1) || ((uVar5 & 7) != 0)) goto LAB_0465d880;
    pcVar7 = *(char **)(param_2 + 8);
    pcVar9 = *(char **)(param_2 + 0x10);
    if ((pcVar7 < pcVar9) && (-1 < *pcVar7)) {
      *(int *)(param_1 + 0x20) = (int)*pcVar7;
      pcVar7 = pcVar7 + 1;
      *(char **)(param_2 + 8) = pcVar7;
    }
    else {
      uVar4 = FUN_05ab2ea0(param_2,param_1 + 0x20);
      if ((int)uVar4 == 0) {
        return uVar4;
      }
      pcVar7 = *(char **)(param_2 + 8);
      pcVar9 = *(char **)(param_2 + 0x10);
    }
    *(uint *)(param_1 + 0x28) = *(uint *)(param_1 + 0x28) | 1;
    if ((pcVar7 < pcVar9) && (*pcVar7 == '\x12')) {
      do {
        *(char **)(param_2 + 8) = pcVar7 + 1;
LAB_0465d8d0:
        iVar3 = *(int *)(param_1 + 0x10);
        iVar6 = *(int *)(param_1 + 0x14);
        if (iVar3 < iVar6) {
          *(int *)(param_1 + 0x10) = iVar3 + 1;
          puVar10 = *(undefined8 **)(*(long *)(param_1 + 8) + (long)iVar3 * 8);
        }
        else {
          if (iVar6 == *(int *)(param_1 + 0x18)) {
            FUN_05ab4038(param_1 + 8,iVar6 + 1);
            iVar6 = *(int *)(param_1 + 0x14);
          }
          *(int *)(param_1 + 0x14) = iVar6 + 1;
          puVar10 = (undefined8 *)__Znwm(0x38);
          *puVar10 = &PTR_FUN_09e91d80;
          puVar10[1] = 0;
          puVar10[2] = &DAT_0a524ad0;
          puVar10[3] = 0;
          puVar10[4] = &DAT_0a524ad0;
          puVar10[5] = 0;
          puVar10[6] = 0;
          iVar3 = *(int *)(param_1 + 0x10);
          *(int *)(param_1 + 0x10) = iVar3 + 1;
          *(undefined8 **)(*(long *)(param_1 + 8) + (long)iVar3 * 8) = puVar10;
        }
        local_54 = -0x55555556;
        pcVar7 = *(char **)(param_2 + 8);
        if ((pcVar7 < *(char **)(param_2 + 0x10)) && (cVar2 = *pcVar7, -1 < cVar2)) {
          *(char **)(param_2 + 8) = pcVar7 + 1;
          local_54 = (int)cVar2;
        }
        else {
          iVar3 = FUN_05ab2ea0(param_2,&local_54);
          if (iVar3 == 0) {
            return 0;
          }
        }
        iVar3 = *(int *)(param_2 + 0x38);
        *(int *)(param_2 + 0x38) = iVar3 + 1;
        if (*(int *)(param_2 + 0x3c) <= iVar3) {
          return 0;
        }
        uVar4 = FUN_05ab26f0(param_2,local_54);
        iVar3 = FUN_0465cb94(puVar10,param_2);
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
        pcVar7 = *(char **)(param_2 + 8);
      } while ((pcVar7 < *(char **)(param_2 + 0x10)) && (*pcVar7 == '\x12'));
      if ((pcVar7 == *(char **)(param_2 + 0x10)) &&
         ((*(int *)(param_2 + 0x2c) != 0 || (*(int *)(param_2 + 0x18) == *(int *)(param_2 + 0x28))))
         ) {
        *(undefined4 *)(param_2 + 0x20) = 0;
        *(undefined1 *)(param_2 + 0x24) = 1;
        return 1;
      }
    }
  } while( true );
}


