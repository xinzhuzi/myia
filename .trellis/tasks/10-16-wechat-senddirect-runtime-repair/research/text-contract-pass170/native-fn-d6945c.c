// Ghidra inferred pseudocode; requested=0xd6945c
// entry=00d6945c end=00d69c2f

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00d6945c(long param_1)

{
  undefined8 ****ppppuVar1;
  undefined8 *****pppppuVar2;
  char cVar3;
  undefined8 ***pppuVar4;
  undefined8 ***pppuVar5;
  int iVar6;
  undefined8 ****ppppuVar7;
  undefined8 uVar8;
  long *plVar9;
  undefined8 uVar10;
  long *plVar11;
  code *pcVar12;
  undefined8 ****ppppuVar13;
  long lVar14;
  undefined8 ****local_1f0;
  long *local_1e8;
  undefined8 ****local_1e0;
  long *local_1d8;
  undefined7 local_1d0;
  char cStack_1c9;
  undefined **local_1c8;
  undefined8 ****ppppuStack_1c0;
  long *local_1b8;
  undefined ***local_1b0;
  undefined8 local_1a8 [2];
  undefined7 local_198;
  char cStack_191;
  undefined8 ****local_d0;
  undefined8 ***pppuStack_c8;
  undefined8 uStack_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  cVar3 = *(char *)(*(long *)(param_1 + 0x188) + 0x4f);
  if (cVar3 < '\0') {
    if (*(long *)(*(long *)(param_1 + 0x188) + 0x40) == 0) goto LAB_00d697ac;
  }
  else if (cVar3 == '\0') {
LAB_00d697ac:
    iVar6 = thunk_FUN_05e1d97c(4);
    if (iVar6 != 0) {
      FUN_0488143c(&local_1e0);
      pppppuVar2 = (undefined8 *****)local_1e0;
      if (-1 < cStack_1c9) {
        pppppuVar2 = &local_1e0;
      }
      if ((DAT_0a2c6f5e & 1) == 0) {
        _DAT_0a2c6f44 = CONCAT44((int)DAT_08499880,(int)DAT_08499878);
        uRam000000000a2c6f4c = CONCAT44((int)DAT_08487d48,(int)DAT_084958e0);
        DAT_0a2c6f54 = CONCAT44((int)DAT_085898b0,(int)DAT_084a9ae8);
        DAT_0a2c6f5c = 99;
        DAT_0a2c6f5e = 1;
      }
      if ((DAT_0a2c70fd & 1) == 0) {
        _DAT_0a2c70e8 = CONCAT44((int)DAT_084e6250,(int)ram0x08490a68);
        uRam000000000a2c70f0 = CONCAT44((int)DAT_085a5e28,(int)DAT_0849a570);
        DAT_0a2c70f8 = (undefined4)DAT_084f5570;
        DAT_0a2c70fc = 0;
        DAT_0a2c70fd = 1;
      }
      FUN_05e1d050(local_1a8,4,pppppuVar2,&DAT_0a2c6f44,&DAT_0a2c70e8,0x22b,0,0);
      if ((DAT_0a2c711e & 1) == 0) {
        _DAT_0a2c7100 = CONCAT44((int)ram0x085a5e38,(int)DAT_08482430);
        uRam000000000a2c7108 = CONCAT44((int)DAT_08499850,(int)DAT_08486a60);
        DAT_0a2c7110 = CONCAT44((int)DAT_084cadd8,(int)DAT_084ca318);
        DAT_0a2c7118 = (undefined4)DAT_0849d5c0;
        DAT_0a2c711c = 0x79;
        DAT_0a2c711e = 1;
      }
      uStack_68 = 0;
      local_70 = 0;
      uStack_58 = 0;
      uStack_60 = 0;
      uStack_88 = 0;
      local_90 = 0;
      uStack_78 = 0;
      uStack_80 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      uStack_a0 = 0;
      pppuStack_c8 = (undefined8 ***)0x0;
      local_d0 = (undefined8 *****)0x0;
      uStack_b8 = 0;
      uStack_c0 = 0;
      FUN_05e1d31c(local_1a8,&DAT_0a2c7100,&local_d0);
      thunk_FUN_05e1d0bc(local_1a8);
      if (cStack_1c9 < '\0') {
        __ZdlPvm(local_1e0,CONCAT17(cStack_1c9,local_1d0) & 0x7fffffffffffffff);
      }
    }
    goto LAB_00d69bfc;
  }
  iVar6 = thunk_FUN_05e1d97c(2);
  if (iVar6 != 0) {
    FUN_0488143c(&local_1e0);
    pppppuVar2 = (undefined8 *****)local_1e0;
    if (-1 < cStack_1c9) {
      pppppuVar2 = &local_1e0;
    }
    if ((DAT_0a2c6f5e & 1) == 0) {
      _DAT_0a2c6f44 = CONCAT44((int)DAT_08499880,(int)DAT_08499878);
      uRam000000000a2c6f4c = CONCAT44((int)DAT_08487d48,(int)DAT_084958e0);
      DAT_0a2c6f54 = CONCAT44((int)DAT_085898b0,(int)DAT_084a9ae8);
      DAT_0a2c6f5c = 99;
      DAT_0a2c6f5e = 1;
    }
    if ((DAT_0a2c70fd & 1) == 0) {
      _DAT_0a2c70e8 = CONCAT44((int)DAT_084e6250,(int)ram0x08490a68);
      uRam000000000a2c70f0 = CONCAT44((int)DAT_085a5e28,(int)DAT_0849a570);
      DAT_0a2c70f8 = (undefined4)DAT_084f5570;
      DAT_0a2c70fc = 0;
      DAT_0a2c70fd = 1;
    }
    FUN_05e1d050(local_1a8,2,pppppuVar2,&DAT_0a2c6f44,&DAT_0a2c70e8,0x22e,0,0);
    if ((DAT_0a2c712e & 1) == 0) {
      DAT_0a2c7120._0_1_ = s_ShowShare__>_085a5e30[0];
      DAT_0a2c7120._1_1_ = s_ShowShare__>_085a5e30[1];
      DAT_0a2c7120._2_1_ = s_ShowShare__>_085a5e30[2];
      DAT_0a2c7120._3_1_ = s_ShowShare__>_085a5e30[3];
      DAT_0a2c7120._4_1_ = s_ShowShare__>_085a5e30[4];
      DAT_0a2c7120._5_1_ = s_ShowShare__>_085a5e30[5];
      DAT_0a2c7120._6_1_ = s_ShowShare__>_085a5e30[6];
      DAT_0a2c7120._7_1_ = s_ShowShare__>_085a5e30[7];
      DAT_0a2c7128 = (undefined4)DAT_084ec170;
      DAT_0a2c712c = 0x77;
      DAT_0a2c712e = 1;
    }
    uStack_68 = 0;
    local_70 = 0;
    uStack_58 = 0;
    uStack_60 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    uStack_80 = 0;
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    uStack_a0 = 0;
    pppuStack_c8 = (undefined8 ***)0x0;
    local_d0 = (undefined8 *****)0x0;
    uStack_b8 = 0;
    uStack_c0 = 0;
    FUN_05e1d31c(local_1a8,&DAT_0a2c7120,&local_d0);
    thunk_FUN_05e1d0bc(local_1a8);
    if (cStack_1c9 < '\0') {
      __ZdlPvm(local_1e0,CONCAT17(cStack_1c9,local_1d0) & 0x7fffffffffffffff);
    }
  }
  lVar14 = *(long *)(param_1 + 0x188);
  local_1e0 = (undefined8 ****)&SUB_aaaaaaaaaaaaaaaa;
  local_1d8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_00d6bd24(&local_1e0,local_1a8);
  ppppuVar7 = (undefined8 ****)__Znwm(0x2e0);
  ppppuVar13 = ppppuVar7 + 1;
  *ppppuVar13 = (undefined8 ***)0x0;
  ppppuVar7[2] = (undefined8 ***)0x0;
  *ppppuVar7 = (undefined8 ***)&PTR_FUN_09c83160;
  ppppuVar1 = ppppuVar7 + 3;
  _bzero(ppppuVar1,0x2c8);
  if (ppppuVar7 != (undefined8 ****)0x0) {
    *ppppuVar13 = (undefined8 ***)((long)*ppppuVar13 + 1);
  }
  local_1e0[0xb9] = ppppuVar1;
  ppppuVar13 = (undefined8 ****)local_1e0[0xba];
  local_1e0[0xba] = ppppuVar7;
  local_d0 = ppppuVar1;
  pppuStack_c8 = ppppuVar7;
  if (ppppuVar13 != (undefined8 ****)0x0) {
    LOAcquire();
    pppuVar4 = ppppuVar13[1];
    ppppuVar13[1] = (undefined8 ***)((long)pppuVar4 + -1);
    LORelease();
    if (pppuVar4 == (undefined8 ***)0x0) {
      (*(code *)(*ppppuVar13)[2])(ppppuVar13);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppppuVar13);
    }
  }
  ppppuVar1 = local_d0;
  FUN_017b5a0c(local_d0,lVar14 + 0x38);
  FUN_012a58d8(ppppuVar1,lVar14 + 0xb0);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(ppppuVar1,lVar14 + 0x170)
  ;
  FUN_013a5688(ppppuVar1,lVar14 + 0x188);
  __ZNSt3__19to_stringEi(local_1a8,*(undefined4 *)(lVar14 + 0x8c));
  FUN_017b5a14(ppppuVar1,local_1a8);
  if (cStack_191 < '\0') {
    __ZdlPvm(local_1a8[0],CONCAT17(cStack_191,local_198) & 0x7fffffffffffffff);
  }
  FUN_017b5a24(ppppuVar1,lVar14 + 0x68);
  FUN_04d1b410(ppppuVar1,0);
  if (*(char *)(lVar14 + 0x90) == '\x01') {
    *(undefined4 *)((long)local_1e0 + 0xe4) = 0x42;
    FUN_04d1b3e0(ppppuVar1,lVar14 + 600);
    FUN_04d1b3d8(ppppuVar1,lVar14 + 0x288);
    if (*(long *)(lVar14 + 0x270) != *(long *)(lVar14 + 0x278)) {
      FUN_04d1b3e8(ppppuVar1,*(long *)(lVar14 + 0x270) + 0x18);
    }
    FUN_04d1b3f8(ppppuVar1,lVar14 + 0x2a0);
  }
  else {
    *(undefined4 *)((long)local_1e0 + 0xe4) = 0x2a;
    FUN_017b5a1c(ppppuVar1,lVar14 + 0x308);
    FUN_01520830(ppppuVar1,lVar14 + 800);
    FUN_017b5a2c(ppppuVar1,lVar14 + 0x338);
    FUN_017b6288(ppppuVar1,lVar14 + 0x350);
    FUN_017b6290(ppppuVar1,lVar14 + 0x368);
    FUN_04d1b398(ppppuVar1,lVar14 + 0x380);
    FUN_04d1b3a0(ppppuVar1,lVar14 + 0x398);
    FUN_04d1b3a8(ppppuVar1,*(undefined4 *)(lVar14 + 0x3b0));
    FUN_04d1b3b0(ppppuVar1,lVar14 + 0x3b8);
    FUN_04d1b3b8(ppppuVar1,lVar14 + 0x3d0);
    FUN_018fb884(ppppuVar1,lVar14 + 1000);
    FUN_04d1b3c0(ppppuVar1,lVar14 + 0x400);
    FUN_04d1b3c8(ppppuVar1,lVar14 + 0x418);
    FUN_0136d508(ppppuVar1,lVar14 + 0x430);
    FUN_04d1b3d0(ppppuVar1,lVar14 + 0x448);
  }
  pppuVar4 = pppuStack_c8;
  if ((undefined8 ****)pppuStack_c8 != (undefined8 ****)0x0) {
    LOAcquire();
    pppuVar5 = (undefined8 ***)pppuStack_c8[1];
    pppuStack_c8[1] = (undefined8 ***)((long)pppuVar5 + -1);
    LORelease();
    if (pppuVar5 == (undefined8 ***)0x0) {
      (*(code *)(*pppuStack_c8)[2])(pppuStack_c8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(pppuVar4);
    }
  }
  plVar11 = local_1d8;
  ppppuVar1 = local_1e0;
  local_d0 = local_1e0;
  pppuStack_c8 = (undefined8 ***)local_1d8;
  if (local_1d8 == (long *)0x0) {
    local_1e8 = (long *)0x0;
  }
  else {
    local_1d8[1] = local_1d8[1] + 1;
    local_1e8 = local_1d8;
    if (local_1d8 != (long *)0x0) {
      local_1d8[1] = local_1d8[1] + 1;
    }
  }
  local_1f0 = local_1e0;
  FUN_01864258(local_1a8,&local_1f0);
  uVar8 = FUN_0186d704(local_1a8,0);
  plVar9 = (long *)FUN_002badd0(DAT_0a52bdd0);
  uVar10 = (**(code **)(*plVar9 + 0x78))();
  uVar8 = FUN_0186d714(uVar8,uVar10);
  if (plVar11 != (long *)0x0) {
    plVar11[1] = plVar11[1] + 1;
  }
  local_1c8 = &PTR_FUN_09c83748;
  ppppuStack_1c0 = ppppuVar1;
  local_1b0 = &local_1c8;
  local_1b8 = plVar11;
  FUN_0186d724(uVar8,&local_1c8);
  plVar11 = (long *)FUN_0186d8d4();
  if (local_1b0 == &local_1c8) {
    pcVar12 = (code *)(*local_1b0)[4];
LAB_00d69b50:
    (*pcVar12)();
  }
  else if (local_1b0 != (undefined ***)0x0) {
    pcVar12 = (code *)(*local_1b0)[5];
    goto LAB_00d69b50;
  }
  FUN_0063e888(local_1a8);
  plVar9 = local_1e8;
  if (local_1e8 != (long *)0x0) {
    LOAcquire();
    lVar14 = local_1e8[1];
    local_1e8[1] = lVar14 + -1;
    LORelease();
    if (lVar14 == 0) {
      (**(code **)(*local_1e8 + 0x10))(local_1e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar9);
    }
  }
  (**(code **)(*plVar11 + 0x1b8))(plVar11);
  pppuVar4 = pppuStack_c8;
  if (pppuStack_c8 != (undefined8 ***)0x0) {
    LOAcquire();
    lVar14 = (long)pppuStack_c8[1];
    pppuStack_c8[1] = (undefined8 **)(lVar14 + -1);
    LORelease();
    if (lVar14 == 0) {
      (**(code **)((long)*pppuStack_c8 + 0x10))(pppuStack_c8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(pppuVar4);
    }
  }
  plVar11 = local_1d8;
  if (local_1d8 != (long *)0x0) {
    LOAcquire();
    lVar14 = local_1d8[1];
    local_1d8[1] = lVar14 + -1;
    LORelease();
    if (lVar14 == 0) {
      (**(code **)(*local_1d8 + 0x10))(local_1d8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar11);
    }
  }
LAB_00d69bfc:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


