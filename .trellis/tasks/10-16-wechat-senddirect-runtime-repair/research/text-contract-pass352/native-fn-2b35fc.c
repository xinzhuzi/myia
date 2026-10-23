// Ghidra inferred pseudocode; requested=0x2b35fc
// entry=002b35fc end=002b389b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 * FUN_002b35fc(undefined8 *param_1)

{
  undefined8 ***pppuVar1;
  char cVar2;
  int iVar3;
  long lVar4;
  ulong uVar5;
  undefined8 **local_168 [2];
  undefined7 local_158;
  char cStack_151;
  undefined1 auStack_150 [144];
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 uStack_48;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  *param_1 = &PTR_FUN_09bf7f90;
  iVar3 = thunk_FUN_05e1d97c(2);
  if (iVar3 == 0) {
LAB_002b37a4:
    if (-1 < *(char *)((long)param_1 + 0x5f)) goto LAB_002b37ac;
LAB_002b3854:
    __ZdlPvm(param_1[9],param_1[0xb] & 0x7fffffffffffffff);
    if (-1 < *(char *)((long)param_1 + 0x47)) goto LAB_002b37b4;
LAB_002b386c:
    __ZdlPvm(param_1[6],param_1[8] & 0x7fffffffffffffff);
    cVar2 = *(char *)((long)param_1 + 0x2f);
  }
  else {
    FUN_0488143c(local_168);
    pppuVar1 = (undefined8 ***)local_168[0];
    if (-1 < cStack_151) {
      pppuVar1 = local_168;
    }
    if ((DAT_0a27ede6 & 1) == 0) {
      uVar5 = 0;
      do {
        (&DAT_0a27edd0)[uVar5] = (&DAT_084e0c20)[uVar5] + 0x8a ^ (&DAT_084e0c10)[uVar5 & 0xf];
        uVar5 = uVar5 + 1;
      } while (uVar5 != 0x16);
      DAT_0a27ede6 = 1;
    }
    if ((DAT_0a27ee02 & 1) == 0) {
      uRam000000000a27edf8._0_1_ = s__SilenceAuthStatnceA_084e0b90[8];
      uRam000000000a27edf8._1_1_ = s__SilenceAuthStatnceA_084e0b90[9];
      uRam000000000a27edf8._2_1_ = s__SilenceAuthStatnceA_084e0b90[10];
      uRam000000000a27edf8._3_1_ = s__SilenceAuthStatnceA_084e0b90[0xb];
      uRam000000000a27edf8._4_1_ = s__SilenceAuthStatnceA_084e0b90[0xc];
      uRam000000000a27edf8._5_1_ = s__SilenceAuthStatnceA_084e0b90[0xd];
      uRam000000000a27edf8._6_1_ = s__SilenceAuthStatnceA_084e0b90[0xe];
      uRam000000000a27edf8._7_1_ = s__SilenceAuthStatnceA_084e0b90[0xf];
      DAT_0a27edf0 = s__SilenceAuthStatnceA_084e0b90[0];
      DAT_0a27edf0_1._0_1_ = s__SilenceAuthStatnceA_084e0b90[1];
      DAT_0a27edf0_1._1_1_ = s__SilenceAuthStatnceA_084e0b90[2];
      DAT_0a27edf0_1._2_1_ = s__SilenceAuthStatnceA_084e0b90[3];
      DAT_0a27edf0_1._3_1_ = s__SilenceAuthStatnceA_084e0b90[4];
      DAT_0a27edf0_1._4_1_ = s__SilenceAuthStatnceA_084e0b90[5];
      DAT_0a27edf0_1._5_1_ = s__SilenceAuthStatnceA_084e0b90[6];
      DAT_0a27edf0_1._6_1_ = s__SilenceAuthStatnceA_084e0b90[7];
      DAT_0a27ee00 = 0x65;
      DAT_0a27ee02 = 1;
    }
    FUN_05e1d050(auStack_150,2,pppuVar1,&DAT_0a27edd0,&DAT_0a27edf0,0x18,0,0);
    if ((DAT_0a27ee1d & 1) == 0) {
      _DAT_0a27ee04 = CONCAT44((int)ram0x084e0ba0,(int)DAT_084d82f8);
      uRam000000000a27ee0c = CONCAT44((int)DAT_0848b6b0,(int)DAT_084e0ba8);
      DAT_0a27ee14 = CONCAT44((int)DAT_084e0bb8,(int)DAT_084e0bb0);
      DAT_0a27ee1c = 0;
      DAT_0a27ee1d = 1;
    }
    uStack_58 = 0;
    local_60 = 0;
    uStack_48 = 0;
    uStack_50 = 0;
    uStack_78 = 0;
    local_80 = 0;
    uStack_68 = 0;
    uStack_70 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_88 = 0;
    uStack_90 = 0;
    uStack_b8 = 0;
    local_c0 = 0;
    uStack_a8 = 0;
    uStack_b0 = 0;
    FUN_05e1d31c(auStack_150,&DAT_0a27ee04,&local_c0);
    thunk_FUN_05e1d0bc(auStack_150);
    if (-1 < cStack_151) goto LAB_002b37a4;
    __ZdlPvm(local_168[0],CONCAT17(cStack_151,local_158) & 0x7fffffffffffffff);
    if (*(char *)((long)param_1 + 0x5f) < '\0') goto LAB_002b3854;
LAB_002b37ac:
    if (*(char *)((long)param_1 + 0x47) < '\0') goto LAB_002b386c;
LAB_002b37b4:
    cVar2 = *(char *)((long)param_1 + 0x2f);
  }
  if (cVar2 < '\0') {
    __ZdlPvm(param_1[3],param_1[5] & 0x7fffffffffffffff);
  }
  *param_1 = &PTR_FUN_09b4bae8;
  lVar4 = param_1[2];
  if (*(int *)(lVar4 + 0x10) != -1) {
    if (*(int *)(lVar4 + 0x10) != 0) {
      LOAcquire();
      iVar3 = *(int *)(lVar4 + 0x10);
      *(int *)(lVar4 + 0x10) = iVar3 + -1;
      LORelease();
      if (iVar3 != 1) goto LAB_002b3804;
      lVar4 = param_1[2];
    }
    FUN_06ec2de0(lVar4,FUN_001ec6fc);
  }
LAB_002b3804:
  FUN_06fd3b24(param_1);
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return param_1;
}


