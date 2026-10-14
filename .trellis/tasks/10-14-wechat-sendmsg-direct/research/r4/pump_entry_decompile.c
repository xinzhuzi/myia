// ===== [d0] FUN_06c5e990 @ 06c5e990 =====

void FUN_06c5e990(long param_1)

{
  bool bVar1;
  int *piVar2;
  uint uVar3;
  undefined4 uVar4;
  char cVar5;
  byte bVar6;
  bool bVar7;
  int iVar8;
  int iVar9;
  ulong uVar10;
  undefined8 uVar11;
  long *plVar12;
  long lVar13;
  uint uVar14;
  undefined4 uVar15;
  long lVar16;
  int iVar17;
  undefined4 uVar18;
  long lVar19;
  uint uVar20;
  undefined1 (*pauVar21) [16];
  double dVar22;
  double dVar23;
  double dVar24;
  double dVar25;
  undefined1 auVar26 [16];
  double local_1f0;
  double dStack_1e8;
  undefined1 auStack_1a0 [12];
  undefined4 local_194;
  double local_190;
  double local_188;
  undefined8 local_180;
  undefined8 uStack_178;
  double dStack_170;
  double dStack_168;
  undefined8 local_160;
  undefined8 uStack_158;
  undefined8 uStack_150;
  undefined8 uStack_148;
  undefined4 local_140;
  undefined4 uStack_13c;
  undefined8 local_138;
  undefined4 *local_130;
  undefined4 *local_128;
  double local_120;
  double dStack_118;
  double local_110;
  double dStack_108;
  undefined **local_100;
  undefined8 local_f8;
  short local_f0;
  ushort local_ee;
  int *local_e8;
  long local_e0;
  undefined8 uStack_d8;
  undefined4 local_d0;
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  uint local_a8;
  undefined4 uStack_a4;
  char local_a0;
  long local_9c;
  
  if ((*(long *)(param_1 + 0x18) == 0) || (*(int *)(*(long *)(param_1 + 0x18) + 4) == 0)) {
    lVar19 = 0;
  }
  else {
    lVar19 = *(long *)(param_1 + 0x20);
  }
  pauVar21 = (undefined1 (*) [16])(param_1 + 0x48);
  dVar22 = *(double *)*pauVar21;
  dVar24 = DAT_0a2201f8 - dVar22;
  dVar25 = -dVar24;
  if (0.0 <= dVar24) {
    dVar25 = dVar24;
  }
  if ((DAT_0a2201f8 == 0.0) || (dVar22 == 0.0)) {
    if (1e-12 < dVar25) goto LAB_06c5eac4;
LAB_06c5ea44:
    dVar22 = *(double *)(param_1 + 0x50);
    dVar24 = DAT_0a220200 - dVar22;
    dVar25 = -dVar24;
    if (0.0 <= dVar24) {
      dVar25 = dVar24;
    }
    if ((DAT_0a220200 == 0.0) || (dVar22 == 0.0)) {
      dVar24 = 1e-12;
    }
    else {
      dVar25 = dVar25 * 1000000000000.0;
      dVar24 = -DAT_0a220200;
      if (0.0 <= DAT_0a220200) {
        dVar24 = DAT_0a220200;
      }
      dVar23 = -dVar22;
      if (0.0 <= dVar22) {
        dVar23 = dVar22;
      }
      if (dVar23 <= dVar24) {
        dVar24 = dVar23;
      }
    }
    bVar7 = dVar25 <= dVar24;
    uVar10 = FUN_059146cc();
  }
  else {
    dVar24 = -DAT_0a2201f8;
    if (0.0 <= DAT_0a2201f8) {
      dVar24 = DAT_0a2201f8;
    }
    dVar23 = -dVar22;
    if (0.0 <= dVar22) {
      dVar23 = dVar22;
    }
    if (dVar23 <= dVar24) {
      dVar24 = dVar23;
    }
    if (dVar25 * 1000000000000.0 <= dVar24) goto LAB_06c5ea44;
LAB_06c5eac4:
    bVar7 = false;
    uVar10 = FUN_059146cc();
  }
  if (((uVar10 & 1) != 0) ||
     (auVar26._0_8_ = *(ulong *)(param_1 + 0x50), auVar26._8_8_ = 0, iVar8 = FUN_059146cc(auVar26),
     iVar8 != 0)) {
    FUN_07136550();
    return;
  }
  if (((DAT_0a220220 & 1) == 0) && (iVar8 = ___cxa_guard_acquire(&DAT_0a220220), iVar8 != 0)) {
    DAT_0a220219 = FUN_06e926a4("QT_QPA_DISABLE_ENHANCED_MOUSE");
    ___cxa_guard_release(&DAT_0a220220);
  }
  uVar20 = DAT_0a526778;
  if ((DAT_0a220219 == '\0') && (iVar8 = *(int *)(param_1 + 0x68), iVar8 != 0)) {
    uVar20 = *(uint *)(param_1 + 100);
    if (iVar8 == 5) {
      if (bVar7) {
        return;
      }
      DAT_0a52677c = *(undefined4 *)(param_1 + 0x30);
      local_110 = *(double *)(param_1 + 0x38);
      dStack_108 = *(double *)(param_1 + 0x40);
      iVar8 = 5;
LAB_06c5ec88:
      local_120 = *(double *)*pauVar21;
      dStack_118 = *(double *)(param_1 + 0x50);
LAB_06c5ec90:
      DAT_0a220200 = dStack_118;
      DAT_0a2201f8 = local_120;
      piVar2 = &DAT_0a2207fc;
      if (*(int *)(param_1 + 0x5c) != 0) {
        piVar2 = &DAT_0a220800;
      }
      dVar22 = local_120 - (double)(long)DAT_0a5267fc;
      dVar25 = -dVar22;
      if (0.0 <= dVar22) {
        dVar25 = dVar22;
      }
      if (dVar25 <= (double)(long)*piVar2) {
        dVar22 = dStack_118 - (double)(long)DAT_0a526800;
        dVar25 = -dVar22;
        if (0.0 <= dVar22) {
          dVar25 = dVar22;
        }
        if (dVar25 <= (double)(long)*piVar2) goto LAB_06c5f03c;
      }
      bVar7 = false;
      DAT_0a5267f8 = 0;
      uVar14 = *(uint *)(param_1 + 0xc);
      goto joined_r0x06c5f2e8;
    }
    if (iVar8 == 0xad) goto LAB_06c5ec74;
    if (!bVar7) {
      uVar11 = *(undefined8 *)(param_1 + 0x28);
      uVar3 = *(uint *)(param_1 + 0x58);
      uVar18 = *(undefined4 *)(param_1 + 0x5c);
      uVar4 = *(undefined4 *)(param_1 + 0x30);
      cVar5 = *(char *)(param_1 + 0x60);
      uVar14 = 5;
      if (cVar5 != '\0') {
        uVar14 = 0xad;
      }
      local_f8 = 0x107;
      local_f0 = CONCAT11(local_f0._1_1_,1);
      if (lVar19 == 0) {
        local_e8 = (int *)0x0;
        local_f8 = 0x200000107;
        uVar15 = 3;
      }
      else {
        local_e8 = (int *)FUN_06ec8b78(lVar19);
        uVar15 = 1;
      }
      local_c8 = *(undefined8 *)(param_1 + 0x38);
      uStack_c0 = *(undefined8 *)(param_1 + 0x40);
      uStack_b0 = SUB168(*pauVar21,8);
      local_b8 = SUB168(*pauVar21,0);
      local_9c = (ulong)uVar14 << 0x20;
      bVar6 = *(byte *)(param_1 + 0xc);
      uStack_d8 = uVar11;
      local_d0 = uVar4;
      uStack_a4 = uVar18;
      local_a0 = cVar5;
      local_a8 = uVar3 ^ uVar20;
      goto joined_r0x06c5ee60;
    }
    DAT_0a52677c = *(undefined4 *)(param_1 + 0x30);
    local_120 = SUB168(*pauVar21,0);
    dStack_118 = SUB168(*pauVar21,8);
    dStack_108 = SUB168(*(undefined1 (*) [16])(param_1 + 0x38),8);
    local_110 = SUB168(*(undefined1 (*) [16])(param_1 + 0x38),0);
    if ((iVar8 == 5) || (iVar8 == 0xad)) goto LAB_06c5ec90;
    DAT_0a526778 = *(uint *)(param_1 + 0x58);
    if ((iVar8 == 0xae) || (iVar8 == 2)) goto LAB_06c5f220;
LAB_06c5f03c:
    bVar7 = false;
    uVar14 = *(uint *)(param_1 + 0xc);
joined_r0x06c5f2c8:
    if ((uVar14 >> 1 & 1) != 0) goto LAB_06c5ed30;
LAB_06c5f348:
    if (lVar19 == 0) {
      return;
    }
  }
  else {
    uVar3 = *(uint *)(param_1 + 0x58);
    uVar14 = uVar3 ^ DAT_0a526778;
    if (!bVar7) {
      if (uVar14 != 0) {
        uVar11 = *(undefined8 *)(param_1 + 0x28);
        uVar18 = *(undefined4 *)(param_1 + 0x30);
        uVar4 = *(undefined4 *)(param_1 + 0x5c);
        cVar5 = *(char *)(param_1 + 0x60);
        local_f8 = 0x107;
        local_f0 = CONCAT11(local_f0._1_1_,1);
        if (lVar19 == 0) {
          local_e8 = (int *)0x0;
          local_f8 = 0x200000107;
          uVar15 = 3;
        }
        else {
          local_e8 = (int *)FUN_06ec8b78(lVar19);
          uVar15 = 1;
        }
        local_c8 = *(undefined8 *)(param_1 + 0x38);
        uStack_c0 = *(undefined8 *)(param_1 + 0x40);
        uStack_b0 = SUB168(*pauVar21,8);
        local_b8 = SUB168(*pauVar21,0);
        local_9c = 0;
        bVar6 = *(byte *)(param_1 + 0xc);
        uStack_d8 = uVar11;
        local_d0 = uVar18;
        uStack_a4 = uVar4;
        local_a0 = cVar5;
        local_a8 = uVar20;
joined_r0x06c5ee60:
        if ((bVar6 & 1) != 0) {
          local_f8 = CONCAT44(uVar15,(undefined4)local_f8);
        }
        local_100 = &PTR_FUN_09fd2690;
        local_e0 = lVar19;
        FUN_06c5e990(&local_100);
        FUN_06c5e990(param_1);
        local_100 = &PTR_FUN_09fd26c8;
        if (local_e8 == (int *)0x0) {
          return;
        }
        LOAcquire();
        iVar8 = *local_e8;
        *local_e8 = iVar8 + -1;
        LORelease();
        if (iVar8 != 1) {
          return;
        }
        if (local_e8 == (int *)0x0) {
          return;
        }
        __ZdlPv();
        return;
      }
      uVar20 = 0;
      iVar8 = 5;
      if (*(char *)(param_1 + 0x60) != '\0') {
        iVar8 = 0xad;
      }
LAB_06c5ec74:
      DAT_0a52677c = *(undefined4 *)(param_1 + 0x30);
      local_110 = *(double *)(param_1 + 0x38);
      dStack_108 = *(double *)(param_1 + 0x40);
      goto LAB_06c5ec88;
    }
    if ((uVar14 & 1) == 0) {
      if ((uVar14 >> 1 & 1) == 0) {
        if ((uVar14 >> 2 & 1) == 0) {
          if ((uVar14 >> 3 & 1) == 0) {
            if ((uVar14 >> 4 & 1) == 0) {
              if ((uVar14 >> 5 & 1) == 0) {
                if ((uVar14 >> 6 & 1) == 0) {
                  if ((uVar14 >> 7 & 1) == 0) {
                    if ((uVar14 >> 8 & 1) == 0) {
                      if ((uVar14 >> 9 & 1) == 0) {
                        if ((uVar14 >> 10 & 1) == 0) {
                          if ((uVar14 >> 0xb & 1) == 0) {
                            if ((uVar14 >> 0xc & 1) == 0) {
                              if ((uVar14 >> 0xd & 1) == 0) {
                                if ((uVar14 >> 0xe & 1) == 0) {
                                  if ((uVar14 >> 0xf & 1) == 0) {
                                    if ((uVar14 >> 0x10 & 1) == 0) {
                                      if ((uVar14 >> 0x11 & 1) == 0) {
                                        if ((uVar14 >> 0x12 & 1) == 0) {
                                          if ((uVar14 >> 0x13 & 1) == 0) {
                                            if ((uVar14 >> 0x14 & 1) == 0) {
                                              if ((uVar14 >> 0x15 & 1) == 0) {
                                                if ((uVar14 >> 0x16 & 1) == 0) {
                                                  if ((uVar14 >> 0x17 & 1) == 0) {
                                                    if ((uVar14 >> 0x18 & 1) == 0) {
                                                      if ((uVar14 >> 0x19 & 1) == 0) {
                                                        if ((uVar14 >> 0x1a & 1) == 0) {
                                                          return;
                                                        }
                                                        uVar20 = 0x4000000;
                                                      }
                                                      else {
                                                        uVar20 = 0x2000000;
                                                      }
                                                    }
                                                    else {
                                                      uVar20 = 0x1000000;
                                                    }
                                                  }
                                                  else {
                                                    uVar20 = 0x800000;
                                                  }
                                                }
                                                else {
                                                  uVar20 = 0x400000;
                                                }
                                              }
                                              else {
                                                uVar20 = 0x200000;
                                              }
                                            }
                                            else {
                                              uVar20 = 0x100000;
                                            }
                                          }
                                          else {
                                            uVar20 = 0x80000;
                                          }
                                        }
                                        else {
                                          uVar20 = 0x40000;
                                        }
                                      }
                                      else {
                                        uVar20 = 0x20000;
                                      }
                                    }
                                    else {
                                      uVar20 = 0x10000;
                                    }
                                  }
                                  else {
                                    uVar20 = 0x8000;
                                  }
                                }
                                else {
                                  uVar20 = 0x4000;
                                }
                              }
                              else {
                                uVar20 = 0x2000;
                              }
                            }
                            else {
                              uVar20 = 0x1000;
                            }
                          }
                          else {
                            uVar20 = 0x800;
                          }
                        }
                        else {
                          uVar20 = 0x400;
                        }
                      }
                      else {
                        uVar20 = 0x200;
                      }
                    }
                    else {
                      uVar20 = 0x100;
                    }
                  }
                  else {
                    uVar20 = 0x80;
                  }
                }
                else {
                  uVar20 = 0x40;
                }
              }
              else {
                uVar20 = 0x20;
              }
            }
            else {
              uVar20 = 0x10;
            }
          }
          else {
            uVar20 = 8;
          }
        }
        else {
          uVar20 = 4;
        }
      }
      else {
        uVar20 = 2;
      }
    }
    else {
      uVar20 = 1;
    }
    DAT_0a52677c = *(undefined4 *)(param_1 + 0x30);
    dStack_118 = SUB168(*pauVar21,8);
    local_120 = SUB168(*pauVar21,0);
    dStack_108 = SUB168(*(undefined1 (*) [16])(param_1 + 0x38),8);
    local_110 = SUB168(*(undefined1 (*) [16])(param_1 + 0x38),0);
    DAT_0a526778 = uVar3;
    if ((uVar20 & uVar3) == 0) {
      bVar7 = false;
      iVar8 = 3;
      if (*(char *)(param_1 + 0x60) != '\0') {
        iVar8 = 0xaf;
      }
      uVar14 = *(uint *)(param_1 + 0xc);
    }
    else {
      iVar8 = 2;
      if (*(char *)(param_1 + 0x60) != '\0') {
        iVar8 = 0xae;
      }
LAB_06c5f220:
      if (DAT_0a526848 == 0) {
        __Znwm(0x10);
        DAT_0a526848 = FUN_06c8b580();
      }
      iVar9 = FUN_06c8b6e8();
      lVar16 = *(long *)(param_1 + 0x28);
      bVar7 = (ulong)(lVar16 - DAT_0a5267f0) < (ulong)(long)iVar9 && uVar20 == DAT_0a5267f8;
      if (0.0 <= DAT_0a2201f8) {
        DAT_0a5267fc = (int)(DAT_0a2201f8 + 0.5);
      }
      else {
        DAT_0a5267fc = (int)((DAT_0a2201f8 - (double)(int)(DAT_0a2201f8 + -1.0)) + 0.5) +
                       (int)(DAT_0a2201f8 + -1.0);
      }
      DAT_0a5267f0 = lVar16;
      DAT_0a5267f8 = uVar20;
      if (0.0 <= DAT_0a220200) {
        DAT_0a526800 = (int)(DAT_0a220200 + 0.5);
        uVar14 = *(uint *)(param_1 + 0xc);
        goto joined_r0x06c5f2c8;
      }
      DAT_0a526800 = (int)((DAT_0a220200 - (double)(int)(DAT_0a220200 + -1.0)) + 0.5) +
                     (int)(DAT_0a220200 + -1.0);
      uVar14 = *(uint *)(param_1 + 0xc);
    }
joined_r0x06c5f2e8:
    if ((uVar14 >> 1 & 1) == 0) goto LAB_06c5f348;
LAB_06c5ed30:
    dVar22 = dStack_118;
    dVar25 = local_120;
    if (0.0 <= local_120) {
      iVar9 = (int)(local_120 + 0.5);
      if (0.0 <= dStack_118) goto LAB_06c5ed6c;
LAB_06c5edac:
      local_100 = (undefined **)
                  CONCAT44((int)((dStack_118 - (double)(int)(dStack_118 + -1.0)) + 0.5) +
                           (int)(dStack_118 + -1.0),iVar9);
      lVar16 = FUN_06c5abf4(&local_100);
    }
    else {
      iVar9 = (int)((local_120 - (double)(int)(local_120 + -1.0)) + 0.5) + (int)(local_120 + -1.0);
      if (dStack_118 < 0.0) goto LAB_06c5edac;
LAB_06c5ed6c:
      local_100 = (undefined **)CONCAT44((int)(dStack_118 + 0.5),iVar9);
      lVar16 = FUN_06c5abf4(&local_100);
    }
    if (lVar16 == 0) {
      return;
    }
    if (*(int *)(param_1 + 0x58) == 0) {
      lVar19 = lVar16;
      if (DAT_0a526808 != 0) {
        lVar16 = 0;
        lVar13 = DAT_0a526808;
        goto LAB_06c5eebc;
      }
    }
    else {
      lVar13 = lVar16;
      lVar19 = DAT_0a526808;
      if (DAT_0a526808 == 0) {
LAB_06c5eebc:
        lVar19 = lVar13;
        DAT_0a526808 = lVar16;
      }
    }
    if (0.0 <= dVar25) {
      iVar9 = (int)(dVar25 + 0.5);
      if (0.0 <= dVar22) goto LAB_06c5eef8;
LAB_06c5ef54:
      dVar24 = (double)iVar9;
      dVar23 = (double)((int)((dVar22 - (double)(int)(dVar22 + -1.0)) + 0.5) + (int)(dVar22 + -1.0))
      ;
      if (0.0 <= dVar25) goto LAB_06c5ef14;
LAB_06c5ef88:
      iVar9 = (int)((dVar25 - (double)(int)(dVar25 + -1.0)) + 0.5) + (int)(dVar25 + -1.0);
      dVar25 = dVar25 - dVar24;
      dVar23 = dVar22 - dVar23;
      if (0.0 <= dVar22) goto LAB_06c5ef30;
LAB_06c5efbc:
      iVar17 = (int)((dVar22 - (double)(int)(dVar22 + -1.0)) + 0.5) + (int)(dVar22 + -1.0);
    }
    else {
      iVar9 = (int)((dVar25 - (double)(int)(dVar25 + -1.0)) + 0.5) + (int)(dVar25 + -1.0);
      if (dVar22 < 0.0) goto LAB_06c5ef54;
LAB_06c5eef8:
      dVar24 = (double)iVar9;
      dVar23 = (double)(int)(dVar22 + 0.5);
      if (dVar25 < 0.0) goto LAB_06c5ef88;
LAB_06c5ef14:
      iVar9 = (int)(dVar25 + 0.5);
      dVar25 = dVar25 - dVar24;
      dVar23 = dVar22 - dVar23;
      if (dVar22 < 0.0) goto LAB_06c5efbc;
LAB_06c5ef30:
      iVar17 = (int)(dVar22 + 0.5);
    }
    local_100 = (undefined **)CONCAT44(iVar17,iVar9);
    uVar11 = FUN_06c6cd6c(lVar19,&local_100);
    local_110 = dVar25 + (double)(int)uVar11;
    dStack_108 = dVar23 + (double)(int)((ulong)uVar11 >> 0x20);
    uVar14 = *(uint *)(param_1 + 0xc);
  }
  if (((uVar14 & 1) == 0) && (lVar16 = FUN_06c67994(lVar19), lVar16 != 0)) {
    plVar12 = (long *)FUN_06b32424();
    plVar12 = (long *)(**(code **)(*plVar12 + 0xb8))();
    if (plVar12 != (long *)0x0) {
      auVar26 = FUN_06c936b4(lVar16,0);
      local_190 = (local_110 - (double)auVar26._8_4_) * auVar26._0_8_ + (double)auVar26._8_4_;
      local_188 = (dStack_108 - (double)auVar26._12_4_) * auVar26._0_8_ + (double)auVar26._12_4_;
      auVar26 = FUN_06c936b4(lVar16,0);
      local_1f0 = (local_120 - (double)auVar26._8_4_) * auVar26._0_8_ + (double)auVar26._8_4_;
      dStack_1e8 = (dStack_118 - (double)auVar26._12_4_) * auVar26._0_8_ + (double)auVar26._12_4_;
      FUN_06c70bf8(&local_100,iVar8,&local_190,&local_190,&local_1f0,uVar20,
                   *(undefined4 *)(param_1 + 0x58),*(undefined4 *)(param_1 + 0x30),
                   *(undefined4 *)(param_1 + 0x5c));
      local_e8 = *(int **)(param_1 + 0x28);
      (**(code **)(*plVar12 + 0x60))(plVar12,&local_100);
      thunk_FUN_06fc1dc0(&local_100);
    }
  }
  FUN_06c70bf8(&local_100,iVar8,&local_110,&local_110,&local_120,uVar20,
               *(undefined4 *)(param_1 + 0x58),*(undefined4 *)(param_1 + 0x30),
               *(undefined4 *)(param_1 + 0x5c));
  local_e8 = *(int **)(param_1 + 0x28);
  if ((*(char *)(*(long *)(lVar19 + 8) + 0xf4) == '\0') ||
     (iVar9 = (**(code **)(**(long **)(DAT_0a52bdd0 + 8) + 0x50))(), iVar9 != 0)) {
    bVar1 = false;
    if (local_f0 == 2) {
      bVar1 = bVar7;
    }
    if (bVar1) {
      uVar10 = thunk_FUN_06c64c74(&local_100);
      local_a8 = local_a8 & 0xff000000 | local_a8 & 0xffff | ((uint)(uVar10 >> 1) & 0x7f) << 0x11 |
                 0x10000;
    }
    FUN_06fbdf2c(lVar19,&local_100);
    *(byte *)(param_1 + 0x10) = (byte)(local_ee >> 2) & 1;
    if ((((local_ee & 4) == 0 && (*(uint *)(param_1 + 0xc) & 1) == 0) &&
        (*(char *)(param_1 + 0x60) == '\0')) && (iVar9 = FUN_06fbd608(0xb), iVar9 != 0)) {
      if (DAT_0a526818 == (long *)0x0) {
        __Znwm(8);
        DAT_0a526818 = (long *)FUN_06c8d48c();
        thunk_FUN_06c8d71c();
      }
      local_128 = &DAT_0a232160;
      local_188 = -NAN;
      auVar26 = NEON_fmov(0xc000000000000000,8);
      dStack_170 = local_120 + auVar26._0_8_;
      dStack_168 = dStack_118 + auVar26._8_8_;
      local_140 = 4;
      uStack_13c = 0;
      local_138 = 0;
      local_130 = &DAT_0a2320b0;
      local_190 = (double)CONCAT44(local_190._4_4_,1);
      uStack_178 = 0;
      local_180 = 0;
      auVar26 = NEON_fmov(0x4010000000000000,8);
      uStack_158 = auVar26._8_8_;
      local_160 = auVar26._0_8_;
      uStack_148 = 0;
      uStack_150 = 0;
      if ((iVar8 != 2) || (uVar18 = 1, uVar20 != 1)) {
        if ((iVar8 == 3) && (uVar20 == 1)) {
          uVar18 = 8;
        }
        else {
          if ((iVar8 != 5) || ((*(byte *)(param_1 + 0x58) & 1) == 0)) {
            FUN_06c6234c(&local_190);
            FUN_06c623a0(&local_128);
            goto LAB_06c5f6cc;
          }
          uVar18 = 2;
        }
      }
      local_140 = uVar18;
      FUN_06c4d8a0(&local_128,&local_190);
      FUN_06c4cce8(auStack_1a0,&local_128,lVar19,*(undefined1 *)(*DAT_0a526818 + 0x14),&local_194);
      FUN_06c62194(&local_1f0,lVar19,*(undefined8 *)(param_1 + 0x28),local_194,DAT_0a526818,
                   auStack_1a0,*(undefined4 *)(param_1 + 0x30));
      dStack_1e8 = (double)((ulong)dStack_1e8 | 0x100000000);
      FUN_06c5fac8(&local_1f0);
      FUN_06c51c08(&local_1f0);
      FUN_06c622c4(auStack_1a0);
      FUN_06c6234c(&local_190);
      FUN_06c623a0(&local_128);
    }
    if (bVar7) {
      DAT_0a5267f8 = 0;
      if ((((*(long *)(param_1 + 0x18) != 0) && (*(int *)(*(long *)(param_1 + 0x18) + 4) != 0)) &&
          (*(long *)(param_1 + 0x20) != 0)) || ((*(byte *)(param_1 + 0xc) >> 1 & 1) != 0)) {
        uVar18 = 4;
        if (*(char *)(param_1 + 0x60) != '\0') {
          uVar18 = 0xb0;
        }
        FUN_06c70bf8(&local_190,uVar18,&local_110,&local_110,&local_120,uVar20,
                     *(undefined4 *)(param_1 + 0x58),*(undefined4 *)(param_1 + 0x30),
                     *(undefined4 *)(param_1 + 0x5c));
        uStack_178 = *(undefined8 *)(param_1 + 0x28);
        FUN_06fbdf2c(lVar19,&local_190);
        thunk_FUN_06fc1dc0(&local_190);
      }
    }
  }
LAB_06c5f6cc:
  thunk_FUN_06fc1dc0(&local_100);
  return;
}



