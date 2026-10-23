// Ghidra inferred pseudocode; requested=0x55bedc4
// entry=055bedc4 end=055bf14b

undefined8 FUN_055bedc4(long param_1,long param_2)

{
  uint uVar1;
  char cVar2;
  undefined8 uVar3;
  ulong uVar4;
  undefined8 *puVar5;
  char *pcVar6;
  uint uVar7;
  char *pcVar8;
  undefined8 *puVar9;
  undefined8 uVar10;
  
LAB_055bedec:
  do {
    pcVar8 = *(char **)(param_2 + 8);
    if (pcVar8 < *(char **)(param_2 + 0x10)) {
      cVar2 = *pcVar8;
      uVar4 = (ulong)cVar2;
      if (cVar2 < 0) goto LAB_055bee14;
      *(int *)(param_2 + 0x20) = (int)cVar2;
      *(char **)(param_2 + 8) = pcVar8 + 1;
      if (cVar2 == '\0') {
        return 1;
      }
    }
    else {
LAB_055bee14:
      uVar4 = FUN_05ab303c(param_2);
      *(int *)(param_2 + 0x20) = (int)uVar4;
      if ((int)uVar4 == 0) {
        return 1;
      }
    }
    uVar7 = (uint)(uVar4 >> 3) & 0x1fffffff;
    uVar1 = (uint)uVar4 & 7;
    if (3 < uVar7) {
      if (uVar7 == 4) {
        if (uVar1 == 2) goto LAB_055bf004;
      }
      else if (uVar7 == 5) {
        if (uVar1 == 2) goto LAB_055bf060;
      }
      else if ((uVar7 == 6) && ((uVar4 & 7) == 0)) {
        pcVar8 = *(char **)(param_2 + 8);
        pcVar6 = *(char **)(param_2 + 0x10);
        if (pcVar8 < pcVar6) goto LAB_055bf0c4;
        goto LAB_055bf0dc;
      }
LAB_055beef4:
      if (uVar1 == 4) {
        return 1;
      }
      uVar4 = FUN_05ab4aac(param_2);
      if ((uVar4 & 1) == 0) {
        return 0;
      }
      goto LAB_055bedec;
    }
    if (uVar7 != 1) {
      if (uVar7 == 2) {
        if (uVar1 == 2) goto LAB_055bef4c;
      }
      else if ((uVar7 == 3) && (uVar1 == 2)) goto LAB_055befa8;
      goto LAB_055beef4;
    }
    if (uVar1 != 2) goto LAB_055beef4;
    *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 1;
    puVar5 = DAT_0a523c00;
    puVar9 = *(undefined8 **)(param_1 + 8);
    if (puVar9 == DAT_0a523c00) {
      puVar9 = (undefined8 *)__Znwm(0x18);
      if (*(char *)((long)puVar5 + 0x17) < '\0') {
        FUN_00018d20(puVar9,*puVar5,puVar5[1]);
      }
      else {
        uVar10 = puVar5[1];
        uVar3 = *puVar5;
        puVar9[2] = puVar5[2];
        puVar9[1] = uVar10;
        *puVar9 = uVar3;
      }
      *(undefined8 **)(param_1 + 8) = puVar9;
    }
    uVar3 = FUN_05ab514c(param_2,puVar9);
    if ((int)uVar3 == 0) {
      return uVar3;
    }
    pcVar8 = *(char **)(param_2 + 8);
    if ((pcVar8 < *(char **)(param_2 + 0x10)) && (*pcVar8 == '\x12')) {
      *(char **)(param_2 + 8) = pcVar8 + 1;
LAB_055bef4c:
      *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 2;
      puVar5 = *(undefined8 **)(param_1 + 0x10);
      if (puVar5 == &DAT_0a524ad0) {
        puVar5 = (undefined8 *)__Znwm(0x18);
        puVar5[1] = 0;
        puVar5[2] = 0;
        *puVar5 = 0;
        *(undefined8 **)(param_1 + 0x10) = puVar5;
      }
      uVar3 = FUN_05ab514c(param_2,puVar5);
      if ((int)uVar3 == 0) {
        return uVar3;
      }
      pcVar8 = *(char **)(param_2 + 8);
      if ((pcVar8 < *(char **)(param_2 + 0x10)) && (*pcVar8 == '\x1a')) {
        *(char **)(param_2 + 8) = pcVar8 + 1;
LAB_055befa8:
        *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 4;
        puVar5 = *(undefined8 **)(param_1 + 0x18);
        if (puVar5 == &DAT_0a524ad0) {
          puVar5 = (undefined8 *)__Znwm(0x18);
          puVar5[1] = 0;
          puVar5[2] = 0;
          *puVar5 = 0;
          *(undefined8 **)(param_1 + 0x18) = puVar5;
        }
        uVar3 = FUN_05ab514c(param_2,puVar5);
        if ((int)uVar3 == 0) {
          return uVar3;
        }
        pcVar8 = *(char **)(param_2 + 8);
        if ((pcVar8 < *(char **)(param_2 + 0x10)) && (*pcVar8 == '\"')) {
          *(char **)(param_2 + 8) = pcVar8 + 1;
LAB_055bf004:
          *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 8;
          puVar5 = *(undefined8 **)(param_1 + 0x20);
          if (puVar5 == &DAT_0a524ad0) {
            puVar5 = (undefined8 *)__Znwm(0x18);
            puVar5[1] = 0;
            puVar5[2] = 0;
            *puVar5 = 0;
            *(undefined8 **)(param_1 + 0x20) = puVar5;
          }
          uVar3 = FUN_05ab514c(param_2,puVar5);
          if ((int)uVar3 == 0) {
            return uVar3;
          }
          pcVar8 = *(char **)(param_2 + 8);
          if ((pcVar8 < *(char **)(param_2 + 0x10)) && (*pcVar8 == '*')) {
            *(char **)(param_2 + 8) = pcVar8 + 1;
LAB_055bf060:
            *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 0x10;
            puVar5 = *(undefined8 **)(param_1 + 0x28);
            if (puVar5 == &DAT_0a524ad0) {
              puVar5 = (undefined8 *)__Znwm(0x18);
              puVar5[1] = 0;
              puVar5[2] = 0;
              *puVar5 = 0;
              *(undefined8 **)(param_1 + 0x28) = puVar5;
            }
            uVar3 = FUN_05ab514c(param_2,puVar5);
            if ((int)uVar3 == 0) {
              return uVar3;
            }
            pcVar8 = *(char **)(param_2 + 8);
            pcVar6 = *(char **)(param_2 + 0x10);
            if ((pcVar8 < pcVar6) && (*pcVar8 == '0')) {
              pcVar8 = pcVar8 + 1;
              *(char **)(param_2 + 8) = pcVar8;
              if (pcVar8 < pcVar6) {
LAB_055bf0c4:
                if (*pcVar8 < 0) goto LAB_055bf0dc;
                *(int *)(param_1 + 0x30) = (int)*pcVar8;
                pcVar8 = pcVar8 + 1;
                *(char **)(param_2 + 8) = pcVar8;
              }
              else {
LAB_055bf0dc:
                uVar3 = FUN_05ab2ea0(param_2,param_1 + 0x30);
                if ((int)uVar3 == 0) {
                  return uVar3;
                }
                pcVar8 = *(char **)(param_2 + 8);
                pcVar6 = *(char **)(param_2 + 0x10);
              }
              *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 0x20;
              if ((pcVar8 == pcVar6) &&
                 ((*(int *)(param_2 + 0x2c) != 0 ||
                  (*(int *)(param_2 + 0x18) == *(int *)(param_2 + 0x28))))) {
                *(undefined4 *)(param_2 + 0x20) = 0;
                *(undefined1 *)(param_2 + 0x24) = 1;
                return 1;
              }
            }
          }
        }
      }
    }
  } while( true );
}


