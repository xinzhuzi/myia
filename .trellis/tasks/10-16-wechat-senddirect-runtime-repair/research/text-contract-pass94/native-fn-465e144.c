// Ghidra inferred pseudocode; requested=0x465e144
// entry=0465e144 end=0465e647

undefined8 FUN_0465e144(long param_1,long param_2)

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
  int local_48;
  int local_44;
  
LAB_0465e168:
  do {
    pcVar7 = *(char **)(param_2 + 8);
    if (pcVar7 < *(char **)(param_2 + 0x10)) {
      cVar1 = *pcVar7;
      uVar4 = (ulong)cVar1;
      if (cVar1 < 0) goto LAB_0465e190;
      *(int *)(param_2 + 0x20) = (int)cVar1;
      *(char **)(param_2 + 8) = pcVar7 + 1;
      if (cVar1 == '\0') {
        return 1;
      }
    }
    else {
LAB_0465e190:
      uVar4 = FUN_05ab303c(param_2);
      *(int *)(param_2 + 0x20) = (int)uVar4;
      if ((int)uVar4 == 0) {
        return 1;
      }
    }
    uVar6 = (uint)(uVar4 >> 3) & 0x1fffffff;
    uVar8 = (uint)uVar4 & 7;
    if (4 < uVar6) {
      if (uVar6 < 7) {
        if (uVar6 == 5) {
          if ((uVar4 & 7) != 0) goto LAB_0465e2a4;
          pcVar7 = *(char **)(param_2 + 8);
          pcVar5 = *(char **)(param_2 + 0x10);
          if (pcVar7 < pcVar5) goto LAB_0465e4a8;
          goto LAB_0465e4c0;
        }
        if ((uVar6 != 6) || ((uVar4 & 7) != 0)) goto LAB_0465e2a4;
        pcVar7 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        if (pcVar7 < pcVar5) goto LAB_0465e504;
        goto LAB_0465e51c;
      }
      if (uVar6 == 7) {
        if ((uVar4 & 7) != 0) goto LAB_0465e2a4;
        pcVar7 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        if (pcVar7 < pcVar5) goto LAB_0465e560;
        goto LAB_0465e578;
      }
      if ((uVar6 != 8) || ((uVar4 & 7) != 0)) goto LAB_0465e2a4;
      pcVar7 = *(char **)(param_2 + 8);
      pcVar5 = *(char **)(param_2 + 0x10);
      if (pcVar7 < pcVar5) goto LAB_0465e5bc;
      goto LAB_0465e5d4;
    }
    if (2 < uVar6) {
      if (uVar6 == 3) {
        if ((uVar4 & 7) == 0) {
          pcVar7 = *(char **)(param_2 + 8);
          pcVar5 = *(char **)(param_2 + 0x10);
          if (pcVar7 < pcVar5) goto LAB_0465e3f0;
          goto LAB_0465e408;
        }
      }
      else if ((uVar6 == 4) && ((uVar4 & 7) == 0)) {
        pcVar7 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        if (pcVar7 < pcVar5) goto LAB_0465e44c;
        goto LAB_0465e464;
      }
LAB_0465e2a4:
      if (uVar8 == 4) {
        return 1;
      }
      uVar4 = FUN_05ab4aac(param_2);
      if ((uVar4 & 1) == 0) {
        return 0;
      }
      goto LAB_0465e168;
    }
    if (uVar6 == 1) {
      if ((uVar4 & 7) != 0) goto LAB_0465e2a4;
      local_48 = -0x55555556;
      pcVar7 = *(char **)(param_2 + 8);
      pcVar5 = *(char **)(param_2 + 0x10);
      if ((pcVar7 < pcVar5) && (cVar1 = *pcVar7, -1 < cVar1)) {
        pcVar7 = pcVar7 + 1;
        *(char **)(param_2 + 8) = pcVar7;
        iVar2 = (int)cVar1;
      }
      else {
        uVar3 = FUN_05ab2ea0(param_2,&local_48);
        if ((int)uVar3 == 0) {
          return uVar3;
        }
        pcVar7 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        iVar2 = local_48;
      }
      *(int *)(param_1 + 0x10) = iVar2;
      uVar8 = *(uint *)(param_1 + 0x34) | 1;
      *(uint *)(param_1 + 0x34) = uVar8;
      if ((pcVar7 < pcVar5) && (*pcVar7 == '\x12')) {
        *(char **)(param_2 + 8) = pcVar7 + 1;
        goto LAB_0465e310;
      }
    }
    else {
      if ((uVar6 != 2) || (uVar8 != 2)) goto LAB_0465e2a4;
      uVar8 = *(uint *)(param_1 + 0x34);
LAB_0465e310:
      *(uint *)(param_1 + 0x34) = uVar8 | 2;
      lVar9 = *(long *)(param_1 + 8);
      if (lVar9 == 0) {
        lVar9 = __Znwm(0x18);
        FUN_04f33c00();
        *(long *)(param_1 + 8) = lVar9;
      }
      local_44 = -0x55555556;
      pcVar7 = *(char **)(param_2 + 8);
      if ((pcVar7 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar7, -1 < cVar1)) {
        *(char **)(param_2 + 8) = pcVar7 + 1;
        local_44 = (int)cVar1;
      }
      else {
        iVar2 = FUN_05ab2ea0(param_2,&local_44);
        if (iVar2 == 0) {
          return 0;
        }
      }
      iVar2 = *(int *)(param_2 + 0x38);
      *(int *)(param_2 + 0x38) = iVar2 + 1;
      if (*(int *)(param_2 + 0x3c) <= iVar2) {
        return 0;
      }
      uVar3 = FUN_05ab26f0(param_2,local_44);
      iVar2 = FUN_04f37b88(lVar9,param_2);
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
      if ((pcVar7 < pcVar5) && (*pcVar7 == '\x18')) {
        pcVar7 = pcVar7 + 1;
        *(char **)(param_2 + 8) = pcVar7;
        if (pcVar7 < pcVar5) {
LAB_0465e3f0:
          if (*pcVar7 < 0) goto LAB_0465e408;
          *(int *)(param_1 + 0x14) = (int)*pcVar7;
          pcVar7 = pcVar7 + 1;
          *(char **)(param_2 + 8) = pcVar7;
        }
        else {
LAB_0465e408:
          uVar3 = FUN_05ab2ea0(param_2,param_1 + 0x14);
          if ((int)uVar3 == 0) {
            return uVar3;
          }
          pcVar7 = *(char **)(param_2 + 8);
          pcVar5 = *(char **)(param_2 + 0x10);
        }
        *(uint *)(param_1 + 0x34) = *(uint *)(param_1 + 0x34) | 4;
        if ((pcVar7 < pcVar5) && (*pcVar7 == ' ')) {
          pcVar7 = pcVar7 + 1;
          *(char **)(param_2 + 8) = pcVar7;
          if (pcVar7 < pcVar5) {
LAB_0465e44c:
            if (*pcVar7 < 0) goto LAB_0465e464;
            *(int *)(param_1 + 0x18) = (int)*pcVar7;
            pcVar7 = pcVar7 + 1;
            *(char **)(param_2 + 8) = pcVar7;
          }
          else {
LAB_0465e464:
            uVar3 = FUN_05ab2ea0(param_2,param_1 + 0x18);
            if ((int)uVar3 == 0) {
              return uVar3;
            }
            pcVar7 = *(char **)(param_2 + 8);
            pcVar5 = *(char **)(param_2 + 0x10);
          }
          *(uint *)(param_1 + 0x34) = *(uint *)(param_1 + 0x34) | 8;
          if ((pcVar7 < pcVar5) && (*pcVar7 == '(')) {
            pcVar7 = pcVar7 + 1;
            *(char **)(param_2 + 8) = pcVar7;
            if (pcVar7 < pcVar5) {
LAB_0465e4a8:
              if (*pcVar7 < 0) goto LAB_0465e4c0;
              *(int *)(param_1 + 0x1c) = (int)*pcVar7;
              pcVar7 = pcVar7 + 1;
              *(char **)(param_2 + 8) = pcVar7;
            }
            else {
LAB_0465e4c0:
              uVar3 = FUN_05ab2ea0(param_2,param_1 + 0x1c);
              if ((int)uVar3 == 0) {
                return uVar3;
              }
              pcVar7 = *(char **)(param_2 + 8);
              pcVar5 = *(char **)(param_2 + 0x10);
            }
            *(uint *)(param_1 + 0x34) = *(uint *)(param_1 + 0x34) | 0x10;
            if ((pcVar7 < pcVar5) && (*pcVar7 == '0')) {
              pcVar7 = pcVar7 + 1;
              *(char **)(param_2 + 8) = pcVar7;
              if (pcVar7 < pcVar5) {
LAB_0465e504:
                if (*pcVar7 < 0) goto LAB_0465e51c;
                *(int *)(param_1 + 0x20) = (int)*pcVar7;
                pcVar7 = pcVar7 + 1;
                *(char **)(param_2 + 8) = pcVar7;
              }
              else {
LAB_0465e51c:
                uVar3 = FUN_05ab2ea0(param_2,param_1 + 0x20);
                if ((int)uVar3 == 0) {
                  return uVar3;
                }
                pcVar7 = *(char **)(param_2 + 8);
                pcVar5 = *(char **)(param_2 + 0x10);
              }
              *(uint *)(param_1 + 0x34) = *(uint *)(param_1 + 0x34) | 0x20;
              if ((pcVar7 < pcVar5) && (*pcVar7 == '8')) {
                pcVar7 = pcVar7 + 1;
                *(char **)(param_2 + 8) = pcVar7;
                if (pcVar7 < pcVar5) {
LAB_0465e560:
                  if (*pcVar7 < 0) goto LAB_0465e578;
                  *(int *)(param_1 + 0x24) = (int)*pcVar7;
                  pcVar7 = pcVar7 + 1;
                  *(char **)(param_2 + 8) = pcVar7;
                }
                else {
LAB_0465e578:
                  uVar3 = FUN_05ab2ea0(param_2,param_1 + 0x24);
                  if ((int)uVar3 == 0) {
                    return uVar3;
                  }
                  pcVar7 = *(char **)(param_2 + 8);
                  pcVar5 = *(char **)(param_2 + 0x10);
                }
                *(uint *)(param_1 + 0x34) = *(uint *)(param_1 + 0x34) | 0x40;
                if ((pcVar7 < pcVar5) && (*pcVar7 == '@')) {
                  pcVar7 = pcVar7 + 1;
                  *(char **)(param_2 + 8) = pcVar7;
                  if (pcVar7 < pcVar5) {
LAB_0465e5bc:
                    if ((long)*pcVar7 < 0) goto LAB_0465e5d4;
                    *(long *)(param_1 + 0x28) = (long)*pcVar7;
                    pcVar7 = pcVar7 + 1;
                    *(char **)(param_2 + 8) = pcVar7;
                  }
                  else {
LAB_0465e5d4:
                    uVar3 = FUN_05ab2d58(param_2,param_1 + 0x28);
                    if ((int)uVar3 == 0) {
                      return uVar3;
                    }
                    pcVar7 = *(char **)(param_2 + 8);
                    pcVar5 = *(char **)(param_2 + 0x10);
                  }
                  *(uint *)(param_1 + 0x34) = *(uint *)(param_1 + 0x34) | 0x80;
                  if ((pcVar7 == pcVar5) &&
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
      }
    }
  } while( true );
}