// ===== [d0] FUN_06c4f0d8 @ 06c4f0d8 =====

bool FUN_06c4f0d8(ulong param_1)

{
  int iVar1;
  int iVar2;
  long *plVar3;
  int iVar4;
  
  FUN_06e9b150(&DAT_0a526768);
  iVar4 = *(int *)(DAT_0a526760 + 8);
  iVar2 = *(int *)(DAT_0a526760 + 0xc);
  FUN_06e9b0f4(&DAT_0a526768);
  if (iVar2 == iVar4) {
    iVar4 = 0;
  }
  else {
    iVar4 = 0;
    if ((param_1 & 1) == 0) {
      do {
        plVar3 = (long *)FUN_06c4b4c0(&DAT_0a526760);
        if (plVar3 == (long *)0x0) break;
        if (DAT_0a526758 == (long *)0x0) {
          iVar4 = iVar4 + 1;
          FUN_06c5e020(plVar3);
          iVar2 = (int)plVar3[1];
        }
        else {
          iVar2 = (**(code **)(*DAT_0a526758 + 0x10))(DAT_0a526758,plVar3);
          iVar4 = iVar4 + iVar2;
          iVar2 = (int)plVar3[1];
        }
        if (iVar2 != 0x20) {
          DAT_0a526750 = (uint)*(byte *)(plVar3 + 2);
        }
        (**(code **)(*plVar3 + 8))(plVar3);
        FUN_06e9b150(&DAT_0a526768);
        iVar2 = *(int *)(DAT_0a526760 + 8);
        iVar1 = *(int *)(DAT_0a526760 + 0xc);
        FUN_06e9b0f4(&DAT_0a526768);
      } while (iVar1 != iVar2);
    }
    else {
      do {
        plVar3 = (long *)FUN_06c4b5b0(&DAT_0a526760);
        if (plVar3 == (long *)0x0) break;
        if (DAT_0a526758 == (long *)0x0) {
          iVar4 = iVar4 + 1;
          FUN_06c5e020(plVar3);
          iVar2 = (int)plVar3[1];
        }
        else {
          iVar2 = (**(code **)(*DAT_0a526758 + 0x10))(DAT_0a526758,plVar3);
          iVar4 = iVar4 + iVar2;
          iVar2 = (int)plVar3[1];
        }
        if (iVar2 != 0x20) {
          DAT_0a526750 = (uint)*(byte *)(plVar3 + 2);
        }
        (**(code **)(*plVar3 + 8))(plVar3);
        FUN_06e9b150(&DAT_0a526768);
        iVar2 = *(int *)(DAT_0a526760 + 8);
        iVar1 = *(int *)(DAT_0a526760 + 0xc);
        FUN_06e9b0f4(&DAT_0a526768);
      } while (iVar1 != iVar2);
    }
  }
  return 0 < iVar4;
}



