// Ghidra inferred pseudocode; requested=0x11b7980
// entry=011b7980 end=011b7e7f

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_011b7980(long param_1)

{
  long lVar1;
  long *plVar2;
  code *pcVar3;
  ulong uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined1 *local_180;
  undefined1 *puStack_178;
  long *local_170;
  undefined1 *local_168;
  long *local_160;
  undefined1 *local_158;
  long *local_150;
  undefined **local_138 [2];
  undefined7 local_128;
  char cStack_121;
  undefined8 local_120;
  long *local_118;
  undefined1 *local_110;
  long *local_108;
  undefined1 *local_100;
  undefined1 *puStack_f8;
  long *local_f0;
  undefined1 *local_e8;
  long *local_e0;
  long alStack_d0 [3];
  long *local_b8;
  long alStack_b0 [3];
  long *local_98;
  undefined **local_90;
  long lStack_88;
  undefined ***local_78;
  long alStack_70 [3];
  long *local_58;
  long local_48;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (*(char *)(param_1 + 0x338) != '\x01') {
LAB_011b79d8:
    if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
      FUN_011b5c04(param_1);
      return;
    }
    goto LAB_011b7e7c;
  }
  if (*(char *)(param_1 + 0x28f) < '\0') {
    if (*(long *)(param_1 + 0x280) == 0) goto LAB_011b79d8;
  }
  else if (*(char *)(param_1 + 0x28f) == '\0') goto LAB_011b79d8;
  if ((*(byte *)(param_1 + 0x238) & 1) == 0) {
    uVar5 = 2;
    if (*(char *)(param_1 + 0x23a) != '\0') {
      uVar5 = 3;
    }
  }
  else {
    uVar5 = 4;
  }
  *(undefined4 *)(param_1 + 0x48) = uVar5;
  *(undefined4 *)(param_1 + 0x4c) = 3;
  FUN_011b519c(param_1);
  local_e0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  puStack_f8 = &SUB_aaaaaaaaaaaaaaaa;
  local_100 = &SUB_aaaaaaaaaaaaaaaa;
  local_e8 = &SUB_aaaaaaaaaaaaaaaa;
  local_f0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  plVar2 = (long *)FUN_04669774();
  (**(code **)(*plVar2 + 0x88))(&local_120);
  local_138[0] = &PTR_FUN_09bf8050;
  local_158 = &SUB_aaaaaaaaaaaaaaaa;
  local_150 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0456f244(&local_158,local_120,local_138);
  plVar2 = local_150;
  local_110 = local_158;
  local_108 = local_150;
  if ((local_150 != (long *)0x0) && (local_150[1] = local_150[1] + 1, local_150 != (long *)0x0)) {
    LOAcquire();
    lVar1 = local_150[1];
    local_150[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_150 + 0x10))(local_150);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  cStack_121 = '\0';
  local_138[0] = (undefined **)((ulong)local_138[0] & 0xffffffffffffff00);
  FUN_041003f0(alStack_70,local_110,param_1 + 0x278,*(undefined4 *)(param_1 + 0x290),param_1 + 0x2b0
               ,local_138,*(undefined1 *)(param_1 + 0x310));
  local_90 = &PTR_FUN_09cb4350;
  local_78 = &local_90;
  local_98 = (long *)0x0;
  local_b8 = (long *)0x0;
  if ((DAT_0a2e55af & 1) == 0) {
    _DAT_0a2e5598 = CONCAT44((int)DAT_08618518,(int)ram0x08618510);
    uRam000000000a2e55a0 = CONCAT44((int)ram0x08495188,(int)DAT_08618520);
    DAT_0a2e55a8 = (undefined4)DAT_0857b9d0;
    DAT_0a2e55ac = 0x6b63;
    DAT_0a2e55ae = 0;
    DAT_0a2e55af = 1;
  }
  if ((DAT_0a2e53e3 & 1) == 0) {
    uVar4 = 0;
    do {
      uVar5 = *(undefined4 *)((long)&DAT_08618987 + uVar4);
      uVar6 = *(undefined4 *)((long)&DAT_08618973 + uVar4 % 0x14);
      *(uint *)((long)&DAT_0a2e5390 + uVar4) =
           CONCAT13((byte)((uint)uVar6 >> 0x18) ^ (byte)((uint)uVar5 >> 0x18),
                    CONCAT12((byte)((uint)uVar6 >> 0x10) ^ (byte)((uint)uVar5 >> 0x10),
                             CONCAT11((byte)((uint)uVar6 >> 8) ^ (byte)((uint)uVar5 >> 8),
                                      (byte)uVar6 ^ (byte)uVar5)));
      uVar4 = uVar4 + 4;
    } while (uVar4 != 0x50);
    DAT_0a2e53e0 = 0x6363;
    DAT_0a2e53e2 = 0;
    DAT_0a2e53e3 = 1;
  }
  lStack_88 = param_1;
  FUN_0003bb6c(&local_158,&DAT_0a2e5598,&DAT_0a2e5390,0x201);
  FUN_011b7f64(&local_100,alStack_70,&local_90,alStack_b0,alStack_d0,&local_158);
  if (local_b8 == alStack_d0) {
    pcVar3 = *(code **)(*local_b8 + 0x20);
LAB_011b7c3c:
    (*pcVar3)();
  }
  else if (local_b8 != (long *)0x0) {
    pcVar3 = *(code **)(*local_b8 + 0x28);
    goto LAB_011b7c3c;
  }
  if (local_98 == alStack_b0) {
    pcVar3 = *(code **)(*local_98 + 0x20);
LAB_011b7c68:
    (*pcVar3)();
  }
  else if (local_98 != (long *)0x0) {
    pcVar3 = *(code **)(*local_98 + 0x28);
    goto LAB_011b7c68;
  }
  if (local_78 == &local_90) {
    pcVar3 = (code *)(*local_78)[4];
LAB_011b7c94:
    (*pcVar3)();
  }
  else if (local_78 != (undefined ***)0x0) {
    pcVar3 = (code *)(*local_78)[5];
    goto LAB_011b7c94;
  }
  if (local_48 != 0) {
    __ZNSt3__119__shared_weak_count14__release_weakEv();
  }
  if (local_58 == alStack_70) {
    pcVar3 = *(code **)(*local_58 + 0x20);
LAB_011b7ccc:
    (*pcVar3)();
  }
  else if (local_58 != (long *)0x0) {
    pcVar3 = *(code **)(*local_58 + 0x28);
    goto LAB_011b7ccc;
  }
  if (cStack_121 < '\0') {
    __ZdlPvm(local_138[0],CONCAT17(cStack_121,local_128) & 0x7fffffffffffffff);
  }
  plVar2 = local_108;
  if (local_108 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_108[1];
    local_108[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_108 + 0x10))(local_108);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  if (local_118 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_118[1];
    local_118[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_118 + 0x10))(local_118);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_118);
    }
  }
  local_180 = local_100;
  puStack_178 = puStack_f8;
  local_170 = local_f0;
  if (local_f0 != (long *)0x0) {
    local_f0[1] = local_f0[1] + 1;
  }
  local_168 = local_e8;
  local_160 = local_e0;
  lVar1 = 0;
  if (local_e0 != (long *)0x0) {
    lVar1 = local_e0[1];
    local_e0[1] = lVar1 + 1;
  }
  FUN_04b1ca4c(lVar1,param_1 + 0x268,0x20e,&local_180);
  plVar2 = local_160;
  if (local_160 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_160[1];
    local_160[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_160 + 0x10))(local_160);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  plVar2 = local_170;
  if (local_170 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_170[1];
    local_170[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_170 + 0x10))(local_170);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  plVar2 = local_e0;
  if (local_e0 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_e0[1];
    local_e0[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_e0 + 0x10))(local_e0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  plVar2 = local_f0;
  if (local_f0 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_f0[1];
    local_f0[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_f0 + 0x10))(local_f0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
LAB_011b7e7c:
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


