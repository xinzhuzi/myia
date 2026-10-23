// Ghidra inferred pseudocode; requested=0x50ddaf4
// entry=050ddaf4 end=050de533

undefined8 FUN_050ddaf4(long param_1,long param_2)

{
  char cVar1;
  int iVar2;
  undefined8 uVar3;
  ulong uVar4;
  char *pcVar5;
  char *pcVar6;
  uint uVar7;
  undefined8 *puVar8;
  int iStack_68;
  int iStack_64;
  
LAB_050ddb40:
  do {
    pcVar6 = *(char **)(param_2 + 8);
    if (pcVar6 < *(char **)(param_2 + 0x10)) {
      cVar1 = *pcVar6;
      uVar4 = (ulong)cVar1;
      if (cVar1 < 0) goto LAB_050ddb68;
      *(int *)(param_2 + 0x20) = (int)cVar1;
      *(char **)(param_2 + 8) = pcVar6 + 1;
      if (cVar1 == '\0') {
        return 1;
      }
    }
    else {
LAB_050ddb68:
      uVar4 = FUN_05ab303c(param_2);
      *(int *)(param_2 + 0x20) = (int)uVar4;
      if ((int)uVar4 == 0) {
        return 1;
      }
    }
    uVar7 = (uint)uVar4 & 7;
    switch((uint)(uVar4 >> 3) & 0x1fffffff) {
    case 1:
      if (uVar7 == 2) {
        *(uint *)(param_1 + 0x8c) = *(uint *)(param_1 + 0x8c) | 1;
        puVar8 = *(undefined8 **)(param_1 + 8);
        if (puVar8 == &DAT_0a524ad0) {
          puVar8 = (undefined8 *)__Znwm(0x18);
          puVar8[1] = 0;
          puVar8[2] = 0;
          *puVar8 = 0;
          *(undefined8 **)(param_1 + 8) = puVar8;
        }
        uVar3 = FUN_05ab514c(param_2,puVar8);
        if ((int)uVar3 == 0) {
          return uVar3;
        }
        pcVar6 = *(char **)(param_2 + 8);
        if ((pcVar6 < *(char **)(param_2 + 0x10)) && (*pcVar6 == '\x12')) {
          *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x050ddc4c:
          *(uint *)(param_1 + 0x8c) = *(uint *)(param_1 + 0x8c) | 2;
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
code_r0x050ddce0:
            if ((pcVar6 < pcVar5) && (-1 < (long)*pcVar6)) {
              *(long *)(param_1 + 0x18) = (long)*pcVar6;
              pcVar6 = pcVar6 + 1;
              *(char **)(param_2 + 8) = pcVar6;
            }
            else {
              uVar3 = FUN_05ab2d58(param_2,param_1 + 0x18);
              if ((int)uVar3 == 0) {
                return uVar3;
              }
              pcVar6 = *(char **)(param_2 + 8);
              pcVar5 = *(char **)(param_2 + 0x10);
            }
            uVar7 = *(uint *)(param_1 + 0x8c) | 4;
            *(uint *)(param_1 + 0x8c) = uVar7;
            if ((pcVar6 < pcVar5) && (*pcVar6 == '\"')) {
              *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x050dddd0:
              *(uint *)(param_1 + 0x8c) = uVar7 | 8;
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
              if ((pcVar6 < *(char **)(param_2 + 0x10)) && (*pcVar6 == '*')) {
                *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x050dde28:
                *(uint *)(param_1 + 0x8c) = *(uint *)(param_1 + 0x8c) | 0x10;
                puVar8 = *(undefined8 **)(param_1 + 0x28);
                if (puVar8 == &DAT_0a524ad0) {
                  puVar8 = (undefined8 *)__Znwm(0x18);
                  puVar8[1] = 0;
                  puVar8[2] = 0;
                  *puVar8 = 0;
                  *(undefined8 **)(param_1 + 0x28) = puVar8;
                }
                uVar3 = FUN_05ab514c(param_2,puVar8);
                if ((int)uVar3 == 0) {
                  return uVar3;
                }
                pcVar6 = *(char **)(param_2 + 8);
                if ((pcVar6 < *(char **)(param_2 + 0x10)) && (*pcVar6 == '2')) {
                  *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x050dde84:
                  *(uint *)(param_1 + 0x8c) = *(uint *)(param_1 + 0x8c) | 0x20;
                  puVar8 = *(undefined8 **)(param_1 + 0x30);
                  if (puVar8 == &DAT_0a524ad0) {
                    puVar8 = (undefined8 *)__Znwm(0x18);
                    puVar8[1] = 0;
                    puVar8[2] = 0;
                    *puVar8 = 0;
                    *(undefined8 **)(param_1 + 0x30) = puVar8;
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
                    if (pcVar6 < pcVar5) {
code_r0x050ddee8:
                      if (*pcVar6 < 0) goto code_r0x050ddf00;
                      *(int *)(param_1 + 0x38) = (int)*pcVar6;
                      pcVar6 = pcVar6 + 1;
                      *(char **)(param_2 + 8) = pcVar6;
                    }
                    else {
code_r0x050ddf00:
                      uVar3 = FUN_05ab2ea0(param_2,param_1 + 0x38);
                      if ((int)uVar3 == 0) {
                        return uVar3;
                      }
                      pcVar6 = *(char **)(param_2 + 8);
                      pcVar5 = *(char **)(param_2 + 0x10);
                    }
                    *(uint *)(param_1 + 0x8c) = *(uint *)(param_1 + 0x8c) | 0x40;
                    if ((pcVar6 < pcVar5) && (*pcVar6 == 'H')) {
                      pcVar6 = pcVar6 + 1;
                      *(char **)(param_2 + 8) = pcVar6;
code_r0x050ddf3c:
                      if ((pcVar6 < pcVar5) && (-1 < *pcVar6)) {
                        *(int *)(param_1 + 0x3c) = (int)*pcVar6;
                        pcVar6 = pcVar6 + 1;
                        *(char **)(param_2 + 8) = pcVar6;
                      }
                      else {
                        uVar3 = FUN_05ab2ea0(param_2,param_1 + 0x3c);
                        if ((int)uVar3 == 0) {
                          return uVar3;
                        }
                        pcVar6 = *(char **)(param_2 + 8);
                        pcVar5 = *(char **)(param_2 + 0x10);
                      }
                      *(uint *)(param_1 + 0x8c) = *(uint *)(param_1 + 0x8c) | 0x80;
                      if ((pcVar6 < pcVar5) && (*pcVar6 == 'P')) {
                        pcVar6 = pcVar6 + 1;
                        *(char **)(param_2 + 8) = pcVar6;
code_r0x050ddf98:
                        if ((pcVar6 < pcVar5) && (-1 < *pcVar6)) {
                          *(int *)(param_1 + 0x48) = (int)*pcVar6;
                          pcVar6 = pcVar6 + 1;
                          *(char **)(param_2 + 8) = pcVar6;
                        }
                        else {
                          uVar3 = FUN_05ab2ea0(param_2,param_1 + 0x48);
                          if ((int)uVar3 == 0) {
                            return uVar3;
                          }
                          pcVar6 = *(char **)(param_2 + 8);
                          pcVar5 = *(char **)(param_2 + 0x10);
                        }
                        uVar7 = *(uint *)(param_1 + 0x8c) | 0x100;
                        *(uint *)(param_1 + 0x8c) = uVar7;
                        if ((pcVar6 < pcVar5) && (*pcVar6 == 'Z')) {
                          *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x050ddff4:
                          *(uint *)(param_1 + 0x8c) = uVar7 | 0x200;
                          puVar8 = *(undefined8 **)(param_1 + 0x40);
                          if (puVar8 == &DAT_0a524ad0) {
                            puVar8 = (undefined8 *)__Znwm(0x18);
                            puVar8[1] = 0;
                            puVar8[2] = 0;
                            *puVar8 = 0;
                            *(undefined8 **)(param_1 + 0x40) = puVar8;
                          }
                          uVar3 = FUN_05ab514c(param_2,puVar8);
                          if ((int)uVar3 == 0) {
                            return uVar3;
                          }
                          pcVar6 = *(char **)(param_2 + 8);
                          pcVar5 = *(char **)(param_2 + 0x10);
                          if ((pcVar6 < pcVar5) && (*pcVar6 == '`')) {
                            pcVar6 = pcVar6 + 1;
                            *(char **)(param_2 + 8) = pcVar6;
code_r0x050de04c:
                            if ((pcVar6 < pcVar5) && (-1 < *pcVar6)) {
                              *(int *)(param_1 + 0x4c) = (int)*pcVar6;
                              pcVar6 = pcVar6 + 1;
                              *(char **)(param_2 + 8) = pcVar6;
                            }
                            else {
                              uVar3 = FUN_05ab2ea0(param_2,param_1 + 0x4c);
                              if ((int)uVar3 == 0) {
                                return uVar3;
                              }
                              pcVar6 = *(char **)(param_2 + 8);
                              pcVar5 = *(char **)(param_2 + 0x10);
                            }
                            uVar7 = *(uint *)(param_1 + 0x8c) | 0x400;
                            *(uint *)(param_1 + 0x8c) = uVar7;
                            if ((pcVar6 < pcVar5) && (*pcVar6 == 'j')) {
                              *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x050de0a8:
                              *(uint *)(param_1 + 0x8c) = uVar7 | 0x800;
                              puVar8 = *(undefined8 **)(param_1 + 0x50);
                              if (puVar8 == &DAT_0a524ad0) {
                                puVar8 = (undefined8 *)__Znwm(0x18);
                                puVar8[1] = 0;
                                puVar8[2] = 0;
                                *puVar8 = 0;
                                *(undefined8 **)(param_1 + 0x50) = puVar8;
                              }
                              uVar3 = FUN_05ab514c(param_2,puVar8);
                              if ((int)uVar3 == 0) {
                                return uVar3;
                              }
                              pcVar6 = *(char **)(param_2 + 8);
                              if ((pcVar6 < *(char **)(param_2 + 0x10)) && (*pcVar6 == 'r')) {
                                *(char **)(param_2 + 8) = pcVar6 + 1;
code_r0x050de100:
                                *(uint *)(param_1 + 0x8c) = *(uint *)(param_1 + 0x8c) | 0x1000;
                                puVar8 = *(undefined8 **)(param_1 + 0x58);
                                if (puVar8 == &DAT_0a524ad0) {
                                  puVar8 = (undefined8 *)__Znwm(0x18);
                                  puVar8[1] = 0;
                                  puVar8[2] = 0;
                                  *puVar8 = 0;
                                  *(undefined8 **)(param_1 + 0x58) = puVar8;
                                }
                                uVar3 = FUN_05ab514c(param_2,puVar8);
                                if ((int)uVar3 == 0) {
                                  return uVar3;
                                }
                                pcVar6 = *(char **)(param_2 + 8);
                                pcVar5 = *(char **)(param_2 + 0x10);
                                if ((pcVar6 < pcVar5) && (*pcVar6 == 'x')) {
                                  pcVar6 = pcVar6 + 1;
                                  *(char **)(param_2 + 8) = pcVar6;
code_r0x050de15c:
                                  if ((pcVar6 < pcVar5) && (-1 < *pcVar6)) {
                                    *(int *)(param_1 + 0x68) = (int)*pcVar6;
                                    pcVar6 = pcVar6 + 1;
                                    *(char **)(param_2 + 8) = pcVar6;
                                  }
                                  else {
                                    uVar3 = FUN_05ab2ea0(param_2,param_1 + 0x68);
                                    if ((int)uVar3 == 0) {
                                      return uVar3;
                                    }
                                    pcVar6 = *(char **)(param_2 + 8);
                                    pcVar5 = *(char **)(param_2 + 0x10);
                                  }
                                  uVar7 = *(uint *)(param_1 + 0x8c) | 0x2000;
                                  *(uint *)(param_1 + 0x8c) = uVar7;
                                  if (((1 < (int)pcVar5 - (int)pcVar6) && (*pcVar6 == -0x7e)) &&
                                     (pcVar6[1] == '\x01')) {
                                    *(char **)(param_2 + 8) = pcVar6 + 2;
code_r0x050de1c8:
                                    *(uint *)(param_1 + 0x8c) = uVar7 | 0x4000;
                                    puVar8 = *(undefined8 **)(param_1 + 0x60);
                                    if (puVar8 == &DAT_0a524ad0) {
                                      puVar8 = (undefined8 *)__Znwm(0x18);
                                      puVar8[1] = 0;
                                      puVar8[2] = 0;
                                      *puVar8 = 0;
                                      *(undefined8 **)(param_1 + 0x60) = puVar8;
                                    }
                                    uVar3 = FUN_05ab514c(param_2,puVar8);
                                    if ((int)uVar3 == 0) {
                                      return uVar3;
                                    }
                                    pcVar6 = *(char **)(param_2 + 8);
                                    if (((1 < *(int *)(param_2 + 0x10) - (int)pcVar6) &&
                                        (*pcVar6 == -0x76)) && (pcVar6[1] == '\x01')) {
                                      *(char **)(param_2 + 8) = pcVar6 + 2;
code_r0x050de234:
                                      *(uint *)(param_1 + 0x8c) = *(uint *)(param_1 + 0x8c) | 0x8000
                                      ;
                                      puVar8 = *(undefined8 **)(param_1 + 0x70);
                                      if (puVar8 == &DAT_0a524ad0) {
                                        puVar8 = (undefined8 *)__Znwm(0x18);
                                        puVar8[1] = 0;
                                        puVar8[2] = 0;
                                        *puVar8 = 0;
                                        *(undefined8 **)(param_1 + 0x70) = puVar8;
                                      }
                                      uVar3 = FUN_05ab514c(param_2,puVar8);
                                      if ((int)uVar3 == 0) {
                                        return uVar3;
                                      }
                                      pcVar6 = *(char **)(param_2 + 8);
                                      pcVar5 = *(char **)(param_2 + 0x10);
                                      if (((1 < (int)pcVar5 - (int)pcVar6) && (*pcVar6 == -0x70)) &&
                                         (pcVar6[1] == '\x01')) {
                                        pcVar6 = pcVar6 + 2;
                                        *(char **)(param_2 + 8) = pcVar6;
                                        if (pcVar6 < pcVar5) {
code_r0x050de2a8:
                                          iVar2 = (int)pcVar5;
                                          if (*pcVar6 < 0) goto code_r0x050de2c0;
                                          *(int *)(param_1 + 0x6c) = (int)*pcVar6;
                                          pcVar6 = pcVar6 + 1;
                                          *(char **)(param_2 + 8) = pcVar6;
                                        }
                                        else {
code_r0x050de2c0:
                                          uVar3 = FUN_05ab2ea0(param_2,param_1 + 0x6c);
                                          if ((int)uVar3 == 0) {
                                            return uVar3;
                                          }
                                          pcVar6 = *(char **)(param_2 + 8);
                                          iVar2 = (int)*(undefined8 *)(param_2 + 0x10);
                                        }
                                        uVar7 = *(uint *)(param_1 + 0x8c) | 0x10000;
                                        *(uint *)(param_1 + 0x8c) = uVar7;
                                        if (((1 < iVar2 - (int)pcVar6) && (*pcVar6 == -0x66)) &&
                                           (pcVar6[1] == '\x01')) {
                                          *(char **)(param_2 + 8) = pcVar6 + 2;
code_r0x050de30c:
                                          *(uint *)(param_1 + 0x8c) = uVar7 | 0x20000;
                                          puVar8 = *(undefined8 **)(param_1 + 0x78);
                                          if (puVar8 == (undefined8 *)0x0) {
                                            puVar8 = (undefined8 *)__Znwm(0x30);
                                            puVar8[1] = 0;
                                            puVar8[2] = 0;
                                            *puVar8 = &PTR_FUN_09edb898;
                                            *(undefined4 *)(puVar8 + 3) = 0;
                                            puVar8[4] = 0;
                                            *(undefined4 *)(puVar8 + 5) = 0;
                                            *(undefined8 **)(param_1 + 0x78) = puVar8;
                                          }
                                          iStack_68 = -0x55555556;
                                          pcVar6 = *(char **)(param_2 + 8);
                                          if ((pcVar6 < *(char **)(param_2 + 0x10)) &&
                                             (cVar1 = *pcVar6, -1 < cVar1)) {
                                            *(char **)(param_2 + 8) = pcVar6 + 1;
                                            iStack_68 = (int)cVar1;
                                          }
                                          else {
                                            iVar2 = FUN_05ab2ea0(param_2,&iStack_68);
                                            if (iVar2 == 0) {
                                              return 0;
                                            }
                                          }
                                          iVar2 = *(int *)(param_2 + 0x38);
                                          *(int *)(param_2 + 0x38) = iVar2 + 1;
                                          if (*(int *)(param_2 + 0x3c) <= iVar2) {
                                            return 0;
                                          }
                                          uVar3 = FUN_05ab26f0(param_2,iStack_68);
                                          iVar2 = FUN_050c9698(puVar8,param_2);
                                          if (iVar2 == 0) {
                                            return 0;
                                          }
                                          if (*(char *)(param_2 + 0x24) != '\x01') {
                                            return 0;
                                          }
                                          FUN_05ab276c(param_2,uVar3);
                                          if (0 < *(int *)(param_2 + 0x38)) {
                                            *(int *)(param_2 + 0x38) = *(int *)(param_2 + 0x38) + -1
                                            ;
                                          }
                                          pcVar6 = *(char **)(param_2 + 8);
                                          if (((1 < *(int *)(param_2 + 0x10) - (int)pcVar6) &&
                                              (*pcVar6 == -0x5e)) && (pcVar6[1] == '\x01')) {
                                            *(char **)(param_2 + 8) = pcVar6 + 2;
code_r0x050de408:
                                            *(uint *)(param_1 + 0x8c) =
                                                 *(uint *)(param_1 + 0x8c) | 0x40000;
                                            puVar8 = *(undefined8 **)(param_1 + 0x80);
                                            if (puVar8 == (undefined8 *)0x0) {
                                              puVar8 = (undefined8 *)__Znwm(0x30);
                                              puVar8[1] = 0;
                                              puVar8[2] = 0;
                                              *puVar8 = &PTR_FUN_09edb988;
                                              *(undefined4 *)(puVar8 + 3) = 0;
                                              puVar8[4] = 0;
                                              *(undefined4 *)(puVar8 + 5) = 0;
                                              *(undefined8 **)(param_1 + 0x80) = puVar8;
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
                                            iVar2 = FUN_050ca74c(puVar8,param_2);
                                            if (iVar2 == 0) {
                                              return 0;
                                            }
                                            if (*(char *)(param_2 + 0x24) != '\x01') {
                                              return 0;
                                            }
                                            FUN_05ab276c(param_2,uVar3);
                                            if (0 < *(int *)(param_2 + 0x38)) {
                                              *(int *)(param_2 + 0x38) =
                                                   *(int *)(param_2 + 0x38) + -1;
                                            }
                                            if ((*(long *)(param_2 + 8) == *(long *)(param_2 + 0x10)
                                                ) && ((*(int *)(param_2 + 0x2c) != 0 ||
                                                      (*(int *)(param_2 + 0x18) ==
                                                       *(int *)(param_2 + 0x28))))) {
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
                }
              }
            }
          }
        }
        goto LAB_050ddb40;
      }
      break;
    case 2:
      if (uVar7 == 2) goto code_r0x050ddc4c;
      break;
    case 3:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x050ddce0;
      }
      break;
    case 4:
      if (uVar7 == 2) {
        uVar7 = *(uint *)(param_1 + 0x8c);
        goto code_r0x050dddd0;
      }
      break;
    case 5:
      if (uVar7 == 2) goto code_r0x050dde28;
      break;
    case 6:
      if (uVar7 == 2) goto code_r0x050dde84;
      break;
    case 8:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        if (pcVar6 < pcVar5) goto code_r0x050ddee8;
        goto code_r0x050ddf00;
      }
      break;
    case 9:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x050ddf3c;
      }
      break;
    case 10:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x050ddf98;
      }
      break;
    case 0xb:
      if (uVar7 == 2) {
        uVar7 = *(uint *)(param_1 + 0x8c);
        goto code_r0x050ddff4;
      }
      break;
    case 0xc:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x050de04c;
      }
      break;
    case 0xd:
      if (uVar7 == 2) {
        uVar7 = *(uint *)(param_1 + 0x8c);
        goto code_r0x050de0a8;
      }
      break;
    case 0xe:
      if (uVar7 == 2) goto code_r0x050de100;
      break;
    case 0xf:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        goto code_r0x050de15c;
      }
      break;
    case 0x10:
      if (uVar7 == 2) {
        uVar7 = *(uint *)(param_1 + 0x8c);
        goto code_r0x050de1c8;
      }
      break;
    case 0x11:
      if (uVar7 == 2) goto code_r0x050de234;
      break;
    case 0x12:
      if ((uVar4 & 7) == 0) {
        pcVar6 = *(char **)(param_2 + 8);
        pcVar5 = *(char **)(param_2 + 0x10);
        if (pcVar6 < pcVar5) goto code_r0x050de2a8;
        goto code_r0x050de2c0;
      }
      break;
    case 0x13:
      if (uVar7 == 2) {
        uVar7 = *(uint *)(param_1 + 0x8c);
        goto code_r0x050de30c;
      }
      break;
    case 0x14:
      if (uVar7 == 2) goto code_r0x050de408;
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


