// Ghidra inferred pseudocode; requested=0x31ce06c
// entry=031ce06c end=031cf17b

/* WARNING: Removing unreachable block (ram,0x031cea50) */
/* WARNING: Removing unreachable block (ram,0x031cf0e4) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_031ce06c(undefined8 *param_1,undefined8 param_2,long *param_3)

{
  undefined1 uVar1;
  uint3 uVar2;
  undefined8 ****ppppuVar3;
  bool bVar4;
  long lVar5;
  int iVar6;
  uint uVar7;
  long *plVar8;
  undefined8 *puVar9;
  undefined8 ****ppppuVar10;
  undefined8 *puVar11;
  ulong uVar12;
  undefined1 *puVar13;
  undefined1 *puVar14;
  long lVar15;
  ulong uVar16;
  undefined8 uVar17;
  undefined4 uVar18;
  undefined4 uVar19;
  undefined8 local_350;
  undefined8 uStack_348;
  ulong local_340;
  long local_330;
  long *local_328;
  long local_320;
  long *plStack_318;
  undefined8 ***local_310;
  long *local_308;
  undefined7 local_300;
  char cStack_2f9;
  undefined8 ***local_2f8 [2];
  undefined7 local_2e8;
  char cStack_2e1;
  undefined8 ***local_2e0;
  long *plStack_2d8;
  undefined8 local_2d0;
  undefined7 local_2c8;
  char cStack_2c1;
  undefined1 *local_2c0;
  long *local_2b8;
  undefined8 local_250;
  undefined8 uStack_248;
  ulong local_240;
  undefined8 local_230;
  long *local_228;
  long local_220;
  long *local_218;
  undefined8 local_210;
  undefined1 *puStack_208;
  undefined1 *local_200;
  undefined1 *puStack_1f8;
  undefined1 *local_1f0;
  long *local_1e8;
  undefined1 *local_1e0;
  undefined1 *puStack_1d8;
  undefined1 *local_1d0;
  undefined8 ***pppuStack_1c8;
  long *local_1c0;
  undefined1 *puStack_1b8;
  undefined1 *puStack_1b0;
  undefined1 *local_1a8;
  undefined8 ***local_1a0;
  undefined8 local_198;
  undefined7 local_190;
  char cStack_189;
  undefined8 ***local_150;
  undefined1 local_148;
  undefined7 local_140;
  char cStack_139;
  undefined8 ***local_100;
  undefined8 ***pppuStack_f8;
  ulong local_f0;
  undefined8 uStack_e8;
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  if ((DAT_0a3e04c8 & 1) == 0) {
    _DAT_0a3e04ac = CONCAT44((int)DAT_087f8a18,(int)DAT_08490810);
    uRam000000000a3e04b4 = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
    DAT_0a3e04bc = CONCAT44((int)DAT_08550e48,(int)ram0x0848ba58);
    DAT_0a3e04c4 = (undefined4)ram0x084cf948;
    DAT_0a3e04c8 = 1;
  }
  if ((DAT_0a3dd403 & 1) == 0) {
    uVar12 = 0;
    do {
      (&DAT_0a3dd39e)[uVar12] = (&DAT_088bcf0a)[uVar12] + 0x8a ^ (&DAT_088bcefa)[uVar12 & 0xf];
      uVar12 = uVar12 + 1;
    } while (uVar12 != 0x65);
    DAT_0a3dd403 = 1;
  }
  puStack_1b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1c0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_1a8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1b0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1e0 = &SUB_aaaaaaaaaaaaaaaa;
  pppuStack_1c8 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
  local_1d0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0003bb6c(&local_2e0,&DAT_0a3e04ac,&DAT_0a3dd39e,
               "ibrary/Frameworks/CoreGraphics.framework/Versions/A/CoreGraphics");
  if ((DAT_0a3e04ec & 1) == 0) {
    _DAT_0a3e04cc = CONCAT44((int)DAT_088bafb8,(int)DAT_087f22b0);
    uRam000000000a3e04d4 = CONCAT44((int)DAT_085929b8,(int)DAT_088bafc0);
    _DAT_0a3e04dc = CONCAT44((int)ram0x087fa960,(int)DAT_0848f630);
    uRam000000000a3e04e4 = CONCAT44((int)ram0x084cf948,(int)DAT_0886bee0);
    DAT_0a3e04ec = 1;
  }
  local_1e0 = (undefined1 *)CONCAT44(local_1e0._4_4_,2);
  local_1c0 = plStack_2d8;
  pppuStack_1c8 = local_2e0;
  local_1d0 = (undefined1 *)0x0;
  puStack_1b8 = (undefined1 *)0x0;
  puStack_1b0 = (undefined1 *)0x0;
  local_1a8 = (undefined1 *)0x0;
  puStack_1d8 = (undefined1 *)FUN_0474715c();
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
            (&puStack_1b8,&DAT_0a3e04cc);
  FUN_030f3214(*param_3,1);
  puStack_1f8 = &SUB_aaaaaaaaaaaaaaaa;
  local_200 = &SUB_aaaaaaaaaaaaaaaa;
  local_1e8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_1f0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_208 = &SUB_aaaaaaaaaaaaaaaa;
  local_210 = (undefined8 ****)&SUB_aaaaaaaaaaaaaaaa;
  local_220 = *param_3;
  local_218 = (long *)param_3[1];
  if (local_218 != (long *)0x0) {
    local_218[1] = local_218[1] + 1;
  }
  FUN_031cf3a4(&local_2e0,param_2,&local_220);
  FUN_03189980(&local_210,&local_100,&local_2e0);
  plVar8 = plStack_2d8;
  if (plStack_2d8 != (long *)0x0) {
    LOAcquire();
    lVar5 = plStack_2d8[1];
    plStack_2d8[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plStack_2d8 + 0x10))(plStack_2d8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  plVar8 = local_218;
  if (local_218 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_218[1];
    local_218[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_218 + 0x10))(local_218);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  local_230 = *(undefined8 *)(*param_3 + 0x18);
  local_228 = *(long **)(*param_3 + 0x20);
  lVar5 = 0;
  if (local_228 != (long *)0x0) {
    lVar5 = local_228[1];
    local_228[1] = lVar5 + 1;
  }
  FUN_031d12e8(lVar5,local_1f0,&local_230);
  plVar8 = local_228;
  if (local_228 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_228[1];
    local_228[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_228 + 0x10))(local_228);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  FUN_031d1444(*param_3 + 0x70,&local_210);
  if ((DAT_0a3e0506 & 1) == 0) {
    _DAT_0a3e04f0 = CONCAT44((int)DAT_088bafc8,(int)DAT_084d1028);
    uRam000000000a3e04f8 = CONCAT44((int)DAT_084a8110,(int)DAT_088a7260);
    DAT_0a3e0500 = (undefined4)DAT_088bafd0;
    DAT_0a3e0504 = 0x62;
    DAT_0a3e0506 = 1;
  }
  plVar8 = (long *)_strlen(&DAT_0a3e04f0);
  if ((long *)0x7ffffffffffffff7 < plVar8) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_2e0);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar8) {
    uVar12 = 0x19;
    if (((ulong)plVar8 | 7) != 0x17) {
      uVar12 = ((ulong)plVar8 | 7) + 1;
    }
    ppppuVar10 = (undefined8 ****)__Znwm(uVar12);
    local_2d0 = uVar12 | 0x8000000000000000;
    local_2e0 = ppppuVar10;
    plStack_2d8 = plVar8;
LAB_031ce42c:
    _memcpy(ppppuVar10,&DAT_0a3e04f0,(size_t)plVar8);
  }
  else {
    local_2d0 = CONCAT17((char)plVar8,(undefined7)local_2d0);
    ppppuVar10 = &local_2e0;
    if (plVar8 != (long *)0x0) goto LAB_031ce42c;
  }
  *(undefined1 *)((long)ppppuVar10 + (long)plVar8) = 0;
  FUN_030f1f08(&local_100,*param_3);
  ppppuVar10 = (undefined8 ****)pppuStack_f8;
  ppppuVar3 = (undefined8 ****)local_100;
  if (-1 < (long)local_f0) {
    ppppuVar10 = (undefined8 ****)(local_f0 >> 0x38);
    ppppuVar3 = &local_100;
  }
  puVar9 = (undefined8 *)
           __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                     (&local_2e0,ppppuVar3,ppppuVar10);
  uStack_248 = puVar9[1];
  local_250 = *puVar9;
  local_240 = puVar9[2];
  puVar9[1] = 0;
  puVar9[2] = 0;
  *puVar9 = 0;
  FUN_02ac5bf8(&local_1e0,&local_250,0x32);
  if ((long)local_240 < 0) {
    __ZdlPvm(local_250,local_240 & 0x7fffffffffffffff);
  }
  if ((long)local_2d0 < 0) {
    __ZdlPvm(local_2e0,local_2d0 & 0x7fffffffffffffff);
  }
  if ((int)local_210 == 0 && local_210._4_4_ == 0) {
    uVar12 = FUN_030f321c(*param_3);
    if ((uVar12 & 1) != 0) {
      local_310 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
      local_308 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      local_320 = *param_3;
      plVar8 = (long *)param_3[1];
      if (plVar8 != (long *)0x0) {
        plVar8[1] = plVar8[1] + 1;
      }
      plStack_318 = plVar8;
      FUN_0318d680(&local_310,param_2,&local_320);
      if (plVar8 == (long *)0x0) {
LAB_031ce890:
        if ((undefined8 ****)local_310 != (undefined8 ****)0x0) goto LAB_031ce898;
LAB_031cef30:
        iVar6 = thunk_FUN_05e1d97c(4);
        if (iVar6 != 0) {
          FUN_0488143c(&local_150);
          ppppuVar10 = (undefined8 ****)local_150;
          if (-1 < cStack_139) {
            ppppuVar10 = &local_150;
          }
          if ((DAT_0a3dd363 & 1) == 0) {
            uVar12 = 0;
            do {
              (&DAT_0a3dd350)[uVar12] =
                   (&DAT_088bce97)[uVar12] + 0x8a ^ (&DAT_088bce87)[uVar12 & 0xf];
              uVar12 = uVar12 + 1;
            } while (uVar12 != 0x13);
            DAT_0a3dd363 = 1;
          }
          if ((DAT_0a3e04c8 & 1) == 0) {
            _DAT_0a3e04ac = CONCAT44((int)DAT_087f8a18,(int)DAT_08490810);
            uRam000000000a3e04b4 = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
            DAT_0a3e04bc = CONCAT44((int)DAT_08550e48,(int)ram0x0848ba58);
            DAT_0a3e04c4 = (undefined4)ram0x084cf948;
            DAT_0a3e04c8 = 1;
          }
          FUN_05e1d050(&local_2e0,4,ppppuVar10,&DAT_0a3dd350,&DAT_0a3e04ac,
                       "eGraphics.framework/Versions/A/CoreGraphics",0,0);
          if ((DAT_0a3e0553 & 1) == 0) {
            uRam000000000a3e0548._0_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[8];
            uRam000000000a3e0548._1_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[9];
            uRam000000000a3e0548._2_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[10];
            uRam000000000a3e0548._3_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[0xb];
            uRam000000000a3e0548._4_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[0xc];
            uRam000000000a3e0548._5_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[0xd];
            uRam000000000a3e0548._6_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[0xe];
            uRam000000000a3e0548._7_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[0xf];
            DAT_0a3e0540 = s_handler_is_nullpGetFileFinalSvri_088bb5e0[0];
            DAT_0a3e0540_1._0_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[1];
            DAT_0a3e0540_1._1_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[2];
            DAT_0a3e0540_1._2_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[3];
            DAT_0a3e0540_1._3_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[4];
            DAT_0a3e0540_1._4_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[5];
            DAT_0a3e0540_1._5_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[6];
            DAT_0a3e0540_1._6_1_ = s_handler_is_nullpGetFileFinalSvri_088bb5e0[7];
            DAT_0a3e0550 = 0x7274;
            DAT_0a3e0552 = 0;
            DAT_0a3e0553 = 1;
          }
          uStack_98 = 0;
          local_a0 = 0;
          uStack_88 = 0;
          local_90 = 0;
          uStack_b8 = 0;
          local_c0 = 0;
          uStack_a8 = 0;
          local_b0 = 0;
          uStack_d8 = 0;
          local_e0 = 0;
          uStack_c8 = 0;
          local_d0 = 0;
          pppuStack_f8 = (undefined8 ****)0x0;
          local_100 = (undefined8 ****)0x0;
          uStack_e8 = 0;
          local_f0 = 0;
          FUN_05e1d31c(&local_2e0,&DAT_0a3e0540,&local_100);
          thunk_FUN_05e1d0bc(&local_2e0);
          if (cStack_139 < '\0') {
            __ZdlPvm(local_150,CONCAT17(cStack_139,local_140) & 0x7fffffffffffffff);
          }
        }
        FUN_030f6650(param_1,1,1,4,4);
      }
      else {
        LOAcquire();
        lVar5 = plVar8[1];
        plVar8[1] = lVar5 + -1;
        LORelease();
        if (lVar5 != 0) goto LAB_031ce890;
        (**(code **)(*plVar8 + 0x10))(plVar8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        if ((undefined8 ****)local_310 == (undefined8 ****)0x0) goto LAB_031cef30;
LAB_031ce898:
        FUN_030f3214(*param_3,3);
        local_330 = *param_3;
        local_328 = (long *)param_3[1];
        if (local_328 != (long *)0x0) {
          local_328[1] = local_328[1] + 1;
        }
        FUN_030d4354(&local_2e0,local_310,&local_330);
        local_210 = (undefined8 ****)local_2e0;
        puVar9 = (undefined8 *)((ulong)&local_210 | 8);
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (puVar9,&plStack_2d8);
        plVar8 = local_1e8;
        if (local_2b8 != (long *)0x0) {
          local_2b8[1] = local_2b8[1] + 1;
        }
        local_1f0 = local_2c0;
        local_1e8 = local_2b8;
        if (plVar8 != (long *)0x0) {
          LOAcquire();
          lVar5 = plVar8[1];
          plVar8[1] = lVar5 + -1;
          LORelease();
          if (lVar5 == 0) {
            (**(code **)(*plVar8 + 0x10))(plVar8);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
          }
        }
        if (local_2b8 != (long *)0x0) {
          LOAcquire();
          lVar5 = local_2b8[1];
          local_2b8[1] = lVar5 + -1;
          LORelease();
          if (lVar5 == 0) {
            (**(code **)(*local_2b8 + 0x10))(local_2b8);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_2b8);
          }
        }
        if (cStack_2c1 < '\0') {
          __ZdlPvm(plStack_2d8,CONCAT17(cStack_2c1,local_2c8) & 0x7fffffffffffffff);
        }
        plVar8 = local_328;
        if (local_328 != (long *)0x0) {
          LOAcquire();
          lVar5 = local_328[1];
          local_328[1] = lVar5 + -1;
          LORelease();
          if (lVar5 == 0) {
            (**(code **)(*local_328 + 0x10))(local_328);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
          }
        }
        if ((DAT_0a3e0569 & 1) == 0) {
          _DAT_0a3e0554 = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
          uRam000000000a3e055c = CONCAT44((int)DAT_0867c9b8,(int)DAT_0854dcf8);
          DAT_0a3e0564 = (undefined4)DAT_084a66b0;
          DAT_0a3e0568 = 0;
          DAT_0a3e0569 = 1;
        }
        plVar8 = (long *)_strlen(&DAT_0a3e0554);
        if ((long *)0x7ffffffffffffff7 < plVar8) {
                    /* WARNING: Subroutine does not return */
          FUN_00018d9c(&local_2e0);
        }
        if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar8) {
          uVar12 = 0x19;
          if (((ulong)plVar8 | 7) != 0x17) {
            uVar12 = ((ulong)plVar8 | 7) + 1;
          }
          ppppuVar10 = (undefined8 ****)__Znwm(uVar12);
          local_2d0 = uVar12 | 0x8000000000000000;
          local_2e0 = ppppuVar10;
          plStack_2d8 = plVar8;
LAB_031cebf8:
          _memcpy(ppppuVar10,&DAT_0a3e0554,(size_t)plVar8);
        }
        else {
          local_2d0 = CONCAT17((char)plVar8,(undefined7)local_2d0);
          ppppuVar10 = &local_2e0;
          if (plVar8 != (long *)0x0) goto LAB_031cebf8;
        }
        *(undefined1 *)((long)ppppuVar10 + (long)plVar8) = 0;
        FUN_030f1f08(&local_100,*param_3);
        ppppuVar10 = (undefined8 ****)pppuStack_f8;
        ppppuVar3 = (undefined8 ****)local_100;
        if (-1 < (long)local_f0) {
          ppppuVar10 = (undefined8 ****)(local_f0 >> 0x38);
          ppppuVar3 = &local_100;
        }
        puVar11 = (undefined8 *)
                  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                            (&local_2e0,ppppuVar3,ppppuVar10);
        uStack_348 = puVar11[1];
        local_350 = *puVar11;
        local_340 = puVar11[2];
        puVar11[1] = 0;
        puVar11[2] = 0;
        *puVar11 = 0;
        FUN_02ac5bf8(&local_1e0,&local_350,0x32);
        if ((long)local_340 < 0) {
          __ZdlPvm(local_350,local_340 & 0x7fffffffffffffff);
        }
        if ((long)local_2d0 < 0) {
          __ZdlPvm(local_2e0,local_2d0 & 0x7fffffffffffffff);
        }
        if ((int)local_210 == 0 && local_210._4_4_ == 0) {
          *param_1 = local_210;
          if (-1 < (long)puStack_1f8) goto LAB_031ceefc;
          FUN_00018d20(param_1 + 1,puStack_208,local_200);
        }
        else {
          iVar6 = thunk_FUN_05e1d97c(4);
          if (iVar6 != 0) {
            FUN_0488143c(&local_1a0);
            ppppuVar10 = (undefined8 ****)local_1a0;
            if (-1 < cStack_189) {
              ppppuVar10 = &local_1a0;
            }
            if ((DAT_0a3dd363 & 1) == 0) {
              uVar12 = 0;
              do {
                (&DAT_0a3dd350)[uVar12] =
                     (&DAT_088bce97)[uVar12] + 0x8a ^ (&DAT_088bce87)[uVar12 & 0xf];
                uVar12 = uVar12 + 1;
              } while (uVar12 != 0x13);
              DAT_0a3dd363 = 1;
            }
            if ((DAT_0a3e04c8 & 1) == 0) {
              _DAT_0a3e04ac = CONCAT44((int)DAT_087f8a18,(int)DAT_08490810);
              uRam000000000a3e04b4 = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
              DAT_0a3e04bc = CONCAT44((int)DAT_08550e48,(int)ram0x0848ba58);
              DAT_0a3e04c4 = (undefined4)ram0x084cf948;
              DAT_0a3e04c8 = 1;
            }
            FUN_05e1d050(&local_2e0,4,ppppuVar10,&DAT_0a3dd350,&DAT_0a3e04ac,
                         "s.framework/Versions/A/CoreGraphics",0,0);
            FUN_030f1f08(local_2f8,*param_3);
            local_150 = local_2f8[0];
            if (-1 < cStack_2e1) {
              local_150 = local_2f8;
            }
            local_148 = 0;
            if ((DAT_0a3e0594 & 1) == 0) {
              _DAT_0a3e056c = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
              uRam000000000a3e0574 = CONCAT44((int)ram0x087e2de8,(int)DAT_084e3ff8);
              _DAT_0a3e057c = CONCAT44((int)DAT_0854dcf8,(int)DAT_087e2df0);
              uRam000000000a3e0584 = CONCAT44((int)DAT_084a66b0,(int)DAT_0867c9b8);
              DAT_0a3e058c = CONCAT44((int)DAT_0847fde8,(int)DAT_0847fde0);
              DAT_0a3e0594 = 1;
            }
            local_f0 = 0;
            pppuStack_f8 = (undefined8 ****)0x0;
            local_100 = &local_150;
            local_e0 = 0;
            uStack_e8 = 0;
            local_d0 = 0;
            uStack_d8 = 0;
            local_c0 = 0;
            uStack_c8 = 0;
            local_b0 = 0;
            uStack_b8 = 0;
            local_a0 = 0;
            uStack_a8 = 0;
            local_90 = 0;
            uStack_98 = 0;
            uStack_88 = 0;
            FUN_05e1d31c(&local_2e0,&DAT_0a3e056c,&local_100);
            if (cStack_2e1 < '\0') {
              __ZdlPvm(local_2f8[0],CONCAT17(cStack_2e1,local_2e8) & 0x7fffffffffffffff);
            }
            thunk_FUN_05e1d0bc(&local_2e0);
            if (cStack_189 < '\0') {
              __ZdlPvm(local_1a0,CONCAT17(cStack_189,local_190) & 0x7fffffffffffffff);
            }
          }
          *param_1 = local_210;
          if ((long)puStack_1f8 < 0) {
            FUN_00018d20(param_1 + 1,puStack_208,local_200);
          }
          else {
LAB_031ceefc:
            uVar17 = *puVar9;
            param_1[2] = puVar9[1];
            param_1[1] = uVar17;
            param_1[3] = puVar9[2];
          }
        }
        param_1[4] = local_1f0;
        param_1[5] = local_1e8;
        if (local_1e8 != (long *)0x0) {
          local_1e8[1] = local_1e8[1] + 1;
        }
      }
      plVar8 = local_308;
      if (local_308 != (long *)0x0) {
        LOAcquire();
        lVar5 = local_308[1];
        local_308[1] = lVar5 + -1;
        LORelease();
        if (lVar5 == 0) {
          (**(code **)(*local_308 + 0x10))(local_308);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        }
      }
      goto LAB_031ceb10;
    }
    lVar5 = *param_3;
    local_2e0 = *(undefined8 ****)(lVar5 + 0x18);
    plVar8 = *(long **)(lVar5 + 0x20);
    if (plVar8 != (long *)0x0) {
      lVar5 = plVar8[1];
      plVar8[1] = lVar5 + 1;
    }
    plStack_2d8 = plVar8;
    FUN_0317d1cc(lVar5,param_2);
    if (plVar8 != (long *)0x0) {
      LOAcquire();
      lVar5 = plVar8[1];
      plVar8[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*plVar8 + 0x10))(plVar8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    *param_1 = local_210;
    if (-1 < (long)puStack_1f8) goto LAB_031ceae0;
    FUN_00018d20(param_1 + 1,puStack_208,local_200);
  }
  else {
    iVar6 = thunk_FUN_05e1d97c(4);
    if (iVar6 != 0) {
      FUN_0488143c(local_2f8);
      ppppuVar10 = (undefined8 ****)local_2f8[0];
      if (-1 < cStack_2e1) {
        ppppuVar10 = local_2f8;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar12 = 0;
        do {
          (&DAT_0a3dd350)[uVar12] = (&DAT_088bce97)[uVar12] + 0x8a ^ (&DAT_088bce87)[uVar12 & 0xf];
          uVar12 = uVar12 + 1;
        } while (uVar12 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3e04c8 & 1) == 0) {
        _DAT_0a3e04ac = CONCAT44((int)DAT_087f8a18,(int)DAT_08490810);
        uRam000000000a3e04b4 = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
        DAT_0a3e04bc = CONCAT44((int)DAT_08550e48,(int)ram0x0848ba58);
        DAT_0a3e04c4 = (undefined4)ram0x084cf948;
        DAT_0a3e04c8 = 1;
      }
      FUN_05e1d050(&local_2e0,4,ppppuVar10,&DAT_0a3dd350,&DAT_0a3e04ac,
                   "ameworks/CoreGraphics.framework/Versions/A/CoreGraphics",0,0);
      FUN_030f1f08(&local_310,*param_3);
      local_150 = local_310;
      if (-1 < cStack_2f9) {
        local_150 = &local_310;
      }
      local_148 = 0;
      uVar12 = FUN_030f320c(*param_3);
      local_1a0 = (undefined8 ***)&local_198;
      if ((DAT_0a3e2eba & 1) == 0) {
        uVar16 = 0;
        do {
          uVar18 = *(undefined4 *)((long)&DAT_088c56c9 + uVar16);
          uVar2 = CONCAT12((char)((uint)uVar18 >> 8),(short)uVar18) & 0xff00ff;
          uVar19 = *(undefined4 *)((long)&DAT_088c56b5 + uVar16 % 0x14);
          *(uint *)((long)&DAT_0a3e2e72 + uVar16) =
               CONCAT13((char)((uint)uVar18 >> 0x18) + 0x69U ^ (byte)((uint)uVar19 >> 0x18),
                        CONCAT12((char)((uint)uVar18 >> 0x10) + 0x69U ^ (byte)((uint)uVar19 >> 0x10)
                                 ,CONCAT11((char)(uVar2 >> 0x10) + 0x69U ^ (byte)((uint)uVar19 >> 8)
                                           ,(char)uVar2 + 0x69U ^ (byte)uVar19)));
          uVar16 = uVar16 + 4;
        } while (uVar16 != 0x48);
        DAT_0a3e2eba = 1;
      }
      lVar5 = 0;
      do {
        lVar15 = lVar5;
        uVar7 = (uint)uVar12;
        *(undefined1 *)((long)&local_198 + lVar15) =
             *(undefined1 *)
              ((long)&DAT_0a3e2e72 + (ulong)(uVar7 + (int)((uVar12 & 0xffffffff) / 10) * -10 + 0x23)
              );
        uVar12 = (uVar12 & 0xffffffff) / 10;
        lVar5 = lVar15 + 1;
      } while (9 < uVar7);
      *(undefined1 *)((long)&local_198 + lVar15 + 1) = 0;
      if (8 < lVar15 + 8U) {
        puVar13 = (undefined1 *)((long)&local_198 + lVar15);
        puVar14 = (undefined1 *)((long)&local_198 + 1);
        do {
          uVar1 = *puVar13;
          *puVar13 = puVar14[-1];
          puVar14[-1] = uVar1;
          bVar4 = puVar14 < puVar13 + -1;
          puVar13 = puVar13 + -1;
          puVar14 = puVar14 + 1;
        } while (bVar4);
      }
      if ((DAT_0a3e053d & 1) == 0) {
        _DAT_0a3e0508 = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
        uRam000000000a3e0510 = CONCAT44((int)DAT_085c65f8,(int)DAT_084e3ff8);
        _DAT_0a3e0518 = CONCAT44((int)DAT_0848f630,(int)DAT_085929b8);
        uRam000000000a3e0520 = CONCAT44((int)DAT_088bafd8,(int)DAT_08659498);
        _DAT_0a3e0528 = CONCAT44((int)DAT_085541f8,(int)DAT_084caf50);
        uRam000000000a3e0530 = CONCAT44((int)DAT_08607208,(int)DAT_0853ae30);
        DAT_0a3e0538 = (undefined4)DAT_084e3fc8;
        DAT_0a3e053c = 0;
        DAT_0a3e053d = 1;
      }
      local_100 = &local_150;
      pppuStack_f8 = &local_1a0;
      uStack_e8 = 0;
      local_f0 = 0;
      uStack_d8 = 0;
      local_e0 = 0;
      uStack_c8 = 0;
      local_d0 = 0;
      uStack_b8 = 0;
      local_c0 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_88 = 0;
      local_90 = 0;
      FUN_05e1d31c(&local_2e0,&DAT_0a3e0508,&local_100);
      if (cStack_2f9 < '\0') {
        __ZdlPvm(local_310,CONCAT17(cStack_2f9,local_300) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_2e0);
      if (cStack_2e1 < '\0') {
        __ZdlPvm(local_2f8[0],CONCAT17(cStack_2e1,local_2e8) & 0x7fffffffffffffff);
      }
    }
    *param_1 = local_210;
    if ((long)puStack_1f8 < 0) {
      FUN_00018d20(param_1 + 1,puStack_208,local_200);
    }
    else {
LAB_031ceae0:
      puVar9 = (undefined8 *)((ulong)&local_210 | 8);
      uVar17 = *puVar9;
      param_1[2] = puVar9[1];
      param_1[1] = uVar17;
      param_1[3] = puVar9[2];
    }
  }
  param_1[4] = local_1f0;
  param_1[5] = local_1e8;
  if (local_1e8 != (long *)0x0) {
    local_1e8[1] = local_1e8[1] + 1;
  }
LAB_031ceb10:
  plVar8 = local_1e8;
  if (local_1e8 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_1e8[1];
    local_1e8[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_1e8 + 0x10))(local_1e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  if ((long)puStack_1f8 < 0) {
    __ZdlPvm(puStack_208,(ulong)puStack_1f8 & 0x7fffffffffffffff);
  }
  if ((long)local_1a8 < 0) {
    __ZdlPvm(puStack_1b8,(ulong)local_1a8 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_78) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


