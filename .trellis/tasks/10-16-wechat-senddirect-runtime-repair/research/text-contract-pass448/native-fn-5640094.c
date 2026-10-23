// Ghidra inferred pseudocode; requested=0x5640094
// entry=05640094 end=056405bb

undefined8 FUN_05640094(long param_1,ulong param_2,long param_3)

{
  long *plVar1;
  undefined1 *puVar2;
  uint uVar3;
  int iVar4;
  uint uVar5;
  ulong uVar6;
  long lVar7;
  long lVar8;
  long lVar9;
  long lVar10;
  long *plVar11;
  undefined8 uVar12;
  undefined8 *local_118;
  undefined8 local_110;
  undefined8 uStack_108;
  int local_100;
  int local_fc;
  int local_f8;
  int local_f4;
  undefined1 *local_f0;
  undefined1 *puStack_e8;
  undefined **local_e0;
  undefined8 **local_d8;
  undefined8 **local_d0;
  undefined8 uStack_c8;
  undefined1 *local_c0;
  undefined1 *puStack_b8;
  undefined1 *puStack_b0;
  undefined1 *puStack_a8;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (*(char *)(param_1 + 0x500) == '\x01') {
    FUN_056930dc(param_3);
  }
  local_c0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0562b77c(&local_c0,param_1 + 0x148);
  uVar12 = *(undefined8 *)(param_1 + 0x4f8);
  FUN_0562b7a8(&local_c0);
  FUN_01e9a160(param_3,uVar12);
  FUN_056456ec(param_3,param_2);
  FUN_056930a8(param_3,*(undefined1 *)(param_1 + 0x529));
  FUN_05695b5c(param_3,*(undefined1 *)(param_1 + 0x528));
  FUN_05634ebc();
  uVar12 = FUN_01369cd0();
  FUN_00cef4cc(param_3,uVar12);
  uVar5 = (uint)param_2 & 0xff;
  FUN_05693088(param_3,uVar5 - 1 < 3 | *(byte *)(param_1 + 0x529) & 1);
  FUN_05696060(param_3,0);
  FUN_05693af8(param_3,99);
  if (uVar5 < 2) {
    plVar1 = (long *)0x0;
    if (param_3 != 0) {
      plVar1 = (long *)(param_3 + -0x38);
    }
    uVar3 = FUN_05658890(param_1 + 0x768);
    if (uVar3 != 0) {
      FUN_05640680(plVar1,&DAT_0a5245b8,param_1 + 0x768);
    }
    if (((uint)param_2 == 0) && (iVar4 = FUN_05683614(param_1 + 0x588), iVar4 != 0)) {
      FUN_05640858(plVar1,&DAT_0a524588,param_1 + 0x588);
    }
    else if ((uVar3 & 1) == 0) {
      *(undefined1 *)(plVar1 + 3) = 0;
      FUN_0562a6cc(plVar1);
      plVar11 = plVar1 + 5;
      FUN_056435bc(plVar1 + 4,*plVar11);
      plVar1[4] = (long)plVar11;
      plVar1[6] = 0;
      *plVar11 = 0;
      (**(code **)(*plVar1 + 0x18))(plVar1);
    }
  }
  uStack_c8 = 0;
  local_e0 = &PTR_FUN_09f1a798;
  local_c0 = &SUB_aaaaaaaaaaaaaaaa;
  local_d8 = &local_d8;
  local_d0 = &local_d8;
  FUN_0562b77c(&local_c0,param_1 + 0x148);
  if (&local_e0 != (undefined ***)(param_1 + 0x508)) {
    FUN_05643638(&local_d8,*(undefined8 *)(param_1 + 0x518),param_1 + 0x510);
  }
  FUN_0562b7a8(&local_c0);
  uVar6 = FUN_05645ef8(param_3,&local_e0);
  if ((uVar6 & 1) == 0) {
    uVar12 = FUN_0109d770(param_3);
    FUN_05627b08(param_1,uVar12);
LAB_056404c0:
    uVar12 = 0;
  }
  else {
    if (uVar5 - 5 < 0xfffffffd) {
      FUN_05692b24(param_3,param_1 + 0x48);
      uVar5 = FUN_05692e8c(param_3);
      local_f0 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_e8 = &SUB_aaaaaaaaaaaaaaaa;
      FUN_05631c54(&local_f0);
      lVar7 = FUN_05631c80();
      uVar6 = FUN_056459bc(param_3);
      if ((uVar6 & 1) == 0) {
        uVar12 = FUN_0109d770(param_3);
        FUN_05627b08(param_1,uVar12);
        thunk_FUN_0001accc(&local_f0);
        goto LAB_056404c0;
      }
      if ((param_2 & 0xff) != 0) {
        uVar5 = 1;
      }
      if ((uVar5 & 1) == 0) {
        FUN_05631c54(&local_c0);
        lVar8 = FUN_05631d14(&local_c0);
        lVar9 = FUN_05631d14(&local_f0);
        thunk_FUN_0001accc(&local_c0);
        lVar10 = FUN_05631c80();
        local_f8 = -0x55555556;
        local_f4 = -0x55555556;
        local_100 = -0x55555556;
        local_fc = -0x55555556;
        iVar4 = FUN_05694bf8(param_3,&local_f4,&local_f8,&local_fc,&local_100);
        if (iVar4 != 0) {
          puStack_b8 = (undefined1 *)((lVar8 - lVar9) / 1000);
          local_110 = 0;
          uStack_108 = 0;
          local_118 = &local_110;
          local_c0._0_1_ = 1;
          FUN_05626090(&local_118,&DAT_0a5244c8,&local_c0);
          FUN_056caefc(&local_c0);
          local_c0._0_1_ = 1;
          puStack_b8 = (undefined1 *)(lVar10 - lVar7);
          FUN_05626090(&local_118,&DAT_0a5244e0,&local_c0);
          FUN_056caefc(&local_c0);
          local_c0._0_1_ = 1;
          puStack_b8 = (undefined1 *)(long)local_f4;
          FUN_05626090(&local_118,&DAT_0a5244f8,&local_c0);
          FUN_056caefc(&local_c0);
          local_c0._0_1_ = 1;
          puStack_b8 = (undefined1 *)(long)local_f8;
          FUN_05626090(&local_118,&DAT_0a524510,&local_c0);
          FUN_056caefc(&local_c0);
          local_c0._0_1_ = 1;
          puStack_b8 = (undefined1 *)(long)local_fc;
          FUN_05626090(&local_118,&DAT_0a524528,&local_c0);
          FUN_056caefc(&local_c0);
          local_c0._0_1_ = 1;
          puStack_b8 = (undefined1 *)(long)local_100;
          FUN_05626090(&local_118,&DAT_0a524540,&local_c0);
          FUN_056caefc(&local_c0);
          lVar7 = FUN_0563d9f0(param_1,0);
          puStack_b8 = (undefined1 *)(lVar7 + 1);
          local_c0 = (undefined1 *)CONCAT71(local_c0._1_7_,1);
          FUN_05626090(&local_118,&DAT_0a5244b0,&local_c0);
          FUN_056caefc(&local_c0);
          uVar12 = FUN_056266d0();
          FUN_0562685c(uVar12,param_1,2,&local_118);
          FUN_03b35c00(&local_118,local_110);
        }
      }
      thunk_FUN_0001accc(&local_f0);
    }
    else if (uVar5 == 4) {
      uVar6 = FUN_056493e4(param_3);
      if ((uVar6 & 1) == 0) {
        uVar12 = thunk_FUN_0109d770(param_3);
        FUN_05627b08(param_1,uVar12);
      }
      else {
        puStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
        local_c0 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_a8 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_b0 = &SUB_aaaaaaaaaaaaaaaa;
        FUN_05649068(&local_c0,param_3,param_1 + 0x48);
        puVar2 = local_c0;
        if (((ulong)local_c0 & 1) == 0) {
          FUN_05627b20(param_1);
        }
        else {
          lVar7 = FUN_009abfd4((ulong)&local_c0 | 8);
          if (lVar7 != 0) {
            thunk_FUN_056967e4(param_3,(ulong)&local_c0 | 8);
          }
        }
        if ((char)local_c0 == '\x01') {
          FUN_0562fd84((ulong)&local_c0 | 8);
        }
        if (((ulong)puVar2 & 1) != 0) goto LAB_05640574;
      }
      goto LAB_056404c0;
    }
LAB_05640574:
    uVar12 = 1;
  }
  FUN_05669924(&local_e0);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return uVar12;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


