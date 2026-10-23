// Ghidra inferred pseudocode; requested=0x5ce5654
// entry=05ce5654 end=05ce5def

undefined8 FUN_05ce5654(long param_1,long param_2)

{
  char cVar1;
  int iVar2;
  undefined8 uVar3;
  ulong uVar4;
  char *pcVar5;
  char *pcVar6;
  uint uVar7;
  undefined8 *puVar8;
  int iStack_54;
  
LAB_05ce5698:
  do {
    pcVar6 = *(char **)(param_2 + 8);
    if (pcVar6 < *(char **)(param_2 + 0x10)) {
      cVar1 = *pcVar6;
      uVar4 = (ulong)cVar1;
      if (cVar1 < 0) goto LAB_05ce56c0;
      *(int *)(param_2 + 0x20) = (int)cVar1;
      *(char **)(param_2 + 8) = pcVar6 + 1;
      if (cVar1 == '\0') {
        return 1;
      }
    }
    else {
LAB_05ce56c0:
      uVar4 = FUN_05ab303c(param_2);
      *(int *)(param_2 + 0x20) = (int)uVar4;
      if ((int)uVar4 == 0) {
        return 1;
      }
    }
    uVar7 = (uint)uVar4 & 7;
    switch((uint)(uVar4 >> 3) & 0x1fffffff) {
    case 1:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        if ((pcVar6 < pcVar5) && (-1 < (long)*pcVar6)) {
          *(long *)(param_1 + 8) = (long)*pcVar6;
          pcVar6 = pcVar6 + 1;
          *(char **)(param_2 + 8) = pcVar6;
        }
        else {
          uVar3 = FUN_05ab2d58(param_2,param_1 + 8);
          if ((int)uVar3 == 0) {
            return uVar3;
          }
          pcVar6 = *(char **)(param_2 + 8);
          pcVar5 = *(char **)(param_2 + 0x10);
        }
        uVar7 = *(uint *)(param_1 + 0x44) | 1;
        *(uint *)(param_1 + 0x44) = uVar7;
        if ((pcVar6 < pcVar5) && (*pcVar6 == '\x12')) {
          *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x05ce5810:
          *(uint *)(param_1 + 0x44) = uVar7 | 2;
          puVar8 = *(undefined8 **)(param_1 + 0x10);
          if (puVar8 == &DAT_0a524ad0) {
            puVar8 = (undefined8 *)__Znwm(0x18);
            puVar8[1] = 0;
            puVar8[2] = 0;
            *puVar8 = 0;
            *(undefined8 **)(param_1 + 0x10) = puVar8;
          }
          uVar3 = FUN_05ab514c(param_2,puVar8);
          if ((int)uVar3 == 0) {
            return uVar3;
          }
          pcVar6 = *(char **)(param_2 + 8);
          pcVar5 = *(char **)(param_2 + 0x10);
          if ((pcVar6 < pcVar5) && (*pcVar6 == '\x18')) {
            pcVar6 = pcVar6 + 1;
            *(char **)(param_2 + 8) = pcVar6;
code_r0x05ce5868:
            if ((pcVar6 < pcVar5) && (cVar1 = *pcVar6, -1 < cVar1)) {
              pcVar6 = pcVar6 + 1;
              *(char **)(param_2 + 8) = pcVar6;
              iVar2 = (int)cVar1;
            }
            else {
              uVar3 = FUN_05ab2ea0(param_2,&iStack_54);
              if ((int)uVar3 == 0) {
                return uVar3;
              }
              pcVar6 = *(char **)(param_2 + 8);
              pcVar5 = *(char **)(param_2 + 0x10);
              iVar2 = iStack_54;
            }
            *(int *)(param_1 + 0x18) = iVar2;
            *(uint *)(param_1 + 0x44) = *(uint *)(param_1 + 0x44) | 4;
            if ((pcVar6 < pcVar5) && (*pcVar6 == ' ')) {
              pcVar6 = pcVar6 + 1;
              *(char **)(param_2 + 8) = pcVar6;
code_r0x05ce58c8:
              if ((pcVar6 < pcVar5) && (cVar1 = *pcVar6, -1 < cVar1)) {
                pcVar6 = pcVar6 + 1;
                *(char **)(param_2 + 8) = pcVar6;
                iVar2 = (int)cVar1;
              }
              else {
                uVar3 = FUN_05ab2ea0(param_2,&iStack_54);
                if ((int)uVar3 == 0) {
                  return uVar3;
                }
                pcVar6 = *(char **)(param_2 + 8);
                pcVar5 = *(char **)(param_2 + 0x10);
                iVar2 = iStack_54;
              }
              *(bool *)(param_1 + 0x28) = iVar2 != 0;
              *(uint *)(param_1 + 0x44) = *(uint *)(param_1 + 0x44) | 8;
              if ((pcVar6 < pcVar5) && (*pcVar6 == '(')) {
                pcVar6 = pcVar6 + 1;
                *(char **)(param_2 + 8) = pcVar6;
code_r0x05ce5930:
                if ((pcVar6 < pcVar5) && (cVar1 = *pcVar6, -1 < cVar1)) {
                  pcVar6 = pcVar6 + 1;
                  *(char **)(param_2 + 8) = pcVar6;
                  iVar2 = (int)cVar1;
                }
                else {
                  uVar3 = FUN_05ab2ea0(param_2,&iStack_54);
                  if ((int)uVar3 == 0) {
                    return uVar3;
                  }
                  pcVar6 = *(char **)(param_2 + 8);
                  pcVar5 = *(char **)(param_2 + 0x10);
                  iVar2 = iStack_54;
                }
                *(bool *)(param_1 + 0x29) = iVar2 != 0;
                *(uint *)(param_1 + 0x44) = *(uint *)(param_1 + 0x44) | 0x10;
                if ((pcVar6 < pcVar5) && (*pcVar6 == '0')) {
                  pcVar6 = pcVar6 + 1;
                  *(char **)(param_2 + 8) = pcVar6;
code_r0x05ce5998:
                  if ((pcVar6 < pcVar5) && (-1 < *pcVar6)) {
                    *(int *)(param_1 + 0x1c) = (int)*pcVar6;
                    pcVar6 = pcVar6 + 1;
                    *(char **)(param_2 + 8) = pcVar6;
                  }
                  else {
                    uVar3 = FUN_05ab2ea0(param_2,param_1 + 0x1c);
                    if ((int)uVar3 == 0) {
                      return uVar3;
                    }
                    pcVar6 = *(char **)(param_2 + 8);
                    pcVar5 = *(char **)(param_2 + 0x10);
                  }
                  uVar7 = *(uint *)(param_1 + 0x44) | 0x20;
                  *(uint *)(param_1 + 0x44) = uVar7;
                  if ((pcVar6 < pcVar5) && (*pcVar6 == ':')) {
                    *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x05ce59f4:
                    *(uint *)(param_1 + 0x44) = uVar7 | 0x40;
                    puVar8 = *(undefined8 **)(param_1 + 0x20);
                    if (puVar8 == &DAT_0a524ad0) {
                      puVar8 = (undefined8 *)__Znwm(0x18);
                      puVar8[1] = 0;
                      puVar8[2] = 0;
                      *puVar8 = 0;
                      *(undefined8 **)(param_1 + 0x20) = puVar8;
                    }
                    uVar3 = FUN_05ab514c(param_2,puVar8);
                    if ((int)uVar3 == 0) {
                      return uVar3;
                    }
                    pcVar6 = *(char **)(param_2 + 8);
                    pcVar5 = *(char **)(param_2 + 0x10);
                    if ((pcVar6 < pcVar5) && (*pcVar6 == '@')) {
                      pcVar6 = pcVar6 + 1;
                      *(char **)(param_2 + 8) = pcVar6;
code_r0x05ce5a4c:
                      if ((pcVar6 < pcVar5) && (cVar1 = *pcVar6, -1 < cVar1)) {
                        pcVar6 = pcVar6 + 1;
                        *(char **)(param_2 + 8) = pcVar6;
                        iVar2 = (int)cVar1;
                      }
                      else {
                        uVar3 = FUN_05ab2ea0(param_2,&iStack_54);
                        if ((int)uVar3 == 0) {
                          return uVar3;
                        }
                        pcVar6 = *(char **)(param_2 + 8);
                        pcVar5 = *(char **)(param_2 + 0x10);
                        iVar2 = iStack_54;
                      }
                      *(bool *)(param_1 + 0x2a) = iVar2 != 0;
                      *(uint *)(param_1 + 0x44) = *(uint *)(param_1 + 0x44) | 0x80;
                      if ((pcVar6 < pcVar5) && (*pcVar6 == 'H')) {
                        pcVar6 = pcVar6 + 1;
                        *(char **)(param_2 + 8) = pcVar6;
code_r0x05ce5ab4:
                        if ((pcVar6 < pcVar5) && (cVar1 = *pcVar6, -1 < cVar1)) {
                          pcVar6 = pcVar6 + 1;
                          *(char **)(param_2 + 8) = pcVar6;
                          iVar2 = (int)cVar1;
                        }
                        else {
                          uVar3 = FUN_05ab2ea0(param_2,&iStack_54);
                          if ((int)uVar3 == 0) {
                            return uVar3;
                          }
                          pcVar6 = *(char **)(param_2 + 8);
                          pcVar5 = *(char **)(param_2 + 0x10);
                          iVar2 = iStack_54;
                        }
                        *(bool *)(param_1 + 0x2b) = iVar2 != 0;
                        uVar7 = *(uint *)(param_1 + 0x44) | 0x100;
                        *(uint *)(param_1 + 0x44) = uVar7;
                        if ((pcVar6 < pcVar5) && (*pcVar6 == 'R')) {
                          *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x05ce5b1c:
                          *(uint *)(param_1 + 0x44) = uVar7 | 0x200;
                          puVar8 = *(undefined8 **)(param_1 + 0x30);
                          if (puVar8 == (undefined8 *)0x0) {
                            puVar8 = (undefined8 *)__Znwm(0x30);
                            *puVar8 = &PTR_FUN_09f476a8;
                            puVar8[1] = 0;
                            puVar8[2] = &DAT_0a524ad0;
                            puVar8[3] = &DAT_0a524ad0;
                            puVar8[4] = &DAT_0a524ad0;
                            puVar8[5] = 0;
                            *(undefined8 **)(param_1 + 0x30) = puVar8;
                          }
                          pcVar6 = *(char **)(param_2 + 8);
                          if ((pcVar6 < *(char **)(param_2 + 0x10)) && (cVar1 = *pcVar6, -1 < cVar1)
                             ) {
                            *(char **)(param_2 + 8) = pcVar6 + 1;
                            iStack_54 = (int)cVar1;
                          }
                          else {
                            iVar2 = FUN_05ab2ea0(param_2,&iStack_54);
                            if (iVar2 == 0) {
                              return 0;
                            }
                          }
                          iVar2 = *(int *)(param_2 + 0x38);
                          *(int *)(param_2 + 0x38) = iVar2 + 1;
                          if (*(int *)(param_2 + 0x3c) <= iVar2) {
                            return 0;
                          }
                          uVar3 = FUN_05ab26f0(param_2,iStack_54);
                          iVar2 = FUN_05ce458c(puVar8,param_2);
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
                          if ((pcVar6 < *(char **)(param_2 + 0x10)) && (*pcVar6 == 'Z')) {
                            *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x05ce5c04:
                            *(uint *)(param_1 + 0x44) = *(uint *)(param_1 + 0x44) | 0x400;
                            puVar8 = *(undefined8 **)(param_1 + 0x38);
                            if (puVar8 == (undefined8 *)0x0) {
                              puVar8 = (undefined8 *)__Znwm(0x28);
                              puVar8[2] = &DAT_0a524ad0;
                              puVar8[3] = 0;
                              *puVar8 = &PTR_FUN_09f47720;
                              puVar8[1] = &DAT_0a524ad0;
                              *(undefined4 *)(puVar8 + 4) = 0;
                              *(undefined8 **)(param_1 + 0x38) = puVar8;
                            }
                            pcVar6 = *(char **)(param_2 + 8);
                            if ((pcVar6 < *(char **)(param_2 + 0x10)) &&
                               (cVar1 = *pcVar6, -1 < cVar1)) {
                              *(char **)(param_2 + 8) = pcVar6 + 1;
                              iStack_54 = (int)cVar1;
                            }
                            else {
                              iVar2 = FUN_05ab2ea0(param_2,&iStack_54);
                              if (iVar2 == 0) {
                                return 0;
                              }
                            }
                            iVar2 = *(int *)(param_2 + 0x38);
                            *(int *)(param_2 + 0x38) = iVar2 + 1;
                            if (*(int *)(param_2 + 0x3c) <= iVar2) {
                              return 0;
                            }
                            uVar3 = FUN_05ab26f0(param_2,iStack_54);
                            iVar2 = FUN_05ce4d4c(puVar8,param_2);
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
                            if ((pcVar6 < pcVar5) && (*pcVar6 == '`')) {
                              pcVar6 = pcVar6 + 1;
                              *(char **)(param_2 + 8) = pcVar6;
code_r0x05ce5ce4:
                              if ((pcVar6 < pcVar5) && (cVar1 = *pcVar6, -1 < cVar1)) {
                                pcVar6 = pcVar6 + 1;
                                *(char **)(param_2 + 8) = pcVar6;
                                iVar2 = (int)cVar1;
                              }
                              else {
                                uVar3 = FUN_05ab2ea0(param_2,&iStack_54);
                                if ((int)uVar3 == 0) {
                                  return uVar3;
                                }
                                pcVar6 = *(char **)(param_2 + 8);
                                pcVar5 = *(char **)(param_2 + 0x10);
                                iVar2 = iStack_54;
                              }
                              *(bool *)(param_1 + 0x2c) = iVar2 != 0;
                              *(uint *)(param_1 + 0x44) = *(uint *)(param_1 + 0x44) | 0x800;
                              if ((pcVar6 < pcVar5) && (*pcVar6 == 'h')) {
                                pcVar6 = pcVar6 + 1;
                                *(char **)(param_2 + 8) = pcVar6;
code_r0x05ce5d4c:
                                if ((pcVar6 < pcVar5) && (cVar1 = *pcVar6, -1 < cVar1)) {
                                  pcVar6 = pcVar6 + 1;
                                  *(char **)(param_2 + 8) = pcVar6;
                                  iVar2 = (int)cVar1;
                                }
                                else {
                                  uVar3 = FUN_05ab2ea0(param_2,&iStack_54);
                                  if ((int)uVar3 == 0) {
                                    return uVar3;
                                  }
                                  pcVar6 = *(char **)(param_2 + 8);
                                  pcVar5 = *(char **)(param_2 + 0x10);
                                  iVar2 = iStack_54;
                                }
                                *(bool *)(param_1 + 0x2d) = iVar2 != 0;
                                *(uint *)(param_1 + 0x44) = *(uint *)(param_1 + 0x44) | 0x1000;
                                if ((pcVar6 == pcVar5) &&
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
        goto LAB_05ce5698;
      }
      break;
    case 2:
      if (uVar7 == 2) {
        uVar7 = *(uint *)(param_1 + 0x44);
        goto code_r0x05ce5810;
      }
      break;
    case 3:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05ce5868;
      }
      break;
    case 4:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05ce58c8;
      }
      break;
    case 5:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05ce5930;
      }
      break;
    case 6:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05ce5998;
      }
      break;
    case 7:
      if (uVar7 == 2) {
        uVar7 = *(uint *)(param_1 + 0x44);
        goto code_r0x05ce59f4;
      }
      break;
    case 8:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05ce5a4c;
      }
      break;
    case 9:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05ce5ab4;
      }
      break;
    case 10:
      if (uVar7 == 2) {
        uVar7 = *(uint *)(param_1 + 0x44);
        goto code_r0x05ce5b1c;
      }
      break;
    case 0xb:
      if (uVar7 == 2) goto code_r0x05ce5c04;
      break;
    case 0xc:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05ce5ce4;
      }
      break;
    case 0xd:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05ce5d4c;
      }
    }
    if (uVar7 == 4) {
      return 1;
    }
    uVar4 = FUN_05ab4aac(param_2);
    if ((uVar4 & 1) == 0) {
      return 0;
    }
  } while( true );
}


