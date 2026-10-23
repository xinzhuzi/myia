// Ghidra inferred pseudocode; requested=0x466ee94
// entry=0466ee94 end=0466f0fb

void FUN_0466ee94(undefined8 *param_1,ulong param_2)

{
  undefined4 uVar1;
  undefined4 uVar2;
  undefined1 *puVar3;
  long *plVar4;
  long lVar5;
  ulong uVar6;
  undefined1 auStack_290 [496];
  undefined1 *local_a0;
  long *plStack_98;
  undefined1 *local_90;
  long *local_88;
  ulong local_80;
  long local_78;
  undefined1 auStack_70 [32];
  
  FUN_04556dc0(auStack_290);
  local_90 = &SUB_aaaaaaaaaaaaaaaa;
  local_88 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_021efaf0(&local_90,auStack_70);
  plVar4 = local_88;
  puVar3 = local_90;
  local_a0 = local_90;
  plStack_98 = local_88;
  if (local_88 != (long *)0x0) {
    local_88[1] = local_88[1] + 1;
  }
  if ((DAT_0a45e7d3 & 1) == 0) {
    DAT_0a45e7c8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
    DAT_0a45e7c8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
    DAT_0a45e7c8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
    DAT_0a45e7c8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
    DAT_0a45e7c8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
    DAT_0a45e7c8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
    DAT_0a45e7c8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
    DAT_0a45e7c8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
    DAT_0a45e7d0 = 0x2928;
    DAT_0a45e7d2 = 0;
    DAT_0a45e7d3 = 1;
  }
  if ((DAT_0a45e308 & 1) == 0) {
    uVar6 = 0;
    do {
      uVar1 = *(undefined4 *)((long)&DAT_08a143c1 + uVar6);
      uVar2 = *(undefined4 *)((long)&DAT_08a143ad + uVar6 % 0x14);
      *(uint *)((long)&DAT_0a45e2c1 + uVar6) =
           CONCAT13((char)((uint)uVar1 >> 0x18) + 0x8aU ^ (byte)((uint)uVar2 >> 0x18),
                    CONCAT12((char)((uint)uVar1 >> 0x10) + 0x8aU ^ (byte)((uint)uVar2 >> 0x10),
                             CONCAT11((char)((uint)uVar1 >> 8) + 0x8aU ^ (byte)((uint)uVar2 >> 8),
                                      (char)uVar1 + 0x8aU ^ (byte)uVar2)));
      uVar6 = uVar6 + 4;
    } while (uVar6 != 0x44);
    DAT_0a45e305 = 0x6363;
    DAT_0a45e307 = 0;
    DAT_0a45e308 = 1;
  }
  FUN_0003bb6c(auStack_70,&DAT_0a45e7c8,&DAT_0a45e2c1,0x44e);
  if ((param_2 & 0xfffffffc00000000) == DAT_09ffaec8) {
    FUN_0003f84c(param_2);
  }
  local_80 = param_2;
  lVar5 = __Znwm(0x230);
  FUN_00033c40(lVar5,FUN_0467bc6c,FUN_0467c688);
  *(ulong *)(lVar5 + 0x28) = param_2;
  local_80 = 0;
  FUN_04556dc0(lVar5 + 0x30,auStack_290);
  *(undefined1 **)(lVar5 + 0x220) = puVar3;
  *(long **)(lVar5 + 0x228) = plVar4;
  if (plVar4 != (long *)0x0) {
    plVar4[1] = plVar4[1] + 1;
  }
  local_78 = lVar5;
  FUN_04b7141c(auStack_70,&local_78,0,0);
  FUN_00033d2c(&local_78);
  if (plVar4 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar4[1];
    plVar4[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar4 + 0x10))(plVar4);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  plVar4 = local_88;
  *param_1 = local_90;
  param_1[1] = local_88;
  if (local_88 != (long *)0x0) {
    local_88[1] = local_88[1] + 1;
    if (local_88 != (long *)0x0) {
      LOAcquire();
      lVar5 = local_88[1];
      local_88[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*local_88 + 0x10))(local_88);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
      }
    }
  }
  FUN_02feb8bc(auStack_290);
  return;
}


