// Ghidra inferred pseudocode; requested=0x2660d9c
// entry=02660d9c end=02660feb

undefined8 FUN_02660d9c(undefined8 param_1,ulong param_2,long param_3,long param_4,int param_5)

{
  undefined4 uVar1;
  long lVar2;
  long lVar3;
  code *pcVar4;
  ulong uVar5;
  undefined4 uVar6;
  undefined1 auStack_c0 [32];
  undefined8 local_a0;
  long *local_98;
  undefined1 auStack_90 [8];
  long *local_88;
  long local_80;
  long local_78;
  ulong local_70;
  long alStack_68 [3];
  long *local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_80 = 0;
  local_78 = 0;
  local_70 = 0;
  if ((param_4 != 0) && (0 < param_5)) {
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
              (&local_80,param_4,param_5);
  }
  FUN_04669774();
  FUN_0466ad74(&local_a0);
  if ((DAT_0a391930 & 1) == 0) {
    DAT_0a391928[0] = s_OnEvent_087e26d0[0];
    DAT_0a391928[1] = s_OnEvent_087e26d0[1];
    DAT_0a391928[2] = s_OnEvent_087e26d0[2];
    DAT_0a391928[3] = s_OnEvent_087e26d0[3];
    DAT_0a391928[4] = s_OnEvent_087e26d0[4];
    DAT_0a391928[5] = s_OnEvent_087e26d0[5];
    DAT_0a391928[6] = s_OnEvent_087e26d0[6];
    DAT_0a391928[7] = s_OnEvent_087e26d0[7];
    DAT_0a391930 = 1;
  }
  if ((DAT_0a39199d & 1) == 0) {
    uVar5 = 0;
    do {
      uVar6 = *(undefined4 *)((long)&DAT_087e2929 + uVar5);
      uVar1 = *(undefined4 *)((long)&DAT_087e2915 + uVar5 % 0x14);
      *(uint *)((long)&DAT_0a391931 + uVar5) =
           CONCAT13((byte)((uint)uVar1 >> 0x18) ^ (byte)((uint)uVar6 >> 0x18),
                    CONCAT12((byte)((uint)uVar1 >> 0x10) ^ (byte)((uint)uVar6 >> 0x10),
                             CONCAT11((byte)((uint)uVar1 >> 8) ^ (byte)((uint)uVar6 >> 8),
                                      (byte)uVar1 ^ (byte)uVar6)));
      uVar5 = uVar5 + 4;
    } while (uVar5 != 0x6c);
    DAT_0a39199d = 1;
  }
  FUN_0003bb6c(auStack_c0,DAT_0a391928,&DAT_0a391931,0x15);
  uVar5 = local_70;
  lVar2 = local_78;
  lVar3 = local_80;
  local_78 = 0;
  local_70 = 0;
  local_80 = 0;
  local_50 = (long *)0x0;
  local_50 = (long *)__Znwm(0x28);
  *local_50 = (long)&PTR_FUN_09d9fa60;
  local_50[1] = lVar3;
  local_50[2] = lVar2;
  local_50[3] = uVar5;
  local_50[4] = param_2 & 0xffffffff | param_3 << 0x20;
  FUN_0453cce8(auStack_90,local_a0,auStack_c0,alStack_68,1);
  if (local_88 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_88[1];
    local_88[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_88 + 0x10))(local_88);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_88);
    }
  }
  if (local_50 == alStack_68) {
    pcVar4 = *(code **)(*local_50 + 0x20);
  }
  else {
    if (local_50 == (long *)0x0) goto LAB_02660f60;
    pcVar4 = *(code **)(*local_50 + 0x28);
  }
  (*pcVar4)();
LAB_02660f60:
  if (local_98 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_98[1];
    local_98[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_98 + 0x10))(local_98);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_98);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return 0;
}


