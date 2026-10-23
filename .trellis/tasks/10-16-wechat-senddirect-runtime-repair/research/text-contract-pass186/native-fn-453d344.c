// Ghidra inferred pseudocode; requested=0x453d344
// entry=0453d344 end=0453d67b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0453d344(undefined8 param_1,long param_2,undefined8 param_3,long *param_4,long *param_5,
                 undefined8 param_6)

{
  undefined8 ****ppppuVar1;
  int iVar2;
  long *plVar3;
  long **pplVar4;
  code *pcVar5;
  undefined8 uVar6;
  undefined8 ***local_1c8 [2];
  undefined7 local_1b8;
  char cStack_1b1;
  undefined1 auStack_1b0 [144];
  long alStack_120 [3];
  long *local_108;
  long alStack_100 [3];
  long *local_e8;
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined8 uStack_d0;
  undefined8 uStack_c8;
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
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  if ((*(long *)(param_2 + 0x10) == 0) && (iVar2 = thunk_FUN_05e1d97c(4), iVar2 != 0)) {
    FUN_0488143c(local_1c8);
    ppppuVar1 = (undefined8 ****)local_1c8[0];
    if (-1 < cStack_1b1) {
      ppppuVar1 = local_1c8;
    }
    if ((DAT_0a455765 & 1) == 0) {
      DAT_0a455758._0_1_ = s_coroutinCoAsync_087e2ce0[0];
      DAT_0a455758._1_1_ = s_coroutinCoAsync_087e2ce0[1];
      DAT_0a455758._2_1_ = s_coroutinCoAsync_087e2ce0[2];
      DAT_0a455758._3_1_ = s_coroutinCoAsync_087e2ce0[3];
      DAT_0a455758._4_1_ = s_coroutinCoAsync_087e2ce0[4];
      DAT_0a455758._5_1_ = s_coroutinCoAsync_087e2ce0[5];
      DAT_0a455758._6_1_ = s_coroutinCoAsync_087e2ce0[6];
      DAT_0a455758._7_1_ = s_coroutinCoAsync_087e2ce0[7];
      DAT_0a455760 = (undefined4)DAT_084c8598;
      DAT_0a455764 = 0;
      DAT_0a455765 = 1;
    }
    if ((DAT_0a4557c2 & 1) == 0) {
      uRam000000000a4557b8._0_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[8];
      uRam000000000a4557b8._1_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[9];
      uRam000000000a4557b8._2_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[10];
      uRam000000000a4557b8._3_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0xb];
      uRam000000000a4557b8._4_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0xc];
      uRam000000000a4557b8._5_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0xd];
      uRam000000000a4557b8._6_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0xe];
      uRam000000000a4557b8._7_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0xf];
      DAT_0a4557b0 = s_coLaunchInterfaccancelAndJoinAll_089febc0[0];
      DAT_0a4557b0_1._0_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[1];
      DAT_0a4557b0_1._1_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[2];
      DAT_0a4557b0_1._2_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[3];
      DAT_0a4557b0_1._3_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[4];
      DAT_0a4557b0_1._4_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[5];
      DAT_0a4557b0_1._5_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[6];
      DAT_0a4557b0_1._6_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[7];
      DAT_0a4557c0 = 0x65;
      DAT_0a4557c2 = 1;
    }
    FUN_05e1d050(auStack_1b0,4,ppppuVar1,&DAT_0a455758,&DAT_0a4557b0,0xd0,0,0);
    if ((DAT_0a4557a4 & 1) == 0) {
      _DAT_0a455774 = CONCAT44((int)DAT_087364e0,(int)DAT_087e2cf0);
      uRam000000000a45577c = CONCAT44((int)DAT_087e2cf8,(int)DAT_084d8298);
      _DAT_0a455784 = CONCAT44((int)DAT_087e2d00,(int)DAT_08482fd0);
      uRam000000000a45578c = CONCAT44((int)DAT_086f2210,(int)DAT_087e2d08);
      _DAT_0a455794 = CONCAT44((int)DAT_084cd470,(int)DAT_087e2d10);
      uRam000000000a45579c = CONCAT44((int)DAT_084ccd20,(int)DAT_087e2d18);
      DAT_0a4557a4 = 1;
    }
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
    uStack_d8 = 0;
    local_e0 = 0;
    uStack_c8 = 0;
    uStack_d0 = 0;
    FUN_05e1d31c(auStack_1b0,&DAT_0a455774,&local_e0);
    thunk_FUN_05e1d0bc(auStack_1b0);
    if (cStack_1b1 < '\0') {
      __ZdlPvm(local_1c8[0],CONCAT17(cStack_1b1,local_1b8) & 0x7fffffffffffffff);
    }
  }
  uVar6 = *(undefined8 *)(param_2 + 0x10);
  pplVar4 = (long **)(param_4 + 3);
  plVar3 = *pplVar4;
  if (plVar3 == (long *)0x0) {
    pplVar4 = &local_e8;
LAB_0453d568:
    *pplVar4 = (long *)0x0;
  }
  else {
    local_e8 = plVar3;
    if (plVar3 != param_4) goto LAB_0453d568;
    local_e8 = alStack_100;
    (**(code **)(*plVar3 + 0x18))(plVar3,alStack_100);
  }
  pplVar4 = (long **)(param_5 + 3);
  plVar3 = *pplVar4;
  if (plVar3 == (long *)0x0) {
    pplVar4 = &local_108;
LAB_0453d5ac:
    *pplVar4 = (long *)0x0;
  }
  else {
    local_108 = plVar3;
    if (plVar3 != param_5) goto LAB_0453d5ac;
    local_108 = alStack_120;
    (**(code **)(*plVar3 + 0x18))(plVar3,alStack_120);
  }
  FUN_0453c7ac(param_1,param_2,uVar6,param_3,alStack_100,alStack_120,param_6);
  if (local_108 == alStack_120) {
    pcVar5 = *(code **)(*local_108 + 0x20);
LAB_0453d614:
    (*pcVar5)();
  }
  else if (local_108 != (long *)0x0) {
    pcVar5 = *(code **)(*local_108 + 0x28);
    goto LAB_0453d614;
  }
  if (local_e8 == alStack_100) {
    pcVar5 = *(code **)(*local_e8 + 0x20);
  }
  else {
    if (local_e8 == (long *)0x0) goto LAB_0453d644;
    pcVar5 = *(code **)(*local_e8 + 0x28);
  }
  (*pcVar5)();
LAB_0453d644:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


