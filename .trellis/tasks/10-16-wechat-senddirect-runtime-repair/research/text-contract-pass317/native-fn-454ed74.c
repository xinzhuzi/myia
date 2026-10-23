// Ghidra inferred pseudocode; requested=0x454ed74
// entry=0454ed74 end=0454f65b

/* WARNING: Removing unreachable block (ram,0x0454f4f0) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 * FUN_0454ed74(undefined8 *param_1)

{
  undefined8 *****pppppuVar1;
  char cVar2;
  undefined4 uVar3;
  uint3 uVar4;
  long lVar5;
  long lVar6;
  int iVar7;
  undefined8 uVar8;
  ulong uVar9;
  long *plVar10;
  long *plVar11;
  long lVar12;
  undefined4 uVar13;
  undefined8 ****local_178 [2];
  undefined7 local_168;
  char cStack_161;
  undefined1 *local_160;
  undefined1 *puStack_158;
  undefined1 *local_150;
  undefined1 *puStack_148;
  undefined1 *local_140;
  undefined1 *puStack_138;
  undefined1 *local_130;
  undefined1 *local_128;
  undefined8 local_d0;
  undefined8 uStack_c8;
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
  *param_1 = &PTR_FUN_09e87768;
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(local_178);
    pppppuVar1 = (undefined8 *****)local_178[0];
    if (-1 < cStack_161) {
      pppppuVar1 = local_178;
    }
    if ((DAT_0a455f21 & 1) == 0) {
      uRam000000000a455f18 = _UNK_089ffce8;
      _DAT_0a455f10 = _DAT_089ffce0;
      DAT_0a455f20 = 0;
      DAT_0a455f21 = 1;
    }
    if ((DAT_0a4560a5 & 1) == 0) {
      _DAT_0a456090 = CONCAT44((int)DAT_0894cd48,(int)DAT_087b7ec8);
      uRam000000000a456098 = CONCAT44((int)DAT_089ffb70,(int)DAT_08492618);
      DAT_0a4560a0 = (undefined4)DAT_0848e550;
      DAT_0a4560a4 = 0;
      DAT_0a4560a5 = 1;
    }
    FUN_05e1d050(&local_160,2,pppppuVar1,&DAT_0a455f10,&DAT_0a456090,0x93,0,0);
    if ((DAT_0a4560c3 & 1) == 0) {
      _DAT_0a4560a8 = CONCAT44((int)DAT_085aff30,(int)DAT_085aff28);
      uRam000000000a4560b0 = CONCAT44((int)DAT_08592988,(int)DAT_0849a618);
      DAT_0a4560b8 = CONCAT44((int)DAT_089c0690,(int)DAT_084d4ae0);
      DAT_0a4560c0 = 0x7469;
      DAT_0a4560c2 = 0;
      DAT_0a4560c3 = 1;
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
    uStack_c8 = 0;
    local_d0 = 0;
    uStack_b8 = 0;
    uStack_c0 = 0;
    FUN_05e1d31c(&local_160,&DAT_0a4560a8,&local_d0);
    thunk_FUN_05e1d0bc(&local_160);
    if (cStack_161 < '\0') {
      __ZdlPvm(local_178[0],CONCAT17(cStack_161,local_168) & 0x7fffffffffffffff);
    }
  }
  puStack_138 = &SUB_aaaaaaaaaaaaaaaa;
  local_140 = &SUB_aaaaaaaaaaaaaaaa;
  local_128 = &SUB_aaaaaaaaaaaaaaaa;
  local_130 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_158 = &SUB_aaaaaaaaaaaaaaaa;
  local_160 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
  local_150 = &SUB_aaaaaaaaaaaaaaaa;
  if ((DAT_0a4560a5 & 1) == 0) {
    _DAT_0a456090 = CONCAT44((int)DAT_0894cd48,(int)DAT_087b7ec8);
    uRam000000000a456098 = CONCAT44((int)DAT_089ffb70,(int)DAT_08492618);
    DAT_0a4560a0 = (undefined4)DAT_0848e550;
    DAT_0a4560a4 = 0;
    DAT_0a4560a5 = 1;
  }
  if ((DAT_0a455fff & 1) == 0) {
    uVar9 = 0;
    do {
      uVar13 = *(undefined4 *)((long)&DAT_08a00242 + uVar9);
      uVar4 = CONCAT12((char)((uint)uVar13 >> 8),(short)uVar13) & 0xff00ff;
      uVar3 = *(undefined4 *)((long)&DAT_08a0022e + uVar9 % 0x14);
      *(uint *)((long)&DAT_0a455f9e + uVar9) =
           CONCAT13((char)((uint)uVar13 >> 0x18) + 0x8aU ^ (byte)((uint)uVar3 >> 0x18),
                    CONCAT12((char)((uint)uVar13 >> 0x10) + 0x8aU ^ (byte)((uint)uVar3 >> 0x10),
                             CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^ (byte)((uint)uVar3 >> 8),
                                      (char)uVar4 + 0x8aU ^ (byte)uVar3)));
      uVar9 = uVar9 + 4;
    } while (uVar9 != 0x60);
    DAT_0a455ffe = 0;
    DAT_0a455fff = 1;
  }
  FUN_0003bb6c(&local_d0,&DAT_0a456090,&DAT_0a455f9e,0x94);
  if ((DAT_0a4560ca & 1) == 0) {
    DAT_0a4560c4 = (undefined4)DAT_08482430;
    DAT_0a4560c8 = 0x65;
    DAT_0a4560ca = 1;
  }
  local_160 = (undefined1 *)CONCAT44(local_160._4_4_,2);
  local_150 = (undefined1 *)0x0;
  local_140 = (undefined1 *)uStack_c8;
  puStack_148 = (undefined1 *)local_d0;
  local_130 = (undefined1 *)0x0;
  local_128 = (undefined1 *)0x0;
  puStack_138 = (undefined1 *)0x0;
  puStack_158 = (undefined1 *)FUN_0474715c();
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
            (&puStack_138,&DAT_0a4560c4);
  plVar10 = (long *)param_1[0x6e];
  param_1[0x6e] = 0;
  param_1[0x6d] = 0;
  if (plVar10 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar10[1];
    plVar10[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar10 + 0x10))(plVar10);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  if ((DAT_0a4560cd & 1) == 0) {
    DAT_0a4560cb = 0x31;
    DAT_0a4560cd = 1;
  }
  FUN_00ebbf48(&local_160,&DAT_0a4560cb,0);
  if ((long)local_128 < 0) {
    __ZdlPvm(puStack_138,(ulong)local_128 & 0x7fffffffffffffff);
  }
  plVar10 = (long *)param_1[0x8d];
  while (plVar10 != (long *)0x0) {
    lVar5 = *plVar10;
    if (*(char *)((long)plVar10 + 0x27) < '\0') {
      __ZdlPvm(plVar10[2],plVar10[4] & 0x7fffffffffffffff);
    }
    __ZdlPvm(plVar10,0x28);
    plVar10 = (long *)lVar5;
  }
  lVar5 = param_1[0x8b];
  param_1[0x8b] = 0;
  if (lVar5 != 0) {
    __ZdlPvm(lVar5,param_1[0x8c] << 3);
  }
  FUN_00999678(param_1 + 0x86);
  plVar10 = (long *)param_1[0x83];
  while (plVar10 != (long *)0x0) {
    lVar5 = *plVar10;
    plVar11 = (long *)plVar10[4];
    if (plVar11 != (long *)0x0) {
      LOAcquire();
      lVar6 = plVar11[1];
      plVar11[1] = lVar6 + -1;
      LORelease();
      if (lVar6 == 0) {
        (**(code **)(*plVar11 + 0x10))(plVar11);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar11);
      }
    }
    __ZdlPvm(plVar10,0x28);
    plVar10 = (long *)lVar5;
  }
  lVar5 = param_1[0x81];
  param_1[0x81] = 0;
  if (lVar5 != 0) {
    __ZdlPvm(lVar5,param_1[0x82] << 3);
  }
  FUN_0006a460(param_1 + 0x77);
  plVar10 = (long *)param_1[0x76];
  if (plVar10 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar10[1];
    plVar10[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar10 + 0x10))(plVar10);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  plVar10 = (long *)param_1[0x74];
  if (plVar10 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar10[1];
    plVar10[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar10 + 0x10))(plVar10);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  plVar10 = (long *)param_1[0x72];
  if (plVar10 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar10[1];
    plVar10[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar10 + 0x10))(plVar10);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  plVar10 = (long *)param_1[0x70];
  if (plVar10 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar10[1];
    plVar10[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar10 + 0x10))(plVar10);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  plVar10 = (long *)param_1[0x6e];
  if (plVar10 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar10[1];
    plVar10[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar10 + 0x10))(plVar10);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  plVar10 = (long *)param_1[0x6c];
  if (plVar10 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar10[1];
    plVar10[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar10 + 0x10))(plVar10);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  plVar10 = (long *)param_1[0x6a];
  if (plVar10 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar10[1];
    plVar10[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar10 + 0x10))(plVar10);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
      cVar2 = *(char *)((long)param_1 + 0x347);
      goto joined_r0x0454f348;
    }
  }
  cVar2 = *(char *)((long)param_1 + 0x347);
joined_r0x0454f348:
  if (cVar2 < '\0') {
    __ZdlPvm(param_1[0x66],param_1[0x68] & 0x7fffffffffffffff);
    cVar2 = *(char *)((long)param_1 + 0x32f);
  }
  else {
    cVar2 = *(char *)((long)param_1 + 0x32f);
  }
  if (cVar2 < '\0') {
    __ZdlPvm(param_1[99],param_1[0x65] & 0x7fffffffffffffff);
  }
  lVar5 = param_1[0x62];
  param_1[0x62] = 0;
  if (lVar5 != 0) {
    __ZdlPvm(lVar5,1);
  }
  lVar5 = param_1[0x61];
  param_1[0x61] = 0;
  if (lVar5 != 0) {
    uVar8 = FUN_0455e43c();
    __ZdlPvm(uVar8,0x10);
  }
  FUN_045571c0(param_1 + 0x57);
  if (*(char *)((long)param_1 + 0x2b7) < '\0') {
    __ZdlPvm(param_1[0x54],param_1[0x56] & 0x7fffffffffffffff);
    cVar2 = *(char *)((long)param_1 + 0x29f);
  }
  else {
    cVar2 = *(char *)((long)param_1 + 0x29f);
  }
  if (cVar2 < '\0') {
    __ZdlPvm(param_1[0x51],param_1[0x53] & 0x7fffffffffffffff);
    lVar5 = param_1[0x4e];
  }
  else {
    lVar5 = param_1[0x4e];
  }
  if (lVar5 == 0) {
    cVar2 = *(char *)((long)param_1 + 0x26f);
  }
  else {
    lVar12 = param_1[0x4f];
    lVar6 = lVar5;
    if (lVar12 != lVar5) {
      do {
        lVar12 = lVar12 + -0x18;
      } while (lVar12 != lVar5);
      lVar6 = param_1[0x4e];
    }
    param_1[0x4f] = lVar5;
    __ZdlPvm(lVar6,param_1[0x50] - lVar6);
    cVar2 = *(char *)((long)param_1 + 0x26f);
  }
  if (cVar2 < '\0') {
    __ZdlPvm(param_1[0x4b],param_1[0x4d] & 0x7fffffffffffffff);
    cVar2 = *(char *)((long)param_1 + 599);
  }
  else {
    cVar2 = *(char *)((long)param_1 + 599);
  }
  if (cVar2 < '\0') {
    __ZdlPvm(param_1[0x48],param_1[0x4a] & 0x7fffffffffffffff);
    cVar2 = *(char *)((long)param_1 + 0x23f);
  }
  else {
    cVar2 = *(char *)((long)param_1 + 0x23f);
  }
  if (cVar2 < '\0') {
    __ZdlPvm(param_1[0x45],param_1[0x47] & 0x7fffffffffffffff);
    cVar2 = *(char *)((long)param_1 + 0x227);
  }
  else {
    cVar2 = *(char *)((long)param_1 + 0x227);
  }
  if (cVar2 < '\0') {
    __ZdlPvm(param_1[0x42],param_1[0x44] & 0x7fffffffffffffff);
    cVar2 = *(char *)((long)param_1 + 0x20f);
  }
  else {
    cVar2 = *(char *)((long)param_1 + 0x20f);
  }
  if (cVar2 < '\0') {
    __ZdlPvm(param_1[0x3f],param_1[0x41] & 0x7fffffffffffffff);
    cVar2 = *(char *)((long)param_1 + 0x1f7);
  }
  else {
    cVar2 = *(char *)((long)param_1 + 0x1f7);
  }
  if (cVar2 < '\0') {
    __ZdlPvm(param_1[0x3c],param_1[0x3e] & 0x7fffffffffffffff);
    cVar2 = *(char *)((long)param_1 + 0x1df);
  }
  else {
    cVar2 = *(char *)((long)param_1 + 0x1df);
  }
  if (cVar2 < '\0') {
    __ZdlPvm(param_1[0x39],param_1[0x3b] & 0x7fffffffffffffff);
    cVar2 = *(char *)((long)param_1 + 0x1c7);
  }
  else {
    cVar2 = *(char *)((long)param_1 + 0x1c7);
  }
  if (cVar2 < '\0') {
    __ZdlPvm(param_1[0x36],param_1[0x38] & 0x7fffffffffffffff);
    cVar2 = *(char *)((long)param_1 + 0x1af);
  }
  else {
    cVar2 = *(char *)((long)param_1 + 0x1af);
  }
  if (cVar2 < '\0') {
    __ZdlPvm(param_1[0x33],param_1[0x35] & 0x7fffffffffffffff);
    cVar2 = *(char *)((long)param_1 + 0x197);
  }
  else {
    cVar2 = *(char *)((long)param_1 + 0x197);
  }
  if (cVar2 < '\0') {
    __ZdlPvm(param_1[0x30],param_1[0x32] & 0x7fffffffffffffff);
  }
  FUN_045572a4(param_1 + 8);
  plVar10 = (long *)param_1[6];
  if (plVar10 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar10[1];
    plVar10[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar10 + 0x10))(plVar10);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  plVar10 = (long *)param_1[4];
  if (plVar10 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar10[1];
    plVar10[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar10 + 0x10))(plVar10);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  if (param_1[2] != 0) {
    __ZNSt3__119__shared_weak_count14__release_weakEv();
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


