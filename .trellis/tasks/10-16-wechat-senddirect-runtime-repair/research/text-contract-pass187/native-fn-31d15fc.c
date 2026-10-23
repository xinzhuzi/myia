// Ghidra inferred pseudocode; requested=0x31d15fc
// entry=031d15fc end=031d21ff

/* WARNING: Removing unreachable block (ram,0x031d21c0) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_031d15fc(long *param_1,undefined8 param_2,long *param_3)

{
  long lVar1;
  int iVar2;
  size_t sVar3;
  undefined8 *******pppppppuVar4;
  undefined8 *puVar5;
  ulong uVar6;
  long *plVar7;
  undefined8 local_280;
  undefined8 uStack_278;
  ulong local_270;
  undefined8 *******local_260 [2];
  undefined7 local_250;
  char cStack_249;
  undefined8 *******local_248 [2];
  undefined7 local_238;
  char cStack_231;
  long local_230;
  long *local_228;
  undefined8 *******local_220;
  size_t sStack_218;
  undefined8 local_210;
  undefined7 local_208;
  char cStack_201;
  long local_200;
  long *local_1f8;
  long local_190;
  long *plStack_188;
  undefined1 *local_180;
  long *local_178;
  undefined1 *local_170;
  undefined1 *puStack_168;
  undefined1 *local_160;
  undefined8 *******pppppppuStack_158;
  undefined1 *local_150;
  undefined1 *puStack_148;
  undefined1 *puStack_140;
  undefined1 *local_138;
  undefined8 *******local_130;
  undefined1 local_128;
  undefined7 local_120;
  char cStack_119;
  undefined8 *******local_e0;
  long *plStack_d8;
  ulong uStack_d0;
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  if ((DAT_0a3e05b6 & 1) == 0) {
    _DAT_0a3e0598 = CONCAT44((int)DAT_087f8a18,(int)DAT_08490810);
    uRam000000000a3e05a0 = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
    DAT_0a3e05a8 = CONCAT44((int)DAT_088baff8,(int)ram0x084f2cf0);
    DAT_0a3e05b0 = (undefined4)DAT_08606108;
    DAT_0a3e05b4 = 0x65;
    DAT_0a3e05b6 = 1;
  }
  if ((DAT_0a3dd403 & 1) == 0) {
    uVar6 = 0;
    do {
      (&DAT_0a3dd39e)[uVar6] = (&DAT_088bcf0a)[uVar6] + 0x8a ^ (&DAT_088bcefa)[uVar6 & 0xf];
      uVar6 = uVar6 + 1;
    } while (uVar6 != 0x65);
    DAT_0a3dd403 = 1;
  }
  puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
  local_150 = &SUB_aaaaaaaaaaaaaaaa;
  local_138 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_140 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_168 = &SUB_aaaaaaaaaaaaaaaa;
  local_170 = &SUB_aaaaaaaaaaaaaaaa;
  pppppppuStack_158 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  local_160 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0003bb6c(&local_220,&DAT_0a3e0598,&DAT_0a3dd39e,"ork/Versions/A/CoreGraphics");
  if ((DAT_0a3e04ec & 1) == 0) {
    _DAT_0a3e04cc = CONCAT44((int)DAT_088bafb8,(int)DAT_087f22b0);
    uRam000000000a3e04d4 = CONCAT44((int)DAT_085929b8,(int)DAT_088bafc0);
    _DAT_0a3e04dc = CONCAT44((int)ram0x087fa960,(int)DAT_0848f630);
    uRam000000000a3e04e4 = CONCAT44((int)ram0x084cf948,(int)DAT_0886bee0);
    DAT_0a3e04ec = 1;
  }
  local_170 = (undefined1 *)CONCAT44(local_170._4_4_,2);
  local_150 = (undefined1 *)sStack_218;
  pppppppuStack_158 = local_220;
  local_160 = (undefined1 *)0x0;
  puStack_148 = (undefined1 *)0x0;
  puStack_140 = (undefined1 *)0x0;
  local_138 = (undefined1 *)0x0;
  puStack_168 = (undefined1 *)FUN_0474715c();
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
            (&puStack_148,&DAT_0a3e04cc);
  local_180 = &SUB_aaaaaaaaaaaaaaaa;
  local_178 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_190 = *param_3;
  plVar7 = (long *)param_3[1];
  if (plVar7 != (long *)0x0) {
    plVar7[1] = plVar7[1] + 1;
  }
  plStack_188 = plVar7;
  FUN_0318d680(&local_180,param_2,&local_190);
  if (plVar7 != (long *)0x0) {
    LOAcquire();
    lVar1 = plVar7[1];
    plVar7[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*plVar7 + 0x10))(plVar7);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
    }
  }
  if (local_180 == (undefined1 *)0x0) {
    iVar2 = thunk_FUN_05e1d97c(4);
    if (iVar2 != 0) {
      FUN_0488143c(&local_130);
      pppppppuVar4 = local_130;
      if (-1 < cStack_119) {
        pppppppuVar4 = &local_130;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar6 = 0;
        do {
          (&DAT_0a3dd350)[uVar6] = (&DAT_088bce97)[uVar6] + 0x8a ^ (&DAT_088bce87)[uVar6 & 0xf];
          uVar6 = uVar6 + 1;
        } while (uVar6 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3e05b6 & 1) == 0) {
        _DAT_0a3e0598 = CONCAT44((int)DAT_087f8a18,(int)DAT_08490810);
        uRam000000000a3e05a0 = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
        DAT_0a3e05a8 = CONCAT44((int)DAT_088baff8,(int)ram0x084f2cf0);
        DAT_0a3e05b0 = (undefined4)DAT_08606108;
        DAT_0a3e05b4 = 0x65;
        DAT_0a3e05b6 = 1;
      }
      FUN_05e1d050(&local_220,4,pppppppuVar4,&DAT_0a3dd350,&DAT_0a3e0598,"/Versions/A/CoreGraphics",
                   0,0);
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
      local_78 = 0;
      uStack_80 = 0;
      local_68 = 0;
      uStack_70 = 0;
      local_98 = 0;
      uStack_a0 = 0;
      local_88 = 0;
      uStack_90 = 0;
      local_b8 = 0;
      uStack_c0 = 0;
      local_a8 = 0;
      uStack_b0 = 0;
      plStack_d8 = (long *)0x0;
      local_e0 = (undefined8 *******)0x0;
      local_c8 = 0;
      uStack_d0 = 0;
      FUN_05e1d31c(&local_220,&DAT_0a3e0540,&local_e0);
      thunk_FUN_05e1d0bc(&local_220);
      if (cStack_119 < '\0') {
        __ZdlPvm(local_130,CONCAT17(cStack_119,local_120) & 0x7fffffffffffffff);
      }
    }
    FUN_030f6650(param_1,1,1,4,4);
    plVar7 = local_178;
    goto joined_r0x031d20dc;
  }
  param_1[3] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[2] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[5] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[4] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = (long)&SUB_aaaaaaaaaaaaaaaa;
  *param_1 = (long)&SUB_aaaaaaaaaaaaaaaa;
  local_230 = *param_3;
  local_228 = (long *)param_3[1];
  if (local_228 != (long *)0x0) {
    local_228[1] = local_228[1] + 1;
  }
  FUN_030d58e0(param_1,local_180,&local_230);
  plVar7 = local_228;
  if (local_228 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_228[1];
    local_228[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_228 + 0x10))(local_228);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
    }
  }
  if ((int)*param_1 == 0 && *(int *)((long)param_1 + 4) == 0) {
    FUN_030f3214(*param_3,6);
    FUN_030f31fc(&local_220,*param_3);
    FUN_031cbd88(param_2,&local_220);
    if ((long)local_210 < 0) {
      __ZdlPvm(local_220,local_210 & 0x7fffffffffffffff);
    }
    local_e0 = *(undefined8 ********)(*param_3 + 0xa0);
    plStack_d8 = *(long **)(*param_3 + 0xa8);
    if (plStack_d8 != (long *)0x0) {
      plStack_d8[1] = plStack_d8[1] + 1;
    }
    FUN_03189980(&local_220,&local_130,&local_e0);
    *param_1 = (long)local_220;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (param_1 + 1,&sStack_218);
    if (local_1f8 != (long *)0x0) {
      local_1f8[1] = local_1f8[1] + 1;
    }
    plVar7 = (long *)param_1[5];
    param_1[4] = local_200;
    param_1[5] = (long)local_1f8;
    if (plVar7 != (long *)0x0) {
      LOAcquire();
      lVar1 = plVar7[1];
      plVar7[1] = lVar1 + -1;
      LORelease();
      if (lVar1 == 0) {
        (**(code **)(*plVar7 + 0x10))(plVar7);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
      }
    }
    if (local_1f8 != (long *)0x0) {
      LOAcquire();
      lVar1 = *(long *)((long)local_1f8 + 8U);
      *(long *)((long)local_1f8 + 8U) = lVar1 + -1;
      LORelease();
      if (lVar1 == 0) {
        (**(code **)(*local_1f8 + 0x10))(local_1f8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_1f8);
      }
    }
    if (cStack_201 < '\0') {
      __ZdlPvm(sStack_218,CONCAT17(cStack_201,local_208) & 0x7fffffffffffffff);
    }
    plVar7 = plStack_d8;
    if (plStack_d8 != (long *)0x0) {
      LOAcquire();
      lVar1 = plStack_d8[1];
      plStack_d8[1] = lVar1 + -1;
      LORelease();
      if (lVar1 == 0) {
        (**(code **)(*plStack_d8 + 0x10))(plStack_d8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
      }
    }
    if ((int)*param_1 != 0 || *(int *)((long)param_1 + 4) != 0) {
      iVar2 = thunk_FUN_05e1d97c(4);
      plVar7 = local_178;
      if (iVar2 == 0) goto joined_r0x031d20dc;
      FUN_0488143c(local_248);
      pppppppuVar4 = local_248[0];
      if (-1 < cStack_231) {
        pppppppuVar4 = local_248;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar6 = 0;
        do {
          (&DAT_0a3dd350)[uVar6] = (&DAT_088bce97)[uVar6] + 0x8a ^ (&DAT_088bce87)[uVar6 & 0xf];
          uVar6 = uVar6 + 1;
        } while (uVar6 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3e05b6 & 1) == 0) {
        _DAT_0a3e0598 = CONCAT44((int)DAT_087f8a18,(int)DAT_08490810);
        uRam000000000a3e05a0 = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
        DAT_0a3e05a8 = CONCAT44((int)DAT_088baff8,(int)ram0x084f2cf0);
        DAT_0a3e05b0 = (undefined4)DAT_08606108;
        DAT_0a3e05b4 = 0x65;
        DAT_0a3e05b6 = 1;
      }
      FUN_05e1d050(&local_220,4,pppppppuVar4,&DAT_0a3dd350,&DAT_0a3e0598,"Graphics",0,0);
      FUN_030f1f08(local_260,*param_3);
      local_130 = local_260[0];
      if (-1 < cStack_249) {
        local_130 = local_260;
      }
      local_128 = 0;
      if ((DAT_0a3e0609 & 1) == 0) {
        _DAT_0a3e05e8 = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
        uRam000000000a3e05f0 = CONCAT44((int)DAT_087e2f50,(int)DAT_084e3ff8);
        _DAT_0a3e05f8 = CONCAT44((int)DAT_084a8110,(int)DAT_088a7260);
        uRam000000000a3e0600 = CONCAT44((int)ram0x08480938,(int)DAT_08545158);
        DAT_0a3e0608 = 0;
        DAT_0a3e0609 = 1;
      }
      uStack_d0 = 0;
      plStack_d8 = (long *)0x0;
      local_e0 = &local_130;
      uStack_c0 = 0;
      local_c8 = 0;
      uStack_b0 = 0;
      local_b8 = 0;
      uStack_a0 = 0;
      local_a8 = 0;
      uStack_90 = 0;
      local_98 = 0;
      uStack_80 = 0;
      local_88 = 0;
      uStack_70 = 0;
      local_78 = 0;
      local_68 = 0;
      FUN_05e1d31c(&local_220,&DAT_0a3e05e8,&local_e0);
      goto LAB_031d1dc4;
    }
    if ((DAT_0a3e061c & 1) == 0) {
      DAT_0a3e0610._0_1_ = s_send_finileF_088bb000[0];
      DAT_0a3e0610._1_1_ = s_send_finileF_088bb000[1];
      DAT_0a3e0610._2_1_ = s_send_finileF_088bb000[2];
      DAT_0a3e0610._3_1_ = s_send_finileF_088bb000[3];
      DAT_0a3e0610._4_1_ = s_send_finileF_088bb000[4];
      DAT_0a3e0610._5_1_ = s_send_finileF_088bb000[5];
      DAT_0a3e0610._6_1_ = s_send_finileF_088bb000[6];
      DAT_0a3e0610._7_1_ = s_send_finileF_088bb000[7];
      DAT_0a3e0618 = (undefined4)DAT_0853ea88;
      DAT_0a3e061c = 1;
    }
    sVar3 = _strlen((char *)&DAT_0a3e0610);
    if (0x7ffffffffffffff7 < sVar3) {
                    /* WARNING: Subroutine does not return */
      FUN_00018d9c(&local_220);
    }
    if (sVar3 < 0x17) {
      local_210 = CONCAT17((char)sVar3,(undefined7)local_210);
      pppppppuVar4 = &local_220;
      if (sVar3 != 0) goto LAB_031d2050;
    }
    else {
      uVar6 = 0x19;
      if ((sVar3 | 7) != 0x17) {
        uVar6 = (sVar3 | 7) + 1;
      }
      pppppppuVar4 = (undefined8 *******)__Znwm(uVar6);
      local_210 = uVar6 | 0x8000000000000000;
      local_220 = pppppppuVar4;
      sStack_218 = sVar3;
LAB_031d2050:
      _memcpy(pppppppuVar4,&DAT_0a3e0610,sVar3);
    }
    *(undefined1 *)((long)pppppppuVar4 + sVar3) = 0;
    FUN_030f1f08(&local_e0,*param_3);
    plVar7 = plStack_d8;
    pppppppuVar4 = local_e0;
    if (-1 < (long)uStack_d0) {
      plVar7 = (long *)(uStack_d0 >> 0x38);
      pppppppuVar4 = &local_e0;
    }
    puVar5 = (undefined8 *)
             __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                       (&local_220,pppppppuVar4,plVar7);
    uStack_278 = puVar5[1];
    local_280 = *puVar5;
    local_270 = puVar5[2];
    puVar5[1] = 0;
    puVar5[2] = 0;
    *puVar5 = 0;
    FUN_02ac5bf8(&local_170,&local_280,0x32);
    if ((long)local_270 < 0) {
      __ZdlPvm(local_280,local_270 & 0x7fffffffffffffff);
    }
    local_248[0] = local_220;
    uVar6 = local_210;
    plVar7 = local_178;
    if (-1 < (long)local_210) goto joined_r0x031d20dc;
  }
  else {
    iVar2 = thunk_FUN_05e1d97c(4);
    plVar7 = local_178;
    if (iVar2 == 0) goto joined_r0x031d20dc;
    FUN_0488143c(local_248);
    pppppppuVar4 = local_248[0];
    if (-1 < cStack_231) {
      pppppppuVar4 = local_248;
    }
    if ((DAT_0a3dd363 & 1) == 0) {
      uVar6 = 0;
      do {
        (&DAT_0a3dd350)[uVar6] = (&DAT_088bce97)[uVar6] + 0x8a ^ (&DAT_088bce87)[uVar6 & 0xf];
        uVar6 = uVar6 + 1;
      } while (uVar6 != 0x13);
      DAT_0a3dd363 = 1;
    }
    if ((DAT_0a3e05b6 & 1) == 0) {
      _DAT_0a3e0598 = CONCAT44((int)DAT_087f8a18,(int)DAT_08490810);
      uRam000000000a3e05a0 = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
      DAT_0a3e05a8 = CONCAT44((int)DAT_088baff8,(int)ram0x084f2cf0);
      DAT_0a3e05b0 = (undefined4)DAT_08606108;
      DAT_0a3e05b4 = 0x65;
      DAT_0a3e05b6 = 1;
    }
    FUN_05e1d050(&local_220,4,pppppppuVar4,&DAT_0a3dd350,&DAT_0a3e0598,"ons/A/CoreGraphics",0,0);
    FUN_030f1f08(local_260,*param_3);
    local_130 = local_260[0];
    if (-1 < cStack_249) {
      local_130 = local_260;
    }
    local_128 = 0;
    if ((DAT_0a3e05e5 & 1) == 0) {
      _DAT_0a3e05b8 = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
      uRam000000000a3e05c0 = CONCAT44((int)ram0x087e2de8,(int)DAT_084e3ff8);
      _DAT_0a3e05c8 = CONCAT44((int)DAT_08508320,(int)DAT_087e2df0);
      uRam000000000a3e05d0 = CONCAT44((int)DAT_086eb4a8,(int)DAT_084a66b0);
      DAT_0a3e05d8 = CONCAT44((int)ram0x08567fa8,(int)DAT_086c55e0);
      DAT_0a3e05e0 = (undefined4)ram0x08480938;
      DAT_0a3e05e4 = 0;
      DAT_0a3e05e5 = 1;
    }
    uStack_d0 = 0;
    plStack_d8 = (long *)0x0;
    local_e0 = &local_130;
    uStack_c0 = 0;
    local_c8 = 0;
    uStack_b0 = 0;
    local_b8 = 0;
    uStack_a0 = 0;
    local_a8 = 0;
    uStack_90 = 0;
    local_98 = 0;
    uStack_80 = 0;
    local_88 = 0;
    uStack_70 = 0;
    local_78 = 0;
    local_68 = 0;
    FUN_05e1d31c(&local_220,&DAT_0a3e05b8,&local_e0);
LAB_031d1dc4:
    if (cStack_249 < '\0') {
      __ZdlPvm(local_260[0],CONCAT17(cStack_249,local_250) & 0x7fffffffffffffff);
    }
    thunk_FUN_05e1d0bc(&local_220);
    plVar7 = local_178;
    if (-1 < cStack_231) goto joined_r0x031d20dc;
    uVar6 = CONCAT17(cStack_231,local_238);
  }
  __ZdlPvm(local_248[0],uVar6 & 0x7fffffffffffffff);
  plVar7 = local_178;
joined_r0x031d20dc:
  local_178 = plVar7;
  if (plVar7 != (long *)0x0) {
    LOAcquire();
    lVar1 = plVar7[1];
    plVar7[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*plVar7 + 0x10))(plVar7);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
    }
  }
  if ((long)local_138 < 0) {
    __ZdlPvm(puStack_148,(ulong)local_138 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


