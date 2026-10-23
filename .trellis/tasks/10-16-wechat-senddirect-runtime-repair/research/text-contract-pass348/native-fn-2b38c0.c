// Ghidra inferred pseudocode; requested=0x2b38c0
// entry=002b38c0 end=002b3c2b

void FUN_002b38c0(long param_1)

{
  undefined4 uVar1;
  long lVar2;
  long *plVar3;
  code *pcVar4;
  ulong uVar5;
  undefined4 uVar6;
  undefined1 *local_140;
  long *local_138;
  undefined8 local_120;
  long *local_118;
  undefined1 *local_110;
  long *local_108;
  undefined1 auStack_100 [16];
  long *local_f0;
  long *local_e0;
  undefined **local_d8;
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
  FUN_002b2b7c();
  plVar3 = (long *)FUN_04669774();
  (**(code **)(*plVar3 + 0x88))(&local_120);
  local_d8 = &PTR_FUN_09bf8050;
  local_140 = &SUB_aaaaaaaaaaaaaaaa;
  local_138 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0456f244(&local_140,local_120,&local_d8);
  plVar3 = local_138;
  local_110 = local_140;
  local_108 = local_138;
  if (local_138 != (long *)0x0) {
    local_138[1] = local_138[1] + 1;
    if (local_138 != (long *)0x0) {
      LOAcquire();
      lVar2 = local_138[1];
      local_138[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*local_138 + 0x10))(local_138);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
      }
    }
  }
  FUN_04101688(alStack_70,local_110,param_1 + 0x18,*(undefined8 *)(param_1 + 0x60),param_1 + 0x30,
               param_1 + 0x48);
  local_90 = &PTR_FUN_09bf8188;
  local_78 = &local_90;
  local_98 = (long *)0x0;
  local_b8 = (long *)0x0;
  if ((DAT_0a27ee2a & 1) == 0) {
    DAT_0a27ee20._0_1_ = s_LoginStalogin_st_LoginStInitStat_084df348[0x18];
    DAT_0a27ee20._1_1_ = s_LoginStalogin_st_LoginStInitStat_084df348[0x19];
    DAT_0a27ee20._2_1_ = s_LoginStalogin_st_LoginStInitStat_084df348[0x1a];
    DAT_0a27ee20._3_1_ = s_LoginStalogin_st_LoginStInitStat_084df348[0x1b];
    DAT_0a27ee20._4_1_ = s_LoginStalogin_st_LoginStInitStat_084df348[0x1c];
    DAT_0a27ee20._5_1_ = s_LoginStalogin_st_LoginStInitStat_084df348[0x1d];
    DAT_0a27ee20._6_1_ = s_LoginStalogin_st_LoginStInitStat_084df348[0x1e];
    DAT_0a27ee20._7_1_ = s_LoginStalogin_st_LoginStInitStat_084df348[0x1f];
    DAT_0a27ee28 = 0x65;
    DAT_0a27ee2a = 1;
  }
  if ((DAT_0a27ee8c & 1) == 0) {
    uVar5 = 0;
    do {
      uVar6 = *(undefined4 *)((long)&DAT_084e0cb7 + uVar5);
      uVar1 = *(undefined4 *)((long)&DAT_084e0ca3 + uVar5 % 0x14);
      *(uint *)((long)&DAT_0a27ee2b + uVar5) =
           CONCAT13((byte)((uint)uVar1 >> 0x18) ^ (byte)((uint)uVar6 >> 0x18),
                    CONCAT12((byte)((uint)uVar1 >> 0x10) ^ (byte)((uint)uVar6 >> 0x10),
                             CONCAT11((byte)((uint)uVar1 >> 8) ^ (byte)((uint)uVar6 >> 8),
                                      (byte)uVar1 ^ (byte)uVar6)));
      uVar5 = uVar5 + 4;
    } while (uVar5 != 0x60);
    DAT_0a27ee8b = 0;
    DAT_0a27ee8c = 1;
  }
  lStack_88 = param_1;
  FUN_0003bb6c(&local_140,&DAT_0a27ee20,&DAT_0a27ee2b,0x1d);
  FUN_002b3cdc(auStack_100,alStack_70,&local_90,alStack_b0,alStack_d0,&local_140);
  if (local_e0 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_e0[1];
    local_e0[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_e0 + 0x10))(local_e0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_e0);
    }
  }
  if (local_f0 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_f0[1];
    local_f0[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_f0 + 0x10))(local_f0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_f0);
    }
  }
  if (local_b8 == alStack_d0) {
    pcVar4 = *(code **)(*local_b8 + 0x20);
LAB_002b3b08:
    (*pcVar4)();
  }
  else if (local_b8 != (long *)0x0) {
    pcVar4 = *(code **)(*local_b8 + 0x28);
    goto LAB_002b3b08;
  }
  if (local_98 == alStack_b0) {
    pcVar4 = *(code **)(*local_98 + 0x20);
LAB_002b3b34:
    (*pcVar4)();
  }
  else if (local_98 != (long *)0x0) {
    pcVar4 = *(code **)(*local_98 + 0x28);
    goto LAB_002b3b34;
  }
  if (local_78 == &local_90) {
    pcVar4 = (code *)(*local_78)[4];
LAB_002b3b60:
    (*pcVar4)();
  }
  else if (local_78 != (undefined ***)0x0) {
    pcVar4 = (code *)(*local_78)[5];
    goto LAB_002b3b60;
  }
  if (local_48 != 0) {
    __ZNSt3__119__shared_weak_count14__release_weakEv();
  }
  if (local_58 == alStack_70) {
    pcVar4 = *(code **)(*local_58 + 0x20);
  }
  else {
    if (local_58 == (long *)0x0) goto LAB_002b3b9c;
    pcVar4 = *(code **)(*local_58 + 0x28);
  }
  (*pcVar4)();
LAB_002b3b9c:
  plVar3 = local_108;
  if (local_108 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_108[1];
    local_108[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_108 + 0x10))(local_108);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  if (local_118 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_118[1];
    local_118[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_118 + 0x10))(local_118);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_118);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