// ===== [d0] FUN_07099570 @ 07099570 =====

void FUN_07099570(long param_1)

{
  ID IVar1;
  ID IVar2;
  undefined1 auStack_28 [8];
  
  if ((*(int *)(param_1 + 0xac) == 0) || ((*(uint *)(param_1 + 0x60) >> 5 & 1) != 0)) {
    FUN_07098678(param_1);
    FUN_07098cf0(param_1);
    if ((*(uint *)(param_1 + 0x60) & 0x24) != 4) {
      return;
    }
    FUN_06ff1abc(auStack_28);
    IVar2 = *(ID *)PTR__NSApp_09b357f0;
    IVar1 = objc_stub::FUN_07145400
                      ((ID)&_OBJC_CLASS___NSEvent,*(undefined8 *)PTR__NSZeroPoint_09b35b90,
                       *(undefined8 *)(PTR__NSZeroPoint_09b35b90 + 8),0,0xf,0,0,0,0x7fff,0,0);
    objc_stub::FUN_071457c0(IVar2,IVar1,0);
  }
  else {
    if ((*(uint *)(param_1 + 0x60) & 0x24) != 4) {
      return;
    }
    FUN_06ff1abc(auStack_28);
    IVar2 = *(ID *)PTR__NSApp_09b357f0;
    IVar1 = objc_stub::FUN_07145400
                      ((ID)&_OBJC_CLASS___NSEvent,*(undefined8 *)PTR__NSZeroPoint_09b35b90,
                       *(undefined8 *)(PTR__NSZeroPoint_09b35b90 + 8),0,0xf,0,0,0,0x7fff,0,0);
    objc_stub::FUN_071457c0(IVar2,IVar1,0);
  }
  thunk_FUN_06ff1b0c(auStack_28);
  return;
}



// ===== [d0] FUN_06d2999c @ 06d2999c =====

void FUN_06d2999c(undefined8 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 local_44;
  undefined4 local_40;
  undefined4 uStack_3c;
  undefined8 local_38;
  undefined4 *puStack_30;
  undefined4 *local_28;
  undefined4 *puStack_20;
  long local_18;
  
  local_18 = *(long *)PTR____stack_chk_guard_09b36c98;
  puStack_30 = &uStack_3c;
  local_38 = 0;
  local_28 = &local_40;
  puStack_20 = &local_44;
  local_44 = param_4;
  local_40 = param_3;
  uStack_3c = param_2;
  FUN_06fd9ad0(param_1,&PTR_DAT_09fd6f20,0,&local_38);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_18) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}



