// Ghidra inferred pseudocode; requested=0x5564bd8
// entry=05564bd8 end=055653ab

undefined8 FUN_05564bd8(long param_1,long param_2)

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
  
LAB_05564c24:
  do {
    pcVar6 = *(char **)(param_2 + 8);
    if (pcVar6 < *(char **)(param_2 + 0x10)) {
      cVar1 = *pcVar6;
      uVar4 = (ulong)cVar1;
      if (cVar1 < 0) goto LAB_05564c4c;
      *(int *)(param_2 + 0x20) = (int)cVar1;
      *(char **)(param_2 + 8) = pcVar6 + 1;
      if (cVar1 == '\0') {
        return 1;
      }
    }
    else {
LAB_05564c4c:
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
code_r0x05564da4:
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
code_r0x05564dfc:
            iStack_64 = -0x55555556;
            if ((pcVar6 < pcVar5) && (cVar1 = *pcVar6, -1 < cVar1)) {
              pcVar6 = pcVar6 + 1;
              *(char **)(param_2 + 8) = pcVar6;
              iVar2 = (int)cVar1;
            }
            else {
              uVar3 = FUN_05ab2ea0(param_2,&iStack_64);
              if ((int)uVar3 == 0) {
                return uVar3;
              }
              pcVar6 = *(char **)(param_2 + 8);
              pcVar5 = *(char **)(param_2 + 0x10);
              iVar2 = iStack_64;
            }
            *(int *)(param_1 + 0x18) = iVar2;
            *(uint *)(param_1 + 0x44) = *(uint *)(param_1 + 0x44) | 4;
            if ((pcVar6 < pcVar5) && (*pcVar6 == ' ')) {
              pcVar6 = pcVar6 + 1;
              *(char **)(param_2 + 8) = pcVar6;
code_r0x05564e60:
              iStack_64 = -0x55555556;
              if ((pcVar6 < pcVar5) && (cVar1 = *pcVar6, -1 < cVar1)) {
                pcVar6 = pcVar6 + 1;
                *(char **)(param_2 + 8) = pcVar6;
                iVar2 = (int)cVar1;
              }
              else {
                uVar3 = FUN_05ab2ea0(param_2,&iStack_64);
                if ((int)uVar3 == 0) {
                  return uVar3;
                }
                pcVar6 = *(char **)(param_2 + 8);
                pcVar5 = *(char **)(param_2 + 0x10);
                iVar2 = iStack_64;
              }
              *(bool *)(param_1 + 0x28) = iVar2 != 0;
              *(uint *)(param_1 + 0x44) = *(uint *)(param_1 + 0x44) | 8;
              if ((pcVar6 < pcVar5) && (*pcVar6 == '(')) {
                pcVar6 = pcVar6 + 1;
                *(char **)(param_2 + 8) = pcVar6;
code_r0x05564ecc:
                iStack_64 = -0x55555556;
                if ((pcVar6 < pcVar5) && (cVar1 = *pcVar6, -1 < cVar1)) {
                  pcVar6 = pcVar6 + 1;
                  *(char **)(param_2 + 8) = pcVar6;
                  iVar2 = (int)cVar1;
                }
                else {
                  uVar3 = FUN_05ab2ea0(param_2,&iStack_64);
                  if ((int)uVar3 == 0) {
                    return uVar3;
                  }
                  pcVar6 = *(char **)(param_2 + 8);
                  pcVar5 = *(char **)(param_2 + 0x10);
                  iVar2 = iStack_64;
                }
                *(bool *)(param_1 + 0x29) = iVar2 != 0;
                *(uint *)(param_1 + 0x44) = *(uint *)(param_1 + 0x44) | 0x10;
                if ((pcVar6 < pcVar5) && (*pcVar6 == '0')) {
                  pcVar6 = pcVar6 + 1;
                  *(char **)(param_2 + 8) = pcVar6;
                  if (pcVar6 < pcVar5) {
code_r0x05564f40:
                    if (*pcVar6 < 0) goto code_r0x05564f58;
                    *(int *)(param_1 + 0x1c) = (int)*pcVar6;
                    pcVar6 = pcVar6 + 1;
                    *(char **)(param_2 + 8) = pcVar6;
                  }
                  else {
code_r0x05564f58:
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
code_r0x05564f94:
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
code_r0x05564fec:
                      iStack_64 = -0x55555556;
                      if ((pcVar6 < pcVar5) && (cVar1 = *pcVar6, -1 < cVar1)) {
                        pcVar6 = pcVar6 + 1;
                        *(char **)(param_2 + 8) = pcVar6;
                        iVar2 = (int)cVar1;
                      }
                      else {
                        uVar3 = FUN_05ab2ea0(param_2,&iStack_64);
                        if ((int)uVar3 == 0) {
                          return uVar3;
                        }
                        pcVar6 = *(char **)(param_2 + 8);
                        pcVar5 = *(char **)(param_2 + 0x10);
                        iVar2 = iStack_64;
                      }
                      *(bool *)(param_1 + 0x2a) = iVar2 != 0;
                      *(uint *)(param_1 + 0x44) = *(uint *)(param_1 + 0x44) | 0x80;
                      if ((pcVar6 < pcVar5) && (*pcVar6 == 'H')) {
                        pcVar6 = pcVar6 + 1;
                        *(char **)(param_2 + 8) = pcVar6;
code_r0x05565058:
                        iStack_64 = -0x55555556;
                        if ((pcVar6 < pcVar5) && (cVar1 = *pcVar6, -1 < cVar1)) {
                          pcVar6 = pcVar6 + 1;
                          *(char **)(param_2 + 8) = pcVar6;
                          iVar2 = (int)cVar1;
                        }
                        else {
                          uVar3 = FUN_05ab2ea0(param_2,&iStack_64);
                          if ((int)uVar3 == 0) {
                            return uVar3;
                          }
                          pcVar6 = *(char **)(param_2 + 8);
                          pcVar5 = *(char **)(param_2 + 0x10);
                          iVar2 = iStack_64;
                        }
                        *(bool *)(param_1 + 0x2b) = iVar2 != 0;
                        uVar7 = *(uint *)(param_1 + 0x44) | 0x100;
                        *(uint *)(param_1 + 0x44) = uVar7;
                        if ((pcVar6 < pcVar5) && (*pcVar6 == 'R')) {
                          *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x055650c4:
                          *(uint *)(param_1 + 0x44) = uVar7 | 0x200;
                          puVar8 = *(undefined8 **)(param_1 + 0x30);
                          if (puVar8 == (undefined8 *)0x0) {
                            puVar8 = (undefined8 *)__Znwm(0x30);
                            *puVar8 = &PTR_FUN_09f0cbe8;
                            puVar8[1] = 0;
                            puVar8[2] = &DAT_0a524ad0;
                            puVar8[3] = &DAT_0a524ad0;
                            puVar8[4] = &DAT_0a524ad0;
                            puVar8[5] = 0;
                            *(undefined8 **)(param_1 + 0x30) = puVar8;
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
                          iVar2 = FUN_0556356c(puVar8,param_2);
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
code_r0x055651b0:
                            *(uint *)(param_1 + 0x44) = *(uint *)(param_1 + 0x44) | 0x400;
                            puVar8 = *(undefined8 **)(param_1 + 0x38);
                            if (puVar8 == (undefined8 *)0x0) {
                              puVar8 = (undefined8 *)__Znwm(0x28);
                              puVar8[2] = &DAT_0a524ad0;
                              puVar8[3] = 0;
                              *puVar8 = &PTR_FUN_09f0cc60;
                              puVar8[1] = &DAT_0a524ad0;
                              *(undefined4 *)(puVar8 + 4) = 0;
                              *(undefined8 **)(param_1 + 0x38) = puVar8;
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
                            iVar2 = FUN_05563f4c(puVar8,param_2);
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
code_r0x05565294:
                              iStack_64 = -0x55555556;
                              if ((pcVar6 < pcVar5) && (cVar1 = *pcVar6, -1 < cVar1)) {
                                pcVar6 = pcVar6 + 1;
                                *(char **)(param_2 + 8) = pcVar6;
                                iVar2 = (int)cVar1;
                              }
                              else {
                                uVar3 = FUN_05ab2ea0(param_2,&iStack_64);
                                if ((int)uVar3 == 0) {
                                  return uVar3;
                                }
                                pcVar6 = *(char **)(param_2 + 8);
                                pcVar5 = *(char **)(param_2 + 0x10);
                                iVar2 = iStack_64;
                              }
                              *(bool *)(param_1 + 0x2c) = iVar2 != 0;
                              *(uint *)(param_1 + 0x44) = *(uint *)(param_1 + 0x44) | 0x800;
                              if ((pcVar6 < pcVar5) && (*pcVar6 == 'h')) {
                                pcVar6 = pcVar6 + 1;
                                *(char **)(param_2 + 8) = pcVar6;
code_r0x05565300:
                                iStack_64 = -0x55555556;
                                if ((pcVar6 < pcVar5) && (cVar1 = *pcVar6, -1 < cVar1)) {
                                  pcVar6 = pcVar6 + 1;
                                  *(char **)(param_2 + 8) = pcVar6;
                                  iVar2 = (int)cVar1;
                                }
                                else {
                                  uVar3 = FUN_05ab2ea0(param_2,&iStack_64);
                                  if ((int)uVar3 == 0) {
                                    return uVar3;
                                  }
                                  pcVar6 = *(char **)(param_2 + 8);
                                  pcVar5 = *(char **)(param_2 + 0x10);
                                  iVar2 = iStack_64;
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
        goto LAB_05564c24;
      }
      break;
    case 2:
      if (uVar7 == 2) {
        uVar7 = *(uint *)(param_1 + 0x44);
        goto code_r0x05564da4;
      }
      break;
    case 3:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05564dfc;
      }
      break;
    case 4:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05564e60;
      }
      break;
    case 5:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05564ecc;
      }
      break;
    case 6:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        if (pcVar6 < pcVar5) goto code_r0x05564f40;
        goto code_r0x05564f58;
      }
      break;
    case 7:
      if (uVar7 == 2) {
        uVar7 = *(uint *)(param_1 + 0x44);
        goto code_r0x05564f94;
      }
      break;
    case 8:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05564fec;
      }
      break;
    case 9:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05565058;
      }
      break;
    case 10:
      if (uVar7 == 2) {
        uVar7 = *(uint *)(param_1 + 0x44);
        goto code_r0x055650c4;
      }
      break;
    case 0xb:
      if (uVar7 == 2) goto code_r0x055651b0;
      break;
    case 0xc:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05565294;
      }
      break;
    case 0xd:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x05565300;
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


