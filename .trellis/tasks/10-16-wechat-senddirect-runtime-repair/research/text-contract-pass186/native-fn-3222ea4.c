// Ghidra inferred pseudocode; requested=0x3222ea4
// entry=03222ea4 end=032230cb

/* WARNING: Removing unreachable block (ram,0x03223044) */
/* WARNING: Removing unreachable block (ram,0x03223054) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_03222ea4(long param_1)

{
  long lVar1;
  long lVar2;
  code *pcVar3;
  ulong uVar4;
  long lVar5;
  undefined1 auStack_98 [32];
  undefined8 local_78;
  long *local_70;
  undefined1 auStack_68 [8];
  long *local_60;
  long alStack_58 [3];
  long *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar5 = *(long *)(param_1 + 0x18);
  FUN_04669774();
  FUN_0466ad74(&local_78);
  if ((DAT_0a3e2ee3 & 1) == 0) {
    DAT_0a3e2ed4._4_1_ = s_StartScaoperatorh_op_084cadf8[8];
    DAT_0a3e2ed4._5_1_ = s_StartScaoperatorh_op_084cadf8[9];
    DAT_0a3e2ed4._6_1_ = s_StartScaoperatorh_op_084cadf8[10];
    DAT_0a3e2ed4._7_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
    DAT_0a3e2ed4_5._3_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
    DAT_0a3e2ed4_5._4_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
    DAT_0a3e2ed4_5._5_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
    DAT_0a3e2ed4_5._6_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
    DAT_0a3e2ee0 = 0x2928;
    DAT_0a3e2ee2 = 0;
    DAT_0a3e2ee3 = 1;
  }
  if ((DAT_0a3dd403 & 1) == 0) {
    uVar4 = 0;
    do {
      (&DAT_0a3dd39e)[uVar4] = (&DAT_088bcf0a)[uVar4] + 0x8a ^ (&DAT_088bcefa)[uVar4 & 0xf];
      uVar4 = uVar4 + 1;
    } while (uVar4 != 0x65);
    DAT_0a3dd403 = 1;
  }
  FUN_0003bb6c(auStack_98,0xa3e2ed8,&DAT_0a3dd39e,0x105a);
  lVar1 = *(long *)(param_1 + 8);
  lVar2 = *(long *)(param_1 + 0x10);
  if (lVar2 != 0) {
    *(long *)(lVar2 + 8) = *(long *)(lVar2 + 8) + 1;
  }
  local_40 = (long *)0x0;
  local_40 = (long *)__Znwm(0x20);
  *local_40 = (long)&PTR_FUN_09def360;
  local_40[1] = lVar1;
  local_40[2] = lVar2;
  local_40[3] = lVar5;
  FUN_0453cce8(auStack_68,local_78,auStack_98,alStack_58,1);
  if (local_60 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_60[1];
    local_60[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_60 + 0x10))(local_60);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_60);
    }
  }
  if (local_40 == alStack_58) {
    pcVar3 = *(code **)(*local_40 + 0x20);
  }
  else {
    if (local_40 == (long *)0x0) goto LAB_0322303c;
    pcVar3 = *(code **)(*local_40 + 0x28);
  }
  (*pcVar3)();
LAB_0322303c:
  if (local_70 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_70[1];
    local_70[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_70 + 0x10))(local_70);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_70);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


