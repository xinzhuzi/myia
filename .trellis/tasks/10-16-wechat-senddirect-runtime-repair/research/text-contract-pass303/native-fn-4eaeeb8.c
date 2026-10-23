// Ghidra inferred pseudocode; requested=0x4eaeeb8
// entry=04eaeeb8 end=04eafbbb

undefined8 FUN_04eaeeb8(long param_1,long param_2)

{
  char cVar1;
  int iVar2;
  undefined8 uVar3;
  ulong uVar4;
  char *pcVar5;
  char *pcVar6;
  uint uVar7;
  undefined8 *puVar8;
  int iStack_64;
  
LAB_04eaef0c:
  pcVar6 = *(char **)(param_2 + 8);
  if (pcVar6 < *(char **)(param_2 + 0x10)) {
    cVar1 = *pcVar6;
    uVar4 = (ulong)cVar1;
    if (cVar1 < 0) goto LAB_04eaef34;
    *(int *)(param_2 + 0x20) = (int)cVar1;
    *(char **)(param_2 + 8) = pcVar6 + 1;
    if (cVar1 == '\0') {
      return 1;
    }
  }
  else {
LAB_04eaef34:
    uVar4 = FUN_05ab303c(param_2);
    *(int *)(param_2 + 0x20) = (int)uVar4;
    if ((int)uVar4 == 0) {
      return 1;
    }
  }
  uVar7 = (uint)uVar4 & 7;
  switch((uint)(uVar4 >> 3) & 0x1fffffff) {
  case 1:
    if ((uVar4 & 7) != 0) break;
    pcVar6 = *(char **)(param_2 + 8);
    pcVar5 = *(char **)(param_2 + 0x10);
    if ((pcVar6 < pcVar5) && (-1 < *pcVar6)) {
      *(int *)(param_1 + 8) = (int)*pcVar6;
      pcVar6 = pcVar6 + 1;
      *(char **)(param_2 + 8) = pcVar6;
    }
    else {
      uVar3 = FUN_05ab2ea0(param_2,param_1 + 8);
      if ((int)uVar3 == 0) {
        return uVar3;
      }
      pcVar6 = *(char **)(param_2 + 8);
      pcVar5 = *(char **)(param_2 + 0x10);
    }
    *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 1;
    if ((pcVar6 < pcVar5) && (*pcVar6 == '\x10')) {
      pcVar6 = pcVar6 + 1;
      *(char **)(param_2 + 8) = pcVar6;
      if (pcVar6 < pcVar5) {
code_r0x04eaf0a0:
        if (*pcVar6 < 0) goto code_r0x04eaf0b8;
        *(int *)(param_1 + 0xc) = (int)*pcVar6;
        pcVar6 = pcVar6 + 1;
        *(char **)(param_2 + 8) = pcVar6;
      }
      else {
code_r0x04eaf0b8:
        uVar3 = FUN_05ab2ea0(param_2,param_1 + 0xc);
        if ((int)uVar3 == 0) {
          return uVar3;
        }
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
      }
      uVar7 = *(uint *)(param_1 + 0x74) | 2;
      *(uint *)(param_1 + 0x74) = uVar7;
      if ((pcVar6 < pcVar5) && (*pcVar6 == '\x1a')) {
        *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x04eaf0f4:
        *(uint *)(param_1 + 0x74) = uVar7 | 4;
        puVar8 = *(undefined8 **)(param_1 + 0x10);
        if (puVar8 == (undefined8 *)0x0) {
          puVar8 = (undefined8 *)__Znwm(0x28);
          *puVar8 = &PTR_FUN_09ec3b98;
          puVar8[1] = 0;
          puVar8[2] = &DAT_0a524ad0;
          puVar8[3] = &DAT_0a524ad0;
          puVar8[4] = 0;
          *(undefined8 **)(param_1 + 0x10) = puVar8;
        }
        iStack_64 = -0x55555556;
        pcVar6 = *(char **)(param_2 + 8);
        if ((pcVar6 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar6, -1 < cVar1)) {
          *(char **)(param_2 + 8) = pcVar6 + 1;
          iStack_64 = (int)cVar1;
        }
        else {
          iVar2 = FUN_05ab2ea0(param_2,&iStack_64);
          if (iVar2 == 0) {
            return 0;
          }
        }
        iVar2 = *(int *)(param_2 + 0x38);
        *(int *)(param_2 + 0x38) = iVar2 + 1;
        if (*(int *)(param_2 + 0x3c) <= iVar2) {
          return 0;
        }
        uVar3 = FUN_05ab26f0(param_2,iStack_64);
        iVar2 = FUN_04ea7100(puVar8,param_2);
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
        pcVar6 = *(char **)(param_2 + 8);
        if ((pcVar6 < *(char **)(param_2 + 0x10)) && (*pcVar6 == '\"')) {
          *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x04eaf1e4:
          *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 8;
          puVar8 = *(undefined8 **)(param_1 + 0x18);
          if (puVar8 == (undefined8 *)0x0) {
            puVar8 = (undefined8 *)__Znwm(0x40);
            puVar8[1] = 0;
            puVar8[2] = 0;
            *puVar8 = &PTR_FUN_09ec3c10;
            *(undefined8 *)((long)puVar8 + 0x15) = 0;
            puVar8[4] = &DAT_0a524ad0;
            puVar8[5] = &DAT_0a524ad0;
            puVar8[6] = 0;
            *(undefined4 *)(puVar8 + 7) = 0;
            *(undefined8 **)(param_1 + 0x18) = puVar8;
          }
          iStack_64 = -0x55555556;
          pcVar6 = *(char **)(param_2 + 8);
          if ((pcVar6 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar6, -1 < cVar1)) {
            *(char **)(param_2 + 8) = pcVar6 + 1;
            iStack_64 = (int)cVar1;
          }
          else {
            iVar2 = FUN_05ab2ea0(param_2,&iStack_64);
            if (iVar2 == 0) {
              return 0;
            }
          }
          iVar2 = *(int *)(param_2 + 0x38);
          *(int *)(param_2 + 0x38) = iVar2 + 1;
          if (*(int *)(param_2 + 0x3c) <= iVar2) {
            return 0;
          }
          uVar3 = FUN_05ab26f0(param_2,iStack_64);
          iVar2 = FUN_04ea7aa8(puVar8,param_2);
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
          pcVar6 = *(char **)(param_2 + 8);
          if ((pcVar6 < *(char **)(param_2 + 0x10)) && (*pcVar6 == '*')) {
            *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x04eaf2dc:
            *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x10;
            puVar8 = *(undefined8 **)(param_1 + 0x20);
            if (puVar8 == (undefined8 *)0x0) {
              puVar8 = (undefined8 *)__Znwm(0x20);
              puVar8[1] = &DAT_0a524ad0;
              puVar8[2] = 0;
              *puVar8 = &PTR_FUN_09ec3d78;
              *(undefined4 *)(puVar8 + 3) = 0;
              *(undefined8 **)(param_1 + 0x20) = puVar8;
            }
            iStack_64 = -0x55555556;
            pcVar6 = *(char **)(param_2 + 8);
            if ((pcVar6 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar6, -1 < cVar1)) {
              *(char **)(param_2 + 8) = pcVar6 + 1;
              iStack_64 = (int)cVar1;
            }
            else {
              iVar2 = FUN_05ab2ea0(param_2,&iStack_64);
              if (iVar2 == 0) {
                return 0;
              }
            }
            iVar2 = *(int *)(param_2 + 0x38);
            *(int *)(param_2 + 0x38) = iVar2 + 1;
            if (*(int *)(param_2 + 0x3c) <= iVar2) {
              return 0;
            }
            uVar3 = FUN_05ab26f0(param_2,iStack_64);
            iVar2 = FUN_04ea9934(puVar8,param_2);
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
            pcVar6 = *(char **)(param_2 + 8);
            if ((pcVar6 < *(char **)(param_2 + 0x10)) && (*pcVar6 == '2')) {
              *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x04eaf3c8:
              *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x20;
              puVar8 = *(undefined8 **)(param_1 + 0x28);
              if (puVar8 == (undefined8 *)0x0) {
                puVar8 = (undefined8 *)__Znwm(0x38);
                puVar8[4] = &DAT_0a524ad0;
                puVar8[5] = 0;
                *puVar8 = &PTR_FUN_09ec3df0;
                puVar8[1] = &DAT_0a524ad0;
                puVar8[2] = &DAT_0a524ad0;
                puVar8[3] = &DAT_0a524ad0;
                *(undefined4 *)(puVar8 + 6) = 0;
                *(undefined8 **)(param_1 + 0x28) = puVar8;
              }
              iStack_64 = -0x55555556;
              pcVar6 = *(char **)(param_2 + 8);
              if ((pcVar6 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar6, -1 < cVar1)) {
                *(char **)(param_2 + 8) = pcVar6 + 1;
                iStack_64 = (int)cVar1;
              }
              else {
                iVar2 = FUN_05ab2ea0(param_2,&iStack_64);
                if (iVar2 == 0) {
                  return 0;
                }
              }
              iVar2 = *(int *)(param_2 + 0x38);
              *(int *)(param_2 + 0x38) = iVar2 + 1;
              if (*(int *)(param_2 + 0x3c) <= iVar2) {
                return 0;
              }
              uVar3 = FUN_05ab26f0(param_2,iStack_64);
              iVar2 = FUN_04eaa27c(puVar8,param_2);
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
              pcVar6 = *(char **)(param_2 + 8);
              if ((pcVar6 < *(char **)(param_2 + 0x10)) && (*pcVar6 == ':')) {
                *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x04eaf4b8:
                *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x40;
                puVar8 = *(undefined8 **)(param_1 + 0x30);
                if (puVar8 == (undefined8 *)0x0) {
                  puVar8 = (undefined8 *)__Znwm(0x38);
                  puVar8[1] = 0;
                  puVar8[2] = 0;
                  *puVar8 = &PTR_thunk_FUN_04ea8dd8_09ec3d00;
                  *(undefined4 *)(puVar8 + 3) = 0;
                  puVar8[4] = &DAT_0a524ad0;
                  puVar8[5] = 0;
                  *(undefined4 *)(puVar8 + 6) = 0;
                  *(undefined8 **)(param_1 + 0x30) = puVar8;
                }
                iStack_64 = -0x55555556;
                pcVar6 = *(char **)(param_2 + 8);
                if ((pcVar6 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar6, -1 < cVar1)) {
                  *(char **)(param_2 + 8) = pcVar6 + 1;
                  iStack_64 = (int)cVar1;
                }
                else {
                  iVar2 = FUN_05ab2ea0(param_2,&iStack_64);
                  if (iVar2 == 0) {
                    return 0;
                  }
                }
                iVar2 = *(int *)(param_2 + 0x38);
                *(int *)(param_2 + 0x38) = iVar2 + 1;
                if (*(int *)(param_2 + 0x3c) <= iVar2) {
                  return 0;
                }
                uVar3 = FUN_05ab26f0(param_2,iStack_64);
                iVar2 = FUN_04ea8f84(puVar8,param_2);
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
                pcVar6 = *(char **)(param_2 + 8);
                if ((pcVar6 < *(char **)(param_2 + 0x10)) && (*pcVar6 == 'B')) {
                  *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x04eaf5ac:
                  *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x80;
                  puVar8 = *(undefined8 **)(param_1 + 0x38);
                  if (puVar8 == (undefined8 *)0x0) {
                    puVar8 = (undefined8 *)__Znwm(0x40);
                    *puVar8 = &PTR_FUN_09ec3e68;
                    puVar8[1] = 0;
                    puVar8[2] = 0;
                    puVar8[3] = &DAT_0a524ad0;
                    puVar8[4] = &DAT_0a524ad0;
                    puVar8[5] = 0;
                    puVar8[6] = 0;
                    *(undefined4 *)(puVar8 + 7) = 0;
                    *(undefined8 **)(param_1 + 0x38) = puVar8;
                  }
                  iStack_64 = -0x55555556;
                  pcVar6 = *(char **)(param_2 + 8);
                  if ((pcVar6 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar6, -1 < cVar1)) {
                    *(char **)(param_2 + 8) = pcVar6 + 1;
                    iStack_64 = (int)cVar1;
                  }
                  else {
                    iVar2 = FUN_05ab2ea0(param_2,&iStack_64);
                    if (iVar2 == 0) {
                      return 0;
                    }
                  }
                  iVar2 = *(int *)(param_2 + 0x38);
                  *(int *)(param_2 + 0x38) = iVar2 + 1;
                  if (*(int *)(param_2 + 0x3c) <= iVar2) {
                    return 0;
                  }
                  uVar3 = FUN_05ab26f0(param_2,iStack_64);
                  iVar2 = FUN_04eaada8(puVar8,param_2);
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
                  pcVar6 = *(char **)(param_2 + 8);
                  if ((pcVar6 < *(char **)(param_2 + 0x10)) && (*pcVar6 == 'J')) {
                    *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x04eaf6a0:
                    *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x100;
                    puVar8 = *(undefined8 **)(param_1 + 0x40);
                    if (puVar8 == (undefined8 *)0x0) {
                      puVar8 = (undefined8 *)__Znwm(0x18);
                      *puVar8 = &PTR_FUN_09ec3ee0;
                      puVar8[1] = &DAT_0a524ad0;
                      puVar8[2] = 0;
                      *(undefined8 **)(param_1 + 0x40) = puVar8;
                    }
                    iStack_64 = -0x55555556;
                    pcVar6 = *(char **)(param_2 + 8);
                    if ((pcVar6 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar6, -1 < cVar1)) {
                      *(char **)(param_2 + 8) = pcVar6 + 1;
                      iStack_64 = (int)cVar1;
                    }
                    else {
                      iVar2 = FUN_05ab2ea0(param_2,&iStack_64);
                      if (iVar2 == 0) {
                        return 0;
                      }
                    }
                    iVar2 = *(int *)(param_2 + 0x38);
                    *(int *)(param_2 + 0x38) = iVar2 + 1;
                    if (*(int *)(param_2 + 0x3c) <= iVar2) {
                      return 0;
                    }
                    uVar3 = FUN_05ab26f0(param_2,iStack_64);
                    iVar2 = FUN_04eabab8(puVar8,param_2);
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
                    pcVar6 = *(char **)(param_2 + 8);
                    if ((pcVar6 < *(char **)(param_2 + 0x10)) && (*pcVar6 == 'R')) {
                      *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x04eaf788:
                      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x200;
                      puVar8 = *(undefined8 **)(param_1 + 0x48);
                      if (puVar8 == (undefined8 *)0x0) {
                        puVar8 = (undefined8 *)__Znwm(0x18);
                        *puVar8 = &PTR_FUN_09ec3f58;
                        puVar8[1] = 0;
                        *(undefined4 *)(puVar8 + 2) = 0;
                        *(undefined8 **)(param_1 + 0x48) = puVar8;
                      }
                      iStack_64 = -0x55555556;
                      pcVar6 = *(char **)(param_2 + 8);
                      if ((pcVar6 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar6, -1 < cVar1)) {
                        *(char **)(param_2 + 8) = pcVar6 + 1;
                        iStack_64 = (int)cVar1;
                      }
                      else {
                        iVar2 = FUN_05ab2ea0(param_2,&iStack_64);
                        if (iVar2 == 0) {
                          return 0;
                        }
                      }
                      iVar2 = *(int *)(param_2 + 0x38);
                      *(int *)(param_2 + 0x38) = iVar2 + 1;
                      if (*(int *)(param_2 + 0x3c) <= iVar2) {
                        return 0;
                      }
                      uVar3 = FUN_05ab26f0(param_2,iStack_64);
                      iVar2 = FUN_04eabfac(puVar8,param_2);
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
                      pcVar6 = *(char **)(param_2 + 8);
                      pcVar5 = *(char **)(param_2 + 0x10);
                      if ((pcVar6 < pcVar5) && (*pcVar6 == 'X')) {
                        pcVar6 = pcVar6 + 1;
                        *(char **)(param_2 + 8) = pcVar6;
                        if (pcVar6 < pcVar5) {
code_r0x04eaf878:
                          if ((long)*pcVar6 < 0) goto code_r0x04eaf890;
                          *(long *)(param_1 + 0x50) = (long)*pcVar6;
                          pcVar6 = pcVar6 + 1;
                          *(char **)(param_2 + 8) = pcVar6;
                        }
                        else {
code_r0x04eaf890:
                          uVar3 = FUN_05ab2d58(param_2,param_1 + 0x50);
                          if ((int)uVar3 == 0) {
                            return uVar3;
                          }
                          pcVar6 = *(char **)(param_2 + 8);
                          pcVar5 = *(char **)(param_2 + 0x10);
                        }
                        uVar7 = *(uint *)(param_1 + 0x74) | 0x400;
                        *(uint *)(param_1 + 0x74) = uVar7;
                        if ((pcVar6 < pcVar5) && (*pcVar6 == 'b')) {
                          *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x04eaf8cc:
                          *(uint *)(param_1 + 0x74) = uVar7 | 0x800;
                          puVar8 = *(undefined8 **)(param_1 + 0x58);
                          if (puVar8 == (undefined8 *)0x0) {
                            puVar8 = (undefined8 *)__Znwm(0x30);
                            *(undefined4 *)(puVar8 + 2) = 0;
                            *puVar8 = &PTR_FUN_09ec40c0;
                            puVar8[1] = 0;
                            *(undefined1 *)((long)puVar8 + 0x14) = 0;
                            puVar8[4] = 0;
                            puVar8[5] = 0;
                            puVar8[3] = 0;
                            *(undefined8 **)(param_1 + 0x58) = puVar8;
                          }
                          iStack_64 = -0x55555556;
                          pcVar6 = *(char **)(param_2 + 8);
                          if ((pcVar6 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar6, -1 < cVar1)
                             ) {
                            *(char **)(param_2 + 8) = pcVar6 + 1;
                            iStack_64 = (int)cVar1;
                          }
                          else {
                            iVar2 = FUN_05ab2ea0(param_2,&iStack_64);
                            if (iVar2 == 0) {
                              return 0;
                            }
                          }
                          iVar2 = *(int *)(param_2 + 0x38);
                          *(int *)(param_2 + 0x38) = iVar2 + 1;
                          if (*(int *)(param_2 + 0x3c) <= iVar2) {
                            return 0;
                          }
                          uVar3 = FUN_05ab26f0(param_2,iStack_64);
                          iVar2 = FUN_04eacfe4(puVar8,param_2);
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
                          pcVar6 = *(char **)(param_2 + 8);
                          if ((pcVar6 < *(char **)(param_2 + 0x10)) && (*pcVar6 == 'j')) {
                            *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x04eaf9b4:
                            *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x1000;
                            puVar8 = *(undefined8 **)(param_1 + 0x60);
                            if (puVar8 == (undefined8 *)0x0) {
                              puVar8 = (undefined8 *)__Znwm(0x18);
                              *puVar8 = &PTR_FUN_09ec4138;
                              *(undefined8 *)((long)puVar8 + 0xc) = 0;
                              *(undefined2 *)(puVar8 + 1) = 0;
                              *(undefined8 **)(param_1 + 0x60) = puVar8;
                            }
                            iStack_64 = -0x55555556;
                            pcVar6 = *(char **)(param_2 + 8);
                            if ((pcVar6 < *(char **)(param_2 + 0x10)) &&
                               (cVar1 = *pcVar6, -1 < cVar1)) {
                              *(char **)(param_2 + 8) = pcVar6 + 1;
                              iStack_64 = (int)cVar1;
                            }
                            else {
                              iVar2 = FUN_05ab2ea0(param_2,&iStack_64);
                              if (iVar2 == 0) {
                                return 0;
                              }
                            }
                            iVar2 = *(int *)(param_2 + 0x38);
                            *(int *)(param_2 + 0x38) = iVar2 + 1;
                            if (*(int *)(param_2 + 0x3c) <= iVar2) {
                              return 0;
                            }
                            uVar3 = FUN_05ab26f0(param_2,iStack_64);
                            iVar2 = FUN_04ead9d8(puVar8,param_2);
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
                            pcVar6 = *(char **)(param_2 + 8);
                            if ((pcVar6 < *(char **)(param_2 + 0x10)) && (*pcVar6 == 'r')) {
                              *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x04eafa98:
                              *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x2000;
                              puVar8 = *(undefined8 **)(param_1 + 0x68);
                              if (puVar8 == (undefined8 *)0x0) {
                                puVar8 = (undefined8 *)__Znwm(0x18);
                                *puVar8 = &PTR_FUN_09ec41b0;
                                *(undefined8 *)((long)puVar8 + 0xc) = 0;
                                *(undefined1 *)(puVar8 + 1) = 0;
                                *(undefined8 **)(param_1 + 0x68) = puVar8;
                              }
                              iStack_64 = -0x55555556;
                              pcVar6 = *(char **)(param_2 + 8);
                              if ((pcVar6 < *(char **)(param_2 + 0x10)) &&
                                 (cVar1 = *pcVar6, -1 < cVar1)) {
                                *(char **)(param_2 + 8) = pcVar6 + 1;
                                iStack_64 = (int)cVar1;
                              }
                              else {
                                iVar2 = FUN_05ab2ea0(param_2,&iStack_64);
                                if (iVar2 == 0) {
                                  return 0;
                                }
                              }
                              iVar2 = *(int *)(param_2 + 0x38);
                              *(int *)(param_2 + 0x38) = iVar2 + 1;
                              if (*(int *)(param_2 + 0x3c) <= iVar2) {
                                return 0;
                              }
                              uVar3 = FUN_05ab26f0(param_2,iStack_64);
                              iVar2 = FUN_04eadf40(puVar8,param_2);
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
              }
            }
          }
        }
      }
    }
    goto LAB_04eaef0c;
  case 2:
    if ((uVar4 & 7) == 0) {
      pcVar6 = *(char **)(param_2 + 8);
      pcVar5 = *(char **)(param_2 + 0x10);
      if (pcVar6 < pcVar5) goto code_r0x04eaf0a0;
      goto code_r0x04eaf0b8;
    }
    break;
  case 3:
    if (uVar7 == 2) {
      uVar7 = *(uint *)(param_1 + 0x74);
      goto code_r0x04eaf0f4;
    }
    break;
  case 4:
    if (uVar7 == 2) goto code_r0x04eaf1e4;
    break;
  case 5:
    if (uVar7 == 2) goto code_r0x04eaf2dc;
    break;
  case 6:
    if (uVar7 == 2) goto code_r0x04eaf3c8;
    break;
  case 7:
    if (uVar7 == 2) goto code_r0x04eaf4b8;
    break;
  case 8:
    if (uVar7 == 2) goto code_r0x04eaf5ac;
    break;
  case 9:
    if (uVar7 == 2) goto code_r0x04eaf6a0;
    break;
  case 10:
    if (uVar7 == 2) goto code_r0x04eaf788;
    break;
  case 0xb:
    if ((uVar4 & 7) == 0) {
      pcVar6 = *(char **)(param_2 + 8);
      pcVar5 = *(char **)(param_2 + 0x10);
      if (pcVar6 < pcVar5) goto code_r0x04eaf878;
      goto code_r0x04eaf890;
    }
    break;
  case 0xc:
    if (uVar7 == 2) {
      uVar7 = *(uint *)(param_1 + 0x74);
      goto code_r0x04eaf8cc;
    }
    break;
  case 0xd:
    if (uVar7 == 2) goto code_r0x04eaf9b4;
    break;
  case 0xe:
    if (uVar7 == 2) goto code_r0x04eafa98;
  }
  if (uVar7 == 4) {
    return 1;
  }
  uVar4 = FUN_05ab4aac(param_2);
  if ((uVar4 & 1) == 0) {
    return 0;
  }
  goto LAB_04eaef0c;
}


